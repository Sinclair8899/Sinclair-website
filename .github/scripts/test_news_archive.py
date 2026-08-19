#!/usr/bin/env python3
"""Offline tests for the N1 news-archive pipeline (no network, no API).

Covers the N1 slice of the reviewer's minimum acceptance matrix:
Taipei midnight / cross-month / cross-year / leap day; same-day rerun
replace; 8th-day trim and middle gaps; true-empty vs all-invalid split;
mixed valid/invalid/duplicate ids; corrupt archive and atomic rollback;
URL scheme and hostname allowlist; insufficient candidates; first 7-day
seed from git history; per-category cap and cross-day duplicate-URL policy.
Since case N4 (dual-write retired): single-file atomic-write fault
injection, stray-legacy-daily non-interference, and removal of the pair
machinery are covered by SingleWriteFaultInjectionTests.

Run:  python3 -m unittest -v test_news_archive
"""
from __future__ import annotations

import calendar
import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seed_news_archive  # noqa: E402
import update_news  # noqa: E402


def utc(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def jload(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def mk_candidates(n: int, source: str = "The Verge"):
    return [{
        "id": i,
        "source": source,
        "title": f"Title {i}",
        "snippet": f"Snippet {i}",
        "url": f"https://www.theverge.com/story-{i}",
        "published": "2026-08-11T20:00:00Z",
    } for i in range(n)]


def mk_feed_stats(kept: int):
    return [{"source": s, "ok": True, "error": None,
             "entries": kept, "kept": kept, "excluded": 0}
            for s, _ in update_news.FEEDS]


def mk_item(i: int, category: str = "ai_infra"):
    return {"id": i, "category": category, "title_zh": f"標題{i}",
            "summary_zh": f"摘要{i}", "relevance": "對應"}


def mk_published_day(date: str, gen: str, n_items: int = 1,
                     source: str = "The Verge", url_prefix: str = ""):
    items = [{
        "title_zh": f"標題{i}", "summary_zh": f"摘要{i}", "relevance": "對應",
        "title": f"Title {i}", "source": source,
        "url": f"https://www.theverge.com/{url_prefix}{date}-{i}",
        "published": None,
    } for i in range(n_items)]
    return update_news.build_day(
        date, gen, "published", n_items, mk_feed_stats(n_items),
        [{"key": "ai_infra", "name": "AI 基礎設施", "items": items}], [])


class DigestDateTests(unittest.TestCase):
    def test_scheduled_run_is_next_taipei_day(self):
        self.assertEqual(update_news.taipei_digest_date(utc("2026-08-11T21:50:00Z")),
                         "2026-08-12")

    def test_taipei_midnight_boundary(self):
        self.assertEqual(update_news.taipei_digest_date(utc("2026-08-11T15:59:59Z")),
                         "2026-08-11")
        self.assertEqual(update_news.taipei_digest_date(utc("2026-08-11T16:00:00Z")),
                         "2026-08-12")

    def test_cross_month(self):
        self.assertEqual(update_news.taipei_digest_date(utc("2026-08-31T16:00:00Z")),
                         "2026-09-01")

    def test_cross_year(self):
        self.assertEqual(update_news.taipei_digest_date(utc("2026-12-31T16:00:00Z")),
                         "2027-01-01")

    def test_leap_day(self):
        self.assertEqual(update_news.taipei_digest_date(utc("2028-02-28T16:00:00Z")),
                         "2028-02-29")

    def test_naive_datetime_rejected(self):
        with self.assertRaises(ValueError):
            update_news.taipei_digest_date(datetime(2026, 8, 11, 21, 50))


class RssEpochTests(unittest.TestCase):
    def test_timegm_is_tz_independent(self):
        epoch = 1754951400
        struct = time.gmtime(epoch)
        self.assertEqual(update_news.entry_epoch_utc(struct), epoch)
        self.assertEqual(update_news.entry_epoch_utc(struct),
                         calendar.timegm(struct))


class UrlAllowlistTests(unittest.TestCase):
    A = "theverge.com"

    def ok(self, url):
        good, reason = update_news.candidate_url_ok(url, self.A)
        self.assertTrue(good, reason)

    def bad(self, url, fragment):
        good, reason = update_news.candidate_url_ok(url, self.A)
        self.assertFalse(good)
        self.assertIn(fragment, reason)

    def test_exact_and_subdomain(self):
        self.ok("https://theverge.com/a")
        self.ok("https://www.theverge.com/a")
        self.ok("https://sub.x.theverge.com/a")

    def test_label_boundary_blocks_fake_domain(self):
        self.bad("https://fake-theverge.com/a", "not under approved domain")
        self.bad("https://theverge.com.evil.net/a", "not under approved domain")

    def test_trailing_dot_and_case(self):
        self.ok("https://WWW.TheVerge.COM./a")

    def test_multiple_trailing_dots_rejected(self):
        self.bad("https://theverge.com../x", "multiple trailing dots")

    def test_scheme_userinfo_host_port(self):
        self.bad("http://www.theverge.com/a", "not https")
        self.bad("https://user@www.theverge.com/a", "userinfo")
        self.bad("https:///a", "missing hostname")
        self.bad("https://www.theverge.com:99999x/a", "invalid port")
        self.bad("", "empty url")


class CollectTests(unittest.TestCase):
    def fake_parse(self, feed_map):
        def parse(url):
            result = feed_map.get(url)
            if isinstance(result, Exception):
                raise result
            return SimpleNamespace(entries=result or [])
        return parse

    def test_per_feed_stats_dedupe_window_and_exclusion(self):
        now_epoch = calendar.timegm(time.strptime(
            "2026-08-11T22:00:00Z", "%Y-%m-%dT%H:%M:%SZ"))
        fresh = time.gmtime(now_epoch - 20 * 3600)   # inside 26h window
        stale = time.gmtime(now_epoch - 27 * 3600)   # outside 26h window
        verge_url = update_news.FEEDS[0][1]
        ars_url = update_news.FEEDS[1][1]
        tc_url = update_news.FEEDS[2][1]
        feed_map = {
            verge_url: [
                {"link": "https://www.theverge.com/a", "title": "A",
                 "summary": "sa", "published_parsed": fresh},
                {"link": "https://www.theverge.com/a", "title": "A dup",
                 "summary": "sa", "published_parsed": fresh},   # same-run dupe
                {"link": "http://www.theverge.com/http", "title": "B",
                 "summary": "sb", "published_parsed": fresh},   # non-https
                {"link": "https://fake-theverge.com/c", "title": "C",
                 "summary": "sc", "published_parsed": fresh},   # bad host
                {"link": "https://www.theverge.com/old", "title": "D",
                 "summary": "sd", "published_parsed": stale},   # too old
            ],
            ars_url: [],                                # feed-level: no entries
            tc_url: RuntimeError("connection refused"),  # feed-level failure
        }
        cands, stats, warnings = update_news.collect_candidates(
            now_epoch=now_epoch, parse_fn=self.fake_parse(feed_map))
        by_source = {s["source"]: s for s in stats}
        self.assertEqual(len(stats), len(update_news.FEEDS))
        verge = by_source["The Verge"]
        self.assertTrue(verge["ok"])
        self.assertEqual(verge["entries"], 5)
        self.assertEqual(verge["kept"], 1)
        self.assertEqual(verge["excluded"], 2)  # the two invalid URLs
        self.assertFalse(by_source["Ars Technica"]["ok"])
        self.assertFalse(by_source["TechCrunch"]["ok"])
        self.assertIn("connection refused", by_source["TechCrunch"]["error"])
        self.assertEqual([c["url"] for c in cands], ["https://www.theverge.com/a"])
        self.assertEqual(cands[0]["id"], 0)
        self.assertTrue(any("excluded url" in w for w in warnings))


class AssembleTests(unittest.TestCase):
    def test_first_valid_wins_and_logs(self):
        cands = mk_candidates(3)
        by_id = {c["id"]: c for c in cands}
        items = [mk_item(0), mk_item(0), mk_item(99), mk_item(1),
                 {"id": 2, "category": "nope", "title_zh": "x",
                  "summary_zh": "y", "relevance": "z"}]
        cats, dropped = update_news.assemble_categories(items, by_id)
        self.assertEqual(sum(len(c["items"]) for c in cats), 2)
        joined = "\n".join(dropped)
        self.assertIn("duplicate id 0", joined)
        self.assertIn("invalid id 99", joined)
        self.assertIn("unknown category", joined)

    def test_per_category_cap(self):
        cands = mk_candidates(10)
        by_id = {c["id"]: c for c in cands}
        items = [mk_item(i) for i in range(7)]
        cats, dropped = update_news.assemble_categories(items, by_id)
        self.assertEqual(len(cats[0]["items"]), update_news.MAX_PER_CATEGORY)
        self.assertTrue(any("category ai_infra full" in d for d in dropped))


class ArchiveValidationTests(unittest.TestCase):
    def wrap(self, days):
        return {"schema_version": 1, "days": days}

    def test_valid_archive_passes(self):
        days = [mk_published_day("2026-08-12", "2026-08-11T22:27:00Z"),
                mk_published_day("2026-08-10", "2026-08-09T22:27:00Z")]
        update_news.validate_archive(self.wrap(days))

    def test_cross_day_duplicate_url_is_allowed(self):
        d1 = mk_published_day("2026-08-12", "2026-08-11T22:27:00Z",
                              url_prefix="same-")
        d2 = mk_published_day("2026-08-11", "2026-08-10T22:27:00Z",
                              url_prefix="same-")
        # force identical URLs across the two days
        d2["categories"][0]["items"][0]["url"] = \
            d1["categories"][0]["items"][0]["url"]
        update_news.validate_archive(self.wrap([d1, d2]))

    def test_rejections(self):
        base = lambda: mk_published_day("2026-08-12", "2026-08-11T22:27:00Z")
        over = base()
        over["categories"][0]["items"] = \
            mk_published_day("2026-08-12", "2026-08-11T22:27:00Z",
                             n_items=6)["categories"][0]["items"]
        cases = []
        cases.append(self.wrap([over]))                       # >5 items
        dup = self.wrap([base(), base()])                      # duplicate dates
        cases.append(dup)
        unsorted_ = self.wrap([
            mk_published_day("2026-08-10", "2026-08-09T22:27:00Z"),
            mk_published_day("2026-08-12", "2026-08-11T22:27:00Z")])
        cases.append(unsorted_)
        span = self.wrap([
            mk_published_day("2026-08-12", "2026-08-11T22:27:00Z"),
            mk_published_day("2026-08-01", "2026-07-31T22:27:00Z")])
        cases.append(span)                                     # >7-day span
        eight = self.wrap([
            mk_published_day(f"2026-08-{d:02d}", f"2026-08-{d-1:02d}T22:27:00Z")
            for d in range(12, 4, -1)])
        cases.append(eight)                                    # 8 entries
        hostful = base()
        hostful["categories"][0]["items"][0]["host"] = "www.theverge.com"
        cases.append(self.wrap([hostful]))                     # dead host field
        badurl = base()
        badurl["categories"][0]["items"][0]["url"] = "http://www.theverge.com/x"
        cases.append(self.wrap([badurl]))                      # non-https item
        emptycat = base()
        emptycat["status"] = "empty"                           # empty w/ cats
        cases.append(self.wrap([emptycat]))
        badver = {"schema_version": 99, "days": []}
        cases.append(badver)                                   # unknown version
        for i, case in enumerate(cases):
            with self.assertRaises(update_news.ArchiveError, msg=f"case {i}"):
                update_news.validate_archive(case)

    def test_upsert_replaces_same_date(self):
        old = mk_published_day("2026-08-12", "2026-08-11T22:27:00Z")
        new = mk_published_day("2026-08-12", "2026-08-12T01:00:00Z")
        days = update_news.upsert_day([old], new)
        self.assertEqual(len(days), 1)
        self.assertEqual(days[0]["generated_utc"], "2026-08-12T01:00:00Z")

    def test_trim_keeps_window_and_gaps(self):
        days = [mk_published_day(d, g) for d, g in [
            ("2026-08-13", "2026-08-12T22:27:00Z"),
            ("2026-08-12", "2026-08-11T22:27:00Z"),
            ("2026-08-11", "2026-08-10T22:27:00Z"),
            ("2026-08-09", "2026-08-08T22:27:00Z"),   # gap at 08-10 stays a gap
            ("2026-08-05", "2026-08-04T22:27:00Z"),   # outside window
        ]]
        trimmed = update_news.trim_window(days, "2026-08-13")
        self.assertEqual([d["date"] for d in trimmed],
                         ["2026-08-13", "2026-08-12", "2026-08-11", "2026-08-09"])


class RunFlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="n1test.")
        os.makedirs(os.path.join(self.tmp, "assets"))
        self.archive_path = os.path.join(self.tmp, "assets", "news_archive.json")
        self.daily_path = os.path.join(self.tmp, "assets", "news_daily.json")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_archive(self, days):
        update_news.write_archive_atomic(
            self.archive_path, {"schema_version": 1, "days": days})

    def collect_ok(self, n=6):
        cands = mk_candidates(n)
        return lambda: (cands, mk_feed_stats(n), [])

    def run_pipeline(self, collect, select, now="2026-08-11T22:27:41Z"):
        return update_news.run(
            [], collect_fn=collect, select_fn=select,
            now_fn=lambda: utc(now), repo_root=self.tmp)

    def test_published_day_single_write_archive_only(self):
        """N4: a published day writes ONLY the archive; the legacy daily
        file is never created."""
        self.write_archive([mk_published_day("2026-08-11",
                                             "2026-08-10T22:27:00Z")])
        rc = self.run_pipeline(self.collect_ok(),
                               lambda c: ([mk_item(0), mk_item(1)], None))
        self.assertEqual(rc, 0)
        archive = jload(self.archive_path)
        self.assertEqual([d["date"] for d in archive["days"]],
                         ["2026-08-12", "2026-08-11"])  # Taipei, not UTC
        self.assertEqual(archive["days"][0]["status"], "published")
        self.assertNotIn("host", archive["days"][0]["categories"][0]["items"][0])
        self.assertFalse(os.path.exists(self.daily_path))

    def test_same_day_rerun_replaces(self):
        self.write_archive([mk_published_day("2026-08-12",
                                             "2026-08-11T22:27:00Z")])
        rc = self.run_pipeline(self.collect_ok(),
                               lambda c: ([mk_item(0)], None),
                               now="2026-08-12T01:00:00Z")
        self.assertEqual(rc, 0)
        archive = jload(self.archive_path)
        self.assertEqual(len(archive["days"]), 1)
        self.assertEqual(archive["days"][0]["generated_utc"],
                         "2026-08-12T01:00:00Z")

    def test_empty_day_exit_zero_no_legacy_file(self):
        self.write_archive([mk_published_day("2026-08-11",
                                             "2026-08-10T22:27:00Z")])
        before = sha256_file(self.archive_path)
        rc = self.run_pipeline(self.collect_ok(), lambda c: ([], None))
        after = sha256_file(self.archive_path)
        print(f"\n[evidence] empty-day: archive sha before={before}")
        print(f"[evidence] empty-day: archive sha after ={after} (changed by design)")
        self.assertEqual(rc, 0)
        self.assertNotEqual(before, after)
        archive = jload(self.archive_path)
        self.assertEqual(archive["days"][0]["status"], "empty")
        self.assertEqual(archive["days"][0]["categories"], [])
        self.assertFalse(os.path.exists(self.daily_path))

    def test_all_invalid_ids_fail_archive_untouched(self):
        self.write_archive([mk_published_day("2026-08-11",
                                             "2026-08-10T22:27:00Z")])
        before = sha256_file(self.archive_path)
        rc = self.run_pipeline(self.collect_ok(),
                               lambda c: ([mk_item(99), mk_item(100)], None))
        after = sha256_file(self.archive_path)
        print(f"\n[evidence] all-invalid: archive sha before={before}")
        print(f"[evidence] all-invalid: archive sha after ={after}")
        self.assertEqual(rc, 1)
        self.assertEqual(before, after)
        self.assertFalse(os.path.exists(self.daily_path))

    def test_insufficient_candidates_fail(self):
        self.write_archive([mk_published_day("2026-08-11",
                                             "2026-08-10T22:27:00Z")])
        before = sha256_file(self.archive_path)
        rc = self.run_pipeline(self.collect_ok(n=3),
                               lambda c: self.fail("select must not run"))
        after = sha256_file(self.archive_path)
        print(f"\n[evidence] too-few-candidates: sha before={before}")
        print(f"[evidence] too-few-candidates: sha after ={after}")
        self.assertEqual(rc, 1)
        self.assertEqual(before, after)

    def test_missing_archive_fails_before_api(self):
        rc = self.run_pipeline(
            lambda: self.fail("collect must not run before archive load"),
            lambda c: self.fail("select must not run"))
        self.assertEqual(rc, 2)
        self.assertFalse(os.path.exists(self.archive_path))

    def test_corrupt_archive_fails_bytes_identical(self):
        with open(self.archive_path, "w") as fh:
            fh.write("{not json")
        before = sha256_file(self.archive_path)
        rc = self.run_pipeline(lambda: self.fail("collect must not run"),
                               lambda c: self.fail("select must not run"))
        after = sha256_file(self.archive_path)
        print(f"\n[evidence] corrupt-archive: sha before={before}")
        print(f"[evidence] corrupt-archive: sha after ={after}")
        self.assertEqual(rc, 2)
        self.assertEqual(before, after)

    def test_unknown_schema_version_fails(self):
        with open(self.archive_path, "w") as fh:
            json.dump({"schema_version": 99, "days": []}, fh)
        before = sha256_file(self.archive_path)
        rc = self.run_pipeline(lambda: self.fail("no collect"),
                               lambda c: self.fail("no select"))
        self.assertEqual(rc, 2)
        self.assertEqual(before, sha256_file(self.archive_path))

    def test_atomic_write_failure_leaves_original_and_no_temp(self):
        self.write_archive([mk_published_day("2026-08-11",
                                             "2026-08-10T22:27:00Z")])
        before = sha256_file(self.archive_path)
        bad_day = mk_published_day("2026-08-12", "2026-08-11T22:27:00Z")
        bad_day["categories"][0]["items"] = []  # invalid: published w/ 0 items
        with self.assertRaises(update_news.ArchiveError):
            update_news.write_archive_atomic(
                self.archive_path,
                {"schema_version": 1, "days": [bad_day]})
        after = sha256_file(self.archive_path)
        print(f"\n[evidence] atomic-rollback: sha before={before}")
        print(f"[evidence] atomic-rollback: sha after ={after}")
        self.assertEqual(before, after)
        leftovers = [f for f in os.listdir(os.path.dirname(self.archive_path))
                     if f.startswith(".news_archive.")]
        self.assertEqual(leftovers, [])


class FeedFailureTests(unittest.TestCase):
    """Blocking-issue-1 tests: any configured feed with ok=False fails the
    run before the model is called, however many candidates the other
    feeds supplied. Exercises the REAL collect_candidates via parse_fn."""

    NOW = calendar.timegm(time.strptime("2026-08-11T22:00:00Z",
                                        "%Y-%m-%dT%H:%M:%SZ"))

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="n1feed.")
        os.makedirs(os.path.join(self.tmp, "assets"))
        self.archive_path = os.path.join(self.tmp, "assets", "news_archive.json")
        self.daily_path = os.path.join(self.tmp, "assets", "news_daily.json")
        update_news.write_archive_atomic(
            self.archive_path,
            {"schema_version": 1,
             "days": [mk_published_day("2026-08-11", "2026-08-10T22:27:00Z")]})

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def good_entries(self, approved, n=3):
        fresh = time.gmtime(self.NOW - 3600)
        return [{"link": f"https://www.{approved}/it-{i}",
                 "title": f"t{i}", "summary": "s",
                 "published_parsed": fresh} for i in range(n)]

    def collect_with_override(self, bad_source, override):
        feed_map = {}
        for source, url in update_news.FEEDS:
            approved = update_news.APPROVED_DOMAINS[source]
            feed_map[url] = (override if source == bad_source
                             else self.good_entries(approved))

        def parse(url):
            result = feed_map[url]
            if isinstance(result, Exception):
                raise result
            return SimpleNamespace(entries=result)

        return lambda: update_news.collect_candidates(
            now_epoch=self.NOW, parse_fn=parse)

    def assert_gated(self, collect, bad_source, label):
        before = sha256_file(self.archive_path)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = update_news.run(
                [], collect_fn=collect,
                select_fn=lambda c: self.fail("select must not be called"),
                now_fn=lambda: utc("2026-08-11T22:27:41Z"),
                repo_root=self.tmp)
        after = sha256_file(self.archive_path)
        print(f"\n[evidence] feed-failure/{label}: sha before={before}")
        print(f"[evidence] feed-failure/{label}: sha after ={after}")
        self.assertEqual(rc, 1)
        self.assertEqual(before, after)
        self.assertFalse(os.path.exists(self.daily_path))
        self.assertIn("feed failure", err.getvalue())
        self.assertIn(bad_source, err.getvalue())

    def test_one_feed_exception_gates_run(self):
        collect = self.collect_with_override(
            "TechCrunch", RuntimeError("connection refused"))
        self.assert_gated(collect, "TechCrunch", "exception")

    def test_one_feed_zero_entries_gates_run(self):
        collect = self.collect_with_override("Nature News", [])
        self.assert_gated(collect, "Nature News", "zero-entries")

    def test_one_feed_all_entries_excluded_gates_run(self):
        fresh = time.gmtime(self.NOW - 3600)
        all_bad = [{"link": f"http://www.arstechnica.com/plain-{i}",
                    "title": f"t{i}", "summary": "s",
                    "published_parsed": fresh} for i in range(4)]
        collect = self.collect_with_override("Ars Technica", all_bad)
        self.assert_gated(collect, "Ars Technica", "all-excluded")


