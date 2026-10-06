---
title: "AI 的經驗如何在真實世界養成"
date: 2026-10-01
draft: false
tags: ["agentic-ai", "tacit-knowledge", "physical-ai", "spatial-intelligence", "world-models"]
description: "我聽過李飛飛多次演講與座談，很早就認同空間智慧與物理 AI 的方向。但最近使用 AI 處理生活中的問題，讓我更在意另一個問題：專業經驗如何養成？AI 已能幫我把想法做成工具；走進物理世界之後，它還需要能觀察、行動、得到回饋，並驗證結果的環境。"
canonical: "https://sinclairhuang.substack.com/p/ai-1a5"
cta: "subscribe"
---

*本文為繁體中文版。English version: [How AI Gains Experience in the Real World](/blog/2026-10-01-how-ai-gains-experience-in-the-real-world/)*

*從 World Labs 到程式學習與現場工作的觀察*

2026 年 10 月 1 日

![陽光下的住宅區，街道兩旁是斜屋頂的一、二層住宅](/images/blog/2026-10-01-how-ai-gains-experience-in-the-real-world/figure1-roofs.jpg)

*旅途中看到的住宅斜屋頂，讓我想起朋友談到的現場工作。作者攝影。*

## 從一筆收購想到經驗如何養成

2026 年 9 月 28 日，AMD 宣布簽訂收購 World Labs 的協議，交易金額約 82 億美元，以全股票方式支付，預計年底前完成，仍須取得相關批准。交割後，李飛飛將出任 AMD 執行副總裁兼首席科學家。[1] 她在宣布加入 AMD 的文章中寫道，宇宙由真實的事物組成，而不只是文字。[2]

我聽過李飛飛多次演講與座談，很早就認同空間智慧與物理 AI 的方向。但最近使用 AI 處理生活中的問題，讓我更在意另一個問題：專業經驗如何養成？AI 已能幫我把想法做成工具；走進物理世界之後，它還需要能觀察、行動、得到回饋，並驗證結果的環境。

## AI 讓我更容易動手學習

一年前，我還在用 Colab 寫程式：貼程式碼、執行、報錯，再把錯誤訊息貼回去問，來回十幾次是常態。現在使用 Claude Code 和 Codex，許多除錯與修改能由工具接續完成。我仍要測試與檢查，但反覆搬移程式碼和訊息的時間少了很多。

我也用不同的 AI 協助寫 Python，嘗試模擬自己喜歡的 EViews 的部分工作方式。EMBA 論文時，我用過 EViews；現在我把資料庫資料接進 Python 進行統計分析，並做成一個初步的 APP，叫作 PyViews。核心迴歸結果已用另一套獨立開發的 Python 套件 linearmodels 交叉核對，係數完全一致；由於我的 EViews 授權已經過期，與 EViews 的直接比對仍待完成。這些嘗試是為了學習、好玩與好奇，也想看看 AI 的能力邊界。

這種學習很直觀。想法很快變成能操作的東西，遇到錯誤便改、再試，成本相對低，我因此更願意探索。先弄清楚想解決什麼，再調用合適的工具或 Skill，一個小創意就可能改變工作方式。和 AI 一起製作、檢查與修改工具，本身也是我累積經驗的過程。

![PyViews 介面截圖：左側選擇樣本與會計年度，右側指令視窗顯示面板最小平方法迴歸結果](/images/blog/2026-10-01-how-ai-gains-experience-in-the-real-world/figure2-pyviews-zh.png)

*在 AI 協助下製作的 PyViews。選擇樣本與年份、輸入一行指令，即可執行面板迴歸。核心結果與一套獨立的 Python 套件一致；與 EViews 的直接比對仍待完成。*

