#!/usr/bin/env bash
# Standard production build + acceptance checks for sinclairhuang.org.
# Usage: scripts/build_and_check.sh   (from anywhere; cds to repo root)
# Used locally AND by all CI workflows — there is no other sanctioned build.
set -uo pipefail
cd "$(dirname "$0")/.."

# Toolchain gate: docs/ is committed build output; a different Hugo rewrites
# hundreds of generated files and still "passes" — so the version is pinned.
REQUIRED_HUGO="v0.152.2"
hugo version | grep -qF "$REQUIRED_HUGO" \
  || { echo "FAIL: Hugo $REQUIRED_HUGO required, found: $(hugo version)"; exit 1; }

# Source-side junk gate (the June Finder-duplication incident reached .git/refs)
JUNK=$(find content static layouts assets .github \( -name '*.bak' -o -name '*.backup' \
       -o -name '*.before-remove' -o -name '*~' -o -name '* ([0-9])*' -o -name '* [0-9]' \
       -o -name '* [0-9].md' -o -name '* [0-9].html' \) 2>/dev/null)
[ -z "$JUNK" ] || { echo "FAIL: backup/duplicate junk in source:"; echo "$JUNK"; exit 1; }
REFJUNK=$(find .git/refs -name '* *' 2>/dev/null)
[ -z "$REFJUNK" ] || { echo "FAIL: junk git refs:"; echo "$REFJUNK"; exit 1; }
[ ! -d public ] || { echo "FAIL: stray public/ directory exists (publishDir is docs/)"; exit 1; }

BEFORE=$(mktemp)
(cd docs 2>/dev/null && find . -name index.html | sed 's|^\.||;s|index\.html$||' | sort) > "$BEFORE" || true

hugo --cleanDestinationDir --panicOnWarning --printPathWarnings \
     --destination docs --baseURL "https://sinclairhuang.org/" || exit 1

scripts/check_site.sh docs "$BEFORE"
