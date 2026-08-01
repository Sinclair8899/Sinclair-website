#!/usr/bin/env bash
# Negative tests for the acceptance checker: each seeded fault MUST make
# scripts/check_site.sh fail, and a pristine tree MUST pass.
# Usage: scripts/test_checks.sh   (requires an up-to-date docs/ build)
set -uo pipefail
cd "$(dirname "$0")/.."

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cp -R docs "$TMP/base"
(cd "$TMP/base" && find . -name index.html | sed 's|^\.||;s|index\.html$||' | sort) > "$TMP/before"

ARTICLE="blog/2026-06-06-ai-needs-a-place-to-land/index.html"   # ordinary article, not in ledger
RESULT=0

expect() { # expect <name> <pass|fail> <dir>
  local name=$1 want=$2 dir=$3 got
  if scripts/check_site.sh "$dir" "$TMP/before" >"$TMP/out-$name" 2>&1; then got=pass; else got=fail; fi
  if [ "$got" = "$want" ]; then
    echo "ok   $name (checker ${got}ed as expected)"
  else
    echo "FAIL $name — checker ${got}ed, expected $want; output:"
    sed 's/^/     /' "$TMP/out-$name" | tail -8
    RESULT=1
  fi
}

fresh() { rm -rf "$TMP/case"; cp -R "$TMP/base" "$TMP/case"; }

fresh
expect pristine pass "$TMP/case"

fresh
printf '<p><a href="%%5Bhttps://example.com%%5D(https://example.com)">x</a></p>\n' >> "$TMP/case/$ARTICLE"
expect malformed-relative-link fail "$TMP/case"

fresh
printf '<img src="http://localhost:57206/live.png">\n' >> "$TMP/case/$ARTICLE"
expect localhost-any-port-leak fail "$TMP/case"

fresh
rm -rf "$TMP/case/$(dirname "$ARTICLE")"
expect unledgered-disappeared-url fail "$TMP/case"

fresh
printf '<div class="advisory-cta">dup</div>\n' >> "$TMP/case/$ARTICLE"
expect duplicate-cta fail "$TMP/case"

fresh
touch "$TMP/case/publications/_index.md.bak"
expect backup-file-in-output fail "$TMP/case"

fresh
mkdir "$TMP/case/blog/some-article 2"
cp "$TMP/case/$ARTICLE" "$TMP/case/blog/some-article 2/index.html"
expect finder-duplicate-dir-in-output fail "$TMP/case"

[ "$RESULT" = 0 ] && echo "NEGATIVE TESTS: all faults detected" || echo "NEGATIVE TESTS FAILED"
exit "$RESULT"
