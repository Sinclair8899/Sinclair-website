#!/usr/bin/env python3
"""Build the daily research-news digest.

Collects the last ~26 hours of headlines from a curated RSS list, then asks
Claude to select only the items relevant to the site's research areas,
translate them into Traditional Chinese, and write a 1-2 sentence summary
each, bounded to the supplied title/snippet metadata.

Outputs (dual-write during the news-page revamp transition, case N1):
  * assets/news_daily.json   -- legacy single-day shape consumed by the
    current /news/ template. Structure unchanged (items keep `host`).
  * assets/news_archive.json -- rolling archive of the last 7 Asia/Taipei
    calendar days (schema_version 1), consumed by the future template (N3).
    Items carry no `host` field (dead data once favicons are removed).

Data-semantics rules (news-page-revamp-spec v2 + binding addendum):
  * digest_date is the Asia/Taipei calendar date of generated_utc, frozen
    once per run. The scheduled 21:50 UTC run belongs to the NEXT Taipei
    day; the archive, the page and (in N2) the commit all use this value.
  * RSS timestamps are UTC struct_times; epoch conversion uses
    calendar.timegm, never time.mktime (which depends on the host tz).
  * Candidate URLs must be absolute https, without userinfo, with a valid
    hostname and port, and the hostname must equal the approving feed's
    domain or end with "." + that domain (label-boundary suffix match).
    Non-conforming entries are excluded and logged; the rest publish.
  * The model returns candidate ids; the published link/title/source come
    from the fetched entry the id points to. Invalid and duplicate ids are
    dropped first-valid-wins and logged. A non-empty selection yielding
    zero valid rows is a FAILURE, never an empty day.
  * Only two success states are persisted: "published" (>=1 valid item)
    and "empty" (feeds, API and schema all fine; the model legitimately
    selected nothing; exit 0). Every other outcome exits non-zero and
    leaves news_archive.json byte-identical: missing key / API / schema
    failure, candidates below MIN_CANDIDATES, all-invalid selection,
    corrupt or missing archive, unknown schema version.
  * Archive writes are atomic: temp file in the same directory, full
    schema + semantic validation, then os.replace(). A corrupt or missing
    archive is never silently recreated -- run seed_news_archive.py first.

Requires ANTHROPIC_API_KEY in the environment (GitHub Actions secret).
Run with --dry-run to test feed collection without calling the API.
"""
from __future__ import annotations

import calendar
import html
import json
import os
import re
import sys
import tempfile
import time
import urllib.parse
from datetime import date as date_cls
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

MODEL = "claude-opus-5"
WINDOW_HOURS = 26
MAX_PER_FEED = 20
MAX_CANDIDATES = 70
SNIPPET_CHARS = 400
# Existing floor carried over from the pre-N1 script's literal
# `if len(candidates) < 5` -- frozen here as a named constant (addendum A3).
MIN_CANDIDATES = 5
# Existing per-category cap carried over from the pre-N1 script's `rows[:5]`.
MAX_PER_CATEGORY = 5

ARCHIVE_SCHEMA_VERSION = 1
ARCHIVE_DAYS = 7
TAIPEI = ZoneInfo("Asia/Taipei")
UTC_FMT = "%Y-%m-%dT%H:%M:%SZ"

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

# Reviewer-approved per-feed hostname allowlist (2026-08-12, all eight rows).
# Matching is label-boundary: host == approved OR host.endswith("." + approved).
APPROVED_DOMAINS = {
    "The Verge": "theverge.com",
    "Ars Technica": "arstechnica.com",
    "TechCrunch": "techcrunch.com",
    "IEEE Spectrum": "spectrum.ieee.org",
    "MIT Technology Review": "technologyreview.com",
    "Nature News": "nature.com",
    "Fierce Biotech": "fiercebiotech.com",
    "TechNews 科技新報": "technews.tw",
}

# Categories mirror the market brief's research baskets plus macro, so the two
# pages read as one system.
CATEGORIES = [
    ("ai_infra", "AI 基礎設施"),
    ("semis_hbm", "半導體/HBM"),
    ("robotics", "機器人與自主"),
    ("bio_ai", "生技×AI"),
    ("macro", "宏觀與政策"),
]
CATEGORY_KEYS = {key for key, _ in CATEGORIES}
CATEGORY_NAMES = dict(CATEGORIES)

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


class ArchiveError(Exception):
    """Raised for any archive load/validation/write problem."""


