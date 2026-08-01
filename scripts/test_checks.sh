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

expect() { # expect <name> <pass|fail> <dir> [required-error-message]
  local name=$1 want=$2 dir=$3 msg=${4:-} got
  if scripts/check_site.sh "$dir" "$TMP/before" >"$TMP/out-$name" 2>&1; then got=pass; else got=fail; fi
  if [ "$got" != "$want" ]; then
    echo "FAIL $name — checker ${got}ed, expected $want; output:"
    sed 's/^/     /' "$TMP/out-$name" | tail -8
    RESULT=1
  elif [ -n "$msg" ] && ! grep -qF "$msg" "$TMP/out-$name"; then
    # failing for the WRONG reason must not count as a pass of the test
    echo "FAIL $name — failed, but without the expected message: $msg"
    sed 's/^/     /' "$TMP/out-$name" | tail -8
    RESULT=1
  else
    echo "ok   $name (checker ${got}ed as expected${msg:+, with the expected message})"
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
expect unledgered-disappeared-url fail "$TMP/case" "URL DISAPPEARED AND NOT IN redirects.tsv"

fresh
printf '<div class="advisory-cta">dup</div>\n' >> "$TMP/case/$ARTICLE"
expect duplicate-cta fail "$TMP/case"

fresh
touch "$TMP/case/publications/_index.md.bak"
expect backup-file-in-output fail "$TMP/case"

fresh
mkdir "$TMP/case/blog/some-article 5"
cp "$TMP/case/$ARTICLE" "$TMP/case/blog/some-article 5/index.html"
expect sync-duplicate-dir-in-output fail "$TMP/case"

fresh
mkdir "$TMP/case/blog/some-article 12"
cp "$TMP/case/$ARTICLE" "$TMP/case/blog/some-article 12/index.html"
expect sync-duplicate-multidigit-dir fail "$TMP/case"

fresh
mkdir "$TMP/case/blog/some-article (12)"
cp "$TMP/case/$ARTICLE" "$TMP/case/blog/some-article (12)/index.html"
expect sync-duplicate-parenthesized-dir fail "$TMP/case"

fresh
touch "$TMP/case/favicon 12.png"
expect sync-duplicate-png fail "$TMP/case" "JUNK FILES"

fresh
touch "$TMP/case/update-news 12.yml"
expect sync-duplicate-yml fail "$TMP/case" "JUNK FILES"

fresh
touch "$TMP/case/data-name 12.json"
expect sync-duplicate-json fail "$TMP/case" "JUNK FILES"

# Hugo version parsing fixtures — official releases carry a commit hash,
# brew carries extra metadata; only the BASE semver may decide.
vexpect() { # vexpect <name> <pass|fail> <version-token>
  local name=$1 want=$2 token=$3 got
  if scripts/check_hugo_version.sh "$token" >/dev/null 2>&1; then got=pass; else got=fail; fi
  if [ "$got" = "$want" ]; then
    echo "ok   $name (version gate ${got}ed as expected)"
  else
    echo "FAIL $name — version gate ${got}ed for '$token', expected $want"
    RESULT=1
  fi
}
vexpect hugo-official-release-hash pass "v0.152.2-6abd821c8dd41a10f7f9ba52a4dfebdaa1a84151+extended"
vexpect hugo-brew-metadata pass "v0.152.2+extended+withdeploy"
vexpect hugo-reject-0.152.20 fail "v0.152.20-6abd821+extended"

[ "$RESULT" = 0 ] && echo "NEGATIVE TESTS: all faults detected" || echo "NEGATIVE TESTS FAILED"
exit "$RESULT"
