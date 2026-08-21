#!/usr/bin/env bash
# Offline page harness for N3: renders the BUILT /news/ page in headless
# Chrome against local fixture archives served from 127.0.0.1 only.
# No origin contact; the real docs/ tree is copied into a sandbox and only
# the copy's data-archive-url is pointed at the local fixture (test-only URL
# injection -- the HTML is otherwise byte-identical to the built page and
# stays byte-identical across every scenario, proving JSON-only updates).
# T12 (icons UI case, 2026-08-21) additionally proves: frozen 18px/flex CSS,
# five build-time icon slots, aria-hidden rendering per known category,
# unknown/hostile names degrade to plain text with no icon and no HTML
# interpretation, and zero /icons/ network requests (inline clone only).
#
# Usage: bash test_news_page.sh
set -u

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPTS_DIR/../.." && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
PORT="${PORT:-8931}"
SHOTS_DIR="${SHOTS_DIR:-}"
ROOT=$(mktemp -d "${TMPDIR:-/tmp}/n3-harness.XXXXXX")
SITE="$ROOT/site"
PAGE="http://127.0.0.1:$PORT/news/"
ARCHIVE="$SITE/news/archive.json"
PASS=0; FAIL=0

say() { printf '%s\n' "$*"; }
okc() { say "  check ok: $1"; }
badc() { say "  check FAILED: $1"; FAIL=$((FAIL+1)); }
verdict() { if [ "$FAIL" -eq "$1" ]; then PASS=$((PASS+1)); say "RESULT: PASS — $2"; else say "RESULT: FAIL — $2"; fi; }

contains() {  # contains <haystack-file> <needle> <desc>
  if grep -qF -- "$2" "$1"; then okc "$3"; else badc "$3 (missing: $2)"; fi
}
not_contains() {
  if grep -qF -- "$2" "$1"; then badc "$3 (present but forbidden: $2)"; else okc "$3"; fi
}
count_is() {  # count_is <file> <needle> <n> <desc>
  local n
  n=$(grep -oF -- "$2" "$1" | wc -l | tr -d ' ')
  if [ "$n" = "$3" ]; then okc "$4 (count=$n)"; else badc "$4 (expected $3, got $n)"; fi
}

# ---------------------------------------------------------------- setup
[ -x "$CHROME" ] || { say "FATAL: Chrome not found at $CHROME"; exit 1; }
cp -R "$REPO_ROOT/docs" "$SITE"
# Test-only URL injection: point the page at the local fixture.
sed -i '' 's|data-archive-url="[^"]*"|data-archive-url="./archive.json"|' \
  "$SITE/news/index.html"
PAGE_SHA=$(shasum -a 256 "$SITE/news/index.html" | cut -d' ' -f1)
say "sandbox page sha256: $PAGE_SHA (constant across all scenarios)"

python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$SITE" >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null' EXIT
sleep 1

dump() {  # dump <outfile> — rendered DOM with <script> bodies stripped, so
          # assertions match RENDERED content, not the page's own JS source
          # (whose string literals legitimately contain the state texts).
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --virtual-time-budget=5000 --dump-dom "$PAGE" 2>/dev/null \
  | python3 -c 'import re,sys; sys.stdout.write(re.sub(r"<script\b[\s\S]*?</script>", "", sys.stdin.read()))' \
  > "$1"
}

shot() {  # shot <outfile> <WxH>
  [ -n "$SHOTS_DIR" ] || return 0
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --virtual-time-budget=6000 --window-size="$2" \
    --screenshot="$SHOTS_DIR/$1" "$PAGE" >/dev/null 2>&1
}

