#!/usr/bin/env bash
# Standard production build + acceptance checks for sinclairhuang.org.
# Usage: scripts/build_and_check.sh   (from anywhere; cds to repo root)
# Used locally AND by all CI workflows — there is no other sanctioned build.
set -uo pipefail
cd "$(dirname "$0")/.."

# Deterministic timestamps: without a pinned TZ, CI flips six generated files
# between CST and +0800 renderings on every run.
export TZ=Asia/Taipei

# Toolchain gate: docs/ is committed build output; a different Hugo rewrites
# hundreds of generated files and still "passes" — so the BASE semver is
# pinned (official releases report v0.152.2-<hash>+extended, brew reports
# v0.152.2+extended+withdeploy; both pass, v0.152.20-* does not).
scripts/check_hugo_version.sh || exit 1

# Source-side junk gate over the WHOLE repo except .git/ and docs/ (data/ was
# a prior incident zone and must be covered); any extension counts.
. scripts/junk_pattern.sh
JUNK=$(find . -path ./.git -prune -o -path ./docs -prune -o -print 2>/dev/null \
       | grep -E "$JUNK_RE")
[ -z "$JUNK" ] || { echo "FAIL: backup/duplicate junk in source:"; echo "$JUNK"; exit 1; }
REFJUNK=$(find .git/refs -name '* *' 2>/dev/null)
[ -z "$REFJUNK" ] || { echo "FAIL: junk git refs:"; echo "$REFJUNK"; exit 1; }
[ ! -d public ] || { echo "FAIL: stray public/ directory exists (publishDir is docs/)"; exit 1; }

BEFORE=$(mktemp)
(cd docs 2>/dev/null && find . -name index.html | sed 's|^\.||;s|index\.html$||' | sort) > "$BEFORE" || true

hugo --cleanDestinationDir --panicOnWarning --printPathWarnings \
     --destination docs --baseURL "https://sinclairhuang.org/" || exit 1

scripts/check_site.sh docs "$BEFORE"