class PairWriteError(ArchiveError):
    """Raised when the published archive+daily pair write fails.

    rolled_back=True: the pair was restored to its pre-run state.
    rolled_back=False: recovery attempts were exhausted and the pair may be
    inconsistent (daily new / archive old) -- the caller must report that
    explicitly instead of claiming no partial state was kept.
    """

    def __init__(self, message: str, rolled_back: bool):
        super().__init__(message)
        self.rolled_back = rolled_back


# --------------------------------------------------------------------------
# Time semantics
# --------------------------------------------------------------------------

def taipei_digest_date(generated_utc: datetime) -> str:
    """Asia/Taipei calendar date of an aware UTC datetime, as YYYY-MM-DD."""
    if generated_utc.tzinfo is None:
        raise ValueError("generated_utc must be timezone-aware")
    return generated_utc.astimezone(TAIPEI).date().isoformat()


def entry_epoch_utc(stamp) -> float:
    """UTC epoch seconds for a feedparser struct_time (which is UTC).

    calendar.timegm interprets the struct as UTC regardless of the host
    timezone; time.mktime would not.
    """
    return calendar.timegm(stamp)


# --------------------------------------------------------------------------
# URL / hostname allowlist (addendum A4)
# --------------------------------------------------------------------------

def candidate_url_ok(url: str, approved: str) -> tuple[bool, str]:
    """Validate a candidate URL against the approving feed's domain.

    Returns (ok, reason). Rules: absolute https only; no userinfo; a
    hostname must be present with a valid port; hostname is lowercased and
    stripped of one legal trailing dot, then must equal `approved` or end
    with "." + approved (label boundary -- fake-theverge.com must fail).
    """
    if not url:
        return False, "empty url"
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return False, "unparseable url"
    if parts.scheme != "https":
        return False, f"scheme {parts.scheme!r} is not https"
    if "@" in parts.netloc:
        return False, "userinfo present"
    host = parts.hostname
    if not host:
        return False, "missing hostname"
    try:
        parts.port  # raises ValueError on an invalid port
    except ValueError:
        return False, "invalid port"
    host = host.lower()
    if host.endswith(".."):
        return False, "multiple trailing dots"
    if host.endswith("."):  # exactly one legal trailing dot may be removed
        host = host[:-1]
    if not host:
        return False, "missing hostname"
    if host == approved or host.endswith("." + approved):
        return True, ""
    return False, f"host {host!r} not under approved domain {approved!r}"


# --------------------------------------------------------------------------
# Collection
# --------------------------------------------------------------------------

def strip_html(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", text or "")).strip()


def collect_candidates(now_epoch: float | None = None, parse_fn=None):
    """Fetch feeds and keep entries from the last WINDOW_HOURS hours.

    Returns (candidates, feed_stats, warnings). feed_stats has one row per
    configured feed: {source, ok, error, entries, kept, excluded} so that a
    feed-level failure is recorded per feed and can never be mistaken for a
    model-judged empty day (addendum A3).
    """
    if parse_fn is None:
        import feedparser  # local import so offline tests need no dependency

        parse_fn = feedparser.parse
    if now_epoch is None:
        now_epoch = time.time()
    cutoff = now_epoch - WINDOW_HOURS * 3600
    candidates, feed_stats, warnings = [], [], []
    seen_urls: set[str] = set()
    for source, url in FEEDS:
        approved = APPROVED_DOMAINS[source]
        stat = {"source": source, "ok": True, "error": None,
                "entries": 0, "kept": 0, "excluded": 0}
        try:
            feed = parse_fn(url)
            entries = list(getattr(feed, "entries", []) or [])
            stat["entries"] = len(entries)
            if not entries:
                stat["ok"] = False
                stat["error"] = "no entries"
                warnings.append(f"{source}: 無條目")
                feed_stats.append(stat)
                continue
            for entry in entries:
                if stat["kept"] >= MAX_PER_FEED:
                    break
                link = entry.get("link", "")
                ok, reason = candidate_url_ok(link, approved)
                if not ok:
                    stat["excluded"] += 1
                    warnings.append(
                        f"{source}: excluded url ({reason}): {str(link)[:120]}")
                    continue
                if link in seen_urls:  # same-run dedupe
                    continue
                stamp = entry.get("published_parsed") or entry.get("updated_parsed")
                # Entries without a parseable date are kept: dropping them
                # silently would bias against feeds with sloppy metadata.
                if stamp and entry_epoch_utc(stamp) < cutoff:
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
                    "published": time.strftime(UTC_FMT, stamp) if stamp else None,
                })
                stat["kept"] += 1
        except Exception as exc:
            stat["ok"] = False
            stat["error"] = str(exc)
            warnings.append(f"{source}: {exc}")
        # A feed whose entries were ALL rejected by the allowlist did not
        # deliver any valid data: ruled a feed failure (2026-08-12 review).
        # Partial exclusion alongside valid kept data stays ok=True.
        if stat["ok"] and stat["entries"] > 0 and stat["excluded"] == stat["entries"]:
            stat["ok"] = False
            stat["error"] = "all entries excluded by allowlist"
            warnings.append(
                f"{source}: all {stat['entries']} entries excluded by allowlist")
        feed_stats.append(stat)
    return candidates[:MAX_CANDIDATES], feed_stats, warnings


