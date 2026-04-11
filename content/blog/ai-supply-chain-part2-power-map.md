---
title: "The Real AI Supply Chain: A Power Map Beyond the GPU"
date: 2026-04-02
draft: false
tags: ["Semiconductors", "Supply Chain", "TSMC", "SK Hynix", "Ajinomoto", "AI Infrastructure", "Investing"]
description: "From TSMC to SK Hynix to Ajinomoto — who holds pricing power, and who is just riding the narrative?"
---

*Series: AI Compute Supply Chain | Part 2 of 5*

The first article in this series explained what CoWoS, HBM, and ABF *are*. This one answers the harder question underneath: **who controls them?**

Knowing that these three layers matter is the entry ticket. The real analytical edge comes from understanding who in each layer has the power to say no — and what happens to the whole chain when they do.

In my years in senior management roles across the electronics industry, I took a long time to learn the hardest lesson of all. When I first started, I thought supply chain management was about inventory, lead times, and negotiating lower prices. Eventually, I understood that the real question is simpler and more ruthless: **in this chain, who has the right to say "no"?**

Whoever can refuse holds the leverage. Whoever can't is the one being priced. That question — not market share, not revenue — is where this analysis starts.

Bottlenecks don't distribute profits evenly. Value concentrates at the nodes that cannot be bypassed.

---

## Layer One — CoWoS: One Node, One Real Answer

Advanced packaging is a phrase everyone uses now. That doesn't mean everyone can do it.

The difficulty in CoWoS isn't whether you *can* package chips together. It's whether you can do it **at scale, with production yields high enough to matter, consistently, for the most demanding customers on earth.**

The market here breaks into two tiers.

**Tier One — the irreplaceable node: TSMC.** CoWoS and TSMC are nearly synonymous at the leading edge. By the end of 2025, TSMC's monthly CoWoS capacity reached 75,000–80,000 wafers. The company's 2024 annual report on Form 20-F, filed with the SEC, disclosed that customers collectively prepaid NT$291.1 billion — approximately US$9 billion — to secure multi-year capacity allocations.

I spent several years in procurement and supply chain roles. Prepayment is not a normal commercial behaviour. Buyers don't voluntarily pay upfront unless they have no alternative. The direction of that behaviour — customer to supplier, not the reverse — is the most direct financial evidence of who holds pricing power. You don't need a market share chart when you have a prepayment line item.

When I evaluate suppliers, I always ask one question first: if this supplier has a problem tomorrow, how long does it take me to find a replacement with equivalent capability? Under three months is not a moat. That's just competition. For CoWoS at production scale and leading-edge yield, my estimate is three to five years — and that's for someone starting with full capital, full equipment access, and strong engineering talent. TSMC grew its own CoWoS capacity from 13,000 wafers per month in late 2023 to 75,000–80,000 by the end of 2025. That trajectory, built on existing infrastructure and decades of process knowledge, took two years under ideal conditions. A new entrant has no such foundation.

The velocity of demand makes that timeline feel even tighter when you look at specific customers. MediaTek, acting as ASIC supplier for Google's Tensor Processing Units, reportedly doubled its 2026 CoWoS wafer allocation from 10,000 to 20,000 wafers for the v7e TPU generation. As the transition moves to the next-generation v8e, projections suggest MediaTek may require over 150,000 CoWoS wafers annually by 2027 — a sevenfold increase from where it started. This is one design win at one customer. Multiply that demand curve across NVIDIA, AMD, Amazon, and Broadcom, and the picture of why TSMC's capacity is sold out through 2026 becomes immediate and concrete.

**Tier Two — important, but not equivalent:** ASE and Amkor absorb TSMC's overflow on lower-complexity RDL processes. Their role is real and growing. But TSMC retains the highest-margin, highest-complexity work — CoWoS-L integration, silicon interposer fabrication, Chip-on-Wafer front-end processes. The overflow is a deliberate allocation decision, not a concession of position.