fixture() {  # fixture <python-days-expr>  (writes archive.json)
  python3 - "$ARCHIVE" "$1" <<'PY'
import json, sys

def pub(date, gen, items):
    return {"date": date, "generated_utc": gen, "status": "published",
            "model": "claude-opus-5", "candidates": 30, "feeds": None,
            "categories": [{"key": "ai_infra", "name": "AI 基礎設施",
                            "items": items}], "warnings": []}

def empty(date, gen):
    return {"date": date, "generated_utc": gen, "status": "empty",
            "model": "claude-opus-5", "candidates": 30, "feeds": None,
            "categories": [], "warnings": []}

def item(tag, **kw):
    base = {"title_zh": "標題-" + tag, "summary_zh": "摘要-" + tag,
            "relevance": "對應-" + tag, "title": "Title " + tag,
            "source": "The Verge",
            "url": "https://www.theverge.com/" + tag, "published": None}
    base.update(kw)
    return base

days = eval(sys.argv[2])  # trusted harness-internal expression
with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump({"schema_version": 1, "days": days}, fh, ensure_ascii=False)
PY
}

day_order() {  # day_order <domfile> -> space-joined date headers in order
  grep -oE 'nw-day-head">[0-9]{4}-[0-9]{2}-[0-9]{2}' "$1" \
    | sed 's/.*>//' | tr '\n' ' '
}

EMPTY_TEXT="未選出符合發布條件的新聞"
ERROR_TEXT="暫時無法載入最新內容"

# ---------------------------------------------------------------- T1 mixed
say ""; say "=== T1 seven-day mixed (published + empty), newest-first ==="
F0=$FAIL
fixture "[pub('2026-08-12','2026-08-11T22:27:39Z',[item('a')]),
          pub('2026-08-11','2026-08-10T22:22:48Z',[item('b')]),
          empty('2026-08-10','2026-08-09T22:15:26Z'),
          pub('2026-08-09','2026-08-08T22:13:19Z',[item('c')]),
          pub('2026-08-08','2026-08-07T22:22:02Z',[item('d')]),
          empty('2026-08-07','2026-08-07T01:27:11Z'),
          pub('2026-08-06','2026-08-05T22:46:03Z',[item('e')])]"
dump "$ROOT/t1.html"
ORDER=$(day_order "$ROOT/t1.html")
[ "$ORDER" = "2026-08-12 2026-08-11 2026-08-10 2026-08-09 2026-08-08 2026-08-07 2026-08-06 " ] \
  && okc "seven dates newest-first ($ORDER)" || badc "order wrong: [$ORDER]"
count_is "$ROOT/t1.html" "$EMPTY_TEXT" 2 "exactly two empty-day notices"
contains "$ROOT/t1.html" "標題-a" "published title rendered"
not_contains "$ROOT/t1.html" "$ERROR_TEXT" "no error state on valid archive"
shot "shot-desktop-mixed.png" "1440,1600"
shot "shot-mobile-mixed.png" "390,844"
verdict "$F0" "T1"

# ---------------------------------------------------------------- T2 all published
say ""; say "=== T2 all seven published ==="
F0=$FAIL
fixture "[pub('2026-08-%02d'%d,'2026-08-%02dT22:00:00Z'%(d-1),[item('t%d'%d)]) for d in range(12,5,-1)]"
dump "$ROOT/t2.html"
count_is "$ROOT/t2.html" 'class="nw-day-head"' 7 "seven day sections"
count_is "$ROOT/t2.html" "$EMPTY_TEXT" 0 "no empty notices"
contains "$ROOT/t2.html" 'href="https://www.theverge.com/t12"' "item link rendered as https href"
contains "$ROOT/t2.html" 'rel="noopener noreferrer"' "noopener noreferrer on links"
contains "$ROOT/t2.html" "摘要-t12" "summary rendered"
contains "$ROOT/t2.html" "The Verge" "source label rendered as text"
not_contains "$ROOT/t2.html" "s2/favicons" "no Google favicon fetch"
verdict "$F0" "T2"

# ---------------------------------------------------------------- T3 all empty
say ""; say "=== T3 all seven empty ==="
F0=$FAIL
fixture "[empty('2026-08-%02d'%d,'2026-08-%02dT22:00:00Z'%(d-1)) for d in range(12,5,-1)]"
dump "$ROOT/t3.html"
count_is "$ROOT/t3.html" 'class="nw-day-head"' 7 "seven day sections survive"
count_is "$ROOT/t3.html" "$EMPTY_TEXT" 7 "seven empty notices"
not_contains "$ROOT/t3.html" "$ERROR_TEXT" "all-empty is not an error"
shot "shot-desktop-empty.png" "1440,1200"
verdict "$F0" "T3"