# --------------------------------------------------------------------------
# Model call (unchanged from pre-N1 behavior)
# --------------------------------------------------------------------------

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


# --------------------------------------------------------------------------
# Assembly (first-valid-wins, logged drops)
# --------------------------------------------------------------------------

def assemble_categories(items, by_id):
    """Map model selections to archive category rows.

    Invalid ids, duplicate ids and unknown categories are dropped
    first-valid-wins with a log line each. Returns (categories, dropped).
    """
    rows_by_cat = {key: [] for key, _ in CATEGORIES}
    dropped = []
    seen_ids: set = set()
    for item in items:
        iid = item.get("id")
        src = by_id.get(iid)
        if src is None:
            dropped.append(f"invalid id {iid!r} dropped")
            continue
        if iid in seen_ids:
            dropped.append(f"duplicate id {iid!r} dropped")
            continue
        cat = item.get("category")
        if cat not in rows_by_cat:
            dropped.append(f"id {iid!r}: unknown category {cat!r} dropped")
            continue
        if len(rows_by_cat[cat]) >= MAX_PER_CATEGORY:
            dropped.append(f"id {iid!r}: category {cat} full, dropped")
            continue
        seen_ids.add(iid)
        rows_by_cat[cat].append({
            "title_zh": item["title_zh"],
            "summary_zh": item["summary_zh"],
            "relevance": item["relevance"],
            "title": src["title"],
            "source": src["source"],
            "url": src["url"],
            "published": src["published"],
        })
    categories = [
        {"key": key, "name": name, "items": rows_by_cat[key]}
        for key, name in CATEGORIES
        if rows_by_cat[key]
    ]
    return categories, dropped


# --------------------------------------------------------------------------
# Archive: load / validate / mutate / atomic write
# --------------------------------------------------------------------------

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _parse_date(s: str) -> date_cls:
    if not isinstance(s, str) or not DATE_RE.match(s):
        raise ArchiveError(f"bad date {s!r}")
    try:
        return date_cls.fromisoformat(s)
    except ValueError as exc:
        raise ArchiveError(f"bad date {s!r}: {exc}") from None


