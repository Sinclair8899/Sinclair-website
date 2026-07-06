---
title: "The AI Capex Money Map v0.2 — America Spends. Who Actually Keeps the Margin?"
date: 2026-07-03
draft: false
tags: ["ai-capex", "semiconductors", "ai", "hbm", "cowos"]
description: "The AI Capex Money Map v0.2 — America Spends. Who Actually Keeps the Margin?From $650B to HBM, CoWoS and power — mapping who gets paid, who keeps margin, and when the bottlenecks move.Most people are "
canonical: "https://medium.com/@sinclairhuang/the-ai-capex-money-map-v0-2-america-spends-who-actually-keeps-the-margin-995fbcc60ea9?source=rss-1f713d63bb6a------2"
---

### The AI Capex Money Map v0.2 — America Spends. Who Actually Keeps the Margin?#### From $650B to HBM, CoWoS and power — mapping who gets paid, who keeps margin, and when the bottlenecks move.Most people are asking whether AI is a bubble. It is an important question, but not a very operational one.

A better one is:

****Of all the AI capex US hyperscalers are spending, whose revenue, whose margin, and whose moat does it actually end up in?****

This is not an investment-bank BOM model precise to every cable and connector. It is a public-data ****v0.2 map****. The goal is not false precision — it is to separate three things that usually get blurred together: ****where capex becomes revenue, where revenue becomes margin, and when the bottlenecks ease.**** Because the answer to each is rarely the same set of companies.

#### 1. AI capex is not one number — it is a set of pipesReuters, citing Bridgewater, estimates that Alphabet, Amazon, Meta and Microsoft will invest roughly ****US$650B**** in AI infrastructure in 2026, up from about US$410B in 2025. One clarification up front: this is the ****Big Four**** figure. It excludes Oracle, Stargate, neoclouds like CoreWeave, xAI, and every non-US operator. So $650B is a ****floor**** for four companies, not a whole-market total.

The money does not spread evenly. It splits into pipes with very different characteristics. This is the first mutually exclusive system layer (illustrative scenario, sums to 100%):

The key point: equipment and materials (ASML, AMAT, TEL, Advantest…) are ****not**** inside this $650B. That is TSMC’s and SK Hynix’s capex — second-order supplier spend, a different denominator. Adding it into hyperscaler spend is the double-counting error v0.1 made, and that many market charts still make.

#### 2. Open the box: the cost centre has moved from logic to HBM + packagingOpen the “Compute Systems” pipe, and you find the most counterintuitive structural shift of this cycle.

Using Epoch AI’s B200 BOM model as a reference: B200 variable manufacturing cost is roughly US$5,700–7,300 (central ~US$6,400), of which ****HBM + advanced packaging together account for about two-thirds.**** A clean 100% stack looks like this:

This chart answers an investment question, not an engineering one: ****when a hyperscaler pays for an accelerator, where do the physical dollars go?**** Nvidia captures IP and platform margin at the top — but the real dollars inside the box flow heavily to ****SK Hynix (HBM) and TSMC (packaging)****. “Who can ship an AI accelerator?” stopped being a logic-die question long ago; it is now a joint constraint of memory allocation, CoWoS, substrate and test.

#### 3. A detail most people skip: chip margin ≠ realised marginNvidia sits on the highest margin in the chain. True. But if you anchor to a single peak quarter, you get an overly rosy picture.

- FY2026 ****Q4**** GAAP / non-GAAP gross margin: ****75.0% / 75.2%****

- FY2026 ****full year****: ****71.1% / 71.3%****

- Epoch, taking a ~$30,000–40,000 sale price against a ~$6,400 build cost, implies a ****chip-level**** gross margin near 82% — but it also notes that most Blackwell revenue comes from server and rack-scale systems, so **** realised margin at the system level runs below the chip level.****

So “Nvidia’s margin is high” has to be said in three layers: chip, platform, system. That is the discipline of the whole map — ****revenue flows down the chain; margin does not. ****Standing where revenue passes through is not the same as keeping the margin.

