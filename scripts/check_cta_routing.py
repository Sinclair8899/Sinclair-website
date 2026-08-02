#!/usr/bin/env python3
"""Step 4 CTA routing checker — semantic, stdlib only. Gate 6b in check_site.sh.

Contract: every non-draft article under content/blog + content/insights
declares cta ("advisory" | "subscribe" | "none") in front matter — the ONLY
routing input — and its rendered page must agree:

  advisory  -> exactly one CTA element, data-cta-type="advisory",
               exactly one link inside, href exactly /advisory/#projects
  subscribe -> exactly one CTA element, data-cta-type="subscribe",
               exactly one link inside, href exactly
               https://sinclairhuang.substack.com/
  none      -> no CTA element at all

Parsing rules (hard requirements):
- Front matter is delimited by FULL LINES equal to "---". Never split the
  file on the substring "---": Medium canonical URLs legitimately contain
  runs of six dashes.
- HTML is parsed with html.parser, never regex: attribute order, extra
  harmless class tokens, and formatting must not matter. A CTA element is
  any element whose class attribute CONTAINS the token "advisory-cta".
- Ordinary in-article links are invisible to this checker (only links
  nested inside a CTA element are inspected).
- Expected counts are derived DYNAMICALLY from source front matter — the
  18/11 split of a particular release is asserted by that release's
  acceptance run, never hardcoded here.
- Pages are paired by Hugo's default path mapping
  content/<sec>/<rel>.md -> docs/<sec>/<rel>/index.html; a missing page,
  an unmapped extra article page, or a meta-refresh alias stub in the
  wrong place is an error. Genuine alias stubs are skipped.

Error message prefixes (stable, asserted by test_checks.sh):
  SOURCE CTA MISSING / SOURCE CTA UNKNOWN / ARTICLE PAGE MISSING /
  CTA MISSING ON PAGE / DUPLICATE CTA ON PAGE / CTA TYPE MISMATCH /
  CTA TARGET WRONG / CTA ON NONE PAGE / UNEXPECTED ARTICLE PAGE
"""
import os
import posixpath
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

VALID_CTA = {"advisory", "subscribe", "none"}
TARGETS = {
    "advisory": "/advisory/#projects",
    "subscribe": "https://sinclairhuang.substack.com/",
}
CTA_LINE = re.compile(r'^cta:\s*["\']?([A-Za-z0-9_-]+)["\']?\s*$')
DRAFT_LINE = re.compile(r'^draft:\s*(true|false)\s*$')
REFRESH_RE = re.compile(r"^\s*(\d+)\s*;\s*url\s*=\s*(\S+)\s*$", re.IGNORECASE)
VOID_TAGS = frozenset(
    "area base br col embed hr img input link meta param source track wbr".split()
)


def parse_front_matter(path):
    """Return the front-matter lines, honoring full-line --- delimiters only."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i]
    return None


class PageScan(HTMLParser):
    """Collects CTA elements (class token advisory-cta), their data-cta-type,
    the hrefs nested inside them, and refresh metas."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ctas = []          # list of dicts: {type: str|None, hrefs: []}
        self.refreshes = []     # raw content strings of http-equiv=refresh metas
        self.canonicals = []    # canonical link hrefs
        self._stack = []        # depth counters for open CTA elements

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "meta" and a.get("http-equiv", "").strip().lower() == "refresh":
            self.refreshes.append(a.get("content", ""))
        if tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonicals.append(a.get("href", "").strip())
        in_cta = bool(self._stack)
        if tag == "a" and in_cta and "href" in a:
            self.ctas[self._stack[-1][0]]["hrefs"].append(a["href"])
        if "advisory-cta" in a.get("class", "").split():
            self.ctas.append({"type": a.get("data-cta-type"), "hrefs": []})
            self._stack.append([len(self.ctas) - 1, 1])
            return
        if self._stack and tag not in VOID_TAGS:
            self._stack[-1][1] += 1

    def handle_endtag(self, tag):
        if self._stack and tag not in VOID_TAGS:
            self._stack[-1][1] -= 1
            if self._stack[-1][1] <= 0:
                self._stack.pop()


def scan_page(path):
    scanner = PageScan()
    with open(path, encoding="utf-8", errors="replace") as fh:
        scanner.feed(fh.read())
    return scanner