---

## Layer Two — HBM: It Looks Like a Memory Market. It Behaves Like a Platform Allocation Market.

The HBM competitive landscape appears straightforward: SK Hynix leads with approximately 62% market share, Micron has moved into second position at around 21%, and Samsung is working to recover ground.

But market share is a lagging indicator. It tells you where the competition *was*. The more important question is what the competition is *becoming*.

The structural shift that matters most in HBM is happening at the architecture level, not the market share level. I spotted this detail while reading through SK Hynix earnings call transcripts — not the analyst summary. Their executives, when describing the HBM4 architecture, used a specific phrase: **"customer-specific logic die."**

In product development, the component you fear most is not the expensive one — it's the one with a custom logic layer underneath. Once that layer is designed for a specific platform, switching suppliers doesn't mean finding an equivalent part. It means redesigning the base architecture and rerunning the entire qualification cycle. I've managed product changes like this before. That cycle is measured in quarters, not weeks, and it carries real risk to production schedules.

HBM4 encodes this dynamic into the silicon itself. Each supplier's product carries the customer's architectural DNA. Goldman Sachs has projected that SK Hynix will maintain above 50% HBM market share through at least 2026, with UBS estimating approximately 70% share in NVIDIA's Rubin platform's HBM4 allocation.

This is no longer a memory market in the traditional sense. It is a **platform qualification market**. The three questions that determine position are: who passed the customer's validation first, who holds the multi-year supply agreement, and whose roadmap is co-developed with the customer's next-generation architecture. On all three, SK Hynix currently leads.

---

## Layer Three — ABF Substrates: The Most Underestimated Node in the Stack

Most AI supply chain analysis stops at chips and packaging. Fewer people go one level deeper to the substrate, and fewer still look at the material that makes the substrate possible.

**The material layer:** Ajinomoto — the Japanese company most people know for its food seasoning products, particularly MSG — holds above 95% global market share in the high-performance semiconductor insulating film used in advanced packaging substrates. This is not market leadership. This is a structural monopoly.

I first encountered this when reading a Broadcom supply chain analysis document — public investor material. The reference was almost parenthetical: ABF material shortage had become one of the root causes of the packaging bottleneck. My reaction was: this company, whose primary public identity is built on food science and amino acid chemistry, occupies a position in the AI supply chain that is nearly impossible to bypass. That discovery made me start systematically scanning upstream for nodes that are "small in volume but structurally non-negotiable."

What makes this case intellectually fascinating goes beyond supply chain mechanics. **The foundational chemistry of ABF was derived from Ajinomoto's basic research into amino acid chemistry and epoxy resins — work that began in the 1970s in a completely different scientific context.** By the late 1990s, precision material science had evolved into the advanced insulators that now sit beneath every leading-edge GPU and CPU on earth. The moat was not built for semiconductors. It was built in food science and pharmaceutical research, and it migrated into silicon. Because it originated in a disparate discipline, traditional semiconductor materials companies spent decades unable to replicate the exact thermal and electrical properties that Ajinomoto had accumulated through an entirely different research lineage. That is a category of competitive advantage that cannot be manufactured by intent — only stumbled upon across generations of scientific work.

To test the depth of any supplier's moat, I ask: if they stopped production tomorrow, how long before a qualified alternative could reach customers? For Ajinomoto's ABF material, the honest answer is that no one has seriously stress-tested this scenario — because the 95% market share means that nearly every advanced packaging qualification in the industry has been run on Ajinomoto's material specification. Switching the material means rerunning the qualification. Qualification cycles run in quarters.