# ---------------------------------------------------------------- T4 fewer than seven
say ""; say "=== T4 three-day archive: no invented dates ==="
F0=$FAIL
fixture "[pub('2026-08-12','2026-08-11T22:27:39Z',[item('x')]),
          empty('2026-08-10','2026-08-09T22:15:26Z'),
          pub('2026-08-06','2026-08-05T22:46:03Z',[item('y')])]"
dump "$ROOT/t4.html"
ORDER=$(day_order "$ROOT/t4.html")
[ "$ORDER" = "2026-08-12 2026-08-10 2026-08-06 " ] \
  && okc "three real dates only, gaps stay gaps ($ORDER)" || badc "order wrong: [$ORDER]"
not_contains "$ROOT/t4.html" 'nw-day-head">2026-08-11' "gap date 08-11 not fabricated"
verdict "$F0" "T4"

# ---------------------------------------------------------------- T5 over-seven + order semantics
say ""; say "=== T5 nine-day fixture: newest seven only; archive order preserved ==="
F0=$FAIL
fixture "[pub('2026-08-%02d'%d,'2026-08-%02dT22:00:00Z'%(d-1),[item('o%d'%d)]) for d in (10,14,8,12,6,13,9,7,11)]"
dump "$ROOT/t5.html"
ORDER=$(day_order "$ROOT/t5.html")
[ "$ORDER" = "2026-08-14 2026-08-13 2026-08-12 2026-08-11 2026-08-10 2026-08-09 2026-08-08 " ] \
  && okc "newest seven, sorted like the archive semantics ($ORDER)" || badc "order wrong: [$ORDER]"
not_contains "$ROOT/t5.html" 'nw-day-head">2026-08-07' "08-07 excluded"
not_contains "$ROOT/t5.html" 'nw-day-head">2026-08-06' "08-06 excluded"
verdict "$F0" "T5"

# ---------------------------------------------------------------- T6 date boundary
say ""; say "=== T6 boundary: digest_date differs from UTC date of generated_utc ==="
F0=$FAIL
fixture "[pub('2026-08-13','2026-08-12T22:27:39Z',[item('z')])]"
dump "$ROOT/t6.html"
contains "$ROOT/t6.html" 'nw-day-head">2026-08-13' "displays archive digest_date 2026-08-13"
not_contains "$ROOT/t6.html" 'nw-day-head">2026-08-12' "does not re-derive 08-12 from UTC"
contains "$ROOT/t6.html" "06:27（UTC+8）更新" "update time from string arithmetic (22:27Z -> 06:27+08)"
grep -q "new Date(" "$REPO_ROOT/layouts/news/list.html" \
  && badc "template JS must not use new Date()" || okc "template JS never consults the clock"
verdict "$F0" "T6"

# ---------------------------------------------------------------- T7 fetch failure
say ""; say "=== T7 fetch failure (404): error state, not an empty day ==="
F0=$FAIL
rm -f "$ARCHIVE"
dump "$ROOT/t7.html"
contains "$ROOT/t7.html" "$ERROR_TEXT" "error message shown"
contains "$ROOT/t7.html" "http-404" "error kind identifies the path"
contains "$ROOT/t7.html" "這不代表今日沒有新聞" "explicitly not claiming an empty day"
not_contains "$ROOT/t7.html" "$EMPTY_TEXT" "no fake empty-day notice"
not_contains "$ROOT/t7.html" 'class="nw-card"' "no stale items rendered"
shot "shot-desktop-error.png" "1440,900"
verdict "$F0" "T7"