def is_genuine_alias(scan, expected):
    """A page may be skipped as an alias stub ONLY when it is a real one:
    exactly one zero-second refresh, exactly one canonical, target equal to
    the canonical, and the target — urlparse -> unquote once ->
    posixpath.normpath — resolving to a KNOWN canonical article page. A
    refresh pointing anywhere else keeps the page in scope and it will be
    reported as UNEXPECTED ARTICLE PAGE."""
    if len(scan.refreshes) != 1 or len(scan.canonicals) != 1:
        return False
    m = REFRESH_RE.match(scan.refreshes[0])
    if not m or int(m.group(1)) != 0:
        return False
    target = m.group(2)
    if not target or target != scan.canonicals[0]:
        return False
    norm = posixpath.normpath(unquote(urlparse(target).path))
    rel = norm.strip("/") + "/index.html"
    return rel in expected


def main(docs, content_root):
    errors = []
    expected = {}   # docs-relative page path -> cta value
    counts = {"advisory": 0, "subscribe": 0, "none": 0}

    for section in ("blog", "insights"):
        src_root = os.path.join(content_root, section)
        for root, _dirs, files in os.walk(src_root):
            for fname in sorted(files):
                if not fname.endswith(".md"):
                    continue
                if fname == "_index.md":
                    continue  # section list page — no CTA layout, not an article
                src = os.path.join(root, fname)
                rel_src = os.path.relpath(src, content_root)
                fm = parse_front_matter(src)
                if fm is None:
                    errors.append(f"SOURCE CTA MISSING: {rel_src} (no front matter)")
                    continue
                cta = draft = None
                for line in fm:
                    m = CTA_LINE.match(line)
                    if m:
                        cta = m.group(1)
                    m = DRAFT_LINE.match(line)
                    if m:
                        draft = m.group(1) == "true"
                if cta is None:
                    errors.append(f"SOURCE CTA MISSING: {rel_src}")
                    continue
                if cta not in VALID_CTA:
                    errors.append(f"SOURCE CTA UNKNOWN: {rel_src} ({cta!r})")
                    continue
                if draft:
                    continue
                rel_page = os.path.splitext(os.path.relpath(src, content_root))[0]
                expected[rel_page.replace(os.sep, "/") + "/index.html"] = cta

    if not errors and not expected:
        errors.append(
            "NO NON-DRAFT ARTICLES FOUND under content blog/insights — "
            "the CTA gate must never pass on an empty set"
        )

    for rel_page, cta in sorted(expected.items()):
        page = os.path.join(docs, rel_page)
        if not os.path.isfile(page):
            errors.append(f"ARTICLE PAGE MISSING: {rel_page}")
            continue
        scan = scan_page(page)
        n = len(scan.ctas)
        counts[cta] += 1
        if cta == "none":
            if n:
                errors.append(f"CTA ON NONE PAGE: {rel_page}")
            continue
        if n == 0:
            errors.append(f"CTA MISSING ON PAGE: {rel_page}")
            continue
        if n > 1:
            errors.append(f"DUPLICATE CTA ON PAGE: {rel_page} ({n} CTAs)")
            continue
        block = scan.ctas[0]
        if block["type"] != cta:
            errors.append(f"CTA TYPE MISMATCH: {rel_page} expected {cta} got {block['type']!r}")
            continue
        want = TARGETS[cta]
        if len(block["hrefs"]) != 1 or block["hrefs"][0] != want:
            errors.append(f"CTA TARGET WRONG: {rel_page} expected exactly [{want}] got {block['hrefs']!r}")

    # No article page may exist without a source expectation.
    for section in ("blog", "insights"):
        sec_root = os.path.join(docs, section)
        for root, _dirs, files in os.walk(sec_root):
            if "index.html" not in files:
                continue
            page = os.path.join(root, "index.html")
            rel = os.path.relpath(page, docs).replace(os.sep, "/")
            if rel == f"{section}/index.html" or "/page/" in rel:
                continue  # section list + pagination
            if rel in expected:
                continue
            if is_genuine_alias(scan_page(page), expected):
                continue  # genuine alias stub onto a known article
            errors.append(f"UNEXPECTED ARTICLE PAGE (no source mapping): {rel}")

    for line in errors[:20]:
        print(line)
    if len(errors) > 20:
        print(f"... and {len(errors) - 20} more CTA-routing errors")
    if not errors:
        checked = sum(counts.values())
        print(
            f"CTA routing: {checked} article pages match their front matter "
            f"({counts['advisory']} advisory / {counts['subscribe']} subscribe / "
            f"{counts['none']} none)"
        )
    return 1 if errors else 0


if __name__ == "__main__":
    docs = sys.argv[1] if len(sys.argv) > 1 else "docs"
    default_content = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content")
    content = sys.argv[2] if len(sys.argv) > 2 else os.path.normpath(default_content)
    sys.exit(main(docs, content))