#### 4. The bottleneck clock: not “is it scarce” but “when does it ease”The usual piece lists CoWoS, HBM, liquid cooling and power as bottlenecks. That is useless for investing. Useful research asks four more things: how tight now? Worsening or easing? Will the new supply be eaten by next-gen demand? And what happens to the margin when it eases?

****CoWoS / advanced packaging:**** TrendForce estimates TSMC’s 2026 monthly capacity could reach 120k–140k wafers; adding 50k–60k of new OSAT capacity, industry total could approach 200k/month, narrowing the supply-demand gap from ~20% toward 10%. But ****” gap narrowing” is not “bottleneck gone.”**** If Rubin / ASIC package area keeps growing, the constraint simply moves from wafer count to package area, yield and equipment — and the high end can stay tight into 2028–2029.

- ****HBM:**** SK Hynix says 2026 output is already sold out; a genuine bottleneck. But it is still memory — if the 2027–2028 expansion lands all at once, watch for a structural shortage reverting to a memory cycle. A counterintuitive signal worth stating plainly: in 2025, HBM share was ~61% SK Hynix, with ****Micron at ~21% now ahead of Samsung at ~17%.**** Same memory giants — yet qualification, yield and customer allocation created a gap wide enough that SK Hynix’s market value briefly passed Samsung’s. (Note: full-year snapshot; quarterly shares fluctuate.)

****Power / liquid cooling / site:**** the most underrated pipe, and the likeliest ****next**** bottleneck. The rack-power trajectory: legacy cloud 10–20kW → GB200 NVL72 ~120–132kW → 2027+ Rubin / Kyber scenarios of 300–700kW (the NVL576 “Kyber” rack is publicly discussed near ~600kW) → the industry already talks about 1MW-class. When per-rack power jumps an order of magnitude, the constraint migrates from chip and package outward to CDU, cold plate, UQD, HVDC, BBU, transformers, grid permits and construction. ****This is a deployment-speed bottleneck, not just a semiconductor-supply one.****

Bottlenecks migrate: chip → package → memory → power/site. Whoever bets on the **last** bottleneck often discovers they’re mispositioned exactly when it eases, and margin normalises.

#### 5. The real divide: revenue capture ≠ margin captureZoom out to the national level, and the same rule amplifies: ****the layer collecting the most revenue is not necessarily the one keeping the most margin.****

In Taiwan, that is not an abstraction — it is a gross-margin staircase visible on Q1 2026 filings. All four of these companies stand at the collection point of the same Nvidia-driven capex flow: TSMC’s Q1 gross margin was 66.2%; liquid-cooling leader AVC posted a record 29.77% (server + networking now ~66.4% of revenue); Hon Hai 6.2%; Quanta 4.78%. ****The same hyperscaler dollar passes through four companies, and the margin retained differs by more than an order of magnitude**** (66.2% vs 4.78% — roughly 14×).

The gap is not effort; it is the physics of the business model. A full AI rack now carries a seven-figure USD price tag, and under the electronics industry’s buy-and-sell rules, the ODM pays out of its own pocket for the most expensive silicon in the box — GPUs, HBM — then assembles, ships, and waits for acceptance before collecting. The better business gets, the more cash it consumes: ****exploding revenue and strained operating cash flow are two faces of the same model.****

How real is the strain? Watch what the companies themselves are doing, not what any analyst says. On its Q1 2026 call, Quanta said it is negotiating with customers to shift new projects to a ****consignment model — customers supplying the key components — explicitly “to relieve operating cash and gross margin” pressure.**** Hon Hai’s 6.2% Q1 margin was itself helped by some server programs already running on consignment. Wistron is planning a rights issue / GDR of up to 250 million shares, earmarked for overseas procurement, working capital, and bank-loan repayment. ****When an industry starts collectively rewriting its transaction model and tapping capital markets for working capital, that tells you more honestly than any spreadsheet: the money flows through here — it does not stay here.****

