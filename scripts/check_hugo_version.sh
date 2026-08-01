#!/usr/bin/env bash
# Gate on Hugo's BASE semver, ignoring build metadata and commit-hash suffixes.
# Official release binaries report e.g. "v0.152.2-6abd821c…+extended", brew
# reports "v0.152.2+extended+withdeploy" — both must pass; "v0.152.20-…" must
# not. Pass a version token as $1 to test the parsing; with no argument the
# installed hugo is checked.
set -uo pipefail
REQUIRED="v0.152.2"
TOKEN="${1:-$(hugo version | awk '{print $2}')}"
BASE="${TOKEN%%[-+]*}"
if [ "$BASE" = "$REQUIRED" ]; then
  exit 0
fi
echo "FAIL: Hugo $REQUIRED required, found: $TOKEN (base semver: $BASE)"
exit 1
