---
title: "Everyone Wants the Next AI Stock. I’m Looking for the Next Physical Bottleneck."
date: 2026-06-10
draft: false
tags: ["cowos", "semiconductors", "hbm", "data-center", "ai-infrastructure"]
description: "From “What’s the next AI stock?” to “Where’s the next bottleneck, who gets paid, and what would prove us wrong?”Sinclair HuangThis essay helps answer four practical questions:- Which AI themes are rea"
canonical: "https://medium.com/@sinclairhuang/everyone-wants-the-next-ai-stock-im-looking-for-the-next-physical-bottleneck-f75737995b64?source=rss-1f713d63bb6a------2"
---

From “What’s the next AI stock?” to “Where’s the next bottleneck, who gets paid, and what would prove us wrong?”

Sinclair Huang

#### This essay helps answer four practical questions:*- Which AI themes are real constraints rather than just attractive stories?*

*- Who can capture gross margin when a constraint binds?*

*- How long might the bottleneck last before capacity, substitution, or efficiency relieves it?*

*- What evidence would prove the thesis wrong?*

The main argument: ****large AI demand explains why the sector is hot; bottlenecks explain who gets paid; spillovers explain who absorbs hidden costs; monetised usage determines whether the buildout is sustainable.****

#### How to use this essay as an investor1. Start with ****Table 1**** and locate the AI theme you care about.

2. Use ****Table 2**** to score it roughly as high/medium/low across the five axes.

3. Use ****Table 7**** to decide which metrics you should actually track.

4. Write down one validation signal and one falsification trigger before adding exposure.

5. If you cannot name the bottleneck, margin-capture mechanism, or kill signal, you may be holding a story rather than a thesis.

#### Author noteThis essay is not a stock-picking note, and it is written in a personal capacity. It is a framework for asking better questions in an AI market increasingly driven by capital expenditure, sovereign competition, compute scarcity, memory shortages, power constraints, consumer AI monetisation, and the financialization of compute.

The goal is simple:

****Do not only ask: “What is the next AI stock?”**

**Ask: “Where is the next bottleneck, who can monetise it, and what evidence would prove us wrong?”****

This article is built from three companion technical verification tables: HBM3E, CoWoS, and process-node verification. The full technical tables are included in the appendix package. The main text uses their conclusions without overloading the reader with engineering detail.

#### 1. Everyone wants the next AI stockOver the past few weeks, I have noticed something very human in several investor groups.

Many people in these groups are highly educated, experienced, and successful. Some were senior executives. They are not uninformed people.

But when the market moves violently, and when every AI-related name seems to attract another bullish argument, most people do not want to hear about process nodes, SRAM bit-cells, CoWoS yield, HBM thermal limits, or power density.

They want to ask one simple question:

****What should I buy next?****

I understand that. Everyone wants to make money. Nobody wants to be the person who missed the AI boom.

But in AI infrastructure, I believe the better question is not only:

****Which stock will go up next?****

The better question is:

****Where is the next physical bottleneck?****

Because in this cycle, demand is only the first layer of the story. The deeper question is where that demand gets trapped — and who has the ability to convert that bottleneck into margin, pricing power, and durable profits.

A note on the word **physical**. I lead with physical bottlenecks because they are the easiest to verify: you can measure yield, lead times, transformer queues, and power. But the same discipline applies to constraints that are not physical at all — monetisation, market structure, and platform distribution. The test never changes. Is the constraint real? Who captures it, and what evidence would prove the thesis wrong?

#### 2. The demand stack is realThis section answers where the demand is coming from before asking who can actually monetise it.

The AI infrastructure cycle is not built on nothing.

The demand pull is real — and it is no longer only corporate. It is becoming a stack.

*Layer 1: U.S. hyperscaler capex*

The first layer is U.S. hyperscaler capex. Microsoft, Google, Amazon, Meta, OpenAI’s ecosystem, and other AI infrastructure buyers are committing enormous sums to data centres, GPUs, custom ASICs, networking, HBM, cooling, and power.

Goldman Sachs’ baseline model estimates ****$765 billion in annual AI capex in 2026****, growing to ****$1.6 trillion in annual AI capex by 2031****, with roughly ****$7.6 trillion of cumulative capex from 2026 to 2031**** (as of the May 2026 version of Goldman’s build-out model; these figures are revised across editions). Goldman frames this as an infrastructure estimate implied by accelerator deployment, data centres, power, and supporting systems — not as a guarantee of end-market demand.[^goldman]

*Layer 2: China sovereign AI capex*

The second layer is sovereign AI capex.

Reuters, citing Bloomberg News, reported that China is preparing a plan worth around ****RMB 2 trillion****, or about ****$295 billion****, over five years to build a nationwide network of AI-focused data centres. The plan is expected to involve key government agencies, state-owned telecom operators such as China Mobile and China Telecom, and a domestic-first supply chain with suppliers such as Huawei providing at least 80% of key AI-related technologies.[^china-295]

