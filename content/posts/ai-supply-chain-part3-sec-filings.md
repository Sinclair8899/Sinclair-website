---
title: "How Deep Is the Moat? Reading TSMC, SK Hynix, and Micron Through Their SEC Filings"
date: 2026-04-04
draft: false
tags: ["Semiconductors", "TSMC", "SK Hynix", "Micron", "SEC Filings", "AI Infrastructure", "Investing"]
description: "Customer prepayments, HBM margin structure, capital expenditure intensity — the numbers say more than the narratives do."
---

*Series: AI Compute Supply Chain | Part 3 of 5*

The previous article built a framework. This one tests it with documents.

Before writing this piece, I set aside the analyst summaries and went to the source: TSMC's 2024 20-F filed with the SEC on April 17, 2025; Micron's most recent 10-K and two 10-Q filings; and SK Hynix earnings call transcripts for the past three quarters.

I have a habit with regulatory filings that I developed over the years of reading them for investment and business decisions. Summaries tell you the conclusion someone chose to highlight. The original document tells you something different: **which number was emphasised, which risk was disclosed only because the regulation required it, and what the company is most careful about saying exactly right.**

This time, I found two gaps between the summaries and the documents worth pausing on.

First: most financial media reporting Micron's HBM customer concentration uses an annualised figure. The 10-Q notation says "first nine months." Not a large error — but a different cross-section, and one that matters for trend analysis.

Second, more significantly, TSMC's 20-F contains one line that I have seen almost no analysis article pull out and examine on its own terms. The customer prepayment figure: NT$291 billion in 2024. That number is the subject of the next section.

---

## TSMC: The Moat Is Written in Customer Behaviour, Not Just Margins

TSMC's gross margin of 56.1% in 2024 is impressive. Operating margin at 45.7% is remarkable. Revenue of US$90.1 billion, up 30% year-over-year, speaks for itself.

But I spent most of my reading time on that prepayment line.

In normal commercial relationships, buyers do not prepay voluntarily. Prepayment happens in two scenarios: when the buyer can negotiate a meaningful price discount in exchange, or when the buyer has no alternative and needs to secure allocation. TSMC's customers — Apple at 22% of revenue, NVIDIA at 12%, with the top ten collectively at 76% — did not prepay to get a discount. They prepaid because the alternative was not getting capacity at all.

The directionality of that behaviour is the most direct financial evidence of pricing power I have seen in any supply chain analysis. It is more informative than market share, more durable than gross margin, and more honest than management commentary.

One additional data point from the 20-F is worth holding together with the prepayment figure: TSMC served 522 customers and manufactured 11,878 distinct products in 2024. The top ten customers represent 76% of revenue — a concentration that looks like risk — but the ecosystem of 522 active customers represents something that cannot be moved by relocating a single fab. It is a manufacturing and co-development network that took decades to build. You can copy a factory floor plan. You cannot copy the collaborative qualification history between TSMC and hundreds of fabless design teams.

Advanced processes (7nm and below) accounted for 69% of wafer revenue in 2024, up from 58% in 2023. The revenue centre of gravity is continuously moving toward the narrower, harder-to-replicate segment. HPC platform revenue grew 58% year-over-year. Each of these trends points in the same direction: TSMC's addressable moat is widening, not narrowing.

---

## SK Hynix and Micron: The HBM Margin Engine and the Most Honest Risk Disclosure in the Industry

SK Hynix management has described HBM inventory status consistently across multiple quarters: sold out. In commodity markets, a sold-out supplier would typically be pressuring prices higher. In HBM, the constraint runs deeper — it is not just price, it is allocation. Customers cannot simply pay more to get more. They need to be in the qualification pipeline, and the qualification pipeline has a finite throughput.

The architecture shift in HBM4 changes this dynamic from cyclical to structural. The "customer-specific logic die" embedded in HBM4 means each supplier's product is engineered to a customer's specific platform requirements. Switching suppliers in a subsequent generation does not mean sourcing a compatible component — it means re-engineering the base die interface and requalifying against a platform that was designed around a different architecture. This elevates switching costs from a technical barrier to an **architectural barrier.**

In product development, I have found that architectural switching costs are the most undervalued form of moat. They are difficult to quantify in a standard financial model, they don't appear on a balance sheet, and analysts often treat them as temporary friction rather than structural lock-in. But anyone who has managed a platform-level component change knows: you don't execute a base die architecture migration in one product cycle. It takes time, engineering capacity, risk budget, and a customer willing to absorb the transition cost. SK Hynix's position in the Rubin platform — with UBS projecting approximately 70% HBM4 share — is not just a market share statistic. It is an architectural entanglement.