這個工具教會我的，與其說來自打造它，不如說來自檢查它。第一次迴歸跑完，沒有出現任何錯誤訊息，裡面卻藏著好幾個問題：IBM 的損益表從未下載，整家公司就這樣無聲地從樣本中消失；Alphabet 的兩種股票被當成了兩家公司；我當初假設 AlphaFold 3 很快會帶動生技股，因而納入二十家健康照護公司，結果其中幾家幾乎沒有營收的生技公司，使「研發／營收」的比率失去意義，扭曲了整體結果。就連 AI 寫的一條排除規則，也與它自己舉的例子矛盾，直到用實際資料檢驗才被發現。AI 的錯誤，靠我對數字是否合理的直覺抓出；我自己的錯誤假設，則由資料揭露。每一次修正，連同當時的預期與實際的發現一起保存下來，就成了我在後文所提「可檢驗的經驗紀錄」的一個小型版本。

## 修車與修屋頂讓我看到現場的差別

數位工作較容易留下可重現的測試紀錄。現場問題的關鍵條件，卻可能沒有被量測，甚至只在某個瞬間出現。我的老車電子駐車煞車就有間歇性故障：警示燈亮起，過一陣子消失，進廠又可能一切正常。我把故障碼和診斷畫面拍給 AI 看，依建議花了兩萬三千元換上整新總成，同樣的警示仍再次出現。AI 隨後轉向懷疑線束與模組通訊，來回數週，問題仍未釐清。

AI 能整理可能原因、建立假說，也能提醒我保留故障當下的資料。但假說合理，不代表原因已被確認；資訊可能不足，推理也可能錯。現場師傅能檢查接頭、聽聲音、比較過往案例。如何取得關鍵證據，本身就是專業判斷的一部分。

在美國，一位做建築與水電小工程的朋友，讓我有另一種體會。他接了浴室工程，我看到桌上放著他手工畫的圖。他兒子學土木，會用 AutoCAD，但他寧可自己去現場量測，再手繪。他很有自信地說，他認為自己的現場製作，是將來 AI 取代不了的。

跟著他在社區散步時，他一邊介紹那些由他換修、維護的斜屋頂。我看著一、二層住宅，腦中不由得浮起機器人笨手笨腳爬上屋頂的畫面，覺得有點好笑。那一刻，我直覺這種場景離日常生活還很遠。

手繪或電腦繪圖，未必足以解釋他的自信；更值得注意的，是他把量測、圖上的安排與實際施工接起來。圖畫得出來，工程能否完成，仍要面對現場條件。我也想，AI 若能幫他整理估算和過往案例，是否可以減輕辛苦，讓他的經驗更容易保存與運用？

Michael Polanyi 在《The Tacit Dimension》中指出，我們知道的往往比我們能說出的更多。[3] 技能與判斷不一定能完整寫進手冊，卻也不表示經驗永遠無法記錄。維修紀錄若只寫「更換零件」，就不足以支持下一次判斷；還需要知道為何更換、預期改善什麼，以及實際是否改善。

## 發球機提供練習 教練幫助改善

在西雅圖的公園散步時，我走到網球場，看見發球機供姊弟兩人練習，旁邊有一位女教練。後來她也親自發球、下場陪打。他們以為我是來等候使用球場，我便順勢問起機器的功能，再問它有沒有教練功能。她笑著說，也許未來會有，但現在仍需要教練找出學習者的盲點與弱點，再特別指導改善。

這讓我更理解，練習機會需要和有效回饋連在一起。發球機供球，教練觀察表現、調整重點。經驗養成不能只計算練了多少次，還要知道哪些地方有進步，哪些錯誤仍在重複。

## 貓砂機聞不到我們無法忍受的臭

砂已經蓋不住排泄物，機器裡也很臭，另一隻貓不敢進去。我聞到之後，判斷這批砂已經不能留，便把它清掉。按 Cycle 篩掉結塊也是一種做法；機器兩種指令都能執行，但它聞不到臭，也不知道這個氣味對住在這裡的人是否已無法忍受。事後問 AI，得到的是按鍵與「全自動」的說明，同樣沒有這層現場判斷。動作可以交給機器，決定要做哪個動作的感受仍在人身上。

![自動貓砂機，一隻橘貓蜷在滾筒裡](/images/blog/2026-10-01-how-ai-gains-experience-in-the-real-world/figure3-litter-box.jpg)

*兒子家的自動貓砂機。機器執行了指令，卻聞不到這批砂對我們是否已不能留。作者攝影。*