Two details matter.

First, this is still a reported plan based on people familiar with the matter, not an officially confirmed spending program. Second, the headline ****RMB 2 trillion**** figure reportedly does ****not**** include private AI spending by firms such as Alibaba and Tencent. If China integrates power-grid infrastructure into the project, reported estimates suggest the total projected investment could reach at least ****RMB 5 trillion****.[^china-5t]

That second point strengthens the main argument of this essay: once power infrastructure is included, capex becomes much larger — and the bottleneck map becomes more important.

China's sovereign AI compute is not merely another source of demand. It is a different bottleneck map.

In the U.S.-led stack, the main constraints are often Nvidia GPUs, custom ASICs, HBM, CoWoS, power, cooling, and networking.

In China’s sovereign stack, the constraints shift toward domestic AI accelerators, SMIC-linked manufacturing capacity, memory bandwidth, software ecosystem maturity, national compute scheduling, and utilisation.

*Layer 3: frontier AGI roadmaps*

The third layer is frontier AI demand.

OpenAI’s latest plan says the company is entering its “third phase,” with goals that include building an automated AI researcher, accelerating the economy through scientific and productivity gains, and giving everyone on Earth a personal AGI. OpenAI says its internal belief is that by March 2028, a significant fraction of its research may be done by AI systems working alongside human researchers.[^openai-plan]

OpenAI has also confirmed a confidential draft S-1 submission to the SEC, while noting that it has not decided on IPO timing and that it “may be a while” before further action.[^openai-s1]

This strengthens the long-term compute-demand narrative. If AI systems can meaningfully accelerate AI research itself, compute demand may not grow only with human user adoption; it may also grow with AI-driven R&amp;D loops.

But this also raises the monetisation bar.

A world where everyone has a personal AGI requires not only better models, but affordable inference, high utilisation, and a business model that can pay for the infrastructure.

*Layer 4: consumer AI platforms*

The fourth layer is consumer AI.

Apple’s WWDC 2026 is important because it moves AI from cloud dashboards and enterprise pilots into everyday consumer devices. Apple announced the next generation of Apple Intelligence and Siri AI across iPhone, iPad, Mac, Apple Watch, AirPods, and Vision Pro. Apple’s materials describe a privacy-first architecture using on-device processing and Private Cloud Compute.[^apple-ai]

Apple also says some Apple Intelligence features have daily usage limits because they rely on powerful server models, while most iCloud+ plans provide increased access.[^apple-ai2]

That is a monetisation signal.

Consumer AI is not only a feature cycle. It is a test of whether platform companies can turn AI into hardware upgrades, services revenue, and ecosystem lock-in.

#### 3. But capex is not the same as monetised demandThis section separates infrastructure spending from paid usage — the difference between building compute and earning an economic return on it.

There is one bottleneck investors should not ignore.

It is not a physical bottleneck.

It is the ****monetisation bottleneck****.

The AI infrastructure bull case starts with capex: hyperscalers, model companies, cloud providers, and now governments are committing enormous sums to data centres, GPUs, networking, power, and cooling.

But infrastructure spending is not the same as sustainable end demand.

At some point, the compute being built has to be paid for by customers who use AI enough and get enough measurable value from it to justify the token bills.

That is where the debate becomes harder.

Bain &amp; Company’s 2025 Global Technology Report estimated that sustaining AI’s scaling trend could require about ****$2 trillion in annual revenue by 2030****. Even with AI-related savings, Bain estimated an ****$800 billion annual revenue gap****, and it also framed the problem as one involving about ****$500 billion of annual data-centre capex**** by 2030.[^bain]

This is the pressure point that AI skeptics such as Ed Zitron emphasise. His argument is not simply that AI is useless. It is that the infrastructure being built requires extremely fast revenue growth from AI software, model usage, and compute customers — growth that may be difficult to achieve if enterprises begin to control token spending more tightly.[^zitron]

There is already evidence of this tension. Reuters Breakingviews recently described a “tokenmaxxing” problem inside corporations: usage-based AI pricing can make IT budgets volatile and hard to justify. The article discussed companies starting to restrain AI usage as costs rise and ROI remains uncertain.[^reuters-token]

There is also a counterforce: algorithmic efficiency. Google DeepMind’s AlphaEvolve is a Gemini-powered coding agent for algorithm discovery and optimisation. DeepMind says AlphaEvolve has been applied to computational infrastructure, data-centre scheduling, accelerator circuit simplification, and LLM training.[^alphaevolve]

That matters because better algorithms can reduce the cost per task. But efficiency gains do not automatically solve the monetisation problem. They change the slope of the curve.

