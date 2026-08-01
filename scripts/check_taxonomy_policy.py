#!/usr/bin/env python3
"""3B taxonomy policy — semantic checker (stdlib only), called by check_site.sh gate 4c.

Rules enforced against a built tree (DOCS):
1. Every real HTML page whose FIRST path segment (relative to DOCS) is
   tags/ or categories/ must carry robots meta that parses to exactly
   {noindex, follow} — attribute order, case, and comma/whitespace variants
   are all accepted; extra or conflicting directives (nofollow, index,
   none, ...) are rejected. googlebot metas on those pages must agree.
2. The ONLY exemption is a genuine pagination alias stub: relative path
   (tags|categories)/**/page/1/index.html AND a zero-second meta refresh
   whose target equals the page's canonical link. A page/1 file that is
   not a valid stub fails; a refresh on any other taxonomy page fails.
3. Outside the taxonomy dirs, any robots/googlebot meta containing
   noindex (or none) fails. Classification is by first path segment only.
4. sitemap.xml is parsed as XML; a <loc> whose URL path — after percent-
   decoding and normalization — has tags or categories as its first
   segment fails (catches /tags, /tags/, and encoded forms alike).
5. While DOCS/research exists, /research/, /research/ai-infrastructure/
   and /research/semiconductors/ must stay in the sitemap.

Error message prefixes are stable and asserted by test_checks.sh:
  TAXONOMY PAGE MISSING NOINDEX / TAXONOMY PAGE HAS UNEXPECTED REFRESH /
  INVALID TAXONOMY PAGINATION STUB / NOINDEX LEAKED OUTSIDE TAXONOMY /
  TAXONOMY URL IN SITEMAP / RESEARCH URL MISSING FROM SITEMAP
"""
import os
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

TAXONOMY_SEGMENTS = {"tags", "categories"}
RESEARCH_URLS = ["/research/", "/research/ai-infrastructure/", "/research/semiconductors/"]
STUB_RE = re.compile(r"^(tags|categories)/.+/page/1/index\.html$")
REFRESH_RE = re.compile(r"^\s*(\d+)\s*;\s*url\s*=\s*(\S+)\s*$", re.IGNORECASE)
MAX_REPORT = 20


class HeadScan(HTMLParser):
    """Collects robots/googlebot metas, refresh metas, and canonical links."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.robots = []     # (meta-name, frozenset of lowercased directives)
        self.refreshes = []  # raw content strings of http-equiv=refresh metas
        self.canonicals = []  # canonical hrefs

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "meta":
            name = a.get("name", "").strip().lower()
            if name in ("robots", "googlebot"):
                directives = frozenset(
                    d.strip().lower() for d in a.get("content", "").split(",") if d.strip()
                )
                self.robots.append((name, directives))
            if a.get("http-equiv", "").strip().lower() == "refresh":
                self.refreshes.append(a.get("content", ""))
        elif tag == "link":
            if "canonical" in a.get("rel", "").lower().split():
                self.canonicals.append(a.get("href", "").strip())


def scan_html(path):
    scanner = HeadScan()
    with open(path, encoding="utf-8", errors="replace") as fh:
        scanner.feed(fh.read())
    return scanner


def has_noindex(directives):
    return "noindex" in directives or "none" in directives


def is_valid_stub(scan):
    """Zero-second refresh whose target equals the single canonical href."""
    if len(scan.refreshes) != 1 or len(scan.canonicals) != 1:
        return False
    m = REFRESH_RE.match(scan.refreshes[0])
    if not m or int(m.group(1)) != 0:
        return False
    return m.group(2) == scan.canonicals[0] != ""


def main(docs):
    errors = []

    for root, _dirs, files in os.walk(docs):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            path = os.path.join(root, fname)
            rel = os.path.relpath(path, docs).replace(os.sep, "/")
            first_segment = rel.split("/", 1)[0]
            scan = scan_html(path)

            if first_segment in TAXONOMY_SEGMENTS:
                if STUB_RE.match(rel):
                    if not is_valid_stub(scan):
                        errors.append(f"INVALID TAXONOMY PAGINATION STUB: {rel}")
                    continue
                if scan.refreshes:
                    errors.append(f"TAXONOMY PAGE HAS UNEXPECTED REFRESH: {rel}")
                names = {name for name, _ in scan.robots}
                exact = all(d == {"noindex", "follow"} for _, d in scan.robots)
                if "robots" not in names or not exact:
                    errors.append(f"TAXONOMY PAGE MISSING NOINDEX: {rel}")
            else:
                if any(has_noindex(d) for _, d in scan.robots):
                    errors.append(f"NOINDEX LEAKED OUTSIDE TAXONOMY: {rel}")

    sitemap = os.path.join(docs, "sitemap.xml")
    if not os.path.isfile(sitemap):
        errors.append(f"SITEMAP MISSING: {sitemap}")
    else:
        try:
            tree = ET.parse(sitemap)
        except ET.ParseError as exc:
            errors.append(f"SITEMAP PARSE ERROR: {exc}")
        else:
            paths = []
            for el in tree.getroot().iter():
                if el.tag.rsplit("}", 1)[-1] == "loc" and el.text:
                    loc = el.text.strip()
                    decoded = unquote(urlparse(loc).path)
                    segments = [s for s in decoded.split("/") if s]
                    paths.append(decoded)
                    if segments and segments[0].casefold() in TAXONOMY_SEGMENTS:
                        errors.append(f"TAXONOMY URL IN SITEMAP: {loc}")
            if os.path.isdir(os.path.join(docs, "research")):
                for url in RESEARCH_URLS:
                    if url not in paths:
                        errors.append(f"RESEARCH URL MISSING FROM SITEMAP: {url}")

    for line in errors[:MAX_REPORT]:
        print(line)
    if len(errors) > MAX_REPORT:
        print(f"... and {len(errors) - MAX_REPORT} more taxonomy-policy errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "docs"))