# ---------------------------------------------------------------- T8 malformed / schema
say ""; say "=== T8 malformed JSON and unknown schema fail safely ==="
F0=$FAIL
printf '{broken json' > "$ARCHIVE"
dump "$ROOT/t8a.html"
contains "$ROOT/t8a.html" "$ERROR_TEXT" "malformed: error state"
contains "$ROOT/t8a.html" "parse" "malformed: kind=parse"
not_contains "$ROOT/t8a.html" 'class="nw-card"' "malformed: no partial DOM"
printf '{"schema_version": 99, "days": []}' > "$ARCHIVE"
dump "$ROOT/t8b.html"
contains "$ROOT/t8b.html" "$ERROR_TEXT" "unknown schema: error state"
contains "$ROOT/t8b.html" "schema" "unknown schema: kind=schema"
verdict "$F0" "T8"

# ---------------------------------------------------------------- T9 XSS / URL safety
say ""; say "=== T9 hostile content: text-only rendering, no executable links ==="
F0=$FAIL
fixture "[pub('2026-08-12','2026-08-11T22:27:39Z',[
  item('evil', title_zh='<img src=x onerror=alert(1)>', title='<script>alert(2)</script>',
       summary_zh='<b>bold</b> not html', url='javascript:alert(3)'),
  item('data', url='data:text/html,hi'),
  item('good')])]"
dump "$ROOT/t9.html"
contains "$ROOT/t9.html" "&lt;img src=x onerror=alert(1)&gt;" "img payload escaped to text"
contains "$ROOT/t9.html" "&lt;script&gt;alert(2)&lt;/script&gt;" "script payload escaped to text"
contains "$ROOT/t9.html" "&lt;b&gt;bold&lt;/b&gt;" "html in summary escaped"
not_contains "$ROOT/t9.html" '<img src=x' "no live img element from payload"
not_contains "$ROOT/t9.html" 'href="javascript:' "javascript: never becomes a link"
not_contains "$ROOT/t9.html" 'href="data:' "data: never becomes a link"
contains "$ROOT/t9.html" 'href="https://www.theverge.com/good"' "legit https link still works"
verdict "$F0" "T9"

# ---------------------------------------------------------------- T11 record-level schema
say ""; say "=== T11 record-level schema counterexamples: whole archive fails safely ==="
F0=$FAIL

bad_case() {  # bad_case <name> <python-days-expr>
  fixture "$2"
  dump "$ROOT/t11-$1.html"
  contains "$ROOT/t11-$1.html" "$ERROR_TEXT" "$1: error state shown"
  contains "$ROOT/t11-$1.html" "schema" "$1: kind=schema"
  not_contains "$ROOT/t11-$1.html" 'class="nw-day-head"' "$1: no day section"
  not_contains "$ROOT/t11-$1.html" 'class="nw-card"' "$1: no card"
  not_contains "$ROOT/t11-$1.html" "$EMPTY_TEXT" "$1: no fake empty-day notice"
}

bad_case "unknown-status" \
  "[dict(pub('2026-08-12','2026-08-11T22:27:39Z',[item('u')]), status='draft')]"
bad_case "published-no-items" \
  "[pub('2026-08-12','2026-08-11T22:27:39Z',[])]"
bad_case "empty-with-items" \
  "[dict(pub('2026-08-12','2026-08-11T22:27:39Z',[item('e')]), status='empty')]"
bad_case "invalid-date" \
  "[pub('not-a-date','2026-08-11T22:27:39Z',[item('d')])]"
bad_case "invalid-generated-utc" \
  "[pub('2026-08-12','yesterday',[item('g')])]"
bad_case "categories-not-array" \
  "[dict(empty('2026-08-12','2026-08-11T22:27:39Z'), categories=None)]"
bad_case "item-missing-title-zh" \
  "[pub('2026-08-12','2026-08-11T22:27:39Z',[{k:v for k,v in item('m').items() if k!='title_zh'}])]"
bad_case "day-not-object" "['garbage-string-day']"

say "  -- retention: valid render followed by invalid archive keeps NOTHING --"
fixture "[pub('2026-08-12','2026-08-11T22:27:39Z',[item('KEEP-ME')])]"
dump "$ROOT/t11-pre.html"
contains "$ROOT/t11-pre.html" "標題-KEEP-ME" "retention: valid fixture rendered first"
fixture "[dict(pub('2026-08-12','2026-08-11T22:27:39Z',[item('KEEP-ME')]), status='empty')]"
dump "$ROOT/t11-post.html"
contains "$ROOT/t11-post.html" "$ERROR_TEXT" "retention: reload shows error state"
not_contains "$ROOT/t11-post.html" "標題-KEEP-ME" "retention: no prior data survives"
not_contains "$ROOT/t11-post.html" 'class="nw-card"' "retention: no cards"
not_contains "$ROOT/t11-post.html" "$EMPTY_TEXT" "retention: no fake empty notice"
verdict "$F0" "T11"