The generative AI boom has also dramatically changed the *consumption rate* of ABF, not just demand volume. A standard PC substrate typically requires around six layers of ABF film. An AI accelerator or HPC substrate requires 16 to 18 layers — roughly three times as many. And the physical surface area of an AI package is approximately 3.5 times larger than a conventional PC package. These two multipliers compound into what the industry has started calling a **"double effect"**: each AI unit consumes exponentially more ABF material than the electronics it is replacing. This is why Ajinomoto has committed to increasing its global ABF production capacity by 50% by 2030, requiring at least JPY 25 billion in capital investment — not because units are growing linearly, but because the content per unit has structurally shifted upward.

**The substrate manufacturing layer:** The top five manufacturers — Unimicron, Ibiden, AT&S, Nan Ya PCB, Shinko Electric — collectively hold approximately 74% of global ABF substrate capacity. Unimicron leads with approximately 22% individual share. This layer is more fragmented than the material layer, but the entry barriers are substantial: high capital intensity, long certification cycles, and the continuous technical demands of AI/HPC substrates pushing toward higher layer counts, finer line widths, and larger package dimensions.

---

## The Framework: Class A, Class B, Class C

Pulling the three layers together, the market players can be sorted into three categories. The sorting criteria are not size or revenue — they are the structural conditions that determine whether pricing power is durable.

**Class A — genuine pricing power:** Technology scarcity, concentrated supply, high customer qualification barriers, long replacement cycles — all four conditions present simultaneously. The current list is short: TSMC, SK Hynix, Ajinomoto.

**Class B — real exposure, but capped upside:** Meaningful businesses, genuine growth, but customers have alternatives, competition has substitutes, and outperformance is more cyclical than structural. ASE, Amkor, Unimicron, Micron (a strong challenger, but not yet at the platform-binding level) — all live here.

**Class C — narrative exposure without structural position:** AI supply chain labelling present, but no major platform qualification, no multi-year supply contracts, no scarcity premium. To identify Class C, three questions are sufficient: Has this company been formally qualified by a major AI platform? Does it hold multi-year supply agreements? If it disappeared tomorrow, how long would the customer need to find an equivalent? Weak answers on all three — regardless of how many AI keywords appear in the investor deck — should invite scepticism.

I can't name Class C companies here, but I can say this: every time an industry narrative peaks, a batch of companies that "touch the keywords but lack real position" get lifted along with it. I've seen this firsthand in the 2000 internet bubble, the 2012 tablet boom, and the automotive chip wave. The speed of narrative diffusion always exceeds the speed of fundamental verification. That gap is the risk.

---

## Closing

In AI hardware, value does not distribute evenly across the stack.

It concentrates where scale, qualification, and scarcity converge simultaneously — and only there.

*Next: We open the SEC filings. What do the actual numbers say about how deep these moats really are?*

---

*This article is part of the AI Compute Supply Chain series. For the full series and related analysis, visit [sinclairhuang.org](https://sinclairhuang.org)*

*A working paper expanding this analysis — including an Irreplaceability Index scoring framework, patent portfolio analysis, and technology evolution roadmap — has been submitted to the Social Science Research Network (SSRN). The paper will be publicly available upon completion of review.*

---

### Further Reading — AI Compute Supply Chain Series

- **Part 1 — Technical Foundations:** CoWoS, HBM, and ABF: what they are, how they work, and why they became the bottlenecks in AI compute.
- **Part 2 — Power Map:** The Real AI Supply Chain: A Power Map Beyond the GPU *(This Article)*
- **Part 3 — SEC Filings:** How Deep Is the Moat? Reading TSMC, SK Hynix, and Micron Through Their SEC Filings
- **Part 4 — Stress Test:** Stress-Testing the Moat: Four Threats That Could Rewrite the AI Supply Chain
- **Part 5 — Industrial Transformation** *(upcoming)*

---

*Disclaimer: This article is for informational and educational purposes only and does not constitute investment advice or a recommendation to buy or sell any security. The views expressed are solely those of the author and are based on information believed to be reliable at the time of writing. Readers should conduct their own research and, if necessary, consult a qualified financial advisor before making investment decisions.*
