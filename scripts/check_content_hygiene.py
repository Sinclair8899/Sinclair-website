#!/usr/bin/env python3
"""Rendered-HTML content-hygiene checker.

Parses built pages' <h1>-<h4> elements and visible text nodes — searching the
Markdown source for literal '###' is NOT sufficient (a fused heading under the
length threshold, or Markdown residue like '**'/stray '*'/escaped '>', only
shows up reliably in the rendered output).

Usage:
  check_content_hygiene.py [DOCS_DIR] [url-path ...]   scan pages (default: all articles)
  check_content_hygiene.py --selftest                  render fixtures and run scan() on them

Exit 1 if any page (or selftest fixture) fails.
"""
import os
import re
import sys
import tempfile
from html.parser import HTMLParser

HEADING_MAX = 110  # a heading longer than this has almost certainly swallowed body text

# Camel-case words that legitimately appear in prose — matched ONLY as whole
# words (a fused "CoWoSThe" must NOT be eaten by the whitelist; the lookarounds
# guarantee the fusion evidence survives for the signatures below).
CAMEL_OK = re.compile(
    r"(?<![A-Za-z])(?:CoWoS|InFO|TurboQuant|MediaTek|TrendForce|SanDisk|AlphaFold|"
    r"AlphaEvolve|VibeGen|InnoVEX|McKinsey|GitHub|YouTube|LinkedIn|OpenAI|DeepMind|InPost|"
    r"HashTags?|IoT|SoIC|TSMC|NVIDIA|BioNTech|EDBA|COMPUTEX|macOS|iOS|iPadOS|SpaceX)"
    r"(?![A-Za-z])")


def fusion_signature(text):
    """Short heading+body fusions that a length threshold misses."""
    stripped = CAMEL_OK.sub("", text)
    return (re.search(r"[a-z]\?[A-Z]", stripped)                 # happen?My
            or re.search(r"(Note|Disclaimer|Summary|Reading|References|Keywords|"
                         r"Ending|Author)[一-鿿]", stripped)  # Note本文-style fusion
                         # (bare [A-Za-z][CJK] would misflag normal titles like "AI晶片")
            or re.search(r"[a-z][A-Z][a-z]{2,}", stripped)        # scarceAnother / TurboQuantThe
            or re.search(r"[A-Z]{2,}[A-Z][a-z]{2,}", stripped)    # AIThe (acronym+word)
            or re.search(r"[a-z][A-Z]{2,}", stripped)             # mattersIPM / CoWoSThe
            or re.search(r"[a-z][A-Z](?=[ ,.!?:;]|$)", stripped))  # factoryA market


def residue_findings(text, where):
    """Markdown residue checks shared by headings AND body text nodes."""
    out = []
    if "**" in text:
        out.append(f"{where} '**' residue: {text[:90]!r}")
    elif "*" in text:  # ANY literal asterisk surviving into rendered text is residue
        out.append(f"{where} '*' residue: {text[:90]!r}")
    if text.startswith(">"):  # escaped blockquote marker rendered as text (also '>Money')
        out.append(f"{where} leading '>' residue: {text[:90]!r}")
    return out


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.headings = []          # (tag, text)
        self._h = None
        self._depth = 0
        self.texts = []             # visible text inside the article body
        self._in_content = 0
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "div" and "post-content" in (d.get("class") or ""):
            self._in_content = self._depth + 1
        if tag in ("script", "style"):
            self._skip += 1
        if tag in ("h1", "h2", "h3", "h4") and self._h is None:
            self._h = [tag, ""]
        self._depth += 1

    def handle_endtag(self, tag):
        self._depth -= 1
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        if self._h and tag == self._h[0]:
            self.headings.append((self._h[0], " ".join(self._h[1].split())))
            self._h = None
        if self._in_content and self._depth < self._in_content:
            self._in_content = 0

    def handle_data(self, data):
        if self._skip:
            return
        if self._h is not None:
            self._h[1] += data
        elif self._in_content:
            t = data.strip()
            if t:
                self.texts.append(t)


