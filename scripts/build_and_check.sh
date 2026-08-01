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
# hundreds of generated files and still "passes" — so the version is pinned.
# Exact match on the version token (grep -F would also accept v0.152.20).
REQUIRED_HUGO="v0.152.2"
HV=$(hugo version | awk '{print $2}' | cut -d+ -f1)
[ "$HV" = "$REQUIRED_HUGO" ] \
  || { echo "FAIL: Hugo $REQUIRED_HUGO required, found: $HV"; exit 1; }

# Source-side junk gate (the June sync-duplication incident reached .git/refs);
# one-or-more digits — " 10" and " (12)" count too
JUNK=$(find content static layouts assets .github 2>/dev/null \
       | grep -E ' \(?[0-9]+\)?(\.(md|html|xml))?$|\.bak$|\.backup$|\.before-remove$|~$')
[ -z "$JUNK" ] || { echo "FAIL: backup/duplicate junk in source:"; echo "$JUNK"; exit 1; }
REFJUNK=$(find .git/refs -name '* *' 2>/dev/null)
[ -z "$REFJUNK" ] || { echo "FAIL: junk git refs:"; echo "$REFJUNK"; exit 1; }
[ ! -d public ] || { echo "FAIL: stray public/ directory exists (publishDir is docs/)"; exit 1; }

BEFORE=$(mktemp)
(cd docs 2>/dev/null && find . -name index.html | sed 's|^\.||;s|index\.html$||' | sort) > "$BEFORE" || true

hugo --cleanDestinationDir --panicOnWarning --printPathWarnings \
     --destination docs --baseURL "https://sinclairhuang.org/" || exit 1

scripts/check_site.sh docs "$BEFORE"
