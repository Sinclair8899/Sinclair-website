---
title: "AI Capex 錢流地圖 v0.2｜美國出錢，誰真的收得到毛利？"
date: 2026-07-03
draft: false
tags: ["ai-capex", "semiconductors", "ai", "hbm", "cowos"]
description: "「AI 是不是泡沫」不夠可操作。更好的問題是：美國投下的資本支出，最後由誰收得到毛利？這是一份追蹤錢流落點的研究筆記。"
canonical: "https://sinclairhuang.substack.com/p/ai-capex-v02"
primary_cluster: "ai-infrastructure"
related_clusters: ["semiconductors", "capital-and-society"]
cta: "advisory"
---

*本文為繁體中文版。English version: [The AI Capex Money Map v0.2 — America Spends. Who Actually Keeps the Margin?](/blog/2026-07-03-the-ai-capex-money-map-v02-america-spends-who-actually-keeps/)*

大多數人現在都在問：「AI 是不是泡沫？」

這個問題重要，但不夠可操作。對投資人與供應鏈觀察者來說，更好的問題只有一句：

**美國大型科技公司花出去的 AI Capex，最後流到誰的收入、誰的毛利、誰的護城河？**

這篇不是拆到每一根電纜的投行 BOM 模型，而是一張用公開資料建立的 **v0.2 錢流地圖**。它的目的不是假裝精準，而是把三件常被混在一起的事情分開來看：**錢在哪裡變成營收、營收在哪裡變成毛利、瓶頸何時鬆解。** 因為這三題的答案，往往不是同一批公司。

**一、AI Capex 不是一個數字，是一組水管**

Reuters 引述 Bridgewater 的估計：Alphabet、Amazon、Meta、Microsoft 四大 2026 年的 AI 基礎設施投資約 **US$650B**，高於 2025 年約 US$410B。先講清楚一件事——這是**四大的地板數**，不含 Oracle、Stargate、CoreWeave 這類 neocloud、xAI，也不含任何非美系業者。所以 $650B 是四家公司的**下限**，不是市場總額。

錢不會平均落下。它會分成幾條性質完全不同的水管。這是第一層、彼此互斥的系統層分配（示意情境，加總 100%）：

圖一：*示意性 capex 分流，加總 100%；設備與材料屬二階供應商 capex，不納入 hyperscaler 直接支出，以避免 double counting。*

關鍵是——**設備與材料（ASML、AMAT、TEL、Advantest…）不在這 $650B 裡。** 那是台積電、SK Hynix 的資本支出，是二階供應商支出、是另一個分母。把它加進 hyperscaler 支出裡相加，就是 v0.1 犯的、也是很多市場圖表仍在犯的 **double counting**。

**二、把箱子打開：成本重心已經從邏輯移到 HBM + 封裝**

把「Compute Systems」這條水管打開，你會看到這一輪最反直覺的結構變化。

以 Epoch AI 對 B200 的 BOM 模型為參考：B200 的 variable manufacturing cost 約 US$5,700–7,300（中心值約 US$6,400），其中 **HBM + 先進封裝合計約占三分之二**。乾淨的 100% stack 大致長這樣：

圖二：*B200 成本重心已從 logic die 移向 HBM 與先進封裝；比例為分析用估算，非廠商揭露 BOM。*

這張圖回答的是投資問題，不是工程問題：**當 hyperscaler 付一顆加速器的錢，那些實體美元真正流到哪裡？** Nvidia 在最上層收走 IP 與平台毛利，但**箱子裡的實體現金，大量流向 SK Hynix（HBM）與台積電（封裝）**。「誰能出貨 AI 加速器」早已不是 logic die 的問題，而是 memory allocation、CoWoS、substrate、測試的聯合約束。

**三、一個很多人跳過的細節：晶片毛利 ≠ 實拿毛利**

Nvidia 是全鏈毛利最高的一段，這沒錯。但如果你只拿它某一季的巔峰數字，就會得到過度樂觀的圖像。

- FY2026 **Q4** GAAP / non-GAAP 毛利率 **75.0% / 75.2%**；

