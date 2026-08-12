#!/usr/bin/env bash
# Offline harness for the N2 news workflow gating (no GitHub, no origin).
#
# Runs the REAL news_workflow_gate.sh inside throwaway sandbox repositories
# with their own local bare "origin", emulating the Actions job semantics:
# a failed step fails the job and skips every later step; stage/commit/push
# only run when generated=true. Covers the reviewer's eight minimum
# acceptance scenarios (work order 2026-08-12, section 10).
#
# Usage: bash test_news_workflow.sh
set -u

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
GATE="$SCRIPTS_DIR/news_workflow_gate.sh"
REPO_ROOT="$(cd "$SCRIPTS_DIR/../.." && pwd)"
WORKFLOW="$REPO_ROOT/.github/workflows/update-news.yml"
N1_PARENT_REF="${N1_PARENT_REF:-HEAD}"
ROOT=$(mktemp -d "${TMPDIR:-/tmp}/n2-harness.XXXXXX")
PASS=0
FAIL=0

say()  { printf '%s\n' "$*"; }
ok()   { PASS=$((PASS+1)); say "RESULT: PASS — $*"; }
bad()  { FAIL=$((FAIL+1)); say "RESULT: FAIL — $*"; }

check() {  # check <description> <expected> <actual>
  if [ "$2" = "$3" ]; then
    say "  check ok: $1"
  else
    say "  check FAILED: $1 (expected [$2], got [$3])"
    FAIL=$((FAIL+1))
  fi
}

json_baseline_archive() {
  cat <<'EOF'
{"schema_version": 1, "days": [{"date": "2026-08-11", "note": "baseline"}]}
EOF
}

make_repo() {  # make_repo <name>  -> echoes workdir
  local name="$1" bare work
  bare="$ROOT/$name-origin.git"
  work="$ROOT/$name"
  git init -q --bare -b main "$bare"
  git init -q -b main "$work"
  git -C "$work" config user.name "Harness"
  git -C "$work" config user.email "harness@example.com"
  mkdir -p "$work/assets"
  json_baseline_archive > "$work/assets/news_archive.json"
  echo '{"date": "2026-08-11", "note": "baseline daily"}' > "$work/assets/news_daily.json"
  git -C "$work" add -- assets/news_archive.json assets/news_daily.json
  git -C "$work" commit -q -m "baseline"
  git -C "$work" remote add origin "$bare"
  git -C "$work" push -q origin main
  echo "$work"
}

gen_add_day() {  # gen_add_day <workdir> <date> <both|archive_only>
  local work="$1" date="$2" mode="$3"
  python3 - "$work/assets/news_archive.json" "$date" <<'PY'
import json, sys
path, date = sys.argv[1], sys.argv[2]
with open(path, encoding="utf-8") as fh:
    obj = json.load(fh)
obj["days"].insert(0, {"date": date, "note": "harness day"})
with open(path, "w", encoding="utf-8") as fh:
    json.dump(obj, fh, ensure_ascii=False, indent=1)
PY
  if [ "$3" = "both" ]; then
    printf '{"date": "%s", "note": "harness daily"}\n' "$date" \
      > "$work/assets/news_daily.json"
  fi
}

# run_job <workdir> <generator_cmd...>
# Emulates the workflow job. Populates globals:
#   JOB (SUCCESS|FAILED)  GEN_RC DETECT_RC STAGE_RC COMMIT_RC PUSH_RC
#   GENERATED DIGEST_DATE STAGED HEAD_BEFORE HEAD_AFTER COMMIT_MSG
run_job() {
  local work="$1"; shift
  GEN_RC=- ; DETECT_RC=- ; STAGE_RC=SKIPPED ; COMMIT_RC=SKIPPED ; PUSH_RC=SKIPPED
  GENERATED="" ; DIGEST_DATE="" ; STAGED="" ; COMMIT_MSG="(no commit)"
  JOB=SUCCESS
  HEAD_BEFORE=$(git -C "$work" rev-parse HEAD)
  local out="$work/.github_output"; : > "$out"

  ( cd "$work" && "$@" ) ; GEN_RC=$?
  say "  step generate: rc=$GEN_RC"
  if [ "$GEN_RC" -ne 0 ]; then
    JOB=FAILED; DETECT_RC=SKIPPED
  else
    ( cd "$work" && GITHUB_OUTPUT="$out" bash "$GATE" detect ) ; DETECT_RC=$?
    say "  step detect: rc=$DETECT_RC"
    if [ "$DETECT_RC" -ne 0 ]; then
      JOB=FAILED
    else
      GENERATED=$(sed -n 's/^generated=//p' "$out" | tail -1)
      DIGEST_DATE=$(sed -n 's/^digest_date=//p' "$out" | tail -1)
      say "  outputs: generated=$GENERATED digest_date=${DIGEST_DATE:-–}"
      if [ "$GENERATED" = "true" ]; then
        ( cd "$work" && bash "$GATE" stage ) ; STAGE_RC=$?
        say "  step stage: rc=$STAGE_RC"
        if [ "$STAGE_RC" -ne 0 ]; then
          JOB=FAILED
        else
          STAGED=$(git -C "$work" diff --cached --name-only | tr '\n' ' ')
          ( cd "$work" && bash "$GATE" commit "$DIGEST_DATE" ) ; COMMIT_RC=$?
          say "  step commit: rc=$COMMIT_RC"
          if [ "$COMMIT_RC" -ne 0 ]; then
            JOB=FAILED
          else
            ( cd "$work" && bash "$GATE" push ) ; PUSH_RC=$?
            say "  step push: rc=$PUSH_RC"
            [ "$PUSH_RC" -ne 0 ] && JOB=FAILED
          fi
        fi
      fi
    fi
  fi
  HEAD_AFTER=$(git -C "$work" rev-parse HEAD)
  if [ "$HEAD_AFTER" != "$HEAD_BEFORE" ]; then
    COMMIT_MSG=$(git -C "$work" log -1 --format=%s)
  fi
  say "  head_before=$HEAD_BEFORE"
  say "  head_after =$HEAD_AFTER"
  say "  staged=[${STAGED:-}]"
  say "  commit_message=$COMMIT_MSG"
  say "  job=$JOB"
}

