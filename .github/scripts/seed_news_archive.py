#!/usr/bin/env python3
"""One-time, reproducible migration: seed assets/news_archive.json from the
Git history of assets/news_daily.json.

HISTORICAL TOOL ONLY (case N4, 2026-08-19): assets/news_daily.json was
retired and deleted from the working tree in N4; this script reads that
path exclusively from GIT HISTORY (`git show <commit>:...`), so it keeps
working for historical archive reconstruction. It is NOT a production
runtime dependency: no workflow step invokes it, and it must never become
part of the nightly pipeline. Retained solely so the pre-N1 daily history
can be re-derived into an archive if ever needed.

Binding rules (news-page-revamp-spec v2, addendum A5):
  * Reads only verifiable historical news_daily.json versions via
    `git show <commit>:assets/news_daily.json` -- never rewrites history.
  * Each historical file's Taipei calendar date comes from its own
    generated_utc (the historical `date` field is UTC-based and one Taipei
    day behind; it is ignored).
  * Several runs on the same Taipei date: the latest generated_utc wins.
  * Only the 7-calendar-day window ending at the frozen launch date is kept.
  * Missing fields, corrupt JSON or unparseable data are never patched by
    guesswork: the offending commit is named and the seed FAILS.
  * Output is validated with the same schema/semantic validator as the
    production writer and written atomically.

Usage:
  python3 seed_news_archive.py [--repo PATH] [--launch-date YYYY-MM-DD]
                               [--output PATH] [--dry-run]

--launch-date is the frozen Asia/Taipei launch day (defaults to today in
Asia/Taipei). Deterministic given the repository state and launch date.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import update_news  # noqa: E402  (shared constants + validators)

HISTORY_PATH = "assets/news_daily.json"


class SeedError(Exception):
    pass


def git(repo: str, *args: str) -> str:
    proc = subprocess.run(["git", "-C", repo, *args],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise SeedError(f"git {' '.join(args)}: {proc.stderr.strip()}")
    return proc.stdout


def history_commits(repo: str) -> list[str]:
    out = git(repo, "log", "--format=%H", "--reverse", "--", HISTORY_PATH)
    return [line for line in out.splitlines() if line]


def convert_commit(repo: str, commit: str) -> dict:
    """Read one historical news_daily.json and convert it to an archive day.

    Raises SeedError naming the commit on any missing/corrupt data.
    """
    try:
        raw = git(repo, "show", f"{commit}:{HISTORY_PATH}")
    except SeedError as exc:
        raise SeedError(f"commit {commit}: cannot read {HISTORY_PATH}: {exc}") from None
    try:
        data = json.loads(raw)
    except ValueError as exc:
        raise SeedError(f"commit {commit}: corrupt JSON: {exc}") from None

    for field in ("generated_utc", "model", "candidates", "categories", "warnings"):
        if field not in data:
            raise SeedError(f"commit {commit}: missing field {field!r}")
    try:
        gen_dt = datetime.strptime(
            data["generated_utc"], update_news.UTC_FMT
        ).replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise SeedError(
            f"commit {commit}: bad generated_utc "
            f"{data['generated_utc']!r}: {exc}") from None

    if not isinstance(data["categories"], list) or not data["categories"]:
        raise SeedError(
            f"commit {commit}: historical file has no categories; "
            "pre-N1 runs never persisted an empty day -- refusing to guess")

    categories = []
    for cat in data["categories"]:
        if not isinstance(cat, dict) or "key" not in cat or "items" not in cat:
            raise SeedError(f"commit {commit}: malformed category {cat!r}")
        items = []
        for it in cat["items"]:
            if not isinstance(it, dict):
                raise SeedError(f"commit {commit}: malformed item {it!r}")
            for field in ("title_zh", "summary_zh", "relevance",
                          "title", "source", "url"):
                if field not in it:
                    raise SeedError(
                        f"commit {commit}: item missing field {field!r}")
            items.append({
                "title_zh": it["title_zh"],
                "summary_zh": it["summary_zh"],
                "relevance": it["relevance"],
                "title": it["title"],
                "source": it["source"],
                "url": it["url"],
                "published": it.get("published"),
            })  # historical `host` is intentionally dropped (dead data)
        categories.append({"key": cat["key"],
                           "name": cat.get("name"),
                           "items": items})

    day = update_news.build_day(
        digest_date=update_news.taipei_digest_date(gen_dt),
        generated_utc=data["generated_utc"],
        status="published",
        candidates_count=data["candidates"],
        feed_stats=None,  # per-feed stats did not exist historically
        categories=categories,
        warnings=data["warnings"],
    )
    try:
        update_news.validate_day(day)
    except update_news.ArchiveError as exc:
        raise SeedError(f"commit {commit}: converted day invalid: {exc}") from None
    return day


def seed(repo: str, launch_date: str, output: str, dry_run: bool = False) -> dict:
    update_news._parse_date(launch_date)  # validate format early
    commits = history_commits(repo)
    if not commits:
        raise SeedError(f"no history for {HISTORY_PATH}")
    print(f"launch date (Asia/Taipei, frozen): {launch_date}")
    print(f"{len(commits)} historical commits touching {HISTORY_PATH}")

    by_date: dict[str, tuple[str, str, dict]] = {}  # date -> (gen_utc, commit, day)
    for commit in commits:
        day = convert_commit(repo, commit)
        d, g = day["date"], day["generated_utc"]
        prev = by_date.get(d)
        if prev is None or g > prev[0]:
            if prev is not None:
                print(f"  {d}: {prev[1][:9]} superseded by {commit[:9]} "
                      f"({prev[0]} -> {g})")
            by_date[d] = (g, commit, day)
        else:
            print(f"  {d}: {commit[:9]} older than kept {prev[1][:9]}, skipped")
        print(f"  commit {commit[:9]} generated_utc={g} -> taipei {d}")

    kept, dropped = [], []
    days = [v[2] for v in by_date.values()]
    days = update_news.trim_window(
        sorted(days, key=lambda d: d["date"], reverse=True), launch_date)
    kept_dates = {d["date"] for d in days}
    for d, (g, commit, _day) in sorted(by_date.items(), reverse=True):
        if d in kept_dates:
            kept.append((d, commit))
            print(f"  keep {d} (from {commit[:9]})")
        else:
            dropped.append((d, commit))
            print(f"  drop {d} (outside window, from {commit[:9]})")

    archive = {"schema_version": update_news.ARCHIVE_SCHEMA_VERSION, "days": days}
    update_news.validate_archive(archive)
    if dry_run:
        print(f"dry-run: would write {output} with {len(days)} day(s)")
        return archive
    update_news.write_archive_atomic(output, archive)
    print(f"wrote {output}: {len(days)} day(s): "
          + ", ".join(d["date"] for d in days))
    return archive


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=update_news._repo_root())
    parser.add_argument("--launch-date",
                        default=update_news.taipei_digest_date(
                            datetime.now(timezone.utc)))
    parser.add_argument("--output", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    output = args.output or os.path.join(args.repo, "assets", "news_archive.json")
    try:
        seed(args.repo, args.launch_date, output, dry_run=args.dry_run)
    except SeedError as exc:
        print(f"ERROR: seed failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