- 但 FY2026 **全年**是 **71.1% / 71.3%**；

- Epoch 用約 US$30,000–40,000 的售價對上約 US$6,400 的製造成本，推得**晶片層**毛利約 82%——但它自己也指出，多數 Blackwell 營收來自 server / rack-scale 系統，**系統層的實拿毛利低於晶片層**。

換句話說，「Nvidia 毛利很高」這句話要分三層講：chip-level、platform-level、system-level。這正是整張地圖的核心紀律——**營收沿著鏈往下流，毛利不會。** 站在營收流過的位置，不等於留得住毛利。

**四、瓶頸時鐘：不是「缺不缺」，而是「何時鬆解」**

一般文章把 CoWoS、HBM、液冷、電力列為瓶頸，然後就停了。這對投資沒用。有用的研究要多問四件事：現在多緊？方向在惡化還是緩解？新增供給會不會被下一代需求吃掉？鬆解後毛利怎麼變？

圖三：*瓶頸不只看「缺不缺」，還要看緊度方向、鬆解時間與下一個監測指標。*

- **CoWoS / 先進封裝：** TrendForce 估台積電 2026 月產能約 120k–140k 片，加上 OSAT 新增 50k–60k，產業總量可能逼近 200k 片/月，供需缺口可能從約 20% 收斂到 10%。但「缺口收斂」不等於「瓶頸消失」——若 Rubin / ASIC 的 package area 持續變大，瓶頸只是從 wafer count 移到封裝面積、良率與設備，高階部分可能緊到 2028–2029。

- **HBM：** SK Hynix 表示 2026 年產出已售罄，是真的瓶頸。但別忘了它本質仍是 memory——若 2027–2028 新產能集中開出，要警惕 structural shortage 轉回 memory cycle。一個反直覺、值得直接點名的訊號：2025 年 HBM 市占約 SK Hynix 61%、**Micron 約 21%（已超過 Samsung）、Samsung 約 17%**。同樣是記憶體巨頭，認證、良率與客戶配置的差異，大到足以讓 SK Hynix 市值一度超越 Samsung。（註：這是全年快照，季度市占會波動；市值超越幅度亦小且有爭議。）

- **電力 / 液冷 / site：** 這是最容易被低估、也最可能成為**下一個**瓶頸的一段。機櫃功率的軌跡是：傳統雲端 10–20kW → GB200 NVL72 約 120–132kW → 2027+ Rubin / Kyber 世代 300–700kW 情境（NVL576「Kyber」機櫃已公開討論到約 600kW）→ 產業已在談 1MW 級。當單櫃功率跳一個數量級，瓶頸就從晶片、封裝一路外移到 CDU、cold plate、UQD、HVDC、BBU、變壓器、併網許可與機房施工。**這是部署速度的瓶頸，不只是半導體供給的瓶頸。**

瓶頸會遷移：chip → package → memory → power / site。押在「上一個瓶頸」的人，常常在瓶頸鬆解、毛利正常化的那一刻，才發現自己站錯位置。

**五、台灣視角：同一筆 Capex，在台灣被切成四種完全不同的生意**

「營收留存 ≠ 毛利留存」在台灣不是抽象概念，是 2026 年 Q1 財報上一道**肉眼可見的毛利率階梯**。同樣站在 Nvidia 這條收款流上：台積電 Q1 毛利率 66.2%；液冷龍頭奇鋐 29.77%（歷史新高，伺服器＋網通產品合計已占營收約 66.4%）；鴻海 6.2%；廣達 4.78%。**同一筆 hyperscaler 的錢流過四家公司，毛利留存差了一個數量級以上（66.2% 對 4.78%，約 14 倍）。**

差距的來源不是誰比較努力，是商業模式的物理結構。一整櫃 AI 系統動輒上百萬美元，而電子業的「代工代料（buy-and-sell）」規則是：ODM 先自己掏錢買下整櫃裡最貴的料——GPU、HBM——組裝、出貨、驗收之後才收得到款。生意愈好，墊的現金愈多——**營收爆增與營運現金流吃緊，在這個模式裡是同一件事的兩面。**

