#!/usr/bin/env python3
"""Build the daily Research x Markets brief.

Pulls end-of-day index levels and research-basket constituents from Yahoo
Finance, computes 1D/1W moves, and writes two files:

  assets/market_brief.json  -> consumed by the /market-brief/ page template

Note: this lives in assets/, not data/, because the repo's daily_crawl workflow
writes a Markdown file into data/ which makes Hugo's data loader fail outright.

Design rules that matter here:
  * End-of-day only. This is an observation page, not a live ticker.
  * Intraday high/low is used only to describe the completed session
    ("盤中一度跌破年線,收盤收復") -- never to publish a mid-session state,
    which could be falsified by the close.
  * The generated prose states what moved. It never invents causation --
    interpretation is bounded to phrasing templates tied to published theses.
  * Any symbol that fails to fetch is dropped and reported in `warnings`,
    never silently rendered as zero.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Sinclair-website-brief/1.0"
# range=2y because the 240-session 年線 needs ~1 year of sessions plus buffer.
CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=2y&interval=1d"

INDICES = [
    ("^SOX", "費城半導體", "SOX"),
    ("^IXIC", "Nasdaq", "IXIC"),
    ("^GSPC", "S&P 500", "SPX"),
    ("^DJI", "道瓊工業", "DJIA"),
    ("^TWII", "台灣加權", "TAIEX"),
    ("^N225", "日經 225", "N225"),
    ("^KS11", "KOSPI", "KS11"),
    ("^STOXX", "STOXX 600", "SXXP"),
]

# Research baskets mirror the author's published research areas. Each basket
# links back to the thesis that argues why these constraints matter, and each
# member carries a label so the published constituent list reads as a
# methodology statement rather than a wall of tickers.
BASKETS = [
    {
        "key": "ai_infra",
        "name": "AI Infrastructure",
        "zh_short": "AI 基礎設施",
        "zh": "算力・電力・互連",
        "note": "涵蓋加速器、網通互連,以及供電與散熱——即論述中「較難壓縮」的那幾層。",
        "members": [
            ("NVDA", "NVIDIA · 加速器"),
            ("AVGO", "Broadcom · 客製晶片與互連"),
            ("ANET", "Arista · 資料中心網通"),
            ("VRT", "Vertiv · 供電與散熱"),
            ("ETN", "Eaton · 電力設備"),
            ("SMCI", "Supermicro · 伺服器整合"),
        ],
        "thesis": "Everyone Is Counting Tokens. Watch the Bandwidth That Gets Paid.",
        "thesis_url": "/blog/",
    },
    {
        "key": "semis_hbm",
        "name": "Semiconductors / HBM",
        "zh_short": "半導體/HBM",
        "zh": "半導體・記憶體・先進封裝",
        "note": "涵蓋晶圓代工、設備與記憶體——記憶體約束是否鬆動,主要看這一籃。",
        "members": [
            ("TSM", "台積電 · 晶圓代工與先進封裝"),
            ("ASML", "ASML · 微影設備"),
            ("AMAT", "Applied Materials · 製程設備"),
            ("LRCX", "Lam Research · 蝕刻與沉積"),
            ("KLAC", "KLA · 製程檢測"),
            ("MU", "Micron · HBM 與記憶體"),
            ("000660.KS", "SK hynix · HBM"),
        ],
        "thesis": "After Memory: Where Physical AI's Next \"No\" Will Form",
        "thesis_url": "/blog/",
    },
    {
        "key": "robotics",
        "name": "Robotics & Autonomy",
        "zh_short": "機器人與自主",
        "zh": "機器人・自駕・無人機",
        "note": "涵蓋工業機器人、致動與自主系統——實體 AI 的執行端。",
        "members": [
            ("ABBNY", "ABB · 工業機器人"),
            ("FANUY", "FANUC · 工業機器人與控制"),
            ("TSLA", "Tesla · 自駕與人形機器人"),
            ("MBLY", "Mobileye · 自駕感知"),
            ("AVAV", "AeroVironment · 無人機"),
            ("OSIS", "OSI Systems · 感測與檢測"),
        ],
        "thesis": "After Memory: Where Physical AI's Next \"No\" Will Form",
        "thesis_url": "/blog/",
    },
    {
        "key": "bio_ai",
        "name": "Biotech × AI",
        "zh_short": "生技×AI",
        "zh": "生技×AI・結構預測生態",
        "note": "涵蓋 AI 驅動藥物發現與其上游工具——AlphaFold 之後的價值落點在哪。",
        "members": [
            ("RXRX", "Recursion · AI 藥物發現"),
            ("SDGR", "Schrödinger · 計算化學平台"),
            ("CRSP", "CRISPR Therapeutics · 基因編輯"),
            ("ILMN", "Illumina · 定序"),
            ("TMO", "Thermo Fisher · 生命科學工具"),
        ],
        "thesis": "From Structure to Behaviour: Why Protein AI Is Entering the Decisive Phase",
        "thesis_url": "/blog/",
    },
]


def fetch_series(symbol: str, retries: int = 3):
    """Return (closes, day_high, day_low) for a symbol, or None after retries.

    day_high/day_low are the latest completed session's range. Close-only data
    hides sessions like "broke below the yearly line intraday, recovered by the
    close", so the range of the last bar is kept; either may be None if the
    feed omits it.
    """
    url = CHART.format(sym=urllib.parse.quote(symbol, safe=""))
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=15) as resp:
                payload = json.load(resp)
            quote = payload["chart"]["result"][0]["indicators"]["quote"][0]
            closes = [c for c in quote["close"] if c is not None]
            if len(closes) < 2:
                raise ValueError("not enough closes")
            last_i = max(i for i, c in enumerate(quote["close"]) if c is not None)
            highs = quote.get("high") or []
            lows = quote.get("low") or []
            day_high = highs[last_i] if last_i < len(highs) else None
            day_low = lows[last_i] if last_i < len(lows) else None
            return closes, day_high, day_low
        except Exception:
            if attempt == retries - 1:
                return None
            time.sleep(1.5 * (attempt + 1))
    return None


def pct(new: float, old: float):
    return None if not old else (new - old) / old * 100.0


def move(closes):
    """1-day and 1-week (5 sessions) percentage moves plus a sparkline series."""
    last = closes[-1]
    d1 = pct(last, closes[-2]) if len(closes) >= 2 else None
    w1 = pct(last, closes[-6]) if len(closes) >= 6 else None
    return {
        "last": round(last, 2),
        "d1": None if d1 is None else round(d1, 2),
        "w1": None if w1 is None else round(w1, 2),
        "spark": [round(c, 4) for c in closes[-15:]],
    }


def moving_averages(closes):
    """Position relative to the 20-, 60-, 120- and 240-session averages.

    Taiwanese and regional investors read indices against 月線 (20-session),
    季線 (60-session), 半年線 (120-session) and 年線 (240-session), so the
    level alone is less informative than whether the index sits above or
    below those lines.
    """
    out = {}
    for label, window in (("ma20", 20), ("ma60", 60), ("ma120", 120), ("ma240", 240)):
        if len(closes) >= window:
            avg = sum(closes[-window:]) / window
            out[label] = round(avg, 2)
            out[label + "_gap"] = round((closes[-1] - avg) / avg * 100.0, 2)
        else:
            out[label] = None
            out[label + "_gap"] = None
    return out


def intraday_ma_event(index):
    """Describe a session whose close and intraday range straddle a key MA.

    Longest line wins (a 年線 event outranks a 月線 one), and the penetration
    must exceed 0.1% so hairline crossings never reach the prose. This is a
    statement about a completed session, not a trend claim.
    """
    high, low, close = index.get("day_high"), index.get("day_low"), index["last"]
    for label, key in (("年線", "ma240"), ("半年線", "ma120"), ("季線", "ma60"), ("月線", "ma20")):
        ma = index.get(key)
        if not ma:
            continue
        if close > ma and low is not None and low <= ma * 0.999:
            return f"{index['name']}盤中一度跌破{label},收盤收復"
        if close < ma and high is not None and high >= ma * 1.001:
            return f"{index['name']}盤中一度站上{label},收盤未能守住"
    return None


def describe(value, up="上漲", down="下跌", flat="持平", threshold=0.05):
    if value is None:
        return "資料未取得"
    if abs(value) < threshold:
        return flat
    return f"{up} {abs(value):.1f}%" if value > 0 else f"{down} {abs(value):.1f}%"


def build_summary(indices, baskets, warnings):
    """Compose the factual paragraph and the research-lens paragraph.

    The factual paragraph reports moves. The lens paragraph only maps today's
    pattern onto an already-published framework -- it never asserts a new causal
    claim, because this text ships unreviewed under the author's name.
    """
    by_code = {i["code"]: i for i in indices}
    sox, ixic = by_code.get("SOX"), by_code.get("IXIC")
    facts = []

    if sox and sox["d1"] is not None:
        line = f"費城半導體指數{describe(sox['d1'])}"
        if ixic and ixic["d1"] is not None:
            gap = sox["d1"] - ixic["d1"]
            rel = "領先" if gap > 0.15 else ("落後" if gap < -0.15 else "同步")
            line += f",相對 Nasdaq({describe(ixic['d1'])}){rel}"
        facts.append(line + "。")

    asia = [by_code[c] for c in ("TAIEX", "N225", "KS11") if c in by_code and by_code[c]["d1"] is not None]
    if asia:
        ups = [a for a in asia if a["d1"] > 0.05]
        downs = [a for a in asia if a["d1"] < -0.05]
        # "全面" must mean every tracked market moved that way -- a flat index
        # is excluded from ups/downs, so guard on the full count.
        if ups and downs:
            facts.append(f"亞洲市場分歧:{'、'.join(a['name'] for a in ups)}收高,{'、'.join(a['name'] for a in downs)}收低。")
        elif ups:
            scope = "亞洲主要市場全面收高" if len(ups) == len(asia) else "亞洲市場收高的有"
            facts.append(f"{scope}({'、'.join(a['name'] for a in ups)})。")
        elif downs:
            scope = "亞洲主要市場全面收低" if len(downs) == len(asia) else "亞洲市場收低的有"
            facts.append(f"{scope}({'、'.join(a['name'] for a in downs)})。")

    # Breadth against the 20-session line: a position statement, not a level.
    with_ma = [i for i in indices if i.get("ma20_gap") is not None]
    if with_ma:
        below = [i for i in with_ma if i["ma20_gap"] < 0]
        if len(below) == len(with_ma):
            facts.append(f"追蹤的 {len(with_ma)} 個指數全數位於月線之下。")
        elif not below:
            facts.append(f"追蹤的 {len(with_ma)} 個指數全數位於月線之上。")
        else:
            facts.append(f"{len(with_ma)} 個追蹤指數中,{len(below)} 個位於月線之下({'、'.join(i['name'] for i in below[:4])}{'等' if len(below) > 4 else ''})。")

    # Sessions whose intraday range crossed a key MA but closed back on the
    # other side -- invisible in close-only numbers, yet exactly the days
    # readers ask about. Capped at 3 so a whipsaw day doesn't flood the prose.
    events = [e for e in (intraday_ma_event(i) for i in indices) if e]
    if events:
        facts.append(";".join(events[:3]) + "。")

    ranked = sorted([b for b in baskets if b["d1"] is not None], key=lambda b: b["d1"], reverse=True)
    if ranked:
        top, bottom = ranked[0], ranked[-1]
        # Prose uses the Chinese short names; the English basket names stay in
        # the basket section where they render as secondary labels.
        if top["key"] == bottom["key"]:
            facts.append(f"{top['zh_short']}{describe(top['d1'])}。")
        elif top["d1"] < -0.05:
            # Everything is down: rank by damage, not by "strength".
            facts.append(f"研究籃子全數收低,{bottom['zh_short']}跌幅最大({describe(bottom['d1'])}),{top['zh_short']}跌幅最小({describe(top['d1'])})。")
        elif bottom["d1"] > 0.05:
            facts.append(f"研究籃子全數收高,{top['zh_short']}漲幅最大({describe(top['d1'])}),{bottom['zh_short']}漲幅最小({describe(bottom['d1'])})。")
        else:
            facts.append(f"研究籃子中,{top['zh_short']}表現最強({describe(top['d1'])}),{bottom['zh_short']}最弱({describe(bottom['d1'])})。")

    lens = None
    infra = next((b for b in baskets if b["key"] == "ai_infra"), None)
    semis = next((b for b in baskets if b["key"] == "semis_hbm"), None)
    if infra and semis and infra["d1"] is not None and semis["d1"] is not None:
        spread = infra["d1"] - semis["d1"]
        # "Relative" language must survive days when both legs fall, so phrase it
        # as outperformance/resilience rather than "strength".
        both_down = infra["d1"] < -0.05 and semis["d1"] < -0.05
        if spread > 0.3:
            lens = (("基礎設施籃子跌幅小於半導體籃子" if both_down else "基礎設施籃子相對半導體籃子走強")
                    + ",與《After Memory》所描述的方向一致:"
                    "當記憶體約束鬆動,定價重心會往電力、互連這類較難壓縮的層移動。單日訊號不構成趨勢確認。")
        elif spread < -0.3:
            lens = (("半導體籃子跌幅小於基礎設施籃子" if both_down else "半導體籃子相對基礎設施籃子走強")
                    + ",與《After Memory》的分支圖相反方向;"
                    "值得追蹤這是短期輪動,還是記憶體約束仍是主要定價變數。")
        else:
            lens = ("兩個籃子走勢接近,今日資料未對《After Memory》的分支判讀提供分辨力——"
                    "這種日子本身就是提醒:要看的是導數,不是單日水位。")

    return {"facts": facts, "lens": lens, "warnings": warnings}


def main() -> int:
    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    warnings = []

    indices = []
    for symbol, name, code in INDICES:
        series = fetch_series(symbol)
        if not series:
            warnings.append(f"指數 {code} 取得失敗,已略過")
            continue
        closes, day_high, day_low = series
        indices.append({"name": name, "code": code,
                        "day_high": None if day_high is None else round(day_high, 2),
                        "day_low": None if day_low is None else round(day_low, 2),
                        **move(closes), **moving_averages(closes)})

    baskets = []
    for spec in BASKETS:
        moves, members, missing = [], [], []
        for ticker, label in spec["members"]:
            series = fetch_series(ticker)
            if not series:
                missing.append(ticker)
                continue
            closes = series[0]
            m = move(closes)
            if m["d1"] is None:
                continue
            moves.append(m)
            # Constituents are published so the basket number is auditable
            # rather than a black box the reader has to take on trust. The
            # per-member 年線 gap turns "many stocks broke their yearly line"
            # from an impression into a countable statement.
            members.append({"ticker": ticker, "label": label,
                            "d1": m["d1"], "w1": m["w1"],
                            "ma240_gap": moving_averages(closes).get("ma240_gap")})
        if missing:
            warnings.append(f"{spec['name']} 缺少成分:{', '.join(missing)}")
        if not moves:
            warnings.append(f"{spec['name']} 無可用成分,已略過")
            continue
        d1 = sum(m["d1"] for m in moves) / len(moves)
        w1_vals = [m["w1"] for m in moves if m["w1"] is not None]
        members.sort(key=lambda x: x["d1"], reverse=True)
        baskets.append({
            "key": spec["key"], "name": spec["name"],
            "zh_short": spec["zh_short"], "zh": spec["zh"],
            "note": spec.get("note", ""),
            "thesis": spec["thesis"], "thesis_url": spec["thesis_url"],
            "count": len(moves),
            "d1": round(d1, 2),
            "w1": round(sum(w1_vals) / len(w1_vals), 2) if w1_vals else None,
            "advancers": sum(1 for m in moves if m["d1"] > 0),
            "decliners": sum(1 for m in moves if m["d1"] < 0),
            "below_ma240": sum(1 for mm in members
                               if mm["ma240_gap"] is not None and mm["ma240_gap"] < 0),
            "members": members,
        })

    if not indices and not baskets:
        print("ERROR: no market data could be fetched; leaving previous brief in place", file=sys.stderr)
        return 1

    out = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "indices": indices,
        "baskets": baskets,
        "summary": build_summary(indices, baskets, warnings),
    }

    data_path = os.path.join(repo, "assets", "market_brief.json")
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    with open(data_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)

    print(f"wrote {data_path}: {len(indices)} indices, {len(baskets)} baskets, {len(warnings)} warnings")
    for w in warnings:
        print(f"  warning: {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