# ---------------------------------------------------------------- T10 live sync
say ""; say "=== T10 JSON-only update refreshes the page; HTML byte-identical ==="
F0=$FAIL
fixture "[pub('2026-08-12','2026-08-11T22:27:39Z',[item('SYNC-A')])]"
dump "$ROOT/t10a.html"
contains "$ROOT/t10a.html" "標題-SYNC-A" "fixture A content shown"
SHA_A=$(shasum -a 256 "$SITE/news/index.html" | cut -d' ' -f1)
fixture "[pub('2026-08-13','2026-08-12T22:27:39Z',[item('SYNC-B')]),
          pub('2026-08-12','2026-08-11T22:27:39Z',[item('SYNC-A')])]"
dump "$ROOT/t10b.html"
SHA_B=$(shasum -a 256 "$SITE/news/index.html" | cut -d' ' -f1)
contains "$ROOT/t10b.html" 'nw-day-head">2026-08-13' "fixture B new digest_date shown"
contains "$ROOT/t10b.html" "標題-SYNC-B" "fixture B content shown"
[ "$SHA_A" = "$PAGE_SHA" ] && [ "$SHA_B" = "$PAGE_SHA" ] \
  && okc "HTML byte-identical across A and B ($PAGE_SHA)" \
  || badc "HTML changed between A/B"
say "  [evidence] live-sync: html sha A=$SHA_A"
say "  [evidence] live-sync: html sha B=$SHA_B"
verdict "$F0" "T10"

# ---------------------------------------------------------------- static states
say ""; say "=== Static: loading state and noscript are baked into the page ==="
F0=$FAIL
contains "$SITE/news/index.html" "正在載入最近七日的每日精選" "loading placeholder present pre-JS"
contains "$SITE/news/index.html" "noscript" "noscript notice present"
verdict "$F0" "static-states"

# ---------------------------------------------------------------- T12 category icons
say ""; say "=== T12 category icons (UI case): frozen assets, safe insertion ==="
F0=$FAIL
# Frozen CSS and markup facts, asserted on the page source itself.
contains "$SITE/news/index.html" "width:18px;height:18px" "frozen 18px icon size in CSS"
contains "$SITE/news/index.html" "flex:0 0 auto" "frozen non-shrinking icon box in CSS"
count_is "$SITE/news/index.html" 'data-name=' 5 "exactly five build-time icon slots"
count_is "$SITE/news/index.html" "innerHTML" 0 "page script never uses innerHTML"

# 12a: all five real category names render one icon each (aria-hidden).
fixture "[{'date':'2026-08-12','generated_utc':'2026-08-11T22:27:39Z','status':'published',
           'model':'claude-opus-5','candidates':30,'feeds':None,'warnings':[],
           'categories':[
             {'key':'ai_infra','name':'AI 基礎設施','items':[item('i1')]},
             {'key':'semis_hbm','name':'半導體/HBM','items':[item('i2')]},
             {'key':'robotics','name':'機器人與自主','items':[item('i3')]},
             {'key':'bio_ai','name':'生技×AI','items':[item('i4')]},
             {'key':'macro','name':'宏觀與政策','items':[item('i5')]}]}]"
dump "$ROOT/t12a.html"
count_is "$ROOT/t12a.html" 'class="ic" aria-hidden="true"' 5 "five rendered icons, all aria-hidden"
contains "$ROOT/t12a.html" "宏觀與政策" "category names still rendered as text"
not_contains "$ROOT/t12a.html" "$ERROR_TEXT" "no error state"