這個壓力有多實際？看業者自己的動作，不用聽分析師的話：廣達在 2026 Q1 法說明確表示，正與客戶洽談把部分新專案改成 **consignment（寄售）模式——由客戶自備關鍵零件——以「舒緩營運現金與毛利」壓力**；鴻海 Q1 6.2% 的毛利，部分原因正是部分伺服器已採 consign 模式；緯創則規劃辦理最高 2.5 億股的現金增資／GDR，用途指向「海外採購、營運資金與銀行還款」。**當一個產業開始集體修改交易模式、並向資本市場伸手要週轉金，這比任何一張 Excel 都誠實地告訴你：錢流經這裡，但不留在這裡。**

同一季還有一個地面細節，說明平台轉換的風險為什麼在台灣先被看見：市場關注 Nvidia 對 Rubin 散熱設計的修改（均熱片由雙件式改為單件式），一度衝擊台廠散熱股（健策亮燈跌停）。鴻海把這個散熱設計變更列為需要「持續觀察」的出貨節奏變數；不過 FII 在 Computex 也表示 Rubin 仍按 H2 2026 進度推進，分析普遍認為此調整**不必然造成整季遞延**。重點不在於某一季是否延一週，而在於：**一個零件的設計變更，就足以牽動整櫃的節奏**——這正是 Bottleneck Clock 裡「server / rack integration 在平台轉換時最緊」的地面版本，也解釋了為什麼高度綁定單一規格的供應商，會對一則設計變更傳聞反應如此劇烈。

（上述毛利率、寄售與資金用途等數字，出自各公司 2026 年 Q1 財報與法說；Rubin 散熱設計變更則按市場報導與公司回應處理，本文僅視為出貨節奏風險，不視為已確認遞延。）

**六、拆分的訊號：ASIC，與聯發科的重新定價**

如果要用一個案例驗證整張地圖，選 custom ASIC。

Counterpoint 預測聯發科到 2028 年可拿下 AI ASIC server compute shipments 約 **26%、接近 5 million units**，成為僅次於 Broadcom 的第二大——相對 2026 年約 40 萬顆，是超過十倍的成長。市場重新定價聯發科，不是因為「AI 三個字」，而是因為背後一串**必須被驗證**的假設：

1. AI ASIC 不是 Broadcom 一家獨大的 turnkey 生意；

2. hyperscaler 願意把 compute die、I/O、HBM 採購、封裝整合拆開（unbundle）；

3. 聯發科拿到的不只是 I/O die——依 Google Cloud Next 2026 相關報導，Google 把第八代 TPU 拆成兩種架構，**Broadcom 主導訓練版（TPU 8t「Sunfish」）、聯發科主導推論版（TPU 8i「Zebrafish」）**，供應鏈報導另指向第二家美系 CSP 專案，但客戶身分仍未確認；

4. 這不是一次性設計服務，而是一個有世代延續性、且毛利有黏性的 custom silicon 平台；

5. CoWoS / HBM / 台積電產能配置撐得起這條出貨曲線。

但這裡有一個不屬共識的關鍵風險，而且它直接指回第五節的美國那一欄：**若 Google 繼續把設計與 HBM 採購控制權更多拿回自己手上，目的之一可能就是壓低中間加價。** 這會成為 Broadcom turnkey margin 的壓力測試——市場也把 Google TPU 供應鏈拆分解讀為獨家地位被削弱——對聯發科則是雙面刃：你可能拿到出貨量與設計角色，但當客戶自己走採購與整合的價差，**「延續性毛利」這個假設就要打一個問號**。市場定價的是量；你要盯的是毛利與客戶集中度。

到 2026 年年中，這串假設已經開始產出可驗證的讀數，而三層證據的可信度不同，值得分開看：

- **公司已確認（最硬）：** 聯發科在 Q1 法說把 2026 年 AI ASIC 營收指引**從 US$1B 上修至約 US$2B**（首個 hyperscaler 專案約 $2B 落在 2026 Q4），並表示第二個專案目標 2027 年底前量產、雲端 ASIC TAM 看到 2027 年約 US$70–80B、目標市占 10–15%。當一門生意從「故事」走到「明確指引」，那是管理層自己蓋的章。