Taken together, these reports say: CapEx can outrun revenue unless pricing, ROI, utilisation, and efficiency all line up.

This does not mean AI adoption will stop.

But it does mean:

****Token usage is not automatically profitable demand.****

For AI infrastructure to be sustainable, the equation is not only:

****More capex → more compute****

It must eventually become:

****Paid usage × willingness to pay × gross margin per token × utilization &gt; capex burden****

That is the economic bottleneck behind the physical bottlenecks.

The right debate is not simply “AI boom or AI bubble.”

The better question is:

****Can paid AI usage grow fast enough to absorb the infrastructure being built?****

#### 4. Big demand is not the same as durable profitThis section turns the demand story into a constraint map: which parts of the chain can actually capture margin, and which parts merely absorb cost.

A huge capex cycle can lift an entire supply chain.

But it does not lift every segment equally.

Some companies capture margin. Some only pass through volume. Some own scarce technology. Some simply ride a theme. Some bottlenecks last for years. Some disappear once capacity arrives.

This is where technical reality becomes useful.

The market often treats AI infrastructure as one big trade. In reality, AI infrastructure is a chain of rotating bottlenecks.

And a bottleneck does not only create winners. When a constraint binds, its cost spills into adjacent markets, into downstream devices, and eventually onto end customers and policymakers. I call this ****bottleneck spillover****, and together with one companion idea — ****announced capacity is not effective capacity**** — it forms the spine of this essay. A bound constraint rarely stays contained, and headline capacity rarely equals deliverable output. Case 1 is the worked example of the first idea; Case 2 is the second.

Each of these can be part of the AI story.

But they are not equal.

The investor’s job is not to chase every AI-related label. The better job is to ask:

1. Is this a real bottleneck?

2. Can the company or segment capture margin from it?

3. How long will the bottleneck last?

4. Can the claim be verified?

5. What evidence would prove the thesis wrong?

6. Is the market already pricing a temporary shortage as a permanent advantage?

#### 5. A bottleneck map is better than a stock tipThis section gives the reusable checklist. It is designed to help readers compare AI themes without pretending that a simple score can predict stock prices.

A stock tip tells you what to buy.

A bottleneck map tells you why the profit pool exists.

That is the real goal.

Not “HBM is good.” Not “CoWoS is good.” Not “power is good.” Not “2nm is good.”

The better question is:

****What is the testable bottleneck thesis?****

If a thesis cannot be validated or falsified, it is just another narrative.

So I use a five-axis rubric.

These five axes are chosen because they map cleanly to P&amp;L and time: how large the demand is, whether the segment actually constrains the system, who captures gross margin, how long the constraint may last, and how observable the claim is.

This is a rubric, not a multiplication model. I do ****not**** multiply ordinal scores or treat them as independent variables. The purpose is to force discipline and make assumptions visible.

Two notes are important.

First, ****Demand Pull is 5/5 in every worked case by design****. This article starts with AI themes where demand is visibly large. Demand is the entry ticket. The real discrimination comes from the other four axes: constraint severity, margin capture, duration, and verification confidence.

Second, ****Verification Confidence means inspectability, not truth****. A 5/5 score means there are multiple observable metrics that can be tracked. It does not mean every vendor claim has already been verified as true.

The framework is useful for one thing:

***Separating real profit pools from AI labels.****

I deliberately avoid a single composite score. The point is to force a conversation axis by axis: high vs. medium vs. low, durable vs. temporary, observable vs. speculative.

#### 6. Case 1 — HBM and the memory spilloverThe HBM thesis is straightforward.

AI accelerators need more high-bandwidth memory. But HBM supply is constrained by stack yield, power, thermal behaviour, customer qualification, wafer allocation, and packaging integration.

This is a real bottleneck because without enough HBM, many AI accelerators cannot ship in full system configurations.

*Prediction*

If HBM remains the binding constraint, suppliers should show stronger pricing, better product mix, longer customer commitments, and spillover tightness into conventional DRAM.

The HBM bottleneck is no longer isolated inside AI servers.

It is spilling into the broader memory market.

As memory suppliers prioritise high-margin AI data centre products, conventional DRAM and NAND supply becomes tighter for PCs, smartphones, automobiles, medical devices, telecom equipment, and general enterprise IT.

This is ****bottleneck spillover**** in action — the mechanism named in Section 4, now with a concrete path.

Reuters reported that U.S. trade groups representing automakers, retailers, electronics firms, medical device manufacturers, telecom groups, and others have warned the U.S. Treasury and Commerce Departments that AI data centres are consuming an enormous share of available memory-chip capacity, creating price pressure and supply risks for other industries.[^reuters-memory]

Morgan Stanley has described the same phenomenon as “chipflation.” According to Reuters, Morgan Stanley analysts warned that memory-chip prices have risen roughly sixfold over the past year, forcing device makers to choose between raising prices and accepting thinner margins.[^reuters-chipflation]

