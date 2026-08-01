#!/usr/bin/env python3
"""Generate a Cloudflare Bulk Redirects upload-ready CSV from redirects.tsv.

Usage: scripts/gen_cloudflare_csv.py   (from repo root; writes redirects-cloudflare.csv)

Excludes GONE rows and self-maps, prefixes the domain, emits 301 rows in
Cloudflare's CSV import format. Only useful once the DNS records are proxied
(orange cloud) — redirects are inert in the current DNS-only setup.
"""
import csv
import sys

DOMAIN = "https://sinclairhuang.org"

def main():
    rows = []
    with open("redirects.tsv", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                print(f"WARNING: malformed TSV line skipped: {line!r}", file=sys.stderr)
                continue
            old, new = parts[0], parts[1]
            if new == "GONE" or new == old:
                continue
            rows.append((DOMAIN + old, DOMAIN + new, "301"))

    # Cloudflare's Bulk Redirect CSV import forbids a header row — the file
    # must contain data rows only.
    with open("redirects-cloudflare.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    print(f"redirects-cloudflare.csv: {len(rows)} redirect rows, no header "
          f"(GONE/self-map excluded)")

if __name__ == "__main__":
    main()