def validate_day(day) -> None:
    if not isinstance(day, dict):
        raise ArchiveError("day is not an object")
    _parse_date(day.get("date"))
    gen = day.get("generated_utc")
    try:
        datetime.strptime(gen, UTC_FMT)
    except (TypeError, ValueError):
        raise ArchiveError(f"day {day.get('date')}: bad generated_utc {gen!r}") from None
    status = day.get("status")
    if status not in ("published", "empty"):
        raise ArchiveError(f"day {day.get('date')}: bad status {status!r}")
    if not isinstance(day.get("model"), str) or not day["model"]:
        raise ArchiveError(f"day {day.get('date')}: bad model")
    if not isinstance(day.get("candidates"), int) or day["candidates"] < 0:
        raise ArchiveError(f"day {day.get('date')}: bad candidates")
    if not isinstance(day.get("warnings"), list):
        raise ArchiveError(f"day {day.get('date')}: bad warnings")
    feeds = day.get("feeds")
    if feeds is not None:  # optional: seeded legacy days have no per-feed stats
        if not isinstance(feeds, list):
            raise ArchiveError(f"day {day.get('date')}: bad feeds")
        for f in feeds:
            if not isinstance(f, dict) or "source" not in f or "ok" not in f:
                raise ArchiveError(f"day {day.get('date')}: bad feed stat {f!r}")
    cats = day.get("categories")
    if not isinstance(cats, list):
        raise ArchiveError(f"day {day.get('date')}: categories not a list")
    if status == "empty":
        if cats:
            raise ArchiveError(f"day {day['date']}: empty day must have no categories")
        return
    total = 0
    seen_keys = set()
    for cat in cats:
        if not isinstance(cat, dict):
            raise ArchiveError(f"day {day['date']}: category not an object")
        key = cat.get("key")
        if key not in CATEGORY_KEYS:
            raise ArchiveError(f"day {day['date']}: unknown category key {key!r}")
        if key in seen_keys:
            raise ArchiveError(f"day {day['date']}: duplicate category {key}")
        seen_keys.add(key)
        if cat.get("name") != CATEGORY_NAMES[key]:
            raise ArchiveError(f"day {day['date']}: category {key} name mismatch")
        items = cat.get("items")
        if not isinstance(items, list) or not (1 <= len(items) <= MAX_PER_CATEGORY):
            raise ArchiveError(
                f"day {day['date']}: category {key} must have 1..{MAX_PER_CATEGORY} items")
        for it in items:
            if not isinstance(it, dict):
                raise ArchiveError(f"day {day['date']}: item not an object")
            for field in ("title_zh", "summary_zh", "relevance", "title", "source", "url"):
                if not isinstance(it.get(field), str) or not it[field]:
                    raise ArchiveError(
                        f"day {day['date']}: item missing field {field!r}")
            if "host" in it:
                raise ArchiveError(
                    f"day {day['date']}: item carries dead field 'host'")
            src = it["source"]
            approved = APPROVED_DOMAINS.get(src)
            if approved is None:
                raise ArchiveError(f"day {day['date']}: unknown source {src!r}")
            ok, reason = candidate_url_ok(it["url"], approved)
            if not ok:
                raise ArchiveError(
                    f"day {day['date']}: item url rejected ({reason}): {it['url'][:120]}")
            pub = it.get("published")
            if pub is not None and not isinstance(pub, str):
                raise ArchiveError(f"day {day['date']}: bad published {pub!r}")
        total += len(items)
    if total < 1:
        raise ArchiveError(f"day {day['date']}: published day with zero items")


def validate_archive(obj) -> None:
    if not isinstance(obj, dict):
        raise ArchiveError("archive is not an object")
    if obj.get("schema_version") != ARCHIVE_SCHEMA_VERSION:
        raise ArchiveError(
            f"unknown schema_version {obj.get('schema_version')!r}")
    days = obj.get("days")
    if not isinstance(days, list):
        raise ArchiveError("days is not a list")
    if len(days) > ARCHIVE_DAYS:
        raise ArchiveError(f"{len(days)} days exceeds window of {ARCHIVE_DAYS}")
    parsed = []
    for day in days:
        validate_day(day)
        parsed.append(_parse_date(day["date"]))
    if len(set(parsed)) != len(parsed):
        raise ArchiveError("duplicate dates in archive")
    if parsed != sorted(parsed, reverse=True):
        raise ArchiveError("days are not sorted newest-first")
    if parsed and (parsed[0] - parsed[-1]).days > ARCHIVE_DAYS - 1:
        raise ArchiveError("dates span more than the 7-day window")


def load_archive(path: str) -> dict:
    if not os.path.exists(path):
        raise ArchiveError(
            f"{path} missing -- run seed_news_archive.py first; "
            "a missing archive is never silently recreated")
    try:
        with open(path, encoding="utf-8") as fh:
            obj = json.load(fh)
    except (OSError, ValueError) as exc:
        raise ArchiveError(f"cannot parse {path}: {exc}") from None
    validate_archive(obj)
    return obj


def upsert_day(days: list, day: dict) -> list:
    """Replace any entry with the same date (same-day rerun), insert, sort."""
    out = [d for d in days if d["date"] != day["date"]]
    out.append(day)
    out.sort(key=lambda d: d["date"], reverse=True)
    return out


def trim_window(days: list, digest_date: str) -> list:
    """Keep only entries inside the 7-calendar-day window ending digest_date.

    Trims only; middle gaps are never backfilled with older data.
    """
    end = _parse_date(digest_date)
    start = end - timedelta(days=ARCHIVE_DAYS - 1)
    return [d for d in days if start <= _parse_date(d["date"]) <= end]


def _unlink_quiet(path: str) -> None:
    try:
        os.unlink(path)
    except OSError:
        pass


def _write_temp_json(path: str, obj: dict) -> str:
    """Serialize obj to a temp file in path's directory; return temp path."""
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix="." + os.path.basename(path) + ".",
                               suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    except BaseException:
        _unlink_quiet(tmp)
        raise
    return tmp


def _write_temp_bytes(path: str, data: bytes) -> str:
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix="." + os.path.basename(path) + ".",
                               suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
    except BaseException:
        _unlink_quiet(tmp)
        raise
    return tmp


