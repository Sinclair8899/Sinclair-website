# sinclairhuang.org — build & deployment rules

Hugo **0.152.2** (pinned — the build script refuses any other version) + PaperMod.
GitHub Pages serves the committed **`docs/`** directory (`publishDir = "docs"`).
**Cloudflare is DNS-only**: records resolve straight to GitHub Pages' IPs and
traffic is served by GitHub/Fastly — there is no Cloudflare proxy, so Cloudflare
Redirect Rules and cache purges have no effect unless proxying is deliberately
enabled first (Sinclair's decision, not yet made).

## Build standard (every build, local and CI)

```sh
scripts/build_and_check.sh
```

Gates before the build: Hugo BASE-semver check (`scripts/check_hugo_version.sh`
— official releases report `v0.152.2-<hash>+extended`, brew reports
`v0.152.2+extended+withdeploy`; both pass, `v0.152.20-*` fails), no
backup/sync-duplicate junk anywhere in the repo except `.git/` and `docs/`
(shared pattern in `scripts/junk_pattern.sh`: one-or-more digits, ANY
extension), no junk `.git/refs`, no stray `public/` tree. Then
`hugo --cleanDestinationDir --panicOnWarning --printPathWarnings` with the
production baseURL, then `scripts/check_site.sh docs <prev-inventory>`:

- root files (CNAME, `.nojekyll`, `robots.txt`, five favicons)
- dev-URL leak — any `localhost`/`127.0.0.1`, **any port**
- no backup/junk files in output (incl. bare `name N`/`name (N)`
  sync-duplicate dirs, one or more digits — a sync-type external process is
  ACTIVELY interfering on this machine: it renamed 21 tag dirs to `name 2`
  and spawned `name 5` variants during the 2026-08-01 session alone. Leading
  hypothesis: iCloud "Desktop & Documents" sync. The repo was moved from
  `~/Desktop/Sinclair-website` to `~/Projects/Sinclair-website` on
  2026-08-01 as risk isolation and as the causal test — if junk recurs at
  the new path, the hypothesis is wrong)
- `/advisory/` fixed anchors (english/chinese/retainer/projects/briefings/start)
- `scripts/check_links.py`: internal links, assets, cross-page anchors, sitemap
  `<loc>`s; **relative or malformed URLs are a hard failure** (they are broken
  Markdown links in disguise — see the 42-link Medium-import incident)
- CTA is **routed** by front matter, and the semantic checker
  `scripts/check_cta_routing.py` (gate 6) is the SOLE authoritative CTA
  gate: `.Params.cta` is the ONLY routing input (`advisory` →
  `data-cta-type="advisory"`, target exactly `/advisory/#projects`;
  `subscribe` → `data-cta-type="subscribe"`, target exactly
  `https://sinclairhuang.substack.com/`; **`none` → the article
  publishes with ZERO CTA — a legal state, not a defect**;
  missing/unknown → the dispatcher `errorf`s and the BUILD FAILS).
  **A newly imported article without an explicit `cta` must never
  silently default to advisory** — the import flow has to write
  `cta: "subscribe"` explicitly. The gate verifies count
  (advisory/subscribe exactly one, none exactly zero), type, and exact
  target per page with semantic HTML parsing, derives expectations
  dynamically from source front matter, fails on an EMPTY non-draft
  article set, and only skips a page as an alias stub when it is
  genuine (exactly one zero-second refresh whose target equals the
  canonical AND normalizes onto a known article page). Per-release
  splits (e.g. 18/11/0) are asserted by that release's acceptance run,
  not hardcoded. Front matter is delimited by FULL `---` lines — never
  split on the substring `---` (Medium canonical URLs contain six-dash
  runs). `check_site.sh` takes an optional third CONTENT_ROOT argument
  for fixtures; production runs use the repo's `content/`.
- a URL that disappears vs the previous build **fails the build** unless it has
  a row in `redirects.tsv`

All three content CI workflows run this same script (they install Hugo
0.152.2 via peaceiris/actions-hugo and share
`concurrency: group: site-content-push`). The fourth workflow,
`daily_crawl.yml`, had its schedule disabled 2026-08-01: its output
(`data/research_news.md`) is not consumed by the site and is the file that
breaks `site.Data`; manual dispatch remains, now inside the same
concurrency group.
An unattended build that hits a new warning fails and leaves the live site as
it was — that is the safe outcome, not an inconvenience.

The checker itself is negative-tested: `scripts/test_checks.sh` runs 44
cases — 1 pristine (must pass), 30 seeded tree faults through the FULL
check_site.sh plus 3 source-side CTA faults against throwaway trees
(must each fail, the newer ones asserted on their specific error
messages so they cannot pass for the wrong reason), 5 positive cases
(must pass), 2 REAL Hugo builds proving the dispatcher's errorf
contract (missing cta and unknown cta each fail the build with their
specific message), and 3 Hugo-version parsing fixtures. The CTA-routing
cases: advisory↔subscribe type swaps, missing CTA, duplicate CTA,
advisory target without `#projects`, wrong subscribe target, and a
fake refresh page that must NOT pass as an alias (all through the full
harness, proving gate 6 is actually wired in), source cta missing,
source cta unknown, none-page-with-CTA (direct calls); positives cover
attribute order, a harmless extra class token, and a published
cta:none article whose zero-CTA page passes the whole harness via the
CONTENT_ROOT fixture override. Positive-case mutations are guarded: a
failed seeding script fails the suite rather than silently testing the
pristine tree. The 23 faults are 12 non-taxonomy —
malformed relative link, `localhost:57206` leak, unledgered disappeared
URL, duplicate CTA, backup file, sync-duplicate dirs
`name 5`/`name 12`/`name (12)`, sync-duplicate files
`favicon 12.png`/`update-news 12.yml`/`data-name 12.json`, zero date in
`docs/research/` — plus 11 taxonomy-policy faults: missing noindex,
robots directive conflict, refresh on a real taxonomy page, corrupted
`page/1` stub, plain noindex leaked onto a research page
(noindex-on-research-page), googlebot-noindex leak outside taxonomy,
taxonomy sitemap locs in plain (`/tags/ai/`), percent-encoded
(`/%74%61%67%73/ai/`), dot-segment (`/blog/../tags/ai/`) and
encoded-dot-segment (`/blog/%2e%2e/tags/ai/`) forms, and a research URL
dropped from the sitemap. The 2 positive cases: a robots variant
(`" NoIndex ,  FOLLOW "` with flipped attribute order) must PASS, and
`/tags/../blog/` must normalize OUT of taxonomy — sitemap paths are
normalized urlparse → unquote-once → `posixpath.normpath`, and the gate
parses HTML/XML semantically via `scripts/check_taxonomy_policy.py`, it
does not grep fixed strings. Version fixtures: official-hash pass,
brew-metadata pass, `v0.152.20` fail. Run the suite after changing any
check logic.

**Never invoke the build through a pipe** (`scripts/build_and_check.sh | tail`
— the pipeline's exit status is tail's, and `pipefail` inside the script
cannot protect the caller). Run it directly, or redirect to a file and read
that.

**`git diff --check` on generated output**: exceptions (PaperMod emits
trailing whitespace in page templates; `gen_cloudflare_csv.py` emits CRLF
rows) must be proven **per batch and per path** — show the same byte
pattern pre-exists in the base tree or is the generator's uniform output,
and assert the exact expected warning count/paths in the seal script.
Never grant a permanent exemption, and never hand-edit generated files to
silence it — `docs/` must stay byte-reproducible by the official build.

**Git path loops in scripts**: `git diff --name-only` quotes non-ASCII
paths (octal escapes wrapped in `"`) under the default `core.quotePath`,
which silently breaks `case docs/*` matching — the three Chinese-named
taxonomy pages hit this during the Release 1 seal. Iterate with a NUL
delimiter (`-z` + `while IFS= read -r -d ''`), or at minimum run the diff
with `git -c core.quotePath=false`.

- **Never run bare `hugo server` here** — it rewrites `docs/` with
  `127.0.0.1` URLs. Preview with
  `hugo --destination /tmp/preview-site --baseURL http://127.0.0.1:PORT/`.
- **Never let `public/` exist** — publishDir is `docs/`; `public/` is
  gitignored and its presence fails the build gate.

## File placement

- **Anything that must exist at the site root lives in `static/`** — CNAME,
  `.nojekyll`, `robots.txt`, `favicon.ico`, `favicon-16x16.png`,
  `favicon-32x32.png`, `apple-touch-icon.png`, `safari-pinned-tab.svg`.
  Nothing may exist only in `docs/`; `docs/` is disposable build output.
- Favicon master SVG: `.github/assets/favicon-master.svg` (regenerate PNGs
  with `rsvg-convert`, ICO via PNG-in-ICO wrapper).
- Search Console verification is **DNS-based** (no HTML verification file has
  ever existed in this repo).
- Page data lives in `assets/` and is read with
  `resources.Get | transform.Unmarshal` — **`site.Data` is broken site-wide**
  (`data/research_news.md` is Markdown; Hugo rejects the whole data dir).

## URL discipline

- **`redirects.tsv`** is the machine-readable old→new URL ledger (checked by
  the build); **`redirects.md`** is the human summary and Cloudflare playbook.
  Any commit that renames a slug, deletes a page, or merges pages must update
  **both**.
- Hugo `aliases` front matter = HTTP 200 + meta refresh with correct
  canonical — the only redirect mechanism currently possible (see DNS-only
  note above). If proxying is ever enabled: use precise Bulk Redirect lists
  from the TSV, never broad regexes over future slugs; Cloudflare dynamic
  expressions use `${1}`/`regex_replace(...)`, not `$1`.
- Contact email published anywhere on the site is
  **research@sinclairhuang.org** only (Gmail is backend/recovery, never
  shown publicly — the About page violation was fixed 2026-08-01).

## Content gotchas

- **Medium imports corrupt links and headings**: nested `[t]([url](url))`,
  asterisk-wrapped `[t](*url*)`, run-on headings (`#### ReferencesText…`),
  `****` bold junk, and U+00A0 non-breaking spaces inside sentences. The
  link checker now catches the link forms; eyeball headings on new imports.
- **Importer transform layer** (`.github/scripts/medium_transform.py`,
  stdlib-only): descriptions are 1–2 complete body sentences in 120–160
  code points chosen in document order — never a `[:200]` cut; headings,
  figures/figcaptions, bylines, series labels, and Field Note blocks are
  excluded; entities decoded, NBSP/whitespace normalized. An article with
  no compliant sentence group FAILS that import (and is NOT recorded in
  `imported_medium.json`, so it retries after a fix). Offline tests
  (`test_import_medium.py`, socket-disabled, zero third-party) run in the
  workflow BEFORE feedparser/requests install and any network fetch.
- PaperMod's footer is `partialCached` — per-section footer content must go in
  section-scoped single templates (`layouts/blog/single.html`,
  `layouts/insights/single.html` → `partials/advisory_cta.html`), never in
  `extend_footer.html`.
- `layouts/_default/single.html` is a theme override adding a
  `hideDescription` page param: front-matter description stays in `<head>`
  for SEO but is not rendered into the body (used by `/advisory/`).

## Process

Executor + independent reviewer: every completed work batch gets a completion
report that has passed `scripts/build_and_check.sh` (and, when checker logic
changed, `scripts/test_checks.sh`), and a third-party review happens before a
phase is declared closed. The executor does not self-accept, and verifying
that evidence exists is not the same as verifying the instrument that
produced it — test the checker with counterexamples.
