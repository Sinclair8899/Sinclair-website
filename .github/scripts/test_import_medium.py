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
            self.assertNotIn(banned, sys.modules, f"{banned} leaked into the transform layer")

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