One more ground-level detail from the same quarter shows how platform-transition risk surfaces in Taiwan first: NVIDIA revised Rubin’s vapour-chamber cooling (from a dual-piece to a single-piece design), which rattled Taiwan thermal names (Jentech hit limit-down). Hon Hai flagged the cooling-design change as a shipment-cadence item ****to monitor**** — though FII said at Computex that Rubin remains on track for H2 2026, so treat this as a cadence risk, not a confirmed delay. The point is not whether one quarter slips: it is that ****a single component redesign can move an entire rack’s schedule**** — the on-the-ground version of the Bottleneck Clock’s “server/rack integration is tightest during platform transitions,” and why suppliers concentrated in a single spec react so violently to a single design-change rumour.

**(The margin, consignment and financing details above come from Q1 2026 filings and earnings calls. The Rubin cooling-design item is treated here through market reporting and company responses: a cadence risk to monitor, not a confirmed delay.)**

#### 6. The disaggregation signal: ASIC and the re-pricing of MediaTekIf you want one case to test the whole map, take a custom ASIC.

Counterpoint projects MediaTek could take ~****26% of AI ASIC server-compute shipments by 2028, near 5 million units**** — second only to Broadcom, roughly a tenfold jump from ~400k units in 2026. The market is re-pricing MediaTek not for the letters “AI,” but for a chain of assumptions that ****must be validated****:

1. AI ASIC is not a Broadcom-only turnkey business;

2. Hyperscalers are willing to unbundle compute die, I/O, HBM procurement and packaging integration;

3. MediaTek’s role is more than an I/O die — per Google Cloud Next 2026 coverage, Google split its eighth-generation TPU into two architectures, with ****Broadcom leading the training variant (TPU 8t “Sunfish”) and MediaTek the inference variant (TPU 8i “Zebrafish”)****, while supply-chain reports point to a second US CSP program whose customer remains unconfirmed;

4. This is not a one-off design service but a custom-silicon platform with generational continuity and margin stickiness;

5. CoWoS / HBM / TSMC allocation can support the shipment curve.

But here is the non-consensus risk, and it maps straight back to the US column in Section 5: ****if Google keeps pulling more design and HBM-procurement control in-house, one goal may be to strip out middleman markup.**** That would stress-test Broadcom’s turnkey margin — the market reads Google’s TPU supply-chain split as a weakening of sole-supplier economics — and it is a double-edged sword for MediaTek. You may win the volume and a design role, but if the customer captures the procurement and integration spread itself, the ****” durable margin” assumption deserves a question mark.**** The market is pricing units; what you should watch is margin and customer concentration.

By mid-2026, the assumption chain has started producing checkable readings — and the three layers of evidence carry different weight, worth keeping separate:

****Company-confirmed (hardest):**** on its Q1 call, MediaTek ****doubled its 2026 AI ASIC revenue guidance from US$1B to ~US$2B**** (first hyperscaler program ~$2B landing in Q4 2026), said a second program is targeted for production by end-2027, and put its cloud-ASIC TAM at ~US$70–80B by 2027 with a 10–15% share target. When a business goes from “story” to “explicit guidance,” that is management’s own stamp.

****Supply-chain-visible (next):**** sell-side capacity work on ASE points to ****MediaTek’s TPU v8 and Amazon’s Trainium 3 ramping meaningfully in final test next year**** — the validation signal surfacing, as this piece argued it would, in Taiwan’s packaging-and-test scheduling before it surfaces in a US analyst report.

****Sell-side re-modelling (reference, not fact):**** sell-side numbers moved up through 2026 (a verifiable Goldman note from April modelled 2027 AI-ASIC revenue ≈ US$12.3B, ~39% of revenue). More bullish 2027/2028 figures circulating in the market (≈US$20B/US$52B, 49%/69% of revenue) ****could not be independently verified against a primary July note and should be treated as sell-side chatter, not fact.**** A Street high-end target near NT$10,000 exists (broker estimate; specific attribution unconfirmed). These are estimates, not evidence; what they pin down is **which set of assumptions the market is now pricing.**

