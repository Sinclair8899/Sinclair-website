---
title: "Everyone Is Counting Tokens. Watch the Bandwidth That Gets Paid"
date: 2026-07-21
draft: false
tags: ["market-structure", "economics", "ai", "semiconductors", "investing"]
description: "AI will be everywhere. The harder question is who still earns a margin when intelligence gets cheap.By SinclairI have watched AI move from conversation and search into data processing, automation, veh"
canonical: "https://medium.com/@sinclairhuang/everyone-is-counting-tokens-watch-the-bandwidth-that-gets-paid-2578c9af3ce4?source=rss-1f713d63bb6a------2"
---

*AI will be everywhere. The harder question is who still earns a margin when intelligence gets cheap.*

By Sinclair

I have watched AI move from conversation and search into data processing, automation, vehicles, robots, industrial tools, and factories. That makes me sceptical of debates that begin with **whether AI demand will exist**. Much of the eventual demand will not look like a deliberate purchase of “AI.” Intelligence will be built into a product or workflow, and the customer will pay for the outcome.

The harder question is economic.

When a cloud company talks about leasing capacity, investors hear oversupply. When a cheaper model appears, they hear that expensive models — and the hardware behind them — may be obsolete. Yet AI can become more useful while its unit price falls. Usage can rise while margins migrate.

From Taiwan, that tension is easier to see. A U.S. capex announcement becomes a packaging slot, an HBM qualification schedule, a substrate-yield problem, a rack-level cooling test, and a working-capital requirement at an ODM. Wall Street sees a capex number. Taiwan sees an engineering queue.

**The core idea:** AI adoption can keep expanding while today’s hardware margins decay. The useful question is what allows each supplier to keep saying “no,” and how long that advantage can last.

#### Three questions behind the AI trade

Behind most AI-infrastructure valuations is one bet: today’s spending wave will produce cash flow that survives competition and normalisation. I reduce that bet to three questions:

- **Demand durability:** How much usage is paid, at what margin, and does it grow quickly enough to offset efficiency and price compression?

- **Cost trajectory:** Does the bottleneck remain scarce, or do capacity and technical improvement remove it?

- **Capture position:** When scarcity eases, which layer keeps the difference between price and cost?

I focus most closely on cost trajectory because it links the other two. It sets the growth hurdle paid demand must clear and affects who can still defend margin when scarcity fades.

#### The half-life of a “no”

In a constrained market, pricing power usually sits with the supplier customers still cannot replace. The question is not simply whether that supplier looks expensive. It is what allows the supplier to refuse lower prices or easier terms — and how long that ability can last.

I call this the **half-life of a “no.”**

A supplier can say no for three different reasons:

1. **Capacity scarcity.** There is not enough physical supply. The resulting margin is cyclical and should eventually mean-revert.

2. **Qualification friction.** An alternative exists, but the customer cannot use it immediately. Validation, reliability work, yield improvement, and system integration can take quarters.

3. **Embedded capability.** The advantage comes from process knowledge, formulation, accumulated learning, or customer co-development that competitors cannot reproduce quickly.

**CoWoS at TSMC** is mainly capacity-backed. Replication still requires specialised tools, process integration, yield learning, and customer qualification.[1] **HBM at SK hynix** is more qualification-backed: a replacement must pass inside a specific system’s performance, power, thermal, reliability, and yield envelope.[3] **Ajinomoto’s ABF film** is closer to capability-backed. The company reports a share above 95%, customer-specific co-development, and greater material use in larger AI package substrates.[4]

#### Taiwan is an engineering loop, not a supplier list

Taiwan’s advantage is often described as geographic concentration. The more important advantage is iteration time.

A package that misses its thermal or warpage target may require changes in substrate construction, material formulation, assembly, cooling, firmware, or rack operation. In a linear chain, every handoff becomes a contract boundary. In Taiwan’s AI-hardware ecosystem, many of those handoffs behave more like a continuous debugging loop.

TSMC has emphasised the close R&amp;D–operations collaboration required during early leading-edge ramps in Taiwan.[2] Ajinomoto describes customer-specific development and in-house reproduction of customer processes, including warpage inspection.[4] Wiwynn describes compute, storage, interconnect, and cooling as a rack-scale system designed together.[5]

The customer is not buying a GPU, a cold plate, and a board separately. It is buying a qualified system that has survived their interaction.

That loop has a financial cost. The integrator may have to fund expensive components, carry work-in-process through validation, and collect only after delivery. If inventory and receivables grow faster than gross profit, revenue can rise while free-cash-flow conversion and ROIC weaken.

System responsibility matters too. At rack-level power densities, a liquid-cooling or integration failure can damage assets worth far more than the failed component. Suppliers able to validate, trace, service, and carry system-level responsibility are harder to replace. Unpriced liability, however, is not a moat. It is a hidden cost.

#### What “paid bandwidth” is trying to measure

At GPT-3.5-equivalent capability, advertised inference prices fell more than 280 times between November 2022 and October 2024. Hardware price-performance improved by roughly 30% per year, so model efficiency, serving optimisation, utilisation, and competition also mattered.[6]

Cheaper intelligence can create far more usage — the Jevons mechanism. It also forces every layer of the supply chain to compete harder for margin.

A recent scenario paper proposes **dollars per petabyte moved through the memory subsystem ($/PB)** as one way to compare serving economics.[7] I use “paid bandwidth” as shorthand for monetised memory traffic. The metric is imperfect, but the question behind it is useful:

**Is monetised traffic growing faster than the profit earned on each unit of traffic is shrinking?**

If the answer is yes, aggregate economics can improve even as unit prices fall. If the answer is no, usage may still rise while the infrastructure growth premium compresses.