# 12b: unknown category name -> text renders, no icon, no error.
fixture "[{'date':'2026-08-12','generated_utc':'2026-08-11T22:27:39Z','status':'published',
           'model':'claude-opus-5','candidates':30,'feeds':None,'warnings':[],
           'categories':[{'key':'x','name':'未知的新分類','items':[item('u1')]}]}]"
dump "$ROOT/t12b.html"
contains "$ROOT/t12b.html" "未知的新分類" "unknown category name rendered"
count_is "$ROOT/t12b.html" 'class="ic" aria-hidden="true"' 0 "no icon for unknown category"
not_contains "$ROOT/t12b.html" "$ERROR_TEXT" "unknown category is not an error"

# 12c: hostile category name stays inert text -- never enters an HTML
# interpretation path, never matches an icon.
fixture "[{'date':'2026-08-12','generated_utc':'2026-08-11T22:27:39Z','status':'published',
           'model':'claude-opus-5','candidates':30,'feeds':None,'warnings':[],
           'categories':[{'key':'x','name':'<img src=x onerror=alert(1)>','items':[item('h1')]}]}]"
dump "$ROOT/t12c.html"
not_contains "$ROOT/t12c.html" '<img src=x' "hostile name not parsed as HTML"
contains "$ROOT/t12c.html" '&lt;img src=x' "hostile name escaped as text"
count_is "$ROOT/t12c.html" 'class="ic" aria-hidden="true"' 0 "no icon for hostile name"

# 12e: prototype-key category names must miss the icon map cleanly
# (Object.create(null)) -- plain text, no icon, no error, and rendering
# CONTINUES: the normal third category still gets its icon and card.
fixture "[{'date':'2026-08-12','generated_utc':'2026-08-11T22:27:39Z','status':'published',
           'model':'claude-opus-5','candidates':30,'feeds':None,'warnings':[],
           'categories':[
             {'key':'x','name':'__proto__','items':[item('p1')]},
             {'key':'y','name':'constructor','items':[item('p2')]},
             {'key':'macro','name':'宏觀與政策','items':[item('p3')]}]}]"
dump "$ROOT/t12e.html"
contains "$ROOT/t12e.html" "__proto__" "__proto__ rendered as plain text"
contains "$ROOT/t12e.html" "constructor" "constructor rendered as plain text"
count_is "$ROOT/t12e.html" 'class="ic" aria-hidden="true"' 1 \
  "prototype keys get no icon; only the normal category's single icon"
contains "$ROOT/t12e.html" "標題-p3" "rendering continues past prototype keys (later card present)"
not_contains "$ROOT/t12e.html" "$ERROR_TEXT" "no error state on prototype-key names"

# 12d: zero network requests for icons -- serve the same sandbox via a
# logging server and prove no /icons/ path is ever fetched.
fixture "[{'date':'2026-08-12','generated_utc':'2026-08-11T22:27:39Z','status':'published',
           'model':'claude-opus-5','candidates':30,'feeds':None,'warnings':[],
           'categories':[{'key':'macro','name':'宏觀與政策','items':[item('n1')]}]}]"
PORT2=$((PORT+1))
python3 -m http.server "$PORT2" --bind 127.0.0.1 --directory "$SITE" > "$ROOT/t12d-access.log" 2>&1 &
SRV2=$!
sleep 1
"$CHROME" --headless=new --disable-gpu --hide-scrollbars \
  --virtual-time-budget=5000 --dump-dom "http://127.0.0.1:$PORT2/news/index.html" \
  >/dev/null 2>&1
kill "$SRV2" 2>/dev/null; wait "$SRV2" 2>/dev/null
if grep -q "icons/" "$ROOT/t12d-access.log"; then
  badc "icon file was fetched over the network (must be inline-only)"
else
  okc "zero /icons/ network requests (inline clone only)"
fi
verdict "$F0" "T12"

# ---------------------------------------------------------------- summary
say ""
say "================================================================"
say "scenario results: PASS=$PASS FAIL=$FAIL (sandbox: $ROOT)"
if [ "$FAIL" -eq 0 ]; then say "ALL PAGE SCENARIOS PASSED"; exit 0; fi
say "SOME PAGE SCENARIOS FAILED"; exit 1
