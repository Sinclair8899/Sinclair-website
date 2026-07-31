#!/usr/bin/env python3
"""Post-build acceptance checks for docs/: internal links, assets, anchors.

Run from repo root after `hugo`. Exits 1 on any broken internal reference.
"""
import os
import re
import sys
from urllib.parse import unquote, urlparse

DOCS = "docs"
SITE_HOSTS = {"sinclairhuang.org", "www.sinclairhuang.org"}
REF_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
ID_RE = re.compile(r"""(?:id|name)\s*=\s*["']([^"']+)["']""", re.I)
SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:")


def served_target(path):
    """Map a URL path to a file under docs/, or None if it doesn't resolve."""
    rel = unquote(path).lstrip("/")
    fs = os.path.join(DOCS, rel) if rel else DOCS
    if os.path.isfile(fs):
        return fs
    if os.path.isdir(fs) and os.path.isfile(os.path.join(fs, "index.html")):
        return os.path.join(fs, "index.html")
    if not rel.endswith("/") and os.path.isfile(fs + "/index.html"):
        return fs + "/index.html"
    return None


def main():
    html_files = []
    for root, _dirs, files in os.walk(DOCS):
        for f in files:
            if f.endswith((".html", ".xml")):
                html_files.append(os.path.join(root, f))

    id_cache = {}

    def ids_of(fs_path):
        if fs_path not in id_cache:
            with open(fs_path, encoding="utf-8", errors="replace") as fh:
                id_cache[fs_path] = set(ID_RE.findall(fh.read()))
        return id_cache[fs_path]

    errors = []
    for hf in html_files:
        if not hf.endswith(".html"):
            continue
        with open(hf, encoding="utf-8", errors="replace") as fh:
            content = fh.read()
        for ref in REF_RE.findall(content):
            if ref.startswith(SKIP_SCHEMES):
                continue
            parsed = urlparse(ref)
            if parsed.scheme in ("http", "https") and parsed.hostname not in SITE_HOSTS:
                continue  # external
            if parsed.scheme and parsed.scheme not in ("http", "https"):
                continue
            path, frag = parsed.path, parsed.fragment
            if not path:  # same-page fragment
                if frag and frag not in ids_of(hf):
                    errors.append(f"{hf}: broken same-page anchor #{frag}")
                continue
            if not path.startswith("/"):
                continue  # relative refs don't occur in this build; ignore
            target = served_target(path)
            if target is None:
                errors.append(f"{hf}: broken internal link {ref}")
            elif frag and target.endswith(".html") and frag not in ids_of(target):
                errors.append(f"{hf}: missing anchor #{frag} at {path}")

    if errors:
        print(f"FAIL: {len(errors)} broken internal reference(s)")
        for e in sorted(set(errors)):
            print("  " + e)
        return 1
    print(f"OK: internal links/assets/anchors verified across {len(html_files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