- **供應鏈可見（次之）：** 賣方對日月光的產能推估顯示，**聯發科 TPU v8 與 Amazon Trainium 3 明年在 final test 明顯放量**——驗證訊號如本文預期，先出現在台灣的封測排程裡，而不是美國分析師報告裡。

- **賣方重新建模（僅供參考，非事實）：** 賣方模型在 2026 年一路上修（可查到的 Goldman 4 月版本，把 2027 AI ASIC 營收看到約 US$12.3B、約占營收 39%）；市場另流傳更積極的 2027／2028 數字（約 US$20B／US$52B、占比 49%／69%），但**此版本目前無法從公開來源獨立查證，應視為賣方傳聞而非事實**。Street 高端目標價出現約 NT$10,000（券商推估，個別機構歸屬未能證實）。這些是估計，不是證據；它們釘住的，只是「市場現在在為哪一組假設定價」。

而在毛利那條線上，連多頭都得讓步：賣方普遍把下一代專案的 ASP 上修，但**毛利率被描述為「大致維持」而非擴張**——也就是成本轉嫁（cost pass-through），不是毛利提升；甚至有券商把新一代專案標為**略為稀釋毛利率**，靠的是營運槓桿。換句話說——**量的故事正在被確認，毛利的故事還在考試。** 這正是這張錢流地圖裡，你要持續盯著的那一格。

**七、六月最後一週：整個故事在台北排練了一次**

先講溫度。同一檔聯發科，你可以在台北同時讀到三支溫度計：外資在建假設鏈模型、往上調目標價；本地第一線分析師多半直說五位數目標價「不可能」——理由不是看空，而是 ASIC 競爭太多，除非聯發科真能從 Broadcom 手上接下同級高單價訂單、且設計能力與成本結構都到位，否則這些都是高不確定性的假設；而散戶熱度，熱到一位百萬訂閱 YouTuber 買**一張**聯發科就上了新聞。**當一檔股票變成娛樂新聞，你就知道此刻的價格裡摻了多少擴音器。**

然後，六月最後一週把我對這個故事最深的懷疑，當場演了一遍。這條鏈我最不信的一環從來不在供給端，而在迴圈的最末端：**漲價鏈的終點，總得有人買單。** 6 月 25 日，多家媒體報導 Apple 因記憶體與儲存成本上升，調漲部分 Mac / iPad 價格（幅度約 11–36%），並引述其「從沒見過零件價格在這麼短時間漲這麼多」的說法。這件事之所以重要，不是因為 Apple 本身，而是因為它把供應鏈漲價的**終點**暴露了出來：再強的品牌，也不是每一分上游成本都能無限吸收。隔天市場把這條漲價鏈的風險重定價了一次——台股單日重挫 1,683 點（史上第三大跌點），外資單日賣超約 NT$1,432 億，聯發科自己亮燈跌停（3,880）。**這個基本的經濟迴圈，不會因為主題叫 AI 就停止運作——而它反手打到的第一排，正是 AI 供應鏈自己的市值。**

下半週一樣值得記錄：五天後市場反彈，那位 YouTuber 獲利約 46 萬元出場；再隔一天，外資又上調聯發科目標價。下跌時，台灣高度 ETF 化的被動買盤與逢低承接接住了跌勢；上漲時，敘事重新扛起漲幅。**此刻的價格裡，一部分是錢流，一部分是夢；這張地圖的全部意義，就是幫你把兩者分開。**

一個誠實的收尾：假設五（產能撐得起出貨曲線）的反面訊號——ASIC 專案與 Nvidia 訂單在封測端出現的實際排擠——我在地面上**還沒**聽到。這可能代表產能還有餘裕，也可能只是訊號還沒浮出。我把它當成一個還沒響的鬧鐘：它響的那天，就是這個故事從「量正在被確認」轉為「產能與毛利互相磨擦」的那天。

**八、與其猜方向，不如建立追蹤紀律**

這張地圖不給你「買什麼」的答案，而是給你一組需要持續更新的指標：

