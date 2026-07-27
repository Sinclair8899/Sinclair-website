#!/usr/bin/env python3
"""Track slow-moving constraint indicators that sit behind the market prices.

The market brief answers "what moved today". This answers "is the underlying
constraint tightening or loosening" -- the derivative the published theses say
to instrument, which no daily price series shows.

Source selection is governed by LICENCE, not by what is technically fetchable:

  * Epoch AI (epoch.ai)  -- CC BY 4.0. Commercial use and redistribution are
    permitted with attribution, so it is safe to derive from and publish on a
    site that also advertises advisory work. USED.
  * EIA (api.eia.gov)    -- US Government work, public domain, commercial use
    fine, but needs a free API key. Wired up but skipped unless EIA_API_KEY is
    present in the environment.
  * FRED                 -- technically open (fredgraph.csv needs no key) but
    the Terms of Use prohibit "data mining, scraping or extraction" AND limit
    free use to non-commercial/educational/personal. NOT USED.
  * WSTS / SEMI / SIA    -- all rights reserved, no open licence, and the file
    URLs embed rotating media IDs. NOT USED.
  * TWSE OpenAPI         -- no key, but republication requires prior written
    consent under its terms. NOT USED here (fine for private analysis).

Only derived aggregates are published, never a copy of the source dataset.
"""
from __future__ import annotations

import csv
import io
import json
import os
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Sinclair-website-indicators/1.0"
EPOCH_CSV = "https://epoch.ai/data/epochdb/notable_ai_models.csv"
EPOCH_ATTRIBUTION = "Epoch AI, “Notable AI Models” (CC BY 4.0)"
EPOCH_URL = "https://epoch.ai/data/notable-ai-models"


def fetch_text(url: str, timeout: int = 60) -> str | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001 - reported, never fatal
        print(f"  fetch failed {url}: {exc}", file=sys.stderr)
        return None


def month_key(date_str: str) -> str | None:
    """Epoch dates are ISO-ish but occasionally partial; keep YYYY-MM only."""
    if not date_str or len(date_str) < 7:
        return None
    return date_str[:7]


