#!/usr/bin/env python3
"""Build the daily research-news digest.

Collects the last ~26 hours of headlines from a curated RSS list, then asks
Claude to select only the items relevant to the site's research areas,
translate them into Traditional Chinese, and write a 1-2 sentence factual
summary each. Writes assets/news_daily.json for the /news/ page template.

Design rules that matter here:
  * The model SELECTS and SUMMARIZES; it never invents facts or causation.
    Summaries are bounded to what the source headline/snippet states.
  * The model returns candidate indices, never URLs -- links and source names
    always come from the fetched feed data, so a hallucinated URL is
    structurally impossible.
  * Any failure (feeds down, API error, refusal, empty selection) exits
    non-zero and leaves the previous day's JSON in place.
  * Headlines + links + our own summaries only. Article bodies are never
    republished, and news photos are never embedded (licence risk) -- the
    template renders source favicons instead.

Requires ANTHROPIC_API_KEY in the environment (GitHub Actions secret).
Run with --dry-run to test feed collection without calling the API.
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone

import feedparser

MODEL = "claude-opus-5"
WINDOW_HOURS = 26
MAX_PER_FEED = 20
MAX_CANDIDATES = 70
SNIPPET_CHARS = 400

FEEDS = [
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("IEEE Spectrum", "https://spectrum.ieee.org/feeds/feed.rss"),
    ("MIT Technology Review", "https://www.technologyreview.com/feed/"),
    ("Nature News", "https://www.nature.com/nature.rss"),
    ("Fierce Biotech", "https://www.fiercebiotech.com/rss/xml"),
    ("TechNews 科技新報", "https://technews.tw/feed/"),
]

# Categories mirror the market brief's research baskets plus macro, so the two
# pages read as one system.
CATEGORIES = [
    ("ai_infra", "AI 基礎設施"),
    ("semis_hbm", "半導體/HBM"),
    ("robotics", "機器人與自主"),
    ("bio_ai", "生技×AI"),
    ("macro", "宏觀與政策"),
]

SYSTEM_PROMPT = """\
你是 sinclairhuang.org 的研究新聞編輯。這個網站的作者發表 AI 基礎設施、半導體與 HBM、\
機器人與自主系統、生技×AI 領域的研究論文,網站上另有一份每日市場簡報。

你的工作:從候選新聞中,只挑出對這些研究領域真正重要的條目,翻成台灣慣用的繁體中文,\
每則寫 1-2 句摘要。

規則:
1. 摘要只能陳述來源標題與摘要裡已有的事實。不推測、不加因果解釋、不加評論。
2. 寧缺勿濫:娛樂、消費性產品評測、與研究領域無關的政治新聞一律略過。每個分類最多 5 則,\
沒有合適的就讓該分類空著。
3. 同一事件多個來源報導時只選一則(選資訊最完整的)。
4. relevance 欄位用一句話說明它與哪個研究主題相關,只做「對應」不做「判讀」,\
例如「HBM 供給——記憶體約束主題」。
5. title_zh 是翻譯,不是改寫;專有名詞(公司名、產品名、技術名)保留原文。"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "category": {
                        "type": "string",
                        "enum": [key for key, _ in CATEGORIES],
                    },
                    "title_zh": {"type": "string"},
                    "summary_zh": {"type": "string"},
                    "relevance": {"type": "string"},
                },
                "required": ["id", "category", "title_zh", "summary_zh", "relevance"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["items"],
    "additionalProperties": False,
}


def strip_html(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", text or "")).strip()


def collect_candidates():
    """Fetch feeds and keep entries from the last WINDOW_HOURS hours."""
    cutoff = time.time() - WINDOW_HOURS * 3600
    candidates, warnings, seen_urls = [], [], set()
    for source, url in FEEDS:
        try:
            feed = feedparser.parse(url)
            if not feed.entries:
                warnings.append(f"{source}: 無條目")
                continue
            kept = 0
            for entry in feed.entries:
                if kept >= MAX_PER_FEED:
                    break
                link = entry.get("link", "")
                if not link or link in seen_urls:
                    continue
                stamp = entry.get("published_parsed") or entry.get("updated_parsed")
                # Entries without a parseable date are kept: dropping them
                # silently would bias against feeds with sloppy metadata.
                if stamp and time.mktime(stamp) < cutoff:
                    continue
                seen_urls.add(link)
                candidates.append({
                    "id": len(candidates),
                    "source": source,
                    "title": strip_html(entry.get("title", ""))[:300],
                    "snippet": strip_html(
                        entry.get("summary", entry.get("description", ""))
                    )[:SNIPPET_CHARS],
                    "url": link,
                    "published": time.strftime("%Y-%m-%dT%H:%M:%SZ", stamp)
                    if stamp else None,
                })
                kept += 1
        except Exception as exc:  # one dead feed must not kill the digest
            warnings.append(f"{source}: {exc}")
    return candidates[:MAX_CANDIDATES], warnings


def select_and_summarize(candidates):
    """One synchronous API call: select, categorize, translate, summarize."""
    import anthropic

    client = anthropic.Anthropic()
    user_content = (
        "以下是過去 24 小時的候選新聞(JSON)。依系統指示挑選、分類、翻譯、摘要。\n\n"
        + json.dumps(candidates, ensure_ascii=False)
    )
    with client.messages.stream(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        output_config={"format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
        messages=[{"role": "user", "content": user_content}],
    ) as stream:
        response = stream.get_final_message()

    if response.stop_reason != "end_turn":
        raise RuntimeError(f"API 未正常完成: stop_reason={response.stop_reason}")
    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)["items"], response.usage


def main() -> int:
    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dry_run = "--dry-run" in sys.argv

    candidates, warnings = collect_candidates()
    for w in warnings:
        print(f"  feed warning: {w}")
    print(f"collected {len(candidates)} candidates from {len(FEEDS)} feeds")
    if dry_run:
        for c in candidates[:10]:
            print(f"  [{c['source']}] {c['title'][:70]}")
        return 0
    if len(candidates) < 5:
        print("ERROR: too few candidates; leaving previous digest in place", file=sys.stderr)
        return 1

    items, usage = select_and_summarize(candidates)
    if not items:
        print("ERROR: model selected zero items; leaving previous digest in place", file=sys.stderr)
        return 1

    by_id = {c["id"]: c for c in candidates}
    categories = []
    for key, name in CATEGORIES:
        rows = []
        for item in items:
            src = by_id.get(item["id"])
            if src is None or item["category"] != key:
                continue
            rows.append({
                "title_zh": item["title_zh"],
                "summary_zh": item["summary_zh"],
                "relevance": item["relevance"],
                "title": src["title"],
                "source": src["source"],
                "url": src["url"],
                "host": urllib.parse.urlparse(src["url"]).netloc,
                "published": src["published"],
            })
        if rows:
            categories.append({"key": key, "name": name, "items": rows[:5]})

    out = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "model": MODEL,
        "candidates": len(candidates),
        "categories": categories,
        "warnings": warnings,
    }
    path = os.path.join(repo, "assets", "news_daily.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)

    total = sum(len(c["items"]) for c in categories)
    print(f"wrote {path}: {total} items in {len(categories)} categories "
          f"(tokens in/out: {usage.input_tokens}/{usage.output_tokens})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