- **CoWoS：** 台積電月產能、OSAT ramp、封裝面積、良率、設備交期。

- **HBM：** 報價、長約、stack mix、SK／Samsung／Micron 各自 capex、DRAM／NAND 排擠。

- **電力 / site：** 變壓器交期、HVDC／BBU 滲透、併網許可、機房施工進度。

- **Server / rack：** 出貨量、burn-in 測試時間、ODM 毛利、庫存、客戶集中度。

- **ASIC：** Google TPU、Meta MTIA、AWS Trainium 量，與 Broadcom／MediaTek／Marvell 的 pipeline。

紀律只有一條：**把 vendor 說的（「已滿載」「量產中」）和財報確認的，分開記。** 前者是方向，後者才是證據。

**Appendix：Regional Margin Capture Map**

文章叫「錢流地圖」，最後就該收在一張國家分帳圖上。美國出錢、亞洲組裝，但每一區留下的毛利完全不同：

圖四：*國家／區域分帳圖：收得到營收，不等於留得住毛利。*

一句話：**這張地圖不是選股清單。它告訴你一家公司是站在收款點，還是只站在市場擴音器旁邊。**

**結論：錢流不會說謊，瓶頸決定誰留住毛利**

AI FOMO 不一定錯。但真正決定長期報酬的，不是你買到「AI」這三個字，而是你押的公司，究竟站在這條 Capex 錢流的**收款端**，還是只站在市場最大聲的**擴音器**旁邊。

**錢流不會說謊。瓶頸決定誰真的留得住毛利。**

**模型邊界：** 這不是一份拆到每根電纜、接頭、建材的投行 BOM 模型，而是一張用公開資料建立的 AI capex 錢流、毛利留存與瓶頸時間 v0.2 地圖。它的目的不是假裝精準，而是避免重複計算、把 hyperscaler 直接支出與二階供應商 capex 分開，並追問：哪一層真的留得住毛利。

**English Summary**

**The AI Capex Money Map v0.2 — America spends; who actually keeps the margin?** Of the ~US$650B the US Big Four will spend on AI infrastructure in 2026 (a floor, not a market total), this public-data map separates three things usually blurred together: where capex becomes **revenue**, where revenue becomes **margin**, and when **bottlenecks** ease. Opening the accelerator box, the cost center has shifted from logic die to **HBM + advanced packaging (~two-thirds of unit cost)** — so the real dollars flow to SK Hynix and TSMC, not just Nvidia. In Taiwan the same capex dollar becomes four different businesses: TSMC’s 66% gross margin versus Quanta’s 4.78% — an order-of-magnitude gap driven by the buy-and-sell/consignment model, not effort. MediaTek’s ASIC re-rating is the case study: volume is being confirmed (guidance doubled to ~US$2B), but the margin story is still unproven, especially if Google keeps more design/procurement control in-house. **Money flow doesn’t lie; bottlenecks decide who keeps the margin.**

**Data / Source Notes / References**

1. **Reuters / Bridgewater** — Big Four (Alphabet, Amazon, Meta, Microsoft) 2026 AI infrastructure investment ≈ US$650B, up from ≈ US$410B in 2025. **(Confirmed.)**

2. **Epoch AI** — B200 variable manufacturing cost ≈ US$5,700–7,300 (central ~US$6,400); HBM + advanced packaging ≈ two-thirds of unit cost; implied chip-level GM ~82% at ~US$30–40k ASP; realized system-level margin lower. **(Confirmed.)**

3. **NVIDIA** — FY2026 revenue US$215.9B; Q4 GAAP/non-GAAP GM 75.0%/75.2%; FY GM 71.1%/71.3%. **(Confirmed.)**

4. **TrendForce** — TSMC 2026 CoWoS ~120k–140k wafers/mo; +OSAT ~50k–60k → industry ~200k/mo; supply-demand gap narrowing ~20%→10% by end-2026. **(Confirmed; gap figures attributed by TrendForce to institutional investors.)**