*Validation metrics*

Track:

- HBM ASP

- HBM gross margin

- HBM4 / HBM4E qualification progress

- Sold-out status for 2026 / 2027

- Customer prepayments or long-term agreements

- Conventional DRAM contract prices

- DDR5 / LPDDR / NAND spot prices

- Memory vendor capex allocation between HBM and conventional DRAM/NAND

- PC / smartphone shipment revisions

- Trade association letters or policy response

*Falsification*

The thesis weakens if:

- HBM capacity expands faster than accelerator demand

- More suppliers pass customer qualification faster than expected

- HBM ASP weakens

- Long-term agreements loosen

- Accelerator architectures reduce HBM intensity per system

- DRAM / NAND prices reverse sharply

- Downstream consumer demand collapses enough to loosen memory supply

- AI data-centre capex is cut due to monetisation concerns

The variant view is that DRAM/NAND elasticity, new supply, or demand destruction caps the spillover. That is what the falsification list is watching for.

****For investors in one sentence:**** HBM is a real, profitable bottleneck as long as prices, contracts, and DRAM/NAND spillover all point the same way.

The key point is not simply “HBM is good.”

The key point is that HBM has a testable bottleneck thesis — and that the bottleneck may spill into the wider economy.

#### 7. Case 2 — CoWoS and advanced packagingThe CoWoS thesis is different.

The question is not only how much capacity is announced.

The question is how much ****effective output**** can actually be delivered after yield, warpage, substrate constraints, equipment readiness, customer qualification, and ramp speed.

This distinction is crucial.

In advanced packaging, announced capacity is not the same as effective capacity.

My CoWoS verification table frames this as the gap between “announced capability” and “effective capacity”: roadmap capability is only the starting point; yield, warpage, wafer-area loss, and ramp execution determine the actual output available to customers.

*Prediction*

CoWoS remains a key bottleneck while AI accelerator demand continues to grow, but the thesis must be updated as capacity expands.

The market should gradually shift from asking:

****How much CoWoS capacity was announced?****

To:

****How much high-end effective capacity can actually be shipped?****

TrendForce expects severe global 2.5D packaging shortages to begin easing slightly by 2027, helped by order spillover and TSMC’s plan to expand CoWoS capacity by more than 60% by 2027.[^trendforce-cowos]

In other words, CoWoS looks more like a 2–3 year execution window than a decade-long moat unless effective output continues to lag announced capacity.

*Validation metrics*

Track:

- Monthly CoWoS capacity

- Actual shipments, not only announced capacity

- Lead times

- CoWoS-S (silicon interposer) versus CoWoS-L (local silicon interconnect / RDL bridge) mix

- Substrate availability

- Customer allocation

- Advanced packaging ASP

- OSAT ability to absorb meaningful high-end demand

- Future AI package size and HBM count

*Falsification*

The thesis weakens if:

- Lead times collapse

- Customer allocation pressure eases

- OSAT or non-TSMC capacity successfully absorbs high-end demand

- CoWoS ASP or margin weakens

- Another bottleneck, such as HBM or power, becomes binding first

- AI accelerator shipments slow due to downstream data-centre constraints

****For investors in one sentence:**** treat CoWoS as an execution window, not a permanent moat, unless effective output keeps lagging announced capacity.

This is why I care less about headline capacity and more about the conversion from:

****announced capacity → effective output****

Capacity is not real until it becomes qualified output.

#### 8. Case 3 — Power and coolingPower and cooling are different again.

The bottleneck is real, but margin capture is more fragmented.

AI data centres need electricity, transformers, switchgear, grid connection, liquid cooling, water systems, and facility redesign. But the profit pool may be distributed across utilities, equipment makers, engineering firms, cooling suppliers, and service providers.

That makes this segment harder than HBM or CoWoS from an equity-selection perspective.

*Prediction*

Power and cooling constraints should create large capex opportunities, but stock selection will be harder than HBM or CoWoS because the ability to capture margin is less concentrated.

A transformer OEM may have a large backlog, but if utilities aggressively bid out projects or standardise specifications, pricing power can be much weaker than headline demand suggests.

The demand side is real. The International Energy Agency estimates that global data centre electricity consumption was around ****415 TWh in 2024**** and could double to around ****945 TWh by 2030**** in its base case, representing just under 3% of global electricity consumption. The IEA also notes that data centres can be operational in two to three years, while the broader energy system has longer lead times for planning and infrastructure buildout.[^iea]

China’s reported AI infrastructure plan reinforces the same point. The headline number is roughly RMB 2 trillion for AI infrastructure, but if China integrates the power grid into the project, reported estimates suggest the total could reach at least RMB 5 trillion.[^china-5t] In other words, power is not a supporting footnote. It can be larger than the compute plan itself.

