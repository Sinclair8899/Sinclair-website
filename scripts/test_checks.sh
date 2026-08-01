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

fresh
printf '<script type="application/ld+json">{"datePublished":"0001-01-01T00:00:00+00:00"}</script>\n' \
  >> "$TMP/case/research/ai-infrastructure/index.html"
expect zero-date-in-research fail "$TMP/case" "YEAR-0001 DATE IN RESEARCH OUTPUT"

fresh
python3 - "$TMP/case/tags/ai/index.html" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
p.write_text(p.read_text().replace('content="noindex,follow"', 'content="index, follow"'))
PY
expect taxonomy-missing-noindex fail "$TMP/case" "TAXONOMY PAGE MISSING NOINDEX"

fresh
python3 - "$TMP/case/sitemap.xml" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
p.write_text(p.read_text().replace('</urlset>', '  <url><loc>https://sinclairhuang.org/tags/ai/</loc></url>\n</urlset>'))
PY
expect taxonomy-url-in-sitemap fail "$TMP/case" "TAXONOMY URL IN SITEMAP"

fresh
printf '<meta name="robots" content="noindex,follow">\n' >> "$TMP/case/research/ai-infrastructure/index.html"
expect noindex-on-research-page fail "$TMP/case" "NOINDEX LEAKED OUTSIDE TAXONOMY"

fresh
python3 - "$TMP/case/sitemap.xml" <<'PY'
import sys, pathlib, re
p = pathlib.Path(sys.argv[1])
t = p.read_text()
t2 = re.sub(r'<url>\s*<loc>https://sinclairhuang\.org/research/ai-infrastructure/</loc>.*?</url>', '', t, count=1, flags=re.S)
assert t2 != t, 'research loc not found in sitemap fixture'
p.write_text(t2)
PY
expect research-url-dropped-from-sitemap fail "$TMP/case" "RESEARCH URL MISSING FROM SITEMAP"

# Semantic taxonomy-policy fixtures (checker-only patch on 3B): the parser
# must reject directive conflicts, refreshes outside genuine page/1 stubs,
# corrupted stubs, googlebot leaks, and encoded sitemap paths — and must
# ACCEPT case/space/attribute-order robots variants.
fresh
python3 - "$TMP/case/tags/ai/index.html" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
old = 'content="noindex,follow"'
assert old in t
p.write_text(t.replace(old, 'content="noindex, nofollow"', 1))
PY
expect taxonomy-robots-conflict fail "$TMP/case" "TAXONOMY PAGE MISSING NOINDEX"

fresh
python3 - "$TMP/case/tags/ai/index.html" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
assert '</head>' in t
p.write_text(t.replace('</head>', '<meta http-equiv="refresh" content="0; url=https://sinclairhuang.org/"></head>', 1))
PY
expect refresh-on-real-taxonomy-page fail "$TMP/case" "TAXONOMY PAGE HAS UNEXPECTED REFRESH"

fresh
python3 - "$TMP/case/tags/ai/page/1/index.html" <<'PY'
import sys, pathlib, re
p = pathlib.Path(sys.argv[1])
t = p.read_text()
t2, n = re.subn(r'(http-equiv="refresh" content="0; url=)[^"]+', r'\g<1>https://sinclairhuang.org/blog/', t, count=1)
assert n == 1, 'refresh meta not found in stub'
p.write_text(t2)
PY
expect stub-target-canonical-mismatch fail "$TMP/case" "INVALID TAXONOMY PAGINATION STUB"

fresh
printf '<meta name="googlebot" content="noindex">\n' >> "$TMP/case/blog/cowos-hbm-abf-explainer/index.html"
expect googlebot-noindex-outside-taxonomy fail "$TMP/case" "NOINDEX LEAKED OUTSIDE TAXONOMY"

fresh
python3 - "$TMP/case/sitemap.xml" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
assert '</urlset>' in t
p.write_text(t.replace('</urlset>', '  <url><loc>https://sinclairhuang.org/%74%61%67%73/ai/</loc></url>\n</urlset>'))
PY
expect encoded-taxonomy-loc-in-sitemap fail "$TMP/case" "TAXONOMY URL IN SITEMAP"

fresh
python3 - "$TMP/case/tags/ai/index.html" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
old = '<meta name="robots" content="noindex,follow">'
assert old in t
p.write_text(t.replace(old, '<meta content=" NoIndex ,  FOLLOW " name="ROBOTS">', 1))
PY
expect robots-variant-still-valid pass "$TMP/case"

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