5. **Reuters / Counterpoint** — 2025 HBM share: SK Hynix ~61%, Micron ~21%, Samsung ~17%; SK Hynix market cap briefly overtook Samsung. **(Confirmed; full-year snapshot, quarterly shares fluctuate.)**

6. **Counterpoint** — MediaTek ~26% of AI ASIC server-compute shipments (~5M units) by 2028, #2 after Broadcom, ~10× vs ~400k in 2026. **(Confirmed.)**

7. **Rack power** — GB200 NVL72 ~120–132kW; Rubin/Kyber-era 300–700kW (NVL576 ~600kW, 2H2027); 1MW-class discussed. **(Confirmed.)**

8. **TSMC Q1 2026** — gross margin 66.2% (above 63–65% guidance); FY2026 capex US$52–56B (guiding to high end). **(Confirmed.)**

9. **AVC / 奇鋐 (3017) Q1 2026** — revenue NT$49.04B (+110% YoY), gross margin 29.77% (record); server + networking ≈66.4% of revenue. **(Confirmed.)**

10. **Quanta (2382) Q1 2026** — GM 4.78%; negotiating consignment shift for some AI-server projects. **Hon Hai (2317) Q1 2026** — GM 6.2%; NVIDIA Rubin vapor-chamber redesign (dual→single) flagged as a shipment-cadence item to monitor. **(Margins & consignment confirmed; a specific one-quarter VR200 slip is NOT supported — FII says Rubin on track for H2 2026.)**

11. **MediaTek (2454) Q1 2026** — 2026 AI ASIC guidance doubled US$1B→~US$2B; second program targeted for production by end-2027; cloud ASIC TAM ~US$70–80B by 2027, 10–15% share target. **(Guidance doubling confirmed; a separate ASIC disclosure line from 2027 is unverified.)**

12. **Google 8th-gen TPU split** — industry coverage points to Broadcom = training (TPU 8t “Sunfish”) and MediaTek = inference (TPU 8i “Zebrafish”), TSMC N2, ~late 2027. The TPU supply-chain split is commonly read as weakening sole-supplier economics. A second US CSP program is reported, but the customer identity remains **unconfirmed**. **(Training/inference roles per Google Cloud Next 2026 coverage.)**

13. **Apple** (Jun 25, 2026) — raised Mac/iPad ~11–36% citing memory/storage cost inflation; “never seen component prices rise so much so fast.” **(Confirmed.)**

14. **Taiwan market** (Jun 26, 2026) — TAIEX −1,683.5 pts (third-largest single-day point drop on record); foreign net sell ≈ NT$143.2B; MediaTek limit-down at 3,880. **(Confirmed.)**

**Sell-side items (Goldman US$20.3B/US$52.5B for 2027/2028; Macquarie NT$10,000; 5% price pass-through) could not be independently verified against a primary July 2026 note and are treated as unverified sell-side estimates. The closest verifiable Goldman note (April 2026) modeled 2027 AI-ASIC revenue ≈ US$12.3B (~39% of revenue).**

**(Extended 21-item source log available on request / in the working draft.)**

**Author**

**Sinclair Huang**

Research notes on AI infrastructure, semiconductors, supply chains, and technology strategy.

**Further Reading / Next Tracking List**

- CoWoS：台積電月產能、OSAT ramp、封裝面積、良率、設備交期。

- HBM：報價、長約、stack mix、SK Hynix／Samsung／Micron capex、DRAM／NAND 排擠。

- Power / site：變壓器交期、HVDC／BBU 滲透、併網許可、機房施工進度。

- Server / rack：ODM 毛利、burn-in 測試時間、庫存、客戶集中度、consignment 比例。

- ASIC：Google TPU、AWS Trainium、Meta MTIA，與 Broadcom／MediaTek／Marvell pipeline。

**免責聲明**

本文為研究筆記與產業分析，不構成任何投資、買賣或資產配置建議。文中數字多為公開資料、產業報告、媒體報導與 v0.2 方向性估算，應持續以公司財報、月營收、法說、訂單、報價、交期、毛利與產能進度更新。標示為賣方估計或未經查證者，請以「估計／待驗證」看待，勿當作事實。
