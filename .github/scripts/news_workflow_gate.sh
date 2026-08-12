#!/usr/bin/env bash
# Gating logic for the Daily Research News workflow (revamp case N2).
#
# Single source of truth: the workflow executes THIS script, and the
# offline harness (test_news_workflow.sh) executes THIS same script inside
# isolated sandbox repositories -- what is tested is what runs.
#
# Frozen semantics (reviewer work order, 2026-08-12):
#   detect  -> generated=true|false from the ACTUAL git diff of the two
#              approved paths (never from the generator's exit code alone);
#              digest_date read from the generator's frozen product (the
#              newest archive record), never from the runner clock.
#   stage   -> refuses a non-clean index; stages exactly the allowlist,
#              file by file (no globs, no directories); verifies the staged
#              set is a non-empty subset of the allowlist.
#   commit  -> frozen message format `chore(news): update digest for
#              YYYY-MM-DD` with the Taipei digest_date passed in.
#   push    -> one plain fast-forward push. No pull, no rebase, no merge,
#              no force; a non-fast-forward failure fails the run.
set -euo pipefail

ALLOW_1="assets/news_archive.json"
ALLOW_2="assets/news_daily.json"
ARCHIVE="$ALLOW_1"
FROZEN_MSG_PREFIX="chore(news): update digest for "

emit_output() {
  # Step output for GitHub Actions; echoed for logs and the offline harness.
  if [ -n "${GITHUB_OUTPUT:-}" ]; then
    echo "$1=$2" >> "$GITHUB_OUTPUT"
  fi
  echo "output: $1=$2"
}

cmd_detect() {
  local changes digest_date
  changes=$(git status --porcelain=v1 -- "$ALLOW_1" "$ALLOW_2")
  if [ -z "$changes" ]; then
    emit_output generated false
    echo "no approved-path changes; nothing to commit"
    return 0
  fi
  echo "approved-path changes:"
  echo "$changes"
  digest_date=$(python3 - "$ARCHIVE" <<'PY'
import json
import re
import sys

with open(sys.argv[1], encoding="utf-8") as fh:
    days = json.load(fh)["days"]
if not days:
    raise SystemExit("ERROR: archive has no day records")
date = days[0]["date"]
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
    raise SystemExit(f"ERROR: bad digest_date {date!r} in archive")
print(date)
PY
  )
  emit_output generated true
  emit_output digest_date "$digest_date"
}

cmd_stage() {
  local pre staged bad
  pre=$(git diff --cached --name-only)
  if [ -n "$pre" ]; then
    echo "ERROR: index already contains staged paths; refusing to stage:" >&2
    echo "$pre" >&2
    exit 1
  fi
  git add -- "$ALLOW_1" "$ALLOW_2"
  staged=$(git diff --cached --name-only)
  if [ -z "$staged" ]; then
    echo "ERROR: nothing staged despite generated=true" >&2
    exit 1
  fi
  bad=$(echo "$staged" | grep -vxF -e "$ALLOW_1" -e "$ALLOW_2" || true)
  if [ -n "$bad" ]; then
    echo "ERROR: non-allowlist path staged; refusing to commit:" >&2
    echo "$bad" >&2
    git reset -q -- .
    exit 1
  fi
  echo "staged paths:"
  echo "$staged"
}

cmd_commit() {
  local digest_date="$1"
  if ! echo "$digest_date" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'; then
    echo "ERROR: invalid digest_date '${digest_date}'" >&2
    exit 1
  fi
  git -c user.name="GitHub Actions" -c user.email="actions@github.com" \
    commit -m "${FROZEN_MSG_PREFIX}${digest_date}"
}

cmd_push() {
  git push origin HEAD:main
}

case "${1:-}" in
  detect) cmd_detect ;;
  stage)  cmd_stage ;;
  commit) shift; cmd_commit "${1:?digest_date required}" ;;
  push)   cmd_push ;;
  *) echo "usage: $0 {detect|stage|commit|push}" >&2; exit 64 ;;
esac
