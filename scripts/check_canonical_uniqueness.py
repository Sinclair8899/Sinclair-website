#!/usr/bin/env python3
"""Source-side canonical uniqueness gate (Importer dedupe P1) — gate 9.

Scans the canonical: front matter of every non-draft article under
content/blog and content/insights (full-line --- delimiters; NEVER the
substring '---': Medium canonicals contain six-dash runs) and fails when
two source paths share a normalized canonical or a Medium ID. This is the
build-side backstop for the 2026-08-03 duplicate import (fe85f9e,
reverted): a duplicate that slips past the importer can no longer pass
the site checks.

It reads SOURCE front matter only. It must never scan rendered
<link rel="canonical"> — that is Hugo's canonicalURL page semantics,
not the importer's provenance field.

Stable messages (asserted by test_checks.sh):
  DUPLICATE CANONICAL / DUPLICATE MEDIUM ID
Usage: check_canonical_uniqueness.py [CONTENT_ROOT]   (default: repo content/)
"""
import os
import re
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".github", "scripts"),
)
from medium_identity import medium_id_from_url, normalize_canonical  # noqa: E402

DRAFT_LINE = re.compile(r"^draft:\s*true\s*$")
CANONICAL_LINE = re.compile(r'^canonical:\s*["\']?(https?://[^"\']+)["\']?\s*$')


def front_matter_lines(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    if not lines or lines[0].strip() != "---":
        return []
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i]
    return []


def main(content_root):
    by_canonical = {}
    by_medium_id = {}
    errors = []
    scanned = 0
    for section in ("blog", "insights"):
        root = os.path.join(content_root, section)
        for dirpath, _dirs, files in os.walk(root):
            for fname in sorted(files):
                if not fname.endswith(".md") or fname == "_index.md":
                    continue
                path = os.path.join(dirpath, fname)
                rel = os.path.relpath(path, content_root).replace(os.sep, "/")
                fm = front_matter_lines(path)
                if any(DRAFT_LINE.match(line) for line in fm):
                    continue
                canonical = next(
                    (m.group(1) for line in fm if (m := CANONICAL_LINE.match(line))),
                    None,
                )
                if not canonical:
                    continue
                scanned += 1
                norm = normalize_canonical(canonical)
                if norm in by_canonical:
                    errors.append(
                        f"DUPLICATE CANONICAL: {norm} -> {by_canonical[norm]} AND {rel}"
                    )
                else:
                    by_canonical[norm] = rel
                medium_id = medium_id_from_url(canonical)
                if medium_id:
                    if medium_id in by_medium_id:
                        errors.append(
                            f"DUPLICATE MEDIUM ID: {medium_id} -> {by_medium_id[medium_id]} AND {rel}"
                        )
                    else:
                        by_medium_id[medium_id] = rel
    for line in errors:
        print(line)
    if not errors:
        print(
            f"Canonical uniqueness: {len(by_canonical)} canonicals / "
            f"{len(by_medium_id)} Medium IDs / 0 duplicates"
        )
    return 1 if errors else 0


if __name__ == "__main__":
    default_root = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content")
    )
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else default_root))