class SingleWriteFaultInjectionTests(unittest.TestCase):
    """N4 tests: the single-file archive write can never half-write.
    Injects os.replace failures on the archive target and proves the
    retired legacy daily is never created or touched."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="n4single.")
        os.makedirs(os.path.join(self.tmp, "assets"))
        self.archive_path = os.path.join(self.tmp, "assets", "news_archive.json")
        self.daily_path = os.path.join(self.tmp, "assets", "news_daily.json")
        update_news.write_archive_atomic(
            self.archive_path,
            {"schema_version": 1,
             "days": [mk_published_day("2026-08-11", "2026-08-10T22:27:00Z")]})

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def archive_replace_fail(self):
        real = os.replace

        def fake(src, dst):
            if os.path.abspath(dst) == os.path.abspath(self.archive_path):
                raise OSError("injected replace failure")
            return real(src, dst)

        return mock.patch("os.replace", new=fake)

    def run_published(self):
        cands = mk_candidates(6)
        return update_news.run(
            [], collect_fn=lambda: (cands, mk_feed_stats(6), []),
            select_fn=lambda c: ([mk_item(0), mk_item(1)], None),
            now_fn=lambda: utc("2026-08-11T22:27:41Z"),
            repo_root=self.tmp)

    def run_empty(self):
        cands = mk_candidates(6)
        return update_news.run(
            [], collect_fn=lambda: (cands, mk_feed_stats(6), []),
            select_fn=lambda c: ([], None),
            now_fn=lambda: utc("2026-08-11T22:27:41Z"),
            repo_root=self.tmp)

    def assert_no_temps(self):
        leftovers = [f for f in os.listdir(os.path.join(self.tmp, "assets"))
                     if ".tmp" in f]
        self.assertEqual(leftovers, [])

    def test_published_replace_failure_leaves_archive_identical(self):
        a_before = sha256_file(self.archive_path)
        err = io.StringIO()
        with self.archive_replace_fail(), contextlib.redirect_stderr(err):
            rc = self.run_published()
        a_after = sha256_file(self.archive_path)
        print(f"\n[evidence] single-write-fault/published: sha before={a_before}")
        print(f"[evidence] single-write-fault/published: sha after ={a_after}")
        self.assertEqual(rc, 2)
        self.assertEqual(a_before, a_after)
        self.assertFalse(os.path.exists(self.daily_path))
        self.assert_no_temps()
        self.assertIn("archive left byte-identical", err.getvalue())

    def test_empty_replace_failure_leaves_archive_identical(self):
        a_before = sha256_file(self.archive_path)
        err = io.StringIO()
        with self.archive_replace_fail(), contextlib.redirect_stderr(err):
            rc = self.run_empty()
        a_after = sha256_file(self.archive_path)
        print(f"\n[evidence] single-write-fault/empty: sha before={a_before}")
        print(f"[evidence] single-write-fault/empty: sha after ={a_after}")
        self.assertEqual(rc, 2)
        self.assertEqual(a_before, a_after)
        self.assertFalse(os.path.exists(self.daily_path))
        self.assert_no_temps()

    def test_success_never_touches_stray_legacy_daily(self):
        """Transition guard: even if a stale news_daily.json is lying in
        the working tree, the pipeline neither rewrites nor deletes it."""
        with open(self.daily_path, "wb") as fh:
            fh.write(b'{"old": "stray legacy daily"}\n')
        d_before = sha256_file(self.daily_path)
        rc = self.run_published()
        d_after = sha256_file(self.daily_path)
        print(f"\n[evidence] stray-daily: sha before={d_before}")
        print(f"[evidence] stray-daily: sha after ={d_after} (byte-identical)")
        self.assertEqual(rc, 0)
        self.assertEqual(d_before, d_after)
        archive = jload(self.archive_path)
        self.assertEqual(archive["days"][0]["date"], "2026-08-12")
        self.assert_no_temps()

    def test_retired_pair_machinery_is_gone(self):
        """The pair-write API must not survive N4 as dead code."""
        for name in ("write_published_pair_atomic", "_restore_daily",
                     "PairWriteError", "ROLLBACK_ATTEMPTS",
                     "_write_temp_bytes"):
            self.assertFalse(hasattr(update_news, name),
                             f"{name} should have been removed in N4")


class SeedTests(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp(prefix="n1seedrepo.")
        os.makedirs(os.path.join(self.repo, "assets"))
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def git(self, *args):
        subprocess.run(["git", "-C", self.repo, *args], check=True,
                       capture_output=True, text=True)

    def commit_daily(self, payload, msg):
        path = os.path.join(self.repo, "assets", "news_daily.json")
        with open(path, "w", encoding="utf-8") as fh:
            if isinstance(payload, str):
                fh.write(payload)
            else:
                json.dump(payload, fh, ensure_ascii=False)
        self.git("add", "assets/news_daily.json")
        self.git("commit", "-q", "-m", msg)

    def legacy_daily(self, gen, tag):
        return {
            "generated_utc": gen,
            "date": gen[:10],  # historical UTC-based date, ignored by seed
            "model": "claude-opus-5",
            "candidates": 30,
            "categories": [{
                "key": "ai_infra", "name": "AI 基礎設施",
                "items": [{
                    "title_zh": f"標題-{tag}", "summary_zh": "摘要",
                    "relevance": "對應", "title": f"Title {tag}",
                    "source": "The Verge",
                    "url": f"https://www.theverge.com/{tag}",
                    "host": "www.theverge.com",
                    "published": None,
                }],
            }],
            "warnings": [],
        }

    def test_seed_window_supersede_and_host_strip(self):
        # taipei 08-06 (in window edge for launch 08-12)
        self.commit_daily(self.legacy_daily("2026-08-05T22:05:00Z", "a"), "d1")
        # taipei 08-05 (outside window)
        self.commit_daily(self.legacy_daily("2026-08-04T22:05:00Z", "b"), "d2")
        # two runs on the same taipei day 08-11: later one must win
        self.commit_daily(self.legacy_daily("2026-08-11T02:00:00Z", "c"), "d3")
        self.commit_daily(self.legacy_daily("2026-08-11T05:00:00Z", "d"), "d4")
        out = os.path.join(self.repo, "assets", "news_archive.json")
        archive = seed_news_archive.seed(self.repo, "2026-08-12", out)
        dates = [d["date"] for d in archive["days"]]
        self.assertEqual(dates, ["2026-08-11", "2026-08-06"])
        kept_0811 = archive["days"][0]
        self.assertEqual(kept_0811["generated_utc"], "2026-08-11T05:00:00Z")
        self.assertNotIn("host", kept_0811["categories"][0]["items"][0])
        self.assertIsNone(kept_0811["feeds"])
        update_news.validate_archive(archive)
        # reproducibility: second run over the same history is identical
        first = sha256_file(out)
        seed_news_archive.seed(self.repo, "2026-08-12", out)
        self.assertEqual(first, sha256_file(out))

    def test_seed_fails_on_corrupt_history_naming_commit(self):
        self.commit_daily(self.legacy_daily("2026-08-11T02:00:00Z", "ok"), "good")
        self.commit_daily("{broken json", "bad")
        out = os.path.join(self.repo, "assets", "news_archive.json")
        with self.assertRaises(seed_news_archive.SeedError) as ctx:
            seed_news_archive.seed(self.repo, "2026-08-12", out)
        self.assertIn("corrupt JSON", str(ctx.exception))
        self.assertRegex(str(ctx.exception), r"commit [0-9a-f]{40}")
        self.assertFalse(os.path.exists(out))

    def test_seed_fails_on_missing_field(self):
        payload = self.legacy_daily("2026-08-11T02:00:00Z", "x")
        del payload["model"]
        self.commit_daily(payload, "missing-model")
        out = os.path.join(self.repo, "assets", "news_archive.json")
        with self.assertRaises(seed_news_archive.SeedError) as ctx:
            seed_news_archive.seed(self.repo, "2026-08-12", out)
        self.assertIn("missing field 'model'", str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