*Validation metrics*

Track:

- Grid connection wait time

- Transformer and switchgear lead times

- Rack power density

- Liquid cooling attach rate

- Data-centre delay rates

- Utility capex plans

- Power purchase agreement trends

- Local permitting and land constraints

- Whether AI clusters are delayed by electricity availability rather than GPU availability

*Falsification*

The thesis weakens if:

- Model efficiency improves faster than expected

- Data-centre buildouts slow

- On-site power solutions relieve grid constraints quickly

- Cooling hardware becomes commoditised

- The sector attracts too much capital, and margins compress

- Utilisation assumptions prove too optimistic

****For investors in one sentence:**** power and cooling are real capex waves, but margin capture is scattered — this is a “pick specific winners” problem, not a “buy the whole theme blindly” thesis.

The lesson:

****A real bottleneck does not automatically mean an easy investment expression.****

#### 9. Five shorter cases: not every thesis is a physical bottleneckThe first three cases deserve the full template because they are direct supply-side constraints. The remaining cases are still important, but they are different kinds of theses: scaling reality, sovereign execution, demand-side monetisation, market structure, and platform distribution.

*Advanced nodes and SRAM scaling*

Advanced process nodes remain strategically critical. But “3nm” or “2nm” does not tell us whether AI chip economics are improving. The real questions are contacted poly pitch (CPP, a gate-pitch metric that helps determine logic density), metal pitch, SRAM bit-cell size, yield, wafer cost, die size, and cost per usable die.

The most important investment implication is SRAM. My process-node verification table shows that TSMC N5 high-density SRAM bit-cell is around ****0.021 µm²****, while N3 is around ****0.0199 µm²****, only about a ****5%**** shrink, even though logic density improves much more. Semiconductor Engineering has also written that SRAM scaling limitations challenge power and performance goals, even as SRAM remains a workhorse memory for AI.[^semieng]

This is why “3nm” is not an investment thesis. It is a starting point for verification.

*China's sovereign AI compute*

China’s AI infrastructure demand should be treated as a separate bottleneck thesis.

It is not simply another source of demand for the existing Nvidia-centred AI stack. It is a state-directed effort to build a domestic-first compute network. The relevant questions are domestic accelerator performance per watt, SMIC-linked capacity, memory bandwidth, national compute scheduling, software migration away from CUDA-dependent workflows, and hub utilisation.

China previously launched the “Eastern Data, Western Computing” project, with the National Development and Reform Commission approving eight national computing hubs and ten national data-centre clusters.[^ndrc] But capex alone does not guarantee effective compute. Reuters has reported that China has also faced concerns about data-centre glut and surplus computing power, leading policymakers to explore national networks for coordinating and selling excess compute capacity.[^china-glut]

****Sovereign capex is real demand, but capex is not the same as effective compute.****

*Token economics and enterprise AI ROI*

The monetisation thesis is the demand-side mirror image of the HBM and CoWoS thesis.

The question is not whether companies are experimenting with AI. They are. The question is whether paid AI usage grows fast enough, with enough measurable ROI, to support the infrastructure being built.

Watch enterprise AI spend per employee, token usage caps, paid conversion, model-provider gross margin, inference cost per task, customer retention, productivity ROI studies, cloud AI revenue quality, data-centre utilisation, and migration to smaller or open-source models.

A physical bottleneck can create a short-term profit pool. Long-term AI infrastructure economics require the monetisation bottleneck to be solved.

### Compute futures and the financialization of AI capacity

There is one more signal that AI compute is becoming a real bottleneck: Wall Street is trying to financialise it.

CME Group and Silicon Data have announced plans to launch compute futures later this year, pending regulatory review. The contracts will be based on Silicon Data’s daily GPU benchmarks for on-demand rental rates.[^cme] ICE and Ornn have announced a similar suite of cash-settled GPU compute futures based on Ornn’s Compute Price Index.[^ice]

This matters because compute is moving from an operational cost to a financial variable. Once a bottleneck has a benchmark, a futures curve, hedging demand, and speculative capital, it becomes easier to observe — but also easier to over-financialise.

The watchlist includes spot GPU rental price, futures curve shape, open interest, trading volume, basis between index prices and real cloud contracts, GPU utilisation, and whether infrastructure lenders use compute futures to hedge exposure.

The lesson: once a bottleneck has a futures curve, the constraint becomes financial as well as physical.

*Apple consumer AI: the tollbooth thesis*

Apple consumer AI is a demand and distribution thesis, not a physical bottleneck thesis.

Apple does not necessarily need to own the largest frontier model to monetise consumer AI. It controls the device, the operating system, the App Store, iCloud, privacy architecture, payment rails, and the user relationship. Wedbush analyst Daniel Ives called Apple’s WWDC an important AI monetisation moment, arguing that Apple’s AI services could create a major opportunity.[^ives]

