# Redirect ledger — 舊 URL → 新 URL

**機器可讀主檔是 [`redirects.tsv`](redirects.tsv)**（`scripts/check_site.sh` 逐列核對：
任何在兩次建置之間消失的 URL 必須在 TSV 有對應列，否則建置失敗）。
本檔是人讀的說明與 Cloudflare 執行指引；改 slug、刪頁、併頁時**兩檔都要更新**。
Search Console 只作後續監控，不取代台帳。

## 機制現況（2026-08-01 實測更正）

- Hugo alias = HTTP 200 + meta refresh（canonical 指向新頁），暫可接受。
- **本網域目前是 Cloudflare DNS-only**：DNS 直接解到 GitHub Pages 四個 IP，
  流量由 GitHub/Fastly 服務（`server: GitHub.com`），**沒有經過 Cloudflare proxy**。
  因此：
  - **Cloudflare Redirect Rules 現在貼了不會生效**（官方文件：redirect 只作用於
    proxied DNS records）。
  - **Purge Cloudflare cache 也無實質作用**——現在的快取在瀏覽器與 GitHub/Fastly 端。
  - 是否啟用 proxy（orange cloud）由 Sinclair 決定；啟用前需先驗證 HTTPS 憑證、
    GitHub Pages 自訂網域與 redirect 行為。**在那之前，真正 301 無法實作，
    alias 的 200 + meta refresh 是現行機制。**

## 若未來啟用 Cloudflare proxy：執行清單

1. **頁面匯流與舊 slug**：TSV 是內部台帳、**不能直接貼進 Cloudflare**。
   上傳用 [`redirects-cloudflare.csv`](redirects-cloudflare.csv)（由
   `scripts/gen_cloudflare_csv.py` 從 TSV 產生：排除 GONE 與 self-map、
   補上完整網域、每列 `source_url,target_url,301`；依 Cloudflare 規格**不含 header 列**，檔案恰為 35 個實體列）。
   **TSV 每次修改後重跑產生器。**
2. **15 個 `-2` 垃圾副本**：不要用涵蓋未來所有 `-2` slug 的寬鬆 regex——
   會誤傷未來任何正好以 `-2` 結尾的正當 slug。同樣放進 Bulk Redirects
   精確清單（15 列都已在 TSV）。
3. 若真要用 dynamic redirect 表達式，Cloudflare 的 capture 語法是
   `regex_replace(...)` 與 `${1}`，**不是** `$1`。

## 分類摘要（明細以 TSV 為準）

| 類別 | 數量 | 處置 |
|---|---|---|
| 頁面匯流 `/contact/`、`/consulting/` → `/advisory/` | 2 | Hugo alias 已生效；proxy 啟用後轉 301 |
| 舊文章 slug（part2–5、posts 變體、ai-was-never-sudden、why-jobs） | 8 | Hugo alias 已生效（2026-07-31 補） |
| 拼錯 tag 頁 → 正確 tag 頁（含 page/1） | 4 | 已 404；301 candidate |
| `-2` 垃圾副本 → 原文（2026-06 Finder 事故） | 15 | 已 404；Bulk Redirect 精確清單 |
| `/news-1/` → `/news/` | 1 | Hugo alias 已生效 |
| 過期 pagination URL → 上層列表頁或 GONE | 16 | 低價值；404 可接受 |
| 廢棄 taxonomy／模板殘留頁 | 8 | GONE（404/410 即可） |

---

**維護規則**：任何改 slug、刪頁、併頁的 commit，必須同步更新 `redirects.tsv`
（機器核對）與本檔（人讀摘要）。Phase 2 建立 `/research/` pillar、taxonomy
停產時，先加台帳列再部署。