# ---------------------------------------------------------------- scenario 1
say ""
say "=== S1 published: archive+daily change -> one commit, frozen message ==="
W=$(make_repo s1)
run_job "$W" gen_add_day "$W" 2026-08-12 both
check "job success" SUCCESS "$JOB"
check "generated" true "$GENERATED"
check "digest_date" 2026-08-12 "$DIGEST_DATE"
check "staged exactly both allowlist files" \
  "assets/news_archive.json assets/news_daily.json " "$STAGED"
check "one commit ahead" \
  "$HEAD_BEFORE" "$(git -C "$W" rev-parse HEAD^)"
check "frozen message" "chore(news): update digest for 2026-08-12" "$COMMIT_MSG"
check "pushed to sandbox origin" \
  "$HEAD_AFTER" "$(git -C "$ROOT/s1-origin.git" rev-parse main)"
[ "$FAIL" -eq 0 ] && ok "S1" || bad "S1"

# ---------------------------------------------------------------- scenario 2
say ""
say "=== S2 empty day: archive-only change -> archive-only commit ==="
F0=$FAIL
W=$(make_repo s2)
run_job "$W" gen_add_day "$W" 2026-08-12 archive_only
check "job success" SUCCESS "$JOB"
check "generated" true "$GENERATED"
check "staged archive only" "assets/news_archive.json " "$STAGED"
check "frozen message" "chore(news): update digest for 2026-08-12" "$COMMIT_MSG"
check "commit touches archive only" "assets/news_archive.json" \
  "$(git -C "$W" diff-tree --no-commit-id --name-only -r HEAD | tr '\n' ' ' | xargs)"
[ "$FAIL" -eq "$F0" ] && ok "S2" || bad "S2"

# ---------------------------------------------------------------- scenario 3
say ""
say "=== S3 success but no diff: generated=false, nothing runs ==="
F0=$FAIL
W=$(make_repo s3)
run_job "$W" true
check "job success" SUCCESS "$JOB"
check "generated" false "$GENERATED"
check "stage skipped" SKIPPED "$STAGE_RC"
check "commit skipped" SKIPPED "$COMMIT_RC"
check "push skipped" SKIPPED "$PUSH_RC"
check "HEAD unchanged" "$HEAD_BEFORE" "$HEAD_AFTER"
[ "$FAIL" -eq "$F0" ] && ok "S3" || bad "S3"

# ---------------------------------------------------------------- scenario 4
say ""
say "=== S4 generator failure: job fails, nothing staged/committed ==="
F0=$FAIL
W=$(make_repo s4)
run_job "$W" bash -c "exit 3"
check "job failed" FAILED "$JOB"
check "generate rc" 3 "$GEN_RC"
check "detect skipped" SKIPPED "$DETECT_RC"
check "HEAD unchanged" "$HEAD_BEFORE" "$HEAD_AFTER"
check "index clean" "" "$(git -C "$W" diff --cached --name-only)"
[ "$FAIL" -eq "$F0" ] && ok "S4" || bad "S4"

# ---------------------------------------------------------------- scenario 5a
say ""
say "=== S5a pre-staged non-allowlist path: stage step refuses ==="
F0=$FAIL
W=$(make_repo s5a)
echo "foreign" > "$W/foreign.txt"
git -C "$W" add foreign.txt
run_job "$W" gen_add_day "$W" 2026-08-12 both
check "job failed" FAILED "$JOB"
check "stage rc" 1 "$STAGE_RC"
check "commit skipped" SKIPPED "$COMMIT_RC"
check "HEAD unchanged" "$HEAD_BEFORE" "$HEAD_AFTER"
[ "$FAIL" -eq "$F0" ] && ok "S5a" || bad "S5a"