That is a thesis, not a conclusion.

Watch AI-compatible installed base, iPhone upgrade cycle, iCloud+ attachment rate, Siri AI usage, developer adoption, device memory configuration, Private Cloud Compute usage limits, EU and China availability, and whether external model or cloud-GPU dependencies dilute margin capture.

Consumer AI is not just another feature cycle. It is a test of whether a platform company can turn AI into hardware upgrades, services revenue, and ecosystem lock-in.

#### 10. The next narrative: AI leaves the data centreThere is now an even bigger story emerging.

If terrestrial data centres are constrained by power, land, cooling, grid connection, and permitting, why not move some compute into space?

The idea is powerful. Space offers abundant solar energy, Low-Earth orbit satellites can provide communication links, launch costs have fallen, and defence demand adds another layer of imagination. Reuters reported that Elon Musk said SpaceX’s planned orbital AI data centres would rely heavily on existing Starlink V3 technologies, use solar power, radiate heat into space, and target about 120 kilowatts of sustained compute power for the first proposed AI satellite.[^spacex]

But this remains an imagination narrative, not a near-term replacement for terrestrial AI infrastructure. Space-based AI data centres may reduce some terrestrial constraints, but they introduce new constraints: launch cost, mass per kilowatt, radiation hardening, thermal rejection, satellite lifetime, maintenance, utilisation, link bandwidth, orbital debris, and regulation.

***The bigger the imagination, the more important the constraint map becomes.****

#### 11. The practical investor dashboardSo what should a rational investor do after reading all this?

Not chase every AI headline.

Not blindly buy every supplier.

Not dismiss the boom either.

The next step is to build a bottleneck dashboard.

For each segment, track a small number of metrics that can validate or falsify the thesis.

This is how a concept becomes actionable.

The point is not to predict tomorrow’s stock move.

The point is to predict where the profit pool may migrate, how long the bottleneck may last, and what evidence would prove the thesis wrong.

That is a more rational next step than asking for the next AI stock tip.

*A five-minute self-check*

If you only have five minutes, do this tonight:

1. List the top three AI stocks or themes you own or are tempted to buy.

2. Map each one to a row in Table 1.

3. For each, write one metric from Table 7 that would validate the thesis.

4. For each, write one falsification trigger that would make you cut or reduce exposure.

*A mini thesis template*

For a hypothetical HBM supplier X, I would write the thesis like this: “This is an HBM / memory-spillover thesis. Demand is high, constraint severity is high, and margin capture should remain strong if HBM ASP, gross margin, long-term agreements, and DRAM contract prices continue to move together. I would watch HBM4 qualification, customer prepayments, DRAM/NAND spillover, and memory-vendor capex allocation. The thesis fails if ASP weakens, contracts loosen, competitors qualify faster than expected, or AI data-centre capex is cut because token monetisation disappoints.”

That is the level of clarity I want before treating any AI theme as more than a story.

#### 12. This is not an anti-AI argumentI am not arguing that AI is fake.

The demand is real.

The capital spending is real.

The engineering progress is real.

The supply chain opportunities are real.

But physics is also real.

And monetisation is also real.

The centre of the argument is this:

****Corporate capex, sovereign capex, frontier AGI roadmaps, and consumer platforms explain why AI demand keeps expanding.**

**Physical bottlenecks explain who can capture the profit pool.**

**Bottleneck spillover explains who pays the hidden cost.**

**Monetised usage explains whether the buildout is sustainable.**

**Compute futures may tell us how the market is pricing scarcity in real time.****

Investors do not need to become semiconductor engineers.

But they do need to distinguish between:

- demand and profit

- claims and verification

- capacity announcements and effective output

- node names and physical metrics

- temporary shortages and durable bottlenecks

- imagination narratives and executable engineering

- capex and monetised usage

- bottleneck pricing and valuation risk

The market may price stories first.

But over time, it prices constraints.

And in AI infrastructure, the constraints are where the real map begins.

#### Appendix note: the three technical verification tablesThis article is based on three technical verification tables that I treat as companion notes rather than material to overload the main text:

The three companion technical verification tables are available in a downloadable appendix PDF:

The appendix includes: (This appendix uses only publicly available sources and the author’s own analysis. It does not reproduce paid teardown images, proprietary reports, confidential information, or material non-public information. Facts, specifications, and calculations are cited to their sources where applicable.)

1. HBM3E verification table
2. CoWoS verification table
3. Process-node verification table

The method is the same across all three:

Take a market slogan, pull it down into measurable constraints, then ask what can be validated and what would falsify the thesis.

That is the whole framework.

