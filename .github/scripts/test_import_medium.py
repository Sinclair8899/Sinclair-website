#!/usr/bin/env python3
"""Offline tests for the importer's transform layer. ZERO network: every
socket operation is disabled for the whole run, and the transform module
must import cleanly with no third-party dependency — this file must pass
BEFORE feedparser/requests are even installed in the workflow."""
import os
import socket
import sys
import unittest

# Hard network kill-switch: any socket construction fails the test run.
class _NoNetworkSocket(socket.socket):
    def __init__(self, *a, **k):
        raise AssertionError("network access attempted during offline importer tests")

socket.socket = _NoNetworkSocket  # type: ignore[misc]

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import medium_transform as mt  # noqa: E402  (after socket guard, by design)

# Snapshot taken immediately after importing the transform layer: the
# stdlib-only assertion checks THIS set, so later tests that stub
# feedparser/requests for the import_medium glue cannot pollute it.
MODULES_AFTER_TRANSFORM_IMPORT = frozenset(sys.modules)

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "medium")


def fixture(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


EXPECTED_RICH = (
    "As AI clusters scale from thousands of accelerators toward "
    "million-GPU systems, the network becomes part of the compute fabric itself."
)


class TransformTests(unittest.TestCase):
    def test_stdlib_only(self):
        for banned in ("feedparser", "requests"):
            self.assertNotIn(
                banned,
                MODULES_AFTER_TRANSFORM_IMPORT,
                f"{banned} leaked into the transform layer",
            )

    def test_block_boundaries_do_not_fuse(self):
        blocks = mt.blocks_from_html(fixture("blocks.html"))
        self.assertEqual(
            blocks,
            [("text", "The first block ends here"), ("text", "then the second begins.")],
        )
        joined = " ".join(t for _, t in blocks)
        self.assertNotIn("herethen", joined)

    def test_entities_and_nbsp_normalized(self):
        texts = [t for _, t in mt.blocks_from_html(fixture("rich.html"))]
        self.assertIn("R&D spending grows.", texts)
        self.assertIn("Yield learning matters.", texts)
        self.assertTrue(all(" " not in t and "  " not in t for t in texts))

    def test_headings_excluded(self):
        desc = mt.description_from_html(fixture("rich.html"))
        self.assertNotIn("optics story", desc)

    def test_figure_and_figcaption_excluded(self):
        blocks = mt.blocks_from_html(fixture("rich.html"))
        self.assertTrue(all("chart caption" not in t for _, t in blocks))

    def test_byline_author_series_fieldnote_excluded(self):
        for noise in (
            "By Po-Sung(Sinclair) Huang",
            "Sinclair Huang wrote this",
            "AI Infrastructure Notes | Part 2",
            "AI Infrastructure Notes｜Article 5",
            "Field Note v4 — updated",
        ):
            self.assertTrue(mt.is_noise(noise), noise)
        self.assertFalse(mt.is_noise("Everyone says AI needs more bandwidth."))
        desc = mt.description_from_html(fixture("rich.html"))
        for fragment in ("Po-Sung", "Sinclair", "Part 2", "Field Note"):
            self.assertNotIn(fragment, desc)

    def test_description_window_and_sentence_boundary(self):
        desc = mt.description_from_html(fixture("rich.html"))
        self.assertEqual(desc, EXPECTED_RICH)
        self.assertTrue(120 <= len(desc) <= 160, len(desc))
        self.assertRegex(desc, r'[.!?…。！？]["”』」)]?$')

    def test_no_compliant_group_fails_explicitly(self):
        with self.assertRaises(mt.DescriptionError):
            mt.description_from_html(fixture("nofit.html"))

    def test_front_matter_has_explicit_subscribe_cta(self):
        fm = mt.front_matter("T", "2026-08-02", ["AI"], "D.", "https://medium.com/x")
        self.assertIn('cta: "subscribe"\n', fm)

    def test_front_matter_never_guesses_primary_cluster(self):
        fm = mt.front_matter("T", "2026-08-02", ["AI"], "D.", "https://medium.com/x")
        self.assertNotIn("primary_cluster", fm)
        self.assertNotIn("related_clusters", fm)

    def test_yaml_quoting_is_safe(self):
        fm = mt.front_matter('A "quoted" title', "2026-08-02", [], 'She said "yes".', "https://m/x")
        self.assertIn('title: "A \\"quoted\\" title"\n', fm)
        self.assertIn('description: "She said \\"yes\\"."\n', fm)

    def test_trailing_fragment_is_not_a_sentence(self):
        self.assertEqual(
            mt.sentences_of("Complete sentence here. Trailing fragment without end"),
            ["Complete sentence here."],
        )

    # --- Step 5 follow-up: edge-case hardening ---

    @staticmethod
    def _yaml_unquote(scalar):
        assert scalar.startswith('"') and scalar.endswith('"')
        out, it = [], iter(scalar[1:-1])
        table = {"n": "\n", "r": "\r", "t": "\t", '"': '"', "\\": "\\"}
        for ch in it:
            out.append(table[next(it)] if ch == "\\" else ch)
        return "".join(out)

    def test_multiline_and_doc_separator_title_roundtrips(self):
        for title in ("Line one\nLine two", "---\nnot a document separator", 'Mix "quote"\tand\ttabs\n---'):
            fm = mt.front_matter(title, "2026-08-02", ["AI"], "D.", "https://m/x")
            lines = fm.split("\n")
            self.assertEqual(lines[0], "---")
            self.assertEqual([i for i, l in enumerate(lines) if l.strip() == "---"], [0, len(lines) - 3])
            title_lines = [l for l in lines if l.startswith("title: ")]
            self.assertEqual(len(title_lines), 1)
            self.assertEqual(self._yaml_unquote(title_lines[0][len("title: "):]), title)

    def test_by_year_prose_is_kept(self):
        self.assertFalse(mt.is_noise("By 2030, the grid will double."))
        sentence = ("By 2030, the grid interconnection queue is expected to double, "
                    "and the binding constraint shifts from chips to electricity, land, and cooling capacity.")
        self.assertEqual(mt.description_from_html(f"<p>{sentence}</p>"), sentence)

    def test_field_notes_prose_is_kept(self):
        self.assertFalse(mt.is_noise("Field notes from deployment sites show a different picture."))
        self.assertTrue(mt.is_noise("Field Note v4 — updated with reference materials."))
        sentence = ("Field notes from deployment sites show utilization, not headline capex, "
                    "deciding which operators actually earn back their accelerated depreciation.")
        self.assertEqual(mt.description_from_html(f"<p>{sentence}</p>"), sentence)

    def test_nested_blocks_keep_document_order_without_fusing(self):
        blocks = mt.blocks_from_html(fixture("nested.html"))
        self.assertEqual(
            blocks,
            [
                ("text", "Lead text before the inner block."),
                ("text", "Inner sentence one."),
                ("text", "Tail text after the inner block."),
                ("text", "After the quote."),
            ],
        )

    # --- Step 5 follow-up 2: byline and figure boundary gaps ---

    EXPLOIT_SENTENCE = ("As AI clusters scale from thousands of accelerators toward "
                        "million-GPU systems, the network becomes part of the compute fabric itself.")

    def test_byline_plain_capital_name_is_noise(self):
        self.assertTrue(mt.is_noise("By Jane Doe"))
        desc = mt.description_from_html(
            f"<p>By Jane Doe</p><p>{self.EXPLOIT_SENTENCE}</p>"
        )
        self.assertEqual(desc, self.EXPLOIT_SENTENCE)
        self.assertNotIn("Jane Doe", desc)

    def test_byline_with_trailing_period_is_noise(self):
        self.assertTrue(mt.is_noise("By Jane Doe."))
        # the reviewer's 147-char exploit: "By Jane Doe." must not pair up
        desc = mt.description_from_html(
            f"<p>By Jane Doe.</p><p>{self.EXPLOIT_SENTENCE}</p>"
        )
        self.assertEqual(desc, self.EXPLOIT_SENTENCE)

    def test_byline_honorific_prefix_is_noise(self):
        self.assertTrue(mt.is_noise("By Dr. Jane Doe"))
        desc = mt.description_from_html(
            f"<p>By Dr. Jane Doe</p><p>{self.EXPLOIT_SENTENCE}</p>"
        )
        self.assertNotIn("By Dr.", desc)
        self.assertEqual(desc, self.EXPLOIT_SENTENCE)

    def test_byline_initials_are_noise(self):
        self.assertTrue(mt.is_noise("By H. L. Cheung"))
        desc = mt.description_from_html(
            f"<p>By H. L. Cheung</p><p>{self.EXPLOIT_SENTENCE}</p>"
        )
        self.assertNotIn("L.", desc.split(self.EXPLOIT_SENTENCE)[0] if self.EXPLOIT_SENTENCE in desc else desc)
        self.assertEqual(desc, self.EXPLOIT_SENTENCE)

    def test_by_year_and_prose_still_kept_after_byline_fix(self):
        self.assertFalse(mt.is_noise("By 2030, the grid will double."))
        self.assertFalse(mt.is_noise("By Grace, we made it home before dark."))
        self.assertFalse(mt.is_noise("By the way, this matters a lot."))

    def test_figure_boundary_no_fusion_document_order(self):
        html = ("<p>toward<figure><img src=\"x.png\">"
                "<figcaption>cap text that must not leak</figcaption></figure>"
                "million-GPU systems now arrive on a predictable schedule.</p>"
                "<p>After the figure.</p>")
        blocks = mt.blocks_from_html(html)
        self.assertEqual(
            blocks,
            [
                ("text", "toward"),
                ("text", "million-GPU systems now arrive on a predictable schedule."),
                ("text", "After the figure."),
            ],
        )
        joined = " | ".join(t for _, t in blocks)
        self.assertNotIn("towardmillion", joined)
        self.assertNotIn("cap text", joined)

    # --- Step 5 follow-up 3: inline and Unicode bylines ---

    def test_inline_byline_in_same_paragraph_is_stripped(self):
        desc = mt.description_from_html(f"<p>By Jane Doe. {self.EXPLOIT_SENTENCE}</p>")
        self.assertEqual(desc, self.EXPLOIT_SENTENCE)
        self.assertNotIn("Jane Doe", desc)

    def test_br_separated_byline_is_stripped(self):
        desc = mt.description_from_html(f"<p>By Jane Doe<br>{self.EXPLOIT_SENTENCE}</p>")
        self.assertEqual(desc, self.EXPLOIT_SENTENCE)
        self.assertNotIn("Jane Doe", desc)

    def test_inline_honorific_byline_is_stripped(self):
        desc = mt.description_from_html(f"<p>By Dr. Jane Doe. {self.EXPLOIT_SENTENCE}</p>")
        self.assertEqual(desc, self.EXPLOIT_SENTENCE)
        self.assertNotIn("Dr.", desc)

    def test_inline_initials_byline_is_stripped(self):
        desc = mt.description_from_html(f"<p>By H. L. Cheung. {self.EXPLOIT_SENTENCE}</p>")
        self.assertEqual(desc, self.EXPLOIT_SENTENCE)
        self.assertNotIn("Cheung", desc)
        self.assertNotIn("L.", desc)

    def test_unicode_uppercase_bylines_are_noise(self):
        self.assertTrue(mt.is_noise("By Élodie Dupont"))
        self.assertTrue(mt.is_noise("By José Álvarez."))
        for byline in ("By Élodie Dupont.", "By José Álvarez."):
            desc = mt.description_from_html(f"<p>{byline}</p><p>{self.EXPLOIT_SENTENCE}</p>")
            self.assertEqual(desc, self.EXPLOIT_SENTENCE)
        inline = mt.description_from_html(f"<p>By Élodie Dupont. {self.EXPLOIT_SENTENCE}</p>")
        self.assertEqual(inline, self.EXPLOIT_SENTENCE)

    def test_prose_counterexamples_survive_prefix_stripping(self):
        for prose in (
            "By 2030, the grid will double.",
            "By Grace, we made it home before dark.",
            "By the way, this matters a lot.",
        ):
            self.assertFalse(mt.is_noise(prose))
            self.assertEqual(mt.strip_byline_prefix(prose), prose)

    def test_nofit_makes_importer_fail_nonzero_without_recording(self):
        import tempfile
        import types
        for stub in ("feedparser", "requests"):
            sys.modules.setdefault(stub, types.ModuleType(stub))
        import import_medium as im

        class FakeEntry:
            def __init__(self, link, title, summary):
                self.summary = summary
                self._d = {"link": link, "title": title}

            def get(self, key, default=None):
                return self._d.get(key, default)

        imported = []
        with tempfile.TemporaryDirectory() as tmp:
            entries = [FakeEntry("https://medium.com/nofit", "No Fit", fixture("nofit.html"))]
            new, failed = im.process_entries("Medium", entries, imported, blog_dir=tmp)
            self.assertEqual((new, failed), (0, 1))
            self.assertEqual(imported, [])
            self.assertEqual(os.listdir(tmp), [])
        self.assertEqual(im.exit_code(1), 1)
        self.assertEqual(im.exit_code(0), 0)


REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


class IdentityAndLedgerTests(unittest.TestCase):
    """Importer dedupe P1: identity extraction, dedup priority, ledger."""

    BODY = ("<p>As AI clusters scale from thousands of accelerators toward "
            "million-GPU systems, the network becomes part of the compute fabric itself.</p>")

    @staticmethod
    def _importer():
        import types
        for stub in ("feedparser", "requests"):
            sys.modules.setdefault(stub, types.ModuleType(stub))
        import import_medium as im
        return im

    class Entry:
        def __init__(self, link, title, summary, guid=""):
            self.summary = summary
            self._d = {"link": link, "title": title, "id": guid}

        def get(self, key, default=None):
            value = self._d.get(key, default)
            return value if value else default

    def test_medium_id_extraction_hosts_and_suffix(self):
        import medium_identity as mi
        self.assertEqual(mi.medium_id_from_url(
            "https://medium.com/@x/some-title-abcdef123456?source=rss"), "abcdef123456")
        self.assertEqual(mi.medium_id_from_url(
            "https://medium.com/p/abcdef123456"), "abcdef123456")
        self.assertEqual(mi.medium_id_from_url(
            "https://sinclairhuang.medium.com/title-abcdef123456"), "abcdef123456")
        self.assertIsNone(mi.medium_id_from_url(
            "https://example.com/some-title-abcdef123456"))  # non-medium host
        self.assertIsNone(mi.medium_id_from_url(
            "https://medium.com/@x/short-hex-abc123"))       # not 12 hex

    def test_canonical_normalization_tracking_vs_meaningful(self):
        import medium_identity as mi
        self.assertEqual(
            mi.normalize_canonical(
                "HTTPS://Medium.com/@x/t-abcdef123456?source=rss&utm_campaign=a#frag"),
            "https://medium.com/@x/t-abcdef123456")
        self.assertEqual(
            mi.normalize_canonical("https://example.com/paper?id=7&utm_source=x"),
            "https://example.com/paper?id=7")  # meaningful query survives

    def test_entry_identity_guid_agreement(self):
        import medium_identity as mi
        ident = mi.entry_identity(
            "https://medium.com/@x/t-abcdef123456?source=rss",
            "https://medium.com/p/abcdef123456")
        self.assertEqual(ident.medium_id, "abcdef123456")

    def test_entry_identity_mismatch_fails_closed(self):
        import medium_identity as mi
        with self.assertRaises(mi.IdentityError):
            mi.entry_identity(
                "https://medium.com/@x/t-abcdef123456",
                "https://medium.com/p/aaaabbbbcccc")

    def test_same_run_duplicate_second_entry_skipped(self):
        import tempfile
        import medium_identity as mi
        im = self._importer()
        with tempfile.TemporaryDirectory() as tmp:
            ledger = mi.Ledger([])
            entries = [
                self.Entry("https://medium.com/@x/fresh-story-abcdef123456?source=rss",
                           "Fresh Story", self.BODY),
                self.Entry("https://medium.com/@x/fresh-story-abcdef123456?utm_source=tw",
                           "Fresh Story", self.BODY),
            ]
            new, failed = im.process_entries("Medium", entries, ledger, blog_dir=tmp)
            self.assertEqual((new, failed), (1, 0))
            self.assertEqual(len(os.listdir(tmp)), 1)

    def test_cross_run_ledger_prevents_reimport(self):
        import tempfile
        import medium_identity as mi
        im = self._importer()
        with tempfile.TemporaryDirectory() as tmp:
            blog = os.path.join(tmp, "blog"); os.makedirs(blog)
            ledger_path = os.path.join(tmp, "ledger.json")
            ledger = mi.Ledger([])
            entry = self.Entry("https://medium.com/@x/fresh-story-abcdef123456?source=rss",
                               "Fresh Story", self.BODY)
            new, failed = im.process_entries("Medium", [entry], ledger, blog_dir=blog)
            self.assertEqual((new, failed), (1, 0))
            ledger.save_atomic(ledger_path)
            first_bytes = open(ledger_path, "rb").read()
            # a later run with an EMPTY blog dir must still dedupe via ledger
            ledger2 = mi.Ledger.load(ledger_path)
            blog2 = os.path.join(tmp, "blog2"); os.makedirs(blog2)
            new2, failed2 = im.process_entries("Medium", [entry], ledger2, blog_dir=blog2)
            self.assertEqual((new2, failed2), (0, 0))
            self.assertEqual(os.listdir(blog2), [])
            ledger2.save_atomic(ledger_path)
            self.assertEqual(open(ledger_path, "rb").read(), first_bytes)

    def test_real_regression_2026_06_29_ai_not_reimported(self):
        """fe85f9e regression: the existing old-short-slug file
        2026-06-29-ai.md vs the same article arriving with a full-CJK slug
        and medium id ba760d82d834 — zero new files, zero overwrite."""
        import shutil
        import tempfile
        import medium_identity as mi
        im = self._importer()
        real = os.path.join(REPO_ROOT, "content", "blog", "2026-06-29-ai.md")
        canonical = mi.canonical_from_markdown(open(real, encoding="utf-8").read())
        self.assertIn("ba760d82d834", canonical)
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copy(real, os.path.join(tmp, "2026-06-29-ai.md"))
            before = open(os.path.join(tmp, "2026-06-29-ai.md"), "rb").read()
            entry = self.Entry(canonical,
                               "AI 需求沒有消失，但價格開始接受壓力測試",
                               self.BODY,
                               guid="https://medium.com/p/ba760d82d834")
            ledger = mi.Ledger([])
            new, failed = im.process_entries("Medium", [entry], ledger, blog_dir=tmp)
            self.assertEqual((new, failed), (0, 0))
            self.assertEqual(os.listdir(tmp), ["2026-06-29-ai.md"])
            self.assertEqual(open(os.path.join(tmp, "2026-06-29-ai.md"), "rb").read(), before)
            self.assertTrue(ledger.has_medium_id("ba760d82d834"))

    def test_url_variants_share_one_identity(self):
        import medium_identity as mi
        base = mi.entry_identity("https://medium.com/@x/t-abcdef123456?source=rss")
        ledger = mi.Ledger([base])
        for variant in (
            "https://medium.com/@x/t-abcdef123456",
            "https://medium.com/@x/t-abcdef123456?utm_medium=email#open",
            "HTTPS://MEDIUM.com/@x/t-abcdef123456?source=twitter",
        ):
            self.assertTrue(ledger.knows(mi.entry_identity(variant)), variant)

    def test_different_ids_same_slug_fail_closed(self):
        import tempfile
        import medium_identity as mi
        im = self._importer()
        with tempfile.TemporaryDirectory() as tmp:
            fm = ('---\ntitle: "Fresh Story"\ndate: 2026-01-01\n'
                  'canonical: "https://medium.com/@x/fresh-story-aaaabbbbcccc"\n---\nbody\n')
            with open(os.path.join(tmp, "2026-01-01-fresh-story.md"), "w", encoding="utf-8") as fh:
                fh.write(fm)
            entry = self.Entry("https://medium.com/@x/fresh-story-abcdef123456",
                               "Fresh Story", self.BODY)
            ledger = mi.Ledger([])
            new, failed = im.process_entries("Medium", [entry], ledger, blog_dir=tmp)
            self.assertEqual((new, failed), (0, 1))          # manual review, not swallowed
            self.assertEqual(len(os.listdir(tmp)), 1)        # nothing new written
            self.assertFalse(ledger.has_medium_id("abcdef123456"))  # not recorded

    def test_ledger_missing_corrupt_unknown_all_fail(self):
        import tempfile
        import medium_identity as mi
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(mi.LedgerError):
                mi.Ledger.load(os.path.join(tmp, "absent.json"))
            corrupt = os.path.join(tmp, "corrupt.json")
            open(corrupt, "w").write("{not json")
            with self.assertRaises(mi.LedgerError):
                mi.Ledger.load(corrupt)
            unknown = os.path.join(tmp, "unknown.json")
            open(unknown, "w").write('{"version": 99, "identities": []}')
            with self.assertRaises(mi.LedgerError):
                mi.Ledger.load(unknown)

    def test_ledger_legacy_url_list_migrates(self):
        import medium_identity as mi
        legacy = ['https://medium.com/@x/t-abcdef123456?source=rss',
                  'https://example.com/elsewhere?id=3&utm_source=x']
        ledger = mi.Ledger.parse(__import__("json").dumps(legacy))
        self.assertTrue(ledger.has_medium_id("abcdef123456"))
        self.assertTrue(ledger.has_canonical("https://example.com/elsewhere?id=3"))
        serialized = ledger.serialize()
        self.assertIn('"version": 1', serialized)

    def test_ledger_atomic_deterministic_write(self):
        import tempfile
        import medium_identity as mi
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ledger.json")
            ledger = mi.Ledger([mi.entry_identity(
                "https://medium.com/@x/t-abcdef123456?source=rss")])
            ledger.save_atomic(path)
            once = open(path, "rb").read()
            ledger.save_atomic(path)
            self.assertEqual(open(path, "rb").read(), once)
            self.assertTrue(once.endswith(b"\n"))
            self.assertEqual([f for f in os.listdir(tmp) if f.startswith(".ledger-")], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