def frontier_compute(rows) -> dict | None:
    """Yearly frontier training compute: the derivative the thesis cares about.

    'Frontier' here is the maximum training compute published in a calendar
    year. If that curve bends, the compressible layer is winning -- which is
    exactly the branch the published thesis asks the reader to watch.
    """
    by_year: dict[int, list[float]] = defaultdict(list)
    for row in rows:
        mk = month_key(row.get("Publication date", ""))
        raw = (row.get("Training compute (FLOP)") or "").strip()
        if not mk or not raw:
            continue
        try:
            flop = float(raw)
        except ValueError:
            continue
        if flop <= 0:
            continue
        by_year[int(mk[:4])].append(flop)

    if not by_year:
        return None

    current_year = datetime.now(timezone.utc).year
    years = sorted(y for y in by_year if y >= 2018)
    if len(years) < 3:
        return None
    # The current calendar year is incomplete AND Epoch backfills compute
    # estimates months after release, so it must never drive a trend claim.
    complete_years = [y for y in years if y < current_year]
    if len(complete_years) < 3:
        return None

    series = []
    for year in years:
        vals = sorted(by_year[year], reverse=True)
        top = vals[0]
        # Median of the year's top 10 keeps one outlier from defining the frontier.
        head = vals[: min(10, len(vals))]
        median = head[len(head) // 2]
        series.append({
            "year": year,
            "max_flop": top,
            "max_exp": round(_log10(top), 2),
            "median_top10_exp": round(_log10(median), 2),
            "models": len(vals),
            "partial": year >= current_year,
        })

    # Growth is measured over COMPLETE years only.
    complete = [s for s in series if not s["partial"]]
    recent = [s for s in complete if s["year"] >= complete[-1]["year"] - 3]
    growth = None
    if len(recent) >= 2:
        span = recent[-1]["year"] - recent[0]["year"]
        if span > 0:
            growth = round((recent[-1]["max_exp"] - recent[0]["max_exp"]) / span, 2)

    latest = complete[-1]
    prior = complete[-2] if len(complete) >= 2 else None
    yoy = round(latest["max_exp"] - prior["max_exp"], 2) if prior else None
    partial = next((s for s in series if s["partial"]), None)

    return {
        "series": series,
        "latest_year": latest["year"],
        "latest_max_exp": latest["max_exp"],
        "partial_year": partial["year"] if partial else None,
        "yoy_oom": yoy,
        "growth_oom_per_year": growth,
        "note": _frontier_note(growth, yoy, latest["year"], partial),
    }


def _log10(x: float) -> float:
    import math
    return math.log10(x)


def _frontier_note(growth, yoy, latest_year, partial) -> str:
    """Describe the trend without asserting a cause, over complete years only."""
    if growth is None:
        return "資料不足以判斷趨勢。"
    if growth >= 0.5:
        pace = f"近三年前沿訓練算力約以每年 {growth} 個數量級的速度成長"
    elif growth > 0.05:
        pace = f"近三年前沿訓練算力成長放緩至每年約 {growth} 個數量級"
    elif growth > -0.05:
        pace = "近三年前沿訓練算力大致持平"
    else:
        pace = f"近三年公布的前沿訓練算力上限反而下降(每年約 {abs(growth)} 個數量級)"
    tail = ""
    if yoy is not None and yoy <= 0:
        tail = ";最近一年的公布上限未再創高。"
    else:
        tail = "。"
    caveat = ""
    if partial:
        caveat = (f"({partial['year']} 年資料尚未完整,且訓練算力估計常於發表後數月才補齊,"
                  f"因此未納入趨勢判斷。)")
    return (f"以完整年度計算至 {latest_year} 年:" + pace + tail +
            "前沿算力若走平,代表效率與蒸餾這類「壓縮」正在追上規模擴張——"
            "這正是《Bandwidth Thesis》要讀者盯的那條分支,而非任何單日價格。" + caveat)


def compute_efficiency(rows) -> dict | None:
    """How many labs reach a given compute scale over time.

    Diffusion of frontier-scale capability is the other half of the compression
    story: when more organisations can reach a scale, the rent at that scale
    erodes.
    """
    threshold_exp = 25.0  # 1e25 FLOP
    by_year: dict[int, set] = defaultdict(set)
    for row in rows:
        mk = month_key(row.get("Publication date", ""))
        raw = (row.get("Training compute (FLOP)") or "").strip()
        org = (row.get("Organization") or "").strip()
        if not mk or not raw or not org:
            continue
        try:
            flop = float(raw)
        except ValueError:
            continue
        if flop <= 0 or _log10(flop) < threshold_exp:
            continue
        by_year[int(mk[:4])].add(org)

    if not by_year:
        return None
    current_year = datetime.now(timezone.utc).year
    years = sorted(by_year)
    series = [{"year": y, "orgs": len(by_year[y]), "partial": y >= current_year} for y in years]
    complete = [s for s in series if not s["partial"]]
    if not complete:
        return None
    latest = complete[-1]
    partial = next((s for s in series if s["partial"]), None)
    caveat = (f"({partial['year']} 年資料尚未完整,僅供參考。)" if partial else "")
    return {
        "threshold": "1e25 FLOP",
        "series": series,
        "latest_year": latest["year"],
        "latest_orgs": latest["orgs"],
        "note": ("達到 1e25 FLOP 訓練規模的機構數量,反映前沿能力的擴散速度。"
                 "擴散越快,該規模本身可收取的租金越薄。" + caveat),
    }


def main() -> int:
    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    indicators = []
    warnings = []

    text = fetch_text(EPOCH_CSV)
    if text:
        rows = list(csv.DictReader(io.StringIO(text)))
        print(f"epoch: {len(rows)} rows")

        frontier = frontier_compute(rows)
        if frontier:
            indicators.append({
                "key": "frontier_compute",
                "title": "前沿模型訓練算力",
                "subtitle": "Frontier training compute",
                "headline": f"{frontier['latest_year']} 年公布上限 10^{frontier['latest_max_exp']} FLOP",
                "note": frontier["note"],
                "series": [{"label": str(s["year"]), "value": s["max_exp"],
                            "count": s["models"], "partial": s["partial"]}
                           for s in frontier["series"]],
                "value_unit": "log₁₀ FLOP",
                "source": EPOCH_ATTRIBUTION,
                "source_url": EPOCH_URL,
            })

        diffusion = compute_efficiency(rows)
        if diffusion:
            indicators.append({
                "key": "compute_diffusion",
                "title": "前沿規模的擴散",
                "subtitle": "Organisations reaching 1e25 FLOP",
                "headline": f"{diffusion['latest_year']} 年有 {diffusion['latest_orgs']} 個機構達到此規模",
                "note": diffusion["note"],
                "series": [{"label": str(s["year"]), "value": s["orgs"],
                            "count": None, "partial": s["partial"]}
                           for s in diffusion["series"]],
                "value_unit": "機構數",
                "source": EPOCH_ATTRIBUTION,
                "source_url": EPOCH_URL,
            })
    else:
        warnings.append("Epoch AI 資料取得失敗,指標未更新")

    if not indicators:
        print("ERROR: no indicators produced; leaving previous file in place", file=sys.stderr)
        return 1

    out = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "indicators": indicators,
        "warnings": warnings,
    }
    path = os.path.join(repo, "assets", "indicators.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(f"wrote {path}: {len(indicators)} indicators, {len(warnings)} warnings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