def write_archive_atomic(path: str, obj: dict) -> None:
    """Validate, write to a temp file in the same directory, os.replace()."""
    validate_archive(obj)
    tmp = _write_temp_json(path, obj)
    try:
        os.replace(tmp, path)
    except BaseException:
        _unlink_quiet(tmp)
        raise


# Bounded rollback budget for the pair write: the initial rollback attempt
# plus one retry. Never unbounded.
ROLLBACK_ATTEMPTS = 2


def _restore_daily(daily_path: str, original_daily: bytes | None) -> bool:
    """Restore the legacy daily to its pre-run state, bounded attempts.

    Each attempt uses a fresh temp file in the target directory; a temp
    that was not consumed by os.replace is always cleaned in `finally`.
    Returns True when the daily is restored (or removed, when it did not
    exist before), False when every attempt failed.
    """
    for attempt in range(1, ROLLBACK_ATTEMPTS + 1):
        try:
            if original_daily is None:
                os.unlink(daily_path)
                return True
            tmp = None
            try:
                tmp = _write_temp_bytes(daily_path, original_daily)
                os.replace(tmp, daily_path)
                tmp = None  # consumed by the successful replace
                return True
            finally:
                if tmp is not None:
                    _unlink_quiet(tmp)
        except OSError as exc:
            print(f"ERROR: daily rollback attempt {attempt}/"
                  f"{ROLLBACK_ATTEMPTS} failed: {exc}", file=sys.stderr)
    return False


def write_published_pair_atomic(archive_path: str, archive_obj: dict,
                                daily_path: str, daily_obj: dict) -> None:
    """Publish archive + legacy daily as an atomic pair (addendum A5).

    Both payloads are fully serialized to temp files in their target
    directories, and the archive is validated, before either real file is
    touched. The legacy daily is replaced first, so any failure preparing
    or replacing it leaves the archive byte-identical. If the archive
    replace then fails, the daily is rolled back from its pre-saved
    original bytes (or removed if it did not exist), so the pair can never
    end up half-published. Temp files never survive a failure.
    """
    validate_archive(archive_obj)
    original_daily = None
    if os.path.exists(daily_path):
        with open(daily_path, "rb") as fh:
            original_daily = fh.read()
    archive_tmp = _write_temp_json(archive_path, archive_obj)
    try:
        daily_tmp = _write_temp_json(daily_path, daily_obj)
    except BaseException:
        _unlink_quiet(archive_tmp)
        raise
    try:
        os.replace(daily_tmp, daily_path)
    except BaseException:
        _unlink_quiet(archive_tmp)
        _unlink_quiet(daily_tmp)
        raise
    try:
        os.replace(archive_tmp, archive_path)
    except BaseException as primary:
        _unlink_quiet(archive_tmp)
        if _restore_daily(daily_path, original_daily):
            raise PairWriteError(
                f"archive replace failed ({primary}); daily rolled back; "
                "pair left byte-identical to its pre-run state",
                rolled_back=True) from primary
        raise PairWriteError(
            f"archive replace failed ({primary}) AND all "
            f"{ROLLBACK_ATTEMPTS} daily rollback attempts failed: pair "
            "consistency NOT recovered (daily may be new while archive is "
            "old); manual intervention required",
            rolled_back=False) from primary


# --------------------------------------------------------------------------
# Run
# --------------------------------------------------------------------------

def _repo_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def build_day(digest_date, generated_utc, status, candidates_count,
              feed_stats, categories, warnings):
    return {
        "date": digest_date,
        "generated_utc": generated_utc,
        "status": status,
        "model": MODEL,
        "candidates": candidates_count,
        "feeds": feed_stats,
        "categories": categories,
        "warnings": warnings,
    }