And on the margin line, even the bulls concede the point: sell-side generally models the next-generation program’s ASP higher but gross margin ****” roughly maintained”**** — i.e. cost pass-through, not expansion — with at least one broker calling it ****slightly gross-margin dilutive****, and operating leverage doing the work. In other words — ****the volume story is being confirmed; the margin story is still sitting the exam.**** That is precisely the cell of this money map you keep watching.

#### 7. In the last week of June, the whole story rehearsed itself in TaipeiStart with temperature. On the same MediaTek, you can read three different thermometers in Taipei at once. Foreign brokers are building assumption-chain models and raising targets. Front-line analysts on local finance shows mostly call the five-digit target “impossible” — not because they are bearish, but because ASIC competition is crowded: unless MediaTek genuinely takes Broadcom-class high-value orders, or its design capability and cost structure both clear the bar, these remain high-uncertainty assumptions. And in the same week, MediaTek became not only an analyst-model story but a retail-attention story: a local influencer’s **one-lot** trade made national news. That matters less as a trading anecdote than as a signal — ****when a stock becomes entertainment news, part of the price is no longer money flow; it is amplification.****

Then, the last week of June staged my deepest doubt about this story, live. The link I trust least has never been on the supply side — it is at the far end of the loop: ****somebody has to pay at the end of a price-hike chain.**** On June 25, multiple outlets reported that Apple, citing memory and storage cost inflation, raised Mac/iPad prices (~11–36%), with Apple quoted as having “never seen component prices rise so much in so short a time.” This matters less because of Apple itself than because it exposes the ****end**** of the supply-chain price hike: even the strongest brand cannot absorb every upstream cost dollar indefinitely. The next day, the market repriced that risk chain: the Taiex fell 1,683 points (third-largest single-day point drop on record), foreign investors sold ~NT$143B in one session, and MediaTek itself hit limit-down (3,880). ****That basic economic loop does not stop applying because the theme is called AI — and the first row it strikes back at is the market cap of the AI supply chain itself.****

The second half of the week is just as worth recording: five days later the market rebounded, the influencer exited with a ~NT$460k profit, and the day after that, a foreign broker raised MediaTek’s target again. On the way down, Taiwan’s heavily ETF-ized passive bid and dip-buying caught the fall; on the way up, narrative did the lifting. ****Part of today’s price is money flow; part of it is dream. The whole point of this map is to help you separate the two.****

One honest closing note: the counter-signal to assumption five (that capacity can support the shipment curve) — concrete crowding-out between ASIC programs and Nvidia orders at the packaging-and-test layer — is something I have **not** yet heard on the ground. That may mean allocation still has slack, or that the signal simply hasn’t surfaced. I treat it as an alarm clock that hasn’t rung: the day it does is the day this story moves from “volume being confirmed” to “capacity and margin grinding against each other.”

#### 8. Instead of guessing direction, build a tracking disciplineThis map does not hand you a “what to buy.” It hands you a set of indicators to keep updating:

- ****CoWoS:**** TSMC monthly capacity, OSAT ramp, package area, yield, equipment lead time.

- ****HBM:**** pricing, long-term agreements, stack mix, SK/Samsung/Micron capex each, DRAM/NAND displacement.

- ****Power/site:**** transformer lead time, HVDC/BBU adoption, grid permits, construction progress.

- ****Server/rack:**** shipments, burn-in test time, ODM margin, inventory, customer concentration.

- ****ASIC:**** Google TPU, Meta MTIA, AWS Trainium volumes, and the Broadcom / MediaTek / Marvell pipeline.

Only one rule: ****keep what a vendor says (“sold out,” “in volume”) separate from what a filing confirms.**** The first is direction; only the second is evidence.

#### Appendix: Regional Margin Capture MapThe piece is called a Money Map, so it should close on a summary of national margin capture. America spends, and Asia builds — but the margin each region retains is completely different:

