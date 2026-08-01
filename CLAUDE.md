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

Gates before the build: Hugo version pin, no backup/Finder-duplicate junk in
source or `.git/refs`, no stray `public/` tree. Then
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
- CTA appears **exactly once** per rendered blog/insights article
  (`class="advisory-cta"`; alias stubs excluded); count with
  `grep -rlo 'class="advisory-cta"' docs/blog docs/insights`
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

The checker itself is negative-tested: `scripts/test_checks.sh` runs one
pristine case (must pass) and eight seeded faults (must each fail): malformed
relative link, `localhost:57206` leak, unledgered disappeared URL (asserted
on its specific error message, so it cannot pass for the wrong reason),
duplicate CTA, backup file, and sync-duplicate dirs `name 5`, `name 12`,
`name (12)`. Run it after changing any check logic.

**Never invoke the build through a pipe** (`scripts/build_and_check.sh | tail`
— the pipeline's exit status is tail's, and `pipefail` inside the script
cannot protect the caller). Run it directly, or redirect to a file and read
that.

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