def run(argv=None, *, collect_fn=None, select_fn=None, now_fn=None,
        repo_root=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    dry_run = "--dry-run" in args
    repo = repo_root or _repo_root()
    daily_path = os.path.join(repo, "assets", "news_daily.json")
    archive_path = os.path.join(repo, "assets", "news_archive.json")

    generated_dt = (now_fn or (lambda: datetime.now(timezone.utc)))()
    generated_utc = generated_dt.strftime(UTC_FMT)
    digest_date = taipei_digest_date(generated_dt)
    print(f"digest_date (Asia/Taipei): {digest_date}  (generated_utc {generated_utc})")

    # Load + validate the archive up front: fail fast (exit 2) before any
    # network or API spend, leaving the file byte-identical.
    if not dry_run:
        try:
            archive = load_archive(archive_path)
        except ArchiveError as exc:
            print(f"ERROR: archive: {exc}", file=sys.stderr)
            return 2

    collect = collect_fn or collect_candidates
    candidates, feed_stats, warnings = collect()
    for s in feed_stats:
        line = (f"  feed {s['source']}: ok={s['ok']} entries={s['entries']} "
                f"kept={s['kept']} excluded={s['excluded']}")
        if s["error"]:
            line += f" error={s['error']}"
        print(line)
    print(f"collected {len(candidates)} candidates from {len(FEEDS)} feeds")
    if dry_run:
        for c in candidates[:10]:
            print(f"  [{c['source']}] {c['title'][:70]}")
        return 0

    # Feed-level failure gate (addendum A3, 2026-08-12 review): ANY
    # configured feed with ok=False fails the run before the model is
    # called, regardless of how many candidates the other feeds supplied.
    failed_feeds = [s for s in feed_stats if not s["ok"]]
    if failed_feeds:
        for s in failed_feeds:
            print(f"ERROR: feed failure: {s['source']}: {s['error']}",
                  file=sys.stderr)
        print("ERROR: feed-level failure; model not called; archive untouched",
              file=sys.stderr)
        return 1

    if len(candidates) < MIN_CANDIDATES:
        print(f"ERROR: {len(candidates)} candidates is below "
              f"MIN_CANDIDATES={MIN_CANDIDATES}; archive untouched",
              file=sys.stderr)
        return 1

    select = select_fn or select_and_summarize
    items, usage = select(candidates)

    if not items:
        # Legitimate model-judged empty day: feeds, API and schema all
        # succeeded. Record it and exit 0. news_daily.json is untouched.
        day = build_day(digest_date, generated_utc, "empty",
                        len(candidates), feed_stats, [], warnings)
        days = trim_window(upsert_day(archive["days"], day), digest_date)
        try:
            write_archive_atomic(
                archive_path,
                {"schema_version": ARCHIVE_SCHEMA_VERSION, "days": days})
        except (ArchiveError, OSError) as exc:
            print(f"ERROR: archive write: {exc}", file=sys.stderr)
            return 2
        print(f"empty day recorded for {digest_date}; news_daily.json untouched")
        return 0

    by_id = {c["id"]: c for c in candidates}
    categories, dropped = assemble_categories(items, by_id)
    for msg in dropped:
        print(f"  drop: {msg}")
    total = sum(len(c["items"]) for c in categories)
    if total == 0:
        print("ERROR: non-empty selection produced zero valid rows "
              "(all ids invalid/duplicate); archive untouched", file=sys.stderr)
        return 1

    day = build_day(digest_date, generated_utc, "published",
                    len(candidates), feed_stats, categories, warnings)
    days = trim_window(upsert_day(archive["days"], day), digest_date)

    # Legacy dual-write payload: same shape as pre-N1 (items keep `host`
    # for the current template's favicon markup) with the date corrected
    # to the frozen Taipei digest_date.
    legacy_categories = []
    for cat in categories:
        legacy_categories.append({
            "key": cat["key"],
            "name": cat["name"],
            "items": [
                dict(it, host=urllib.parse.urlparse(it["url"]).netloc)
                for it in cat["items"]
            ],
        })
    legacy = {
        "generated_utc": generated_utc,
        "date": digest_date,
        "model": MODEL,
        "candidates": len(candidates),
        "categories": legacy_categories,
        "warnings": warnings,
    }
    try:
        write_published_pair_atomic(
            archive_path,
            {"schema_version": ARCHIVE_SCHEMA_VERSION, "days": days},
            daily_path, legacy)
    except (ArchiveError, OSError) as exc:
        if getattr(exc, "rolled_back", True):
            print(f"ERROR: publish write failed ({exc}); no partial state "
                  "kept", file=sys.stderr)
        else:
            print(f"ERROR: publish write failed ({exc}); PAIR STATE MAY BE "
                  "INCONSISTENT -- do not commit; manual intervention "
                  "required", file=sys.stderr)
        return 2

    if usage is not None:
        print(f"wrote {archive_path} and {daily_path}: {total} items in "
              f"{len(categories)} categories "
              f"(tokens in/out: {usage.input_tokens}/{usage.output_tokens})")
    else:
        print(f"wrote {archive_path} and {daily_path}: {total} items in "
              f"{len(categories)} categories")
    return 0


def main() -> int:
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