#### 👉 Download the appendix:#### [Download the technical appendix PDF](https://drive.google.com/file/d/1mSmqdWJIcqm9ZNK59tzhm04W5FLT3fOC/view?usp=sharing)#### Further reading- The three appendix tables in this package: HBM3E, CoWoS, and process-node verification.

- Goldman Sachs, “The Assumptions Shaping the Scale of the AI Build-Out.”

- Bain &amp; Company, “How Can We Meet AI’s Insatiable Demand for Compute Power?”

- IEA, “Energy and AI.”

- TSMC, A14 technology overview.

- Semiconductor Engineering, SRAM scaling coverage.

- Reuters coverage on China's sovereign AI buildout, memory chip shortages, and AI chipflation.

- CME Group and ICE announcements on compute futures.

- Apple Newsroom coverage of Apple Intelligence / Siri AI and Apple leadership transition.

- OpenAI’s “Built to benefit everyone: our plan” and confidential S-1 announcement.

- Google DeepMind’s AlphaEvolve article and white paper.

#### References[^goldman]: Goldman Sachs, “The Assumptions Shaping the Scale of the AI Build-Out,” May 2026. [https://www.goldmansachs.com/insights/articles/tracking-trillions-the-assumptions-shaping-scale-of-the-ai-build-out](https://www.goldmansachs.com/insights/articles/tracking-trillions-the-assumptions-shaping-scale-of-the-ai-build-out)

