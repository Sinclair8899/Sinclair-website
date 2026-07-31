#!/usr/bin/env bash
# Standard production build + acceptance checks for sinclairhuang.org.
# Usage: scripts/build_and_check.sh   (from anywhere; cds to repo root)
set -uo pipefail
cd "$(dirname "$0")/.."

BEFORE=$(mktemp) AFTER=$(mktemp)
url_inventory() { (cd docs 2>/dev/null && find . -name index.html | sed 's|^\.||;s|index\.html$||' | sort) || true; }
url_inventory > "$BEFORE"

hugo --cleanDestinationDir --panicOnWarning --printPathWarnings \
     --destination docs --baseURL "https://sinclairhuang.org/" || exit 1

FAIL=0

# Root files that must survive every build (all sourced from static/)
for f in CNAME .nojekyll robots.txt favicon.ico favicon-16x16.png \
         favicon-32x32.png apple-touch-icon.png safari-pinned-tab.svg; do
  [ -f "docs/$f" ] || { echo "MISSING: docs/$f"; FAIL=1; }
done
[ "$(cat docs/CNAME 2>/dev/null)" = "sinclairhuang.org" ] || { echo "BAD CNAME"; FAIL=1; }

# Dev-server URL leak
LEAK=$(grep -rl '127\.0\.0\.1:1313\|localhost:1313' docs/ 2>/dev/null | head -5)
[ -z "$LEAK" ] || { echo "DEV URL LEAK:"; echo "$LEAK"; FAIL=1; }

# Advisory fixed anchors (linked from pillar CTAs and external notes)
for a in english chinese retainer projects briefings start; do
  grep -q "id=\"$a\"" docs/advisory/index.html || { echo "MISSING ANCHOR #$a on /advisory/"; FAIL=1; }
done

# Internal links, assets, cross-page anchors
python3 scripts/check_links.py || FAIL=1

# URLs that disappeared vs the previous build — must be intentional & ledgered
url_inventory > "$AFTER"
GONE=$(comm -23 "$BEFORE" "$AFTER")
if [ -n "$GONE" ]; then
  echo "WARNING — URLs disappeared this build (add to redirects.md if intentional):"
  echo "$GONE"
fi

[ "$FAIL" = 0 ] && echo "BUILD + CHECKS PASSED" || echo "BUILD CHECKS FAILED"
exit "$FAIL"