def scan(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        p = Page()
        p.feed(fh.read())
    findings = []
    for tag, text in p.headings:
        if len(text) > HEADING_MAX:
            findings.append(f"{tag} swallowed body ({len(text)} chars): {text[:90]!r}…")
        if text.startswith("#") or "###" in text:
            findings.append(f"{tag} literal markdown: {text[:90]!r}")
        if fusion_signature(text):
            findings.append(f"{tag} fusion signature: {text[:90]!r}")
        findings.extend(residue_findings(text, tag))
    for t in p.texts:
        if t.startswith(("#", "## ", "### ")) and not t.startswith("#!") \
                and not re.fullmatch(r"(#[A-Za-z0-9][\w]*[\s]*)+", t):
            findings.append(f"visible literal #: {t[:90]!r}")  # hashtag blocks are whitelisted
        findings.extend(residue_findings(t, "visible"))
    return findings


def selftest():
    """Render fixture HTML and run the REAL scan() on it — the fixtures are the
    checker's own past misses; a scanner change that reopens one fails here."""
    must_flag = {  # marker -> fixture rendered as a real element
        "AIThe": '<h4>The third phase of AIThe first phase of AI was about models.</h4>',
        "mattersIPM": "<h3>Why this mattersIPM is not a magic number.</h3>",
        "happen?My": "<h3>Why does this happen?My reading is that</h3>",
        "Note本文": "<h3>Author Note本文以中文寫作</h3>",
        "factoryA": "<h4>The index can move faster than the factoryA market can reprice</h4>",
        "CoWoSThe": "<h4>CoWoSThe next phase of packaging</h4>",
        "TurboQuantThe": "<h4>TurboQuantThe next phase of compression</h4>",
        "SpaceXThe": "<h4>SpaceXThe next phase of launch</h4>",
        "macOSThe": "<h4>macOSThe next phase of the desktop</h4>",
        "InPostThe": "<h4>InPostThe next phase of lockers</h4>",
        "heading-star": "<h4>*Broken emphasis in a heading</h4>",
        "heading-quote": "<h4>&gt; Broken quote in a heading</h4>",
        "body-star": "<p>*For the full research version, see the Substack edition on *</p>",
        "body-quote-nospace": "<p>&gt;Money flow doesn't lie.</p>",
        "body-double-star": "<p>So the rule is ** realised margin runs below chip level.</p>",
    }
    must_pass = {
        "CoWoS-standalone": "<h3>CoWoS and HBM allocation</h3>",
        "TurboQuant-standalone": "<h3>TurboQuant and the Limits of Compression</h3>",
        "AI晶片": "<h1>2025 AI晶片產業趨勢</h1>",
        "SpaceX-standalone": "<h4>SpaceX and the launch market</h4>",
        "macOS-standalone": "<h4>macOS and iOS deployment targets</h4>",
        "InPost-standalone": "<h4>InPost and the next market</h4>",
        "plain-title": "<h3>AI Infrastructure Is Not One Trade</h3>",
        "hashtags": "<p>#AIInfrastructure #HBM #CoWoS</p>",
        "normal-paragraph": "<p>Normal paragraph about HBM allocation.</p>",
    }

    def render_and_scan(fragment):
        html = f'<html><body><div class="post-content">{fragment}</div></body></html>'
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(html)
            path = fh.name
        try:
            return scan(path)
        finally:
            os.unlink(path)

    failures = []
    for marker, frag in must_flag.items():
        if not render_and_scan(frag):
            failures.append(f"NOT flagged by scan() (should be): {marker}: {frag}")
    for marker, frag in must_pass.items():
        got = render_and_scan(frag)
        if got:
            failures.append(f"flagged by scan() (should pass): {marker}: {got}")

    if failures:
        print("SELFTEST FAIL:")
        for f in failures:
            print("  " + f)
        return 1
    print(f"SELFTEST OK: {len(must_flag)} fault fixtures caught by scan(), "
          f"{len(must_pass)} controls pass")
    return 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    docs = sys.argv[1] if len(sys.argv) > 1 else "docs"
    targets = sys.argv[2:]
    if not targets:
        targets = []
        for section in ("blog", "insights"):
            for root, _dirs, files in os.walk(os.path.join(docs, section)):
                if "index.html" in files and "/page/" not in root + "/":
                    with open(os.path.join(root, "index.html"), encoding="utf-8", errors="replace") as fh:
                        head = fh.read(4096)
                    if 'http-equiv="refresh"' in head:
                        continue
                    targets.append(os.path.relpath(root, docs))
        targets = [t for t in targets if t not in ("blog", "insights")]
    bad = 0
    for t in sorted(targets):
        f = os.path.join(docs, t, "index.html")
        if not os.path.isfile(f):
            print(f"MISSING PAGE: {t}")
            bad += 1
            continue
        findings = scan(f)
        if findings:
            bad += 1
            print(f"\n{t}: {len(findings)} finding(s)")
            for x in findings:
                print("  " + x)
    if bad:
        print(f"\nFAIL: {bad} page(s) with hygiene findings")
        return 1
    print(f"OK: {len(targets)} pages clean (rendered h1-h4 + visible text)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