[^china-295]: Reuters, “China prepares $295 billion plan to fund nationwide AI buildout, Bloomberg News reports,” June 9, 2026. [https://www.reuters.com/world/china/china-prepares-295-billion-plan-fund-nationwide-ai-buildout-bloomberg-news-2026-06-09/](https://www.reuters.com/world/china/china-prepares-295-billion-plan-fund-nationwide-ai-buildout-bloomberg-news-2026-06-09/)

[^china-5t]: The Business Times / Bloomberg, “China prepares two trillion yuan plan to fund nationwide AI build-out,” June 9, 2026. [https://www.businesstimes.com.sg/international/china-prepares-two-trillion-yuan-plan-fund-nationwide-ai-build-out](https://www.businesstimes.com.sg/international/china-prepares-two-trillion-yuan-plan-fund-nationwide-ai-build-out)

[^openai-plan]: OpenAI, “Built to benefit everyone: our plan,” June 2026. [https://openai.com/index/built-to-benefit-everyone-our-plan/](https://openai.com/index/built-to-benefit-everyone-our-plan/)

[^openai-s1]: OpenAI, “Confidential submission of draft S-1 to the SEC,” June 2026. [https://openai.com/index/openai-submits-confidential-s-1/](https://openai.com/index/openai-submits-confidential-s-1/)

[^apple-ai]: Apple Newsroom, “Apple Intelligence brings powerful AI capabilities into everyday experiences,” June 2026. [https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/](https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/)

[^apple-ai2]: Apple Newsroom, “Apple unveils next generation of Apple Intelligence, Siri AI, and more,” June 2026. [https://www.apple.com/newsroom/2026/06/apple-unveils-next-generation-of-apple-intelligence-siri-ai-and-more/](https://www.apple.com/newsroom/2026/06/apple-unveils-next-generation-of-apple-intelligence-siri-ai-and-more/)

[^bain]: Bain &amp; Company, “$2 trillion in new revenue needed to fund AI’s scaling trend — Bain &amp; Company’s 6th annual Global Technology Report,” September 23, 2025. [https://www.bain.com/about/media-center/press-releases/20252/%242-trillion-in-new-revenue-needed-to-fund-ais-scaling-trend---bain--companys-6th-annual-global-technology-report/](https://www.bain.com/about/media-center/press-releases/20252/%242-trillion-in-new-revenue-needed-to-fund-ais-scaling-trend---bain--companys-6th-annual-global-technology-report/)

[^zitron]: Ed Zitron, “AI Is Slowing Down,” Where’s Your Ed At, 2026. [https://www.wheresyoured.at/ai-is-slowing-down/](https://www.wheresyoured.at/ai-is-slowing-down/)

[^reuters-token]: Reuters Breakingviews, “Corporate AI sticker shock will force restraint,” June 2, 2026. [https://www.reuters.com/commentary/breakingviews/corporate-ai-sticker-shock-will-force-restraint-2026-06-02/](https://www.reuters.com/commentary/breakingviews/corporate-ai-sticker-shock-will-force-restraint-2026-06-02/)

[^alphaevolve]: Google DeepMind, “AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms,” May 2025; AlphaEvolve white paper. [https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) and [https://arxiv.org/abs/2506.13131](https://arxiv.org/abs/2506.13131)

[^reuters-memory]: Reuters, “Automakers, retailers warn US memory-chip shortage is impacting prices,” June 3, 2026. [https://www.reuters.com/business/autos-transportation/automakers-retailers-warn-memory-chip-shortage-impacting-prices-2026-06-03/](https://www.reuters.com/business/autos-transportation/automakers-retailers-warn-memory-chip-shortage-impacting-prices-2026-06-03/)

[^reuters-chipflation]: Reuters, “AI ‘chipflation’ spreading from data centers to wider economy, Morgan Stanley warns,” June 3, 2026. [https://www.reuters.com/business/retail-consumer/ai-chipflation-spreading-data-centers-wider-economy-morgan-stanley-warns-2026-06-03/](https://www.reuters.com/business/retail-consumer/ai-chipflation-spreading-data-centers-wider-economy-morgan-stanley-warns-2026-06-03/)

[^trendforce-cowos]: TrendForce, “AI Competition Turns into a Supply Chain Arms Race,” April 30, 2026. [https://www.trendforce.com/presscenter/news/20260430-13028.html](https://www.trendforce.com/presscenter/news/20260430-13028.html)

[^iea]: International Energy Agency, “Energy demand from AI,” Energy and AI report. [https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai](https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai)

[^semieng]: Semiconductor Engineering, “SRAM Scaling Issues, And What Comes Next,” February 2024. [https://semiengineering.com/sram-scaling-issues-and-what-comes-next/](https://semiengineering.com/sram-scaling-issues-and-what-comes-next/)

[^ndrc]: NDRC, “China launches mega project of computing power hubs,” February 2022. [https://en.ndrc.gov.cn/news/mediarusources/202202/t20220218_1315947.html](https://en.ndrc.gov.cn/news/mediarusources/202202/t20220218_1315947.html)

[^china-glut]: Reuters, “China plans network to sell surplus computing power in crackdown on data centre glut,” July 24, 2025. [https://www.reuters.com/technology/china-plans-network-sell-surplus-computing-power-crackdown-data-centre-glut-2025-07-24/](https://www.reuters.com/technology/china-plans-network-sell-surplus-computing-power-crackdown-data-centre-glut-2025-07-24/)

[^cme]: CME Group, “CME Group and Silicon Data Partner to Launch First Compute Futures,” May 12, 2026. [https://www.cmegroup.com/media-room/press-releases/2026/5/12/cme_group_and_silicondatapartnertolaunchfirstcomputefutures.html](https://www.cmegroup.com/media-room/press-releases/2026/5/12/cme_group_and_silicondatapartnertolaunchfirstcomputefutures.html)

[^ice]: ICE, “ICE and Ornn to Launch GPU Compute Futures Contracts,” May 19, 2026. [https://ir.theice.com/press/news-details/2026/ICE-and-Ornn-to-Launch-GPU-Compute-Futures-Contracts/default.aspx](https://ir.theice.com/press/news-details/2026/ICE-and-Ornn-to-Launch-GPU-Compute-Futures-Contracts/default.aspx)

[^ives]: MarketWatch, “An Apple bull says the WWDC event ‘did not disappoint’,” June 2026. [https://www.marketwatch.com/livecoverage/apple-wwdc-keynote-live-siri-ai-watch-ios/card/an-apple-bull-says-the-wwdc-event-did-not-disappoint--xYFmVxRjdQv6WZibj7vK](https://www.marketwatch.com/livecoverage/apple-wwdc-keynote-live-siri-ai-watch-ios/card/an-apple-bull-says-the-wwdc-event-did-not-disappoint--xYFmVxRjdQv6WZibj7vK)

[^spacex]: Reuters, “Ahead of SpaceX IPO, Musk says AI satellites will use mostly existing technology,” June 9, 2026. [https://www.reuters.com/business/media-telecom/ahead-spacex-ipo-musk-says-ai-satellites-will-use-mostly-existing-technology-2026-06-09/](https://www.reuters.com/business/media-telecom/ahead-spacex-ipo-musk-says-ai-satellites-will-use-mostly-existing-technology-2026-06-09/)

#### DisclaimerThis article is for educational and research purposes only. It is not investment advice, not a recommendation to buy or sell any security, and not a prediction of short-term stock prices. Any companies or sectors mentioned are used as examples to illustrate a framework. Investors should conduct their own research and consider valuation, risk tolerance, liquidity, time horizon, and professional advice before making investment decisions.

#### Hashtags#AIInfrastructure #Semiconductors #HBM #CoWoS #DataCenters #AICapex #Memory #Chipflation #TSMC #AppleIntelligence #ComputeFutures #SovereignAI #AIInvesting #MooresLaw #PowerAndCooling #Substack #Medium

---

*This article was originally published on Medium. [Read the full version with charts and figures →](https://medium.com/@sinclairhuang/everyone-wants-the-next-ai-stock-im-looking-for-the-next-physical-bottleneck-f75737995b64?source=rss-1f713d63bb6a------2)*