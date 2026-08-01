#!/usr/bin/env python3
"""Rendered-HTML content-hygiene checker.

Parses built pages' <h1>-<h4> elements and visible text nodes — searching the
Markdown source for literal '###' is NOT sufficient (a fused heading under the
length threshold, or Markdown residue like '**'/stray '*'/escaped '>', only
shows up reliably in the rendered output).

Usage: check_content_hygiene.py [DOCS_DIR] [url-path ...]
With no url-paths, scans every blog/insights article page.
Exit 1 if any page has findings.
"""
import os
import re
import sys
from html.parser import HTMLParser

HEADING_MAX = 110  # a heading longer than this has almost certainly swallowed body text



# Camel-case words that legitimately appear inside headings.
CAMEL_OK = re.compile(
    r"CoWoS|InFO|TurboQuant|MediaTek|TrendForce|SanDisk|AlphaFold|AlphaEvolve|"
    r"VibeGen|InnoVEX|McKinsey|GitHub|YouTube|LinkedIn|OpenAI|DeepMind|InPost|"
    r"HashTags?|IoT|SoIC|TSMC|NVIDIA|BioNTech|EDBA|COMPUTEX|macOS|iOS|iPadOS|SpaceX")


def fusion_signature(text):
    """Short heading+body fusions that a length threshold misses."""
    stripped = CAMEL_OK.sub("", text)
    return (re.search(r"[a-z]\?[A-Z]", stripped)                 # happen?My
            or re.search(r"(Note|Disclaimer|Summary|Reading|References|Keywords|"
                          r"Ending|Author)[\u4e00-\u9fff]", stripped)  # Note本文-style fusion
                          # (bare [A-Za-z][CJK] would misflag normal mixed titles like "AI晶片")
            or re.search(r"[a-z][A-Z][a-z]{2,}", stripped)        # scarceAnother
            or re.search(r"[A-Z]{2,}[A-Z][a-z]{2,}", stripped)    # AIThe (acronym+word)
            or re.search(r"[a-z][A-Z]{2,}", stripped)             # mattersIPM
            or re.search(r"[a-z][A-Z](?=[ ,.!?:;]|$)", stripped))  # factoryA market


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
    for t in p.texts:
        if t.startswith(("#", "## ", "### ")) and not t.startswith("#!") \
                and not re.fullmatch(r"(#[A-Za-z0-9][\w]*[\s]*)+", t):
            findings.append(f"visible literal #: {t[:90]!r}")  # hashtag blocks are whitelisted
        if "**" in t:
            findings.append(f"visible '**' residue: {t[:90]!r}")
        elif "*" in t:  # ANY literal asterisk surviving into rendered text is residue
            findings.append(f"visible '*' residue: {t[:90]!r}")
        if re.match(r">\s", t):  # escaped blockquote marker rendered as text
            findings.append(f"leading '>' residue: {t[:90]!r}")
    return findings




def selftest():
    """Fixtures: each named fault class must be caught; controls must pass."""
    must_flag = [
        "The third phase of AIThe first phase of AI was about models.",
        "Why this mattersIPM is not a magic number.",
        "Why does this happen?My reading is that",
        "Author Note本文以中文寫作",
        "The index can move faster than the factoryA market can reprice",
    ]
    must_pass = [
        "What Are CoWoS, HBM, and ABF — And Why Do They Matter",
        "TurboQuant and the Limits of Compression",
        "2025 AI晶片產業趨勢",
        "AI Infrastructure Is Not One Trade",
        "SK Hynix and Micron: The HBM Margin Engine",
        "macOS and iOS deployment targets",
    ]
    failures = []
    for s in must_flag:
        if not fusion_signature(s):
            failures.append(f"NOT flagged (should be): {s!r}")
    for s in must_pass:
        if fusion_signature(s):
            failures.append(f"flagged (should pass): {s!r}")
    text_cases = [  # (text, should_flag)
        ("*For the full research version, see the Substack edition on *", True),
        ("> Money flow doesn't lie.", True),
        ("#AIInfrastructure #HBM #CoWoS", False),
        ("Normal paragraph about HBM allocation.", False),
    ]
    for s, want in text_cases:
        got = bool("**" in s or ("*" in s) or re.match(r">\s", s)) if want or True else None
        flagged = bool(("*" in s) or re.match(r">\s", s))
        if flagged != want:
            failures.append(f"text case wrong (flagged={flagged}, want={want}): {s!r}")
    if failures:
        print("SELFTEST FAIL:")
        for f in failures:
            print("  " + f)
        return 1
    print(f"SELFTEST OK: {len(must_flag)} fault fixtures caught, "
          f"{len(must_pass)} controls pass, {len(text_cases)} text cases correct")
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
