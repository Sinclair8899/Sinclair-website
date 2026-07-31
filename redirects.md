# Redirect ledger — 舊 URL → 新 URL 主對照表

單一事實來源：所有曾公開存在、之後移動或刪除的 URL 都記錄在這裡。
Search Console 只作後續監控，不取代本表。

**機制現況**：Hugo alias 產生 HTTP 200 + meta refresh（canonical 指向新頁），暫可接受。
重要舊網址應逐步改用 **Cloudflare Redirect Rules** 做真正 301——candidate 欄標記 `301` 者優先。

## 1. 頁面匯流（Hugo alias 已生效）

| 舊 URL | 新 URL | 機制 | Cloudflare |
|---|---|---|---|
| `/contact/` | `/advisory/` | alias（content/advisory.md） | 301 candidate |
| `/consulting/` | `/advisory/` | alias（content/advisory.md） | 301 candidate |

## 2. 舊文章 slug（2026-07-31 乾淨重建清出的孤兒頁，本輪已補 alias 恢復可達）

| 舊 URL | 新 URL | 機制 | Cloudflare |
|---|---|---|---|
| `/blog/ai-supply-chain-part2-power-map/` | `/blog/2026-04-01-article-2-the-real-ai-supply-chain-a-power-map-beyond-the-gp/` | alias | 301 candidate |
| `/posts/ai-supply-chain-part2-power-map/` | 同上 | alias | 301 candidate |
| `/blog/ai-supply-chain-part3-sec-filings/` | `/blog/2026-04-02-article-3-how-deep-is-the-moat-reading-tsmc-sk-hynix-and-mic/` | alias | 301 candidate |
| `/posts/ai-supply-chain-part3-sec-filings/` | 同上 | alias | 301 candidate |
| `/blog/ai-supply-chain-part4-stress-test/` | `/blog/2026-04-07-article-4-stress-testing-the-moat-four-threats-that-could-re/` | alias | 301 candidate |
| `/blog/ai-supply-chain-part5-industrial-transformation/` | `/blog/2026-04-11-beyond-the-gpu-what-the-ai-infrastructure-buildout-means-for/` | alias | 301 candidate |
| `/blog/ai-was-never-sudden/` | `/blog/2026-04-15-ai-was-never-sudden-a-30-year-view-on-the-great-repricing-of/` | alias | 301 candidate |
| `/blog/why-jobs-are-no-longer-enough/` | `/blog/2026-04-17-why-jobs-are-no-longer-enough-in-the-ai-economy/` | alias | 301 candidate |

## 3. 拼錯的 tag 頁（本輪修正 front matter 後自然消失）

| 舊 URL | 新 URL | 機制 | Cloudflare |
|---|---|---|---|
| `/tags/ai-infrastruture/` | `/tags/ai-infrastructure/` | 已 404（tag 改拼） | 301 candidate |
| `/tags/industialstrategy/` | `/tags/industrial-strategy/` | 已 404（tag 改拼） | 301 candidate |

## 4. 2026-06 Finder 複製事故的垃圾頁（2026-07-31 清除，共 15 篇 `-2` 副本 + `/news-1/`）

短暫上線約一個月，可能被少量索引。單條 Cloudflare 規則即可全數涵蓋：

| 舊 URL 模式 | 新 URL | 機制 | Cloudflare |
|---|---|---|---|
| `/blog/<slug>-2/`（15 篇） | `/blog/<slug>/` | 已 404 | 一條 regex 規則：`^/blog/(.+)-2/$` → `/blog/$1/` |
| `/news-1/` | `/news/` | alias（content/news/_index.md） | 301 candidate |
| `/blog/thoughts/yyyy-mm-dd-title/` | —（模板殘留，無對應內容） | 已 404 | 不處理（410 即可） |

## 5. 廢棄 taxonomy 頁（低價值，不設 redirect，404/410 即可）

`/categories/ai-compute-supply-chain/`、`/categories/research/`、
`/tags/ajinomoto/`、`/tags/geopolitics/`、`/tags/sec-filings/`、
`/tags/society/`、`/tags/strategy/`、`/tags/tag1/`、`/tags/tag2/`
（皆為 2026-07-31 乾淨重建清出的過期 taxonomy 頁；`tag1`/`tag2` 為測試殘留。）

---

**維護規則**：任何改 slug、刪頁、併頁的 commit，必須同步更新本表。
Phase 2 建立 `/research/` pillar、taxonomy 頁停產時，新增條目到本表。