Taiwan shows why the formula cannot stop at the chip. Memory traffic becomes cash flow only after the system is packaged, powered, cooled, qualified, delivered, and financed. Revenue passage is not the same as value capture.

#### A practical way to stay sane

I would not call the turn from one headline. I would look for confirmation across a small set of signals:

- margins relative to the through-cycle baseline;

- lead times, allocation language, and usable second sources;

- packaging yield, substrate warpage, rack burn-in, and cooling reliability;

- inventory, receivables, customer deposits, and operating cash conversion;

- whether monetised traffic is expanding faster than unit economics compress.

There is an important limitation: I am not aware of a major public operator that reports monetised PB as a standard filing metric. It has to be estimated. That is not a weakness to hide. It is the work.

The serious break occurs when two things fail together: the supplier’s ability to say no weakens and aggregate operating contribution contracts.

This is a way to stay sane in a market where everyone watches the same tickers for different reasons. AI is likely to become cheaper, more capable, and more widely embedded. None of that guarantees that today’s infrastructure margins are permanent.

From New York, the cycle looks like capex. From Taiwan, it looks like queues, yield, thermal budgets, qualification, liability, and cash conversion. Those are the variables that reveal whether a “no” is holding or decaying.

#### Author

Po-Sung (Sinclair) Huang

Independent researcher focused on AI infrastructure economics, semiconductor value chains, and market structure.

His work sits at the intersection of industrial organisation, technology cycles, and financial markets — with a focus on identifying where value actually accrues as new technological regimes form.

**Disclaimer and disclosure**

This essay is analytical and educational, not a recommendation to buy or sell any security. The author may hold, trade, establish, reduce, or close positions in securities or industries discussed; positions may change without notice, and this is not a real-time position report. Any material commercial relationship directly relevant to this article will be disclosed where applicable. The Taiwan-side observations rely on public filings, company materials, and industry reporting — not confidential supplier information—data and source cut-off: 21 July 2026.

#### Further reading

– Stanford HAI — AI Index Report 2025 
– Deloitte — TMT Predictions 2026 (AI compute outlook) 
– Matsuoka (2026) — Memory Scarcity &amp; AI Industry Structure (arXiv) 
– TSMC 20-F / SK Hynix disclosures (for supply-side signals)

*For the full research version, including the valuation bridge, model-vintage analysis, decision tree, and monitoring framework, see the Substack edition on *[https://open.substack.com/pub/sinclairhuang/p/everyone-is-counting-tokens-watch?r=2focqg&amp;utm_campaign=post&amp;utm_medium=web&amp;showWelcomeOnShare=true](https://open.substack.com/pub/sinclairhuang/p/everyone-is-counting-tokens-watch?r=2focqg&amp;utm_campaign=post&amp;utm_medium=web&amp;showWelcomeOnShare=true)

**Related research: [The Architecture of Leverage](https://ssrn.com/abstract=6504361) develops the Irreplaceability Index; [The Mid-2026 Semiconductor Correction](https://ssrn.com/abstract=7013899) applies IRI, ECDR, and gross margin to Micron; and [Infrastructure-Led Leading Indicators](https://ssrn.com/abstract=6285318) develops the Equipment-CapEx Divergence Ratio.**

### Sources

1. Moore Morris, [“TSMC’s CoWoS capacity,” *Nomad Semi*](https://www.nomadsemi.com/p/tsmcs-cowos-capacity); TSMC, [*2025 Form 20-F*](https://investor.tsmc.com/sites/ir/sec-filings/2025_20F%20Report.pdf), Note 22(c).

2. Reuters, [TSMC on multi-year AI demand and Taiwan-based leading-edge collaboration](https://www.reuters.com/world/asia-pacific/tsmc-expects-strong-multi-year-demand-ai-chips-it-ramps-up-arizona-investment-2026-07-19/) and [Chiayi advanced-packaging expansion](https://www.reuters.com/world/asia-pacific/tsmc-add-2-advanced-chip-packaging-plants-chiayi-taiwan-minister-says-2026-07-13/).

3. SK hynix, [“Rulebreakers’ Revolutions: Design Scheme Elevates HBM3E”](https://news.skhynix.com/rulebreakers-revolutions-design-scheme-elevates-hbm3e/); Reuters, [Samsung HBM3E qualification update](https://www.reuters.com/technology/samsung-posts-weaker-profit-recovery-it-misses-out-ai-boom-2024-10-30/).

4. Ajinomoto, [*Growth Strategy for the Electronic Materials Business*](https://www.ajinomoto.co.jp/company/en/ir/event/business_briefing/main/011117/teaserItems1/01/linkList/03/link/20260630_presentation_E.pdf); [Build-up Film Innovation Story](https://www.ajinomoto.com/innovation/our_innovation/buildupfilm).

5. Wiwynn, [*2024 Annual Report*](https://www.wiwynn.com/hubfs/Investors/Shareholders_Services/2025_Annual_Report_EN.pdf) and [COMPUTEX 2026 recap](https://www.wiwynn.com/news/recap-of-wiwynn-at-computex-2026-scaling-the-ai-future).

6. Stanford HAI, [*2025 AI Index Report*](https://hai.stanford.edu/ai-index/2025-ai-index-report).

7. Satoshi Matsuoka, [*Memory Scarcity, Open Models, and the Restructuring of the AI Industry, 2026–2030*](https://arxiv.org/abs/2607.07207). Non-peer-reviewed scenario paper; numerical outputs are not observed market facts.

#### HashTags

#AI #Semiconductors #Investing #Economics #MarketStructure

---

*This article was originally published on Medium. [Read the full version with charts and figures →](https://medium.com/@sinclairhuang/everyone-is-counting-tokens-watch-the-bandwidth-that-gets-paid-2578c9af3ce4?source=rss-1f713d63bb6a------2)*