# sinclairhuang.org — build & deployment rules

Hugo 0.152.2 + PaperMod. GitHub Pages serves the committed **`docs/`** directory
(`publishDir = "docs"`), DNS/cache via Cloudflare.

## Build standard (every build, not just after incidents)

```sh
scripts/build_and_check.sh
```

That runs `hugo --cleanDestinationDir --panicOnWarning --printPathWarnings
--destination docs --baseURL "https://sinclairhuang.org/"` and then the
acceptance checks: root files (CNAME, .nojekyll, robots.txt, 5 favicons),
dev-URL leak, /advisory/ fixed anchors, internal links/assets/anchors
(`scripts/check_links.py`), and a diff of URLs that disappeared vs the previous
build. A completion report is not done until this passes — the executor does
not self-accept.

- **Never run bare `hugo server` here** — it rewrites `docs/` with
  `127.0.0.1` URLs. Preview with
  `hugo --destination /tmp/preview-site --baseURL http://127.0.0.1:PORT/`.
- CI workflows build with `--cleanDestinationDir` but without
  `--panicOnWarning` (a stray warning must not kill unattended daily jobs);
  the panic flag is part of the local/manual acceptance build.

## File placement

- **Anything that must exist at the site root lives in `static/`** — CNAME,
  `.nojekyll`, `robots.txt`, `favicon.ico`, `favicon-16x16.png`,
  `favicon-32x32.png`, `apple-touch-icon.png`, `safari-pinned-tab.svg`.
  Nothing may exist only in `docs/`; `docs/` is disposable build output
  (`--cleanDestinationDir` wipes it every build).
- Favicon master SVG: `.github/assets/favicon-master.svg` (regenerate PNGs
  with `rsvg-convert`, ICO via PNG-in-ICO wrapper).
- Search Console verification is **DNS-based** (no HTML verification file has
  ever existed in this repo) — nothing to preserve in `static/`.
- Page data lives in `assets/` and is read with
  `resources.Get | transform.Unmarshal` — **`site.Data` is broken site-wide**
  (`data/research_news.md` is Markdown; Hugo rejects the whole data dir).

## URL discipline

- **`redirects.md`** at the repo root is the master old→new URL ledger. Any
  commit that renames a slug, deletes a page, or merges pages must update it.
- Hugo `aliases` front matter = HTTP 200 + meta refresh with correct
  canonical (acceptable interim). True 301s are done in **Cloudflare Redirect
  Rules** — the ledger marks candidates. Search Console is monitoring only,
  never a substitute for the ledger.
- Contact email published on the site is **research@sinclairhuang.org** only
  (Gmail is backend/recovery, never shown publicly).

## Layout gotchas

- PaperMod's footer is `partialCached` — per-section footer content must go in
  section-scoped single templates (`layouts/blog/single.html`,
  `layouts/insights/single.html` → `partials/advisory_cta.html`), never in
  `extend_footer.html`.
- `layouts/_default/single.html` is a theme override adding a
  `hideDescription` page param: front-matter description stays in `<head>` for
  SEO but is not rendered into the body (used by `/advisory/`).
- The article CTA is **template-injected** (blog + insights sections only);
  the number of pages carrying it always equals rendered blog + insights
  articles — count with
  `grep -rl advisory-cta docs/blog docs/insights` after a build.

## Process

Executor + independent reviewer: every completed work batch gets a completion
report that has passed `scripts/build_and_check.sh`, and a third-party review
happens before a phase is declared closed. Do not skip the script because a
change "looks trivial" — favicon 404s, CTA miscounts, and meta-refresh-vs-301
were all caught only in review.