## 我的具體主張：可查核的經驗紀錄

我一直在想，能否把自駕車的感知、定位與導航方法移用到無人機，讓 AI 透過載具觀察世界、累積觀察日誌。方法有共通性，但三維運動與感測條件不同，仍須適應與驗證。不過無論載具是什麼，更根本的問題是：經驗要用什麼形式留下來？

孩子成長需要探索與回饋；領域大師的養成，需要面對不同案例、辨認失敗原因並修正做法。AI 要累積專業能力，也需要適當的任務與評量。大量重複不能保證進步，錯誤回饋甚至可能強化偏差。

我想提出的具體做法，是建立<strong>「可查核的經驗紀錄」</strong>。它至少要做到四件事：保留環境與原始資料；把實際觀察和模型推論分開；記下採取的行動與當時的預期；再對照實際結果。結果不一致時，才有依據追問：是缺資料、判斷錯誤，還是執行條件改變？若我的修車過程從一開始就這樣記錄，數週的來回就不會一再繞回已經排除的可能。改善是否有效，也需要衡量，不能只由 AI 寫成一段流暢敘事。

家人告訴我，他工作的公司已要求把裝機與維護寫成報告，輸入 AI 系統。各地客戶工廠的實作紀錄，以及裝機流程與原理，都可搜尋，工程師能查找類似案例。目前尚未納入現場照片與影像；下一步若把影像、設備狀態、處置與結果連起來，紀錄就能更完整。報告可供搜尋，不等於 AI 已學會操作，但能讓人找回經驗，再判斷是否適用。

## 模擬可以加速 現實仍須驗證

World Labs 正在推進訓練環境。公司於 2026 年 9 月介紹 Atlas，涵蓋空間重建、時空模擬及機器人 Real-to-Sim 工作流程；7 月也公布從真實任務建立模擬，再把訓練策略帶回實體機器人測試的成果。[6][7] 這些是公司公布的能力與結果，適用範圍仍須依任務與測試條件判斷。世界模型能提供表徵與模擬，操作仍需要感測、控制與執行系統。

無人機研究也提供例子。2023 年的 Swift 系統結合模擬訓練與實體飛行資料，校正誤差，再到真實賽道競賽。[8] 另有 2021 年研究，策略完全在模擬中訓練，再成功移轉到未參與訓練的真實環境。[9] 每一步訓練未必都在現場進行，但可靠性仍需要實際測試。

這很像新藥開發中的計算與濕實驗：模型提出候選與預測，實驗提供修正依據。2026 年一項分子發現研究，就把演算法設計、合成與生物測試接起來，依結果選擇下一輪方向。[10] 這裡沒有捷徑：不能只因推論合理，就省略實際效果的驗證；模擬與自動化可以加速這個過程。

## 保存經驗 也記得人的價值

這讓我重新思考個人 AI 的價值。它若能保存我遇過的案例、採取的措施與後續結果，就能減少重複猜測，幫我比較哪些假說已被否定、哪些仍缺證據。共通知識與個別歷史結合，下一次討論才更有依據。資料放在個人設備或私有環境，不會自動讓判斷更準確；仍須完整紀錄、適當檢索與持續修正。

我用 AI 做工具，學習與試錯變得容易；朋友與工程師的工作，則提醒我判斷必須接受結果的檢驗。我希望把兩種經驗接起來：更容易動手，也把成敗整理好，成為下一次可以查核、修正的依據。

有一次，朋友的太太去學跳舞，我看著一位烏克蘭女老師和一群好學的學生投入其中，感受到人的精神與藝能之美。那一刻，我暫時把 AI 拋在腦後，只是欣賞人們學習與表達的樣子。

這兩天讀《以弗所書》，「我們原是他的工作」（2:10）也讓我停下來想：當 AI 能完成更多工作，我是否仍習慣用產出與效率衡量人的價值？對我而言，信仰提醒我，人本身值得被珍惜。我更願意把 AI 用在幫助人學習、減輕辛苦的地方；工具越有能力，我也越需要分辨，誠實面對成果與限制，留意它會如何影響身邊的人。

