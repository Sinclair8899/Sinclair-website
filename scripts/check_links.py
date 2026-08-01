#!/usr/bin/env python3
"""Post-build link/asset/anchor checks for the built site.

Usage: check_links.py [DOCS_DIR]   (default: docs)

Rules
-----
- Root-relative (`/...`) and absolute-to-site refs must resolve to a built file.
- Cross-page and same-page fragments must match an id/name in the target page.
- Any other relative or malformed href/src (e.g. `%5Bhttps...`, `*https...*`,
  `foo/bar.html`) is an ERROR — the build must not emit relative URLs at all,
  so anything relative is a broken Markdown link in disguise.
- Every <loc> in sitemap.xml must resolve to a built page.

Exit 1 on any failure. Reports the exact number of HTML files scanned.
"""
import os
import re
import sys
from urllib.parse import unquote, urlparse

SITE_HOSTS = {"sinclairhuang.org", "www.sinclairhuang.org"}
REF_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
ID_RE = re.compile(r"""(?:id|name)\s*=\s*["']([^"']+)["']""", re.I)
LOC_RE = re.compile(r"<loc>([^<]+)</loc>")
SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:")


def served_target(docs, path):
    """Map a URL path to a file under docs, or None if it doesn't resolve."""
    rel = unquote(path).lstrip("/")
    fs = os.path.join(docs, rel) if rel else docs
    if os.path.isfile(fs):
        return fs
    if os.path.isdir(fs) and os.path.isfile(os.path.join(fs, "index.html")):
        return os.path.join(fs, "index.html")
    if not rel.endswith("/") and os.path.isfile(fs + "/index.html"):
        return fs + "/index.html"
    return None


def main():
    docs = sys.argv[1] if len(sys.argv) > 1 else "docs"
    if not os.path.isdir(docs):
        print(f"FAIL: no such directory: {docs}")
        return 1

    html_files = []
    for root, _dirs, files in os.walk(docs):
        html_files.extend(os.path.join(root, f) for f in files if f.endswith(".html"))

    id_cache = {}

    def ids_of(fs_path):
        if fs_path not in id_cache:
            with open(fs_path, encoding="utf-8", errors="replace") as fh:
                id_cache[fs_path] = set(ID_RE.findall(fh.read()))
        return id_cache[fs_path]

    errors, refs_checked = [], 0
    for hf in html_files:
        with open(hf, encoding="utf-8", errors="replace") as fh:
            content = fh.read()
        for ref in REF_RE.findall(content):
            if ref.startswith(SKIP_SCHEMES):
                continue
            parsed = urlparse(ref)
            if parsed.scheme in ("http", "https") and parsed.hostname not in SITE_HOSTS:
                continue  # external
            if parsed.scheme and parsed.scheme not in ("http", "https"):
                errors.append(f"{hf}: unexpected scheme in {ref!r}")
                continue
            refs_checked += 1
            path, frag = parsed.path, parsed.fragment
            if not path:  # same-page fragment
                if frag and frag not in ids_of(hf):
                    errors.append(f"{hf}: broken same-page anchor #{frag}")
                continue
            if not path.startswith("/"):
                errors.append(f"{hf}: relative or malformed URL {ref!r}")
                continue
            target = served_target(docs, path)
            if target is None:
                errors.append(f"{hf}: broken internal link {ref}")
            elif frag and target.endswith(".html") and frag not in ids_of(target):
                errors.append(f"{hf}: missing anchor #{frag} at {path}")

    sitemap = os.path.join(docs, "sitemap.xml")
    locs_checked = 0
    if os.path.isfile(sitemap):
        with open(sitemap, encoding="utf-8", errors="replace") as fh:
            for loc in LOC_RE.findall(fh.read()):
                locs_checked += 1
                p = urlparse(loc)
                if p.hostname not in SITE_HOSTS:
                    errors.append(f"sitemap.xml: foreign host in <loc> {loc}")
                elif served_target(docs, p.path) is None:
                    errors.append(f"sitemap.xml: <loc> does not resolve: {loc}")
    else:
        errors.append("sitemap.xml missing")

    if errors:
        print(f"FAIL: {len(errors)} broken reference(s) "
              f"({len(html_files)} HTML files scanned, {refs_checked} internal refs, "
              f"{locs_checked} sitemap locs)")
        for e in sorted(set(errors)):
            print("  " + e)
        return 1
    print(f"OK: {len(html_files)} HTML files scanned; {refs_checked} internal refs "
          f"and {locs_checked} sitemap locs verified; relative/malformed URLs: none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