Micron offers a different kind of value in this analysis: the most transparent risk disclosure in the sector. The 10-K Risk Factors section contains a passage worth reading carefully:

> *"If HBM demand weakens and suppliers shift capacity back to conventional DRAM, conventional DRAM supply would surge, putting downward pressure on pricing across the entire DRAM market."*

One thing I appreciate about reading US public company 10-Ks is precisely this: SEC regulations compel companies to disclose risks honestly, or face legal consequences later. Ironically, the more detailed and clear a company's risk factor section is, the more it suggests management truly understands the industry. I read Micron's paragraph about HBM demand reversal twice. Not because it was scary, but because it was accurate.

This is the fundamental fragility of the HBM thesis, stated precisely by the company most likely to feel the downside first. HBM's high margins are partially a function of the capacity reallocation away from conventional DRAM that created artificial scarcity in that market. The premium is real, but it has a mechanism — and that mechanism can run in reverse.

---

## The Barclays Demand Framework: What If the Denominator Is Wrong?

Supply-side moats only hold their value if the demand that justifies them is real and durable. Before closing this analysis, one demand-side data point is worth examining — not for the headline number, but for the methodology.

Barclays analyst Tom O'Malley's team did not use token usage or query demand models to estimate AI infrastructure spending. They analysed financial disclosures from OpenAI and Anthropic — published in *The Information* — to reverse-engineer implied chip spending by hyperscalers. Working backwards from accounting flows is methodologically cleaner than projecting forward from usage assumptions, because token usage models require compounding assumptions at every step: applications deployed, compute per token, and hardware generation efficiency. Each assumption multiplies the error. Accounting flows don't have that problem: the money either moved or it didn't.

The conclusion: consensus hyperscaler capex forecasts for 2027 and 2028 are more than US$225 billion too low. The capital expenditure up-cycle likely runs to at least 2028, not 2026–2027 as many models assume. The five largest US hyperscalers have committed to US$660–690 billion in combined capex for 2026 alone — nearly double 2025 levels.

When I was doing product planning, the scenario I feared most was not demand collapse. It was systematic demand underestimation — where the supply chain plans conservatively, and the catch-up cost when reality arrives is enormous. If the Barclays model is directionally correct, the Class A nodes we identified in the previous article are not just maintaining their moats. They are facing a demand environment that will test whether those moats are deep enough.

---

## Closing

The competitive logic of this market has shifted from *who can do this* to *who has already been qualified, contracted, and prepaid.*

That shift is visible in the documents if you look for it — in prepayment line items, in sold-out inventory characterisations, in risk factor language that quietly names the conditions under which the whole structure could reverse.

*Moats are not announced. They are buried in 10-K risk factors, prepayment footnotes, and base die architecture decisions. You just have to know where to look.*

*Next: Four pressures that could crack these moats — and which one actually keeps me up at night.*

---

*This article is part of the AI Compute Supply Chain series. For the full series and related analysis, visit [sinclairhuang.org](https://sinclairhuang.org)*

*A working paper expanding this analysis — including an Irreplaceability Index scoring framework, patent portfolio analysis, and technology evolution roadmap — has been submitted to the Social Science Research Network (SSRN). The paper will be publicly available upon completion of review.*

---

### Further Reading — AI Compute Supply Chain Series

- **Part 1 — Technical Foundations:** CoWoS, HBM, and ABF: what they are, how they work, and why they became the bottlenecks in AI compute.
- **Part 2 — Power Map:** The Real AI Supply Chain: A Power Map Beyond the GPU
- **Part 3 — SEC Filings:** How Deep Is the Moat? Reading TSMC, SK Hynix, and Micron Through Their SEC Filings *(This Article)*
- **Part 4 — Stress Test:** Stress-Testing the Moat: Four Threats That Could Rewrite the AI Supply Chain
- **Working Paper — SSRN:** The Architecture of Leverage: Structural Concentration and Competitive Moats in the AI Compute Supply Chain

---

*Disclaimer: This article is for informational and educational purposes only and does not constitute investment advice or a recommendation to buy or sell any security. The views expressed are solely those of the author and are based on information believed to be reliable at the time of writing. Readers should conduct their own research and, if necessary, consult a qualified financial advisor before making investment decisions.*