# ---------------------------------------------------------------- scenario 5b
say ""
say "=== S5b unstaged foreign change: never staged, commit stays clean ==="
F0=$FAIL
W=$(make_repo s5b)
echo "foreign" > "$W/foreign.txt"
run_job "$W" gen_add_day "$W" 2026-08-12 both
check "job success" SUCCESS "$JOB"
check "commit touches only allowlist" \
  "assets/news_archive.json assets/news_daily.json" \
  "$(git -C "$W" diff-tree --no-commit-id --name-only -r HEAD | tr '\n' ' ' | xargs)"
check "foreign file still untracked" "?? foreign.txt" \
  "$(git -C "$W" status --porcelain=v1 -- foreign.txt)"
[ "$FAIL" -eq "$F0" ] && ok "S5b" || bad "S5b"

# ---------------------------------------------------------------- scenario 6
say ""
say "=== S6 non-fast-forward push: fails, no pull/rebase/merge/force ==="
F0=$FAIL
W=$(make_repo s6)
OTHER="$ROOT/s6-other"
git clone -q "$ROOT/s6-origin.git" "$OTHER"
git -C "$OTHER" config user.name "Other"
git -C "$OTHER" config user.email "other@example.com"
echo "advance" > "$OTHER/advance.txt"
git -C "$OTHER" add advance.txt
git -C "$OTHER" commit -q -m "remote advanced"
git -C "$OTHER" push -q origin main
REMOTE_ADVANCED=$(git -C "$ROOT/s6-origin.git" rev-parse main)
run_job "$W" gen_add_day "$W" 2026-08-12 both
check "job failed" FAILED "$JOB"
check "push rc non-zero" 1 "$([ "$PUSH_RC" -ne 0 ] && echo 1 || echo 0)"
check "local commit intact after push failure" \
  "chore(news): update digest for 2026-08-12" \
  "$(git -C "$W" log -1 --format=%s)"
check "remote untouched by failed push" \
  "$REMOTE_ADVANCED" "$(git -C "$ROOT/s6-origin.git" rev-parse main)"
check "no merge/rebase/pull in local reflog" "" \
  "$(git -C "$W" reflog | grep -iE 'merge|rebase|pull' || true)"
check "gate script contains no pull/rebase/merge/force" "" \
  "$(grep -nE 'git (pull|rebase|merge)|--force|push -f' "$GATE" || true)"
check "exactly one local commit formed (no repair commit)" \
  "$HEAD_BEFORE" "$(git -C "$W" rev-parse HEAD^)"
[ "$FAIL" -eq "$F0" ] && ok "S6" || bad "S6"

# ---------------------------------------------------------------- scenario 7
say ""
say "=== S7 date boundary: commit uses Taipei digest_date, not runner UTC ==="
F0=$FAIL
W=$(make_repo s7)
RUNNER_UTC=$(date -u +%Y-%m-%d)
run_job "$W" gen_add_day "$W" 2026-08-13 both
say "  runner UTC today: $RUNNER_UTC (differs from digest_date by design)"
check "digest_date from archive" 2026-08-13 "$DIGEST_DATE"
check "frozen message uses archive date" \
  "chore(news): update digest for 2026-08-13" "$COMMIT_MSG"
if [ "$RUNNER_UTC" != "2026-08-13" ]; then
  say "  check ok: message date differs from runner UTC date ($RUNNER_UTC)"
else
  say "  note: runner UTC happens to equal fixture date today; boundary still"
  say "        proven because the date came from the archive, not the clock"
fi
[ "$FAIL" -eq "$F0" ] && ok "S7" || bad "S7"

# ---------------------------------------------------------------- scenario 8
say ""
say "=== S8 concurrency block byte-identical to N1 parent workflow ==="
F0=$FAIL
git -C "$REPO_ROOT" show "$N1_PARENT_REF:.github/workflows/update-news.yml" \
  > "$ROOT/old-workflow.yml"
OLD_BLOCK=$(sed -n '/^concurrency:/,/^[^ ]/p' "$ROOT/old-workflow.yml" | sed '$d')
NEW_BLOCK=$(sed -n '/^concurrency:/,/^[^ ]/p' "$WORKFLOW" | sed '$d')
say "--- concurrency block (N1 parent) ---"; say "$OLD_BLOCK"
say "--- concurrency block (N2)        ---"; say "$NEW_BLOCK"
check "concurrency block byte-identical" "$OLD_BLOCK" "$NEW_BLOCK"
[ "$FAIL" -eq "$F0" ] && ok "S8" || bad "S8"

# ---------------------------------------------------------------- summary
say ""
say "================================================================"
say "scenario results: PASS=$PASS FAIL=$FAIL (sandbox: $ROOT)"
if [ "$FAIL" -eq 0 ]; then
  say "ALL SCENARIOS PASSED"
  exit 0
fi
say "SOME SCENARIOS FAILED"
exit 1
