#!/usr/bin/env bash
# Post-build acceptance checks, testable against any built tree.
# Usage: scripts/check_site.sh [DOCS_DIR] [PREV_URL_INVENTORY_FILE] [CONTENT_ROOT]
#   DOCS_DIR defaults to docs; PREV inventory enables the disappeared-URL gate;
#   CONTENT_ROOT overrides the CTA gate's source root (fixtures only —
#   production runs use the repo's content/).
# Exits 1 on any failure. Negative-tested by scripts/test_checks.sh.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DOCS="${1:-docs}"
PREV="${2:-}"
CONTENT="${3:-}"
FAIL=0

# 1. Root files that must survive every build (all sourced from static/)
for f in CNAME .nojekyll robots.txt favicon.ico favicon-16x16.png \
         favicon-32x32.png apple-touch-icon.png safari-pinned-tab.svg; do
  [ -f "$DOCS/$f" ] || { echo "MISSING: $DOCS/$f"; FAIL=1; }
done
[ "$(cat "$DOCS/CNAME" 2>/dev/null)" = "sinclairhuang.org" ] || { echo "BAD CNAME"; FAIL=1; }

# 2. Dev-server URL leak — any localhost/127.0.0.1, any port
LEAK=$(grep -rlE 'https?://(localhost|127\.0\.0\.1)([:/]|")|(localhost|127\.0\.0\.1):[0-9]+' "$DOCS" 2>/dev/null | head -5)
[ -z "$LEAK" ] || { echo "DEV URL LEAK:"; echo "$LEAK"; FAIL=1; }

# 3. Backup / sync-duplicate junk must never reach the built site.
#    Shared pattern (scripts/junk_pattern.sh): one-or-more digits, ANY
#    extension — " 10", " (12)", "favicon 12.png", "update-news 12.yml".
. "$REPO/scripts/junk_pattern.sh"
JUNK=$(find "$DOCS" 2>/dev/null | grep -E "$JUNK_RE")
[ -z "$JUNK" ] || { echo "JUNK FILES IN BUILD OUTPUT:"; echo "$JUNK"; FAIL=1; }

# 4. Advisory fixed anchors (linked from CTAs and external notes)
for a in english chinese retainer projects briefings start; do
  grep -q "id=\"$a\"" "$DOCS/advisory/index.html" 2>/dev/null \
    || { echo "MISSING ANCHOR #$a on /advisory/"; FAIL=1; }
done

# 4b. Zero-date leak in the research section — a date-less page renders
#     0001-01-01 into JSON-LD and "Mon, 01 Jan 0001" into RSS. Scoped to
#     docs/research/ only: the three legacy zero-date RSS entries
#     (advisory/data/about) are separately ledgered old debt.
if [ -d "$DOCS/research" ]; then
  ZDATE=$(grep -rlE '0001-01-01|Jan 0001|January 1, 0001' "$DOCS/research" 2>/dev/null | head -5)
  [ -z "$ZDATE" ] || { echo "YEAR-0001 DATE IN RESEARCH OUTPUT:"; echo "$ZDATE"; FAIL=1; }
fi

# 4c. Taxonomy policy (3B): /tags/ and /categories/ pages keep their URLs
#     but must be exactly noindex,follow and out of the sitemap; nothing
#     outside the taxonomy dirs may carry noindex, and the research pages
#     must stay in the sitemap. Semantic HTML/XML parsing (robots variants,
#     encoded sitemap paths, genuine zero-second page/1 stubs only) lives
#     in scripts/check_taxonomy_policy.py. NOTE: pre-3B trees fail this
#     gate by design — the policy is part of acceptance from 3B on.
python3 "$REPO/scripts/check_taxonomy_policy.py" "$DOCS" || FAIL=1

# 5. Internal links, assets, anchors, sitemap (rejects relative/malformed URLs)
python3 "$REPO/scripts/check_links.py" "$DOCS" || FAIL=1

# 6. CTA routing (Step 4, sole authoritative CTA gate): every blog/insights
#    article's rendered CTA must match its front-matter cta param — count
#    (advisory/subscribe exactly one, none exactly zero), data-cta-type,
#    and exact target — parsed semantically by scripts/check_cta_routing.py.
#    Expectations derive from source front matter dynamically; an empty
#    non-draft article set is itself a failure. The optional third
#    CONTENT_ROOT argument exists for fixtures; production default is the
#    repo's content/.
if [ -n "$CONTENT" ]; then
  python3 "$REPO/scripts/check_cta_routing.py" "$DOCS" "$CONTENT" || FAIL=1
else
  python3 "$REPO/scripts/check_cta_routing.py" "$DOCS" || FAIL=1
fi

# 7. Disappeared URLs must be ledgered in redirects.tsv (machine-readable)
if [ -n "$PREV" ] && [ -f "$PREV" ]; then
  NOW=$(mktemp)
  (cd "$DOCS" && find . -name index.html | sed 's|^\.||;s|index\.html$||' | sort) > "$NOW"
  while IFS= read -r gone; do
    [ -n "$gone" ] || continue
    if printf '%s\n' "$gone" | grep -qE ' \(?[0-9]+\)?/'; then
      # sync-duplicate junk vanishing is cleanup, not loss
      echo "NOTE: junk URL removed by clean rebuild (OK): $gone"; continue
    fi
    awk -F'\t' -v p="$gone" '$1==p{found=1} END{exit !found}' "$REPO/redirects.tsv" \
      || { echo "URL DISAPPEARED AND NOT IN redirects.tsv: $gone"; FAIL=1; }
  done < <(comm -23 "$PREV" "$NOW")
  rm -f "$NOW"
else
  echo "NOTE: no previous inventory supplied — disappeared-URL gate skipped"
fi

[ "$FAIL" = 0 ] && echo "SITE CHECKS PASSED" || echo "SITE CHECKS FAILED"
exit "$FAIL"