One line: **** This map is not a stock list. It tells you whether a company stands at the collection point or merely next to the market’s amplifier.****

#### Conclusion: money flow doesn’t lie; bottlenecks decide who keeps the marginAI FOMO isn’t necessarily wrong. But long-run returns aren’t decided by buying the letters “AI” — they’re decided by whether the company you back stands at the ****collection point**** of this capex flow, or merely next to the market’s ****amplifier.****

&gt; ****Money flow doesn’t lie. Bottlenecks decide who actually keeps the margin.****

****Model boundary:**** This is not a full investment-bank BOM model down to every cable, connector or construction material. It is a public-data v0.2 map of AI capex flows, margin capture and bottleneck timing. The goal is not false precision — it is to avoid double counting, separate direct hyperscaler spend from second-order supplier capex, and ask which layers actually retain margin.

#### Author**Sinclair Huang**

Research notes on AI infrastructure, semiconductors, supply chains, and technology strategy.

#### References / Data Anchors1. [Bridgewater Associates](https://www.bridgewater.com/understanding-ais-more-dangerous-phase-content-ctd) — US Big Four 2026 AI infrastructure investment expected around US$650B versus US$410B in 2025.

2. [Epoch AI](https://epoch.ai/data-insights/b200-cost-breakdown) — B200 variable manufacturing cost estimate and HBM + advanced packaging cost share.

3. [NVIDIA](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026) — FY2026 revenue and gross-margin disclosures.

4. [TrendForce](https://www.trendforce.com/news/2026/06/15/news-tsmc-cowos-supply-demand-gap-reportedly-seen-narrowing-from-20-to-10-by-end-2026-as-capacity-expands/) — TSMC CoWoS capacity and supply-demand-gap estimates.

5. [Counterpoint Research](https://counterpointresearch.com/en/insights/MediaTek-to-Contribute-1-in-4-AI-ASIC-Server-Compute-Shipments-in-2028) — MediaTek AI ASIC server-compute shipment forecast.

6. [TSMC Investor Relations](https://investor.tsmc.com/english/quarterly-results/2026/q1) — Q1 2026 gross margin and quarterly results.

7. [Google Cloud](https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive) / industry coverage — TPU 8t and TPU 8i architecture split.

8. Public company filings, earnings calls, and market reporting for Taiwan ODM, thermal, ASIC, and market-data sections.

**Data / Source Notes (14 items) and an Extended Source Log (21 items) are maintained with the working draft; the Chinese full version is published on Substack / Vocus (方格子).**

#### Further Reading / Tracking List- CoWoS: TSMC monthly capacity, OSAT ramp, package area, yield, equipment lead time.

- HBM: pricing, long-term agreements, stack mix, SK Hynix / Samsung / Micron capex, DRAM / NAND displacement.

- Power/site: transformer lead time, HVDC / BBU adoption, grid permits, construction progress.

- Server/rack: ODM margin, burn-in test time, inventory, customer concentration, consignment share.

- ASIC: Google TPU, AWS Trainium, Meta MTIA, and the Broadcom / MediaTek / Marvell pipeline.

#### DisclaimerThis is research and industry analysis, not investment advice. Figures are drawn from public data, industry reports, media reporting and v0.2 directional estimates, and should be continuously updated against filings, monthly revenue, earnings calls, orders, pricing, lead times, gross margin and capacity progress. Items marked as sell-side estimates or unverified should be treated as estimates, not facts.

#### Hashtags#AI #Semiconductors #AICapex #HBM #CoWoS #TSMC #MediaTek #Nvidia #SupplyChain #Taiwan #ASIC #DataCenters #Investing

---

*This article was originally published on Medium. [Read the full version with charts and figures →](https://medium.com/@sinclairhuang/the-ai-capex-money-map-v0-2-america-spends-who-actually-keeps-the-margin-995fbcc60ea9?source=rss-1f713d63bb6a------2)*