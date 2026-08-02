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

expect() { # expect <name> <pass|fail> <dir> [required-error-message] [content-root]
  local name=$1 want=$2 dir=$3 msg=${4:-} croot=${5:-} got
  if scripts/check_site.sh "$dir" "$TMP/before" ${croot:+"$croot"} >"$TMP/out-$name" 2>&1; then got=pass; else got=fail; fi
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

# Dot-segment normalization: sitemap paths are urlparse -> unquote-once ->
# posixpath.normpath, so classification follows the real destination.
fresh
python3 - "$TMP/case/sitemap.xml" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
assert '</urlset>' in t
p.write_text(t.replace('</urlset>', '  <url><loc>https://sinclairhuang.org/blog/../tags/ai/</loc></url>\n</urlset>'))
PY
expect dotdot-taxonomy-loc-in-sitemap fail "$TMP/case" "TAXONOMY URL IN SITEMAP"

fresh
python3 - "$TMP/case/sitemap.xml" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
assert '</urlset>' in t
p.write_text(t.replace('</urlset>', '  <url><loc>https://sinclairhuang.org/blog/%2e%2e/tags/ai/</loc></url>\n</urlset>'))
PY
expect encoded-dotdot-taxonomy-loc fail "$TMP/case" "TAXONOMY URL IN SITEMAP"

# Positive-case mutations are guarded: if the seeding python fails, the
# suite FAILS — a pristine tree must never masquerade as a mutated positive.
fresh
if python3 - "$TMP/case/tags/ai/index.html" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
old = '<meta name="robots" content="noindex,follow">'
assert old in t
p.write_text(t.replace(old, '<meta content=" NoIndex ,  FOLLOW " name="ROBOTS">', 1))
PY
then
  expect robots-variant-still-valid pass "$TMP/case"
else
  echo "FAIL robots-variant-still-valid — fixture mutation failed; not testing a pristine tree"
  RESULT=1
fi

fresh
if python3 - "$TMP/case/sitemap.xml" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
assert '</urlset>' in t
p.write_text(t.replace('</urlset>', '  <url><loc>https://sinclairhuang.org/tags/../blog/</loc></url>\n</urlset>'))
PY
then
  expect dotdot-escape-normalizes-out-of-taxonomy pass "$TMP/case"
else
  echo "FAIL dotdot-escape-normalizes-out-of-taxonomy — fixture mutation failed; not testing a pristine tree"
  RESULT=1
fi

# CTA-routing fixtures (Step 4). The through-check_site.sh cases double as
# proof the routing checker is WIRED INTO the harness — if the 6b hookup
# were removed, each of them would go green for the wrong reason and fail
# its message assertion. Source-side faults use throwaway content/docs
# trees and call the checker directly.
ADV_PAGE="blog/cowos-hbm-abf-explainer/index.html"        # cta: advisory
SUB_PAGE="blog/trust-before-efficiency/index.html"        # cta: subscribe

fresh
python3 - "$TMP/case/$ADV_PAGE" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
assert 'data-cta-type="advisory"' in t
t = t.replace('data-cta-type="advisory"', 'data-cta-type="subscribe"', 1)
t = t.replace('href="/advisory/#projects"', 'href="https://sinclairhuang.substack.com/"', 1)
p.write_text(t)
PY
expect cta-advisory-rendered-as-subscribe fail "$TMP/case" "CTA TYPE MISMATCH"

fresh
python3 - "$TMP/case/$SUB_PAGE" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
assert 'data-cta-type="subscribe"' in t
t = t.replace('data-cta-type="subscribe"', 'data-cta-type="advisory"', 1)
t = t.replace('href="https://sinclairhuang.substack.com/"', 'href="/advisory/#projects"', 1)
p.write_text(t)
PY
expect cta-subscribe-rendered-as-advisory fail "$TMP/case" "CTA TYPE MISMATCH"

fresh
python3 - "$TMP/case/$ADV_PAGE" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
start = t.index('<aside class="advisory-cta"')
end = t.index('</aside>', start) + len('</aside>')
p.write_text(t[:start] + t[end:])
PY
expect cta-missing-on-page fail "$TMP/case" "CTA MISSING ON PAGE"

fresh
python3 - "$TMP/case/$ADV_PAGE" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
start = t.index('<aside class="advisory-cta"')
end = t.index('</aside>', start) + len('</aside>')
p.write_text(t[:end] + t[start:end] + t[end:])
PY
expect cta-duplicate-on-page fail "$TMP/case" "DUPLICATE CTA ON PAGE"

fresh
python3 - "$TMP/case/$ADV_PAGE" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
assert 'href="/advisory/#projects"' in t
p.write_text(t.replace('href="/advisory/#projects"', 'href="/advisory/"', 1))
PY
expect cta-advisory-target-missing-anchor fail "$TMP/case" "CTA TARGET WRONG"

fresh
python3 - "$TMP/case/$SUB_PAGE" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
assert 'href="https://sinclairhuang.substack.com/"' in t
p.write_text(t.replace('href="https://sinclairhuang.substack.com/"', 'href="https://substack.com/@sinclairhuang"', 1))
PY
expect cta-subscribe-target-wrong fail "$TMP/case" "CTA TARGET WRONG"

# Source-side faults: throwaway content/docs trees, checker called directly.
cta_direct() { # cta_direct <name> <pass|fail> <docs> <content> [msg]
  local name=$1 want=$2 docs=$3 content=$4 msg=${5:-} got
  if python3 scripts/check_cta_routing.py "$docs" "$content" >"$TMP/out-$name" 2>&1; then got=pass; else got=fail; fi
  if [ "$got" != "$want" ]; then
    echo "FAIL $name — checker ${got}ed, expected $want"; sed 's/^/     /' "$TMP/out-$name" | tail -4; RESULT=1
  elif [ -n "$msg" ] && ! grep -qF "$msg" "$TMP/out-$name"; then
    echo "FAIL $name — failed, but without the expected message: $msg"; RESULT=1
  else
    echo "ok   $name (checker ${got}ed as expected${msg:+, with the expected message})"
  fi
}

mkdir -p "$TMP/src-miss/blog" "$TMP/docs-empty/blog"
printf -- '---\ntitle: "X"\ndate: 2026-01-01\n---\nbody\n' > "$TMP/src-miss/blog/x.md"
cta_direct source-cta-missing fail "$TMP/docs-empty" "$TMP/src-miss" "SOURCE CTA MISSING"

mkdir -p "$TMP/src-unknown/blog"
printf -- '---\ntitle: "X"\ncta: "banana"\n---\nbody\n' > "$TMP/src-unknown/blog/x.md"
cta_direct source-cta-unknown fail "$TMP/docs-empty" "$TMP/src-unknown" "SOURCE CTA UNKNOWN"

mkdir -p "$TMP/src-none/blog" "$TMP/docs-none/blog/x"
printf -- '---\ntitle: "X"\ncta: "none"\n---\nbody\n' > "$TMP/src-none/blog/x.md"
printf '<html><body><aside class="advisory-cta" data-cta-type="advisory"><a href="/advisory/#projects">go</a></aside></body></html>\n' > "$TMP/docs-none/blog/x/index.html"
cta_direct none-page-still-has-cta fail "$TMP/docs-none" "$TMP/src-none" "CTA ON NONE PAGE"

# Positive: attribute order must not matter to any CTA gate.
fresh
if python3 - "$TMP/case/$ADV_PAGE" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
old = '<aside class="advisory-cta" data-cta-type="advisory" style='
assert old in t
p.write_text(t.replace(old, '<aside data-cta-type="advisory" class="advisory-cta" style=', 1))
PY
then
  expect cta-attribute-order-variant pass "$TMP/case"
else
  echo "FAIL cta-attribute-order-variant — fixture mutation failed; not testing a pristine tree"
  RESULT=1
fi

# Positive: a harmless extra class token must not break counting or routing.
fresh
if python3 - "$TMP/case/$ADV_PAGE" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
old = 'class="advisory-cta"'
assert old in t
p.write_text(t.replace(old, 'class="advisory-cta cta-highlight"', 1))
PY
then
  expect cta-extra-class-token pass "$TMP/case"
else
  echo "FAIL cta-extra-class-token — fixture mutation failed; not testing a pristine tree"
  RESULT=1
fi

# Positive: a published (non-draft) cta:none article renders zero CTA and the
# FULL harness passes — the none contract is honored end to end. Uses the
# CONTENT_ROOT override (third check_site.sh argument, fixtures only).
cp -R content "$TMP/content-none"
printf -- '---\ntitle: "None Fixture"\ndate: 2026-08-02\ndraft: false\ncta: "none"\n---\nA fixture article that publishes without any CTA.\n' \
  > "$TMP/content-none/blog/cta-none-fixture.md"
fresh
mkdir -p "$TMP/case/blog/cta-none-fixture"
printf '<!DOCTYPE html><html><head><title>None Fixture</title></head><body><article><p>A fixture article that publishes without any CTA.</p></article></body></html>\n' \
  > "$TMP/case/blog/cta-none-fixture/index.html"
expect published-none-article pass "$TMP/case" "" "$TMP/content-none"

# A refresh alone must not exempt a page: only a genuine zero-second alias
# whose target equals its canonical AND resolves to a known article may be
# skipped. Anything else stays in scope.
fresh
mkdir -p "$TMP/case/blog/fake-refresh-page"
printf '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=https://sinclairhuang.org/writing/"></head><body></body></html>\n' \
  > "$TMP/case/blog/fake-refresh-page/index.html"
expect fake-refresh-not-an-alias fail "$TMP/case" "UNEXPECTED ARTICLE PAGE"

# The dispatcher's errorf contract is proven against REAL Hugo builds on
# throwaway mini sites that use the actual partial.
hugo_dispatcher_case() { # <name> <extra-front-matter> <required-message>
  local name=$1 extra=$2 msg=$3
  local site="$TMP/hugo-$name"
  mkdir -p "$site/content/blog" "$site/layouts/_default" "$site/layouts/partials"
  printf 'baseURL = "https://example.org/"\ndisableKinds = ["taxonomy", "term", "RSS", "sitemap"]\n' > "$site/hugo.toml"
  cp layouts/partials/advisory_cta.html "$site/layouts/partials/"
  printf '{{ partial "advisory_cta.html" . }}\n' > "$site/layouts/_default/single.html"
  printf 'list\n' > "$site/layouts/_default/list.html"
  printf 'home\n' > "$site/layouts/index.html"
  printf -- '---\ntitle: "X"\ndate: 2026-01-01\n%s---\nbody\n' "$extra" > "$site/content/blog/x.md"
  if hugo --source "$site" --destination "$site/public" > "$TMP/out-$name" 2>&1; then
    echo "FAIL $name — hugo build passed, expected the dispatcher errorf to fail it"
    RESULT=1
  elif ! grep -qF "$msg" "$TMP/out-$name"; then
    echo "FAIL $name — hugo build failed, but without the expected message: $msg"
    sed 's/^/     /' "$TMP/out-$name" | tail -4
    RESULT=1
  else
    echo "ok   $name (hugo build failed as expected, with the expected message)"
  fi
}
hugo_dispatcher_case hugo-missing-cta "" "is missing the cta front matter"
hugo_dispatcher_case hugo-unknown-cta 'cta: "banana"
' "has unknown cta value"

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