經驗之所以珍貴，正因為它來自真實的人，在真實世界裡的嘗試與承擔。AI 可以幫我們把經驗記得更完整，但經驗的主人，始終是人。

## 參考來源

[1] AMD（2026 年 9 月 28 日）。AMD to Acquire World Labs to Advance the Future of AI Compute。[原文](https://ir.amd.com/news-events/press-releases/detail/1299/amd-to-acquire-world-labs-to-advance-the-future-of-ai-compute)

[2] Fei-Fei Li（2026 年 9 月 28 日）。To Seek a Newer World。[原文](https://drfeifei.substack.com/p/worldlabs-joining-amd)

[3] Polanyi, M.（2009，原著 1966）。The Tacit Dimension。University of Chicago Press。[原文](https://press.uchicago.edu/ucp/books/book/chicago/T/bo6035368)

[4] Whisker。Litter-Robot 4 Getting started。[原文](https://www.litter-robot.com/ca/support/article/litter-robot-4-getting-started/)

[5] Whisker。Litter-Robot 4 Drawer full indicator DFI sensors。[原文](https://www.litter-robot.com/eu/support/article/litter-robot-4-drawer-full-indicator-dfi-sensors/)

[6] World Labs（2026 年 9 月 1 日）。Atlas: A World Model for Spatial Intelligence。[原文](https://www.worldlabs.ai/blog/atlas)

[7] World Labs（2026 年 7 月 28 日）。Building Worlds That Train Robots。[原文](https://www.worldlabs.ai/blog/real-to-sim-to-real)

[8] Kaufmann, E., et al.（2023）。Champion-level drone racing using deep reinforcement learning.Nature, 620, 982–987。[原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10468397/)

[9] Loquercio, A., et al.（2021）。Learning High-Speed Flight in the Wild.Science Robotics, 6（59）, eabg5810。[原文](https://arxiv.org/abs/2110.05113)

[10] Piticari, A.-S., et al.（2026）。Algorithm-driven, phenotype-directed bioactive molecular discovery.Communications Chemistry, 9, 267。 [原文](https://www.nature.com/articles/s42004-026-02066-8)

## 延伸閱讀

Li, F.-F.（2025）。From Words to Worlds: Spatial Intelligence is AI’s Next Frontier。李飛飛闡述空間智慧與世界模型的完整構想。[ 原文](https://drfeifei.substack.com/p/from-words-to-worlds-spatial-intelligence)

Li, F.-F.（2023）。The Worlds I See: Curiosity, Exploration, and Discovery at the Dawn of AI.Flatiron Books。李飛飛的自傳，可了解她一路走向空間智慧的脈絡。

Sennett, R.（2008）。The Craftsman。Yale University Press。從工匠傳統談手與腦如何一起形成判斷。

Crawford, M. B.（2009）。Shop Class as Soulcraft。Penguin Press。一位哲學博士轉行修摩托車，反思實作工作中的知識與價值。

## 免責聲明

本文為作者個人經驗與觀點分享，不構成汽車維修、投資或任何專業建議。文中提及之公司與交易僅作為討論背景，並非投資推薦。有關 AI 能力的描述以公開資料為準，可能隨技術發展而改變。本文寫作過程使用 AI 工具協助整理與校對；文中經驗、照片與觀點均出自作者本人。

## 關鍵字

空間智慧、物理 AI、世界模型、World Labs、內隱知識、代理 AI、經驗紀錄、人機協作

## 關於作者

<strong>黃柏松（Sinclair Huang）</strong>，退休高階主管，現為顧問與獨立研究者，擁有台灣電子、化工與生技產業約 30 年跨領域經驗。HEC Liège 企業管理博士（EDBA），現任 Continental Carbon Co., Ltd. 董事長特別顧問。研究興趣涵蓋 AI 與半導體、產業競爭力與技術價值評估。

ORCID：[0009-0007-8173-5672](https://orcid.org/0009-0007-8173-5672)｜網站：[lab.sinclairhuang.org](https://lab.sinclairhuang.org/)

---

*本文原刊於 [Substack](https://sinclairhuang.substack.com/p/ai-1a5)。*