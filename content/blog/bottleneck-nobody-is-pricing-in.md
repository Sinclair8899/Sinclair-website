---
title: "The Bottleneck Nobody Is Pricing In: Where AI Compute Really Breaks"
date: 2026-03-21
description: "Every layer that looks solved hides another constraint beneath it. A deep look at CoWoS, HBM, and ABF substrate — the three physical bottlenecks shaping AI infrastructure."
tags: ["AI", "Semiconductors", "Supply Chain", "Infrastructure", "Investment"]
---

Every layer that looks solved hides another constraint beneath it.

## §1 The Illusion of Infinite Compute

The headlines say NVIDIA is winning. The hyperscalers are spending. The models are getting bigger.

But the real question is not where demand is going. It is where compute, physically, can still be built fast enough to meet it.

The harder answer requires tracing the full physical stack — from silicon wafer, through memory stack, through packaging interposer, through substrate material — and asking at each layer: can this actually scale at the speed the demand curve requires?

The answer, at every layer, is the same: not yet, and not linearly.

TSMC said as much in its 2025 Q2 earnings call. The framing was not "we have solved CoWoS supply." The framing was that the company is "working to narrow the supply-demand gap" — present tense, ongoing. Demand is scaling faster than the ecosystem that must physically deliver it.

This piece maps three layers of that gap. Each one is real. Each one has a different resolution timeline. And at least one of them is almost entirely absent from mainstream investor conversation.

## §2 CoWoS: The Integration Layer That Cannot Be Rushed

Most coverage of AI infrastructure treats packaging as a backend afterthought — something that happens after the real engineering is done. This framing is wrong, and it is costing analysts real insight.

CoWoS — Chip on Wafer on Substrate — is not a packaging step. It is, as TSMC's own technical documentation states, the integration platform designed specifically for AI and ultra-high performance computing applications. What CoWoS does is physically bond logic chiplets and HBM memory together on a large-area silicon interposer, at densities and interconnect speeds that no other approach currently matches at production scale.

This is why you cannot simply "open another line."

A conventional packaging facility and a CoWoS facility share almost nothing in terms of equipment, process know-how, or yield management. The interposer itself must be manufactured at leading-edge fab precision. The bonding of HBM stacks to logic dies at scale, with acceptable yield, is a process that took years to develop and cannot be transferred quickly.

Consider what TSMC's own actions imply: in its 1Q25 earnings call, TSMC stated it was working to double CoWoS capacity through 2025. Doubling is an aggressive posture. It is also, read carefully, an admission of how tight the baseline was. The company has since announced additional advanced packaging capacity in Arizona — but the operative word remains *additional*, not *sufficient*. Its language through 2025 and into 2026 consistently signals a gap, not a clearing.

> CoWoS is not merely a backend packaging step; it is the integration layer that turns AI silicon into a shippable system product.

For investors: CoWoS capacity is the near-term gating factor on how many H100/B200-class systems actually ship in any given quarter. Revenue recognition at NVIDIA, and utilization rates at hyperscalers, are both downstream of this constraint.

## §3 HBM: This Is Not a Memory Story. It Is a Capacity Allocation Story.

High Bandwidth Memory is where most supply chain analysis stops when it goes deeper than CoWoS. But even here, the standard narrative — "SK Hynix is ahead, Samsung is catching up, Micron is entering" — understates the structural rigidity of what is actually happening.

Current market structure: SK Hynix holds approximately 57% of HBM supply. Samsung holds approximately 22%. These figures describe not a competitive market but a functional duopoly with a strong leader. And that leader — SK Hynix — remains NVIDIA's primary HBM supplier.

The reason this structure does not change quickly has nothing to do with ambition or capital. It has to do with physics and process.

HBM3E involves stacking multiple DRAM dies with through-silicon vias at tolerances where yield management is genuinely difficult. Qualification cycles with end customers like NVIDIA are not formalities — they are multi-quarter processes involving thermal validation, signal integrity testing, and system-level burn-in. A new entrant or a trailing supplier does not simply "catch up" by building more fab capacity. They catch up by surviving the qualification gauntlet, which takes time that market demand does not pause for.

More structurally: the SK Group chairman was quoted as stating that HBM is extremely wafer-intensive, that wafer shortages could persist to 2030, and that building new wafer capacity takes four to five years. The current wafer shortage already exceeds 20%.

Read that again: four to five years to bring new wafer capacity online, against a demand curve that is re-accelerating every six months.

> HBM is not just a memory story; it is a capacity-allocation story across wafers, yields, validation, and customer trust.

Samsung's response — moving toward longer-term supply agreements to lock in AI memory customers — confirms that this is no longer a spot-market dynamic. It is a platform supply competition, and the positions being established now will persist for years.

## §4 Substrate and Materials: The Constraint Nobody Is Writing About

This is the layer that separates supply chain analysis from supply chain understanding.

Every CoWoS package, every advanced AI accelerator, requires an ABF substrate — a laminate built using Ajinomoto Build-up Film as its core dielectric material. Ajinomoto holds more than 95% share of the global market for insulating films used in high-performance semiconductors. That figure is not a rounding error. It is the supply structure.

The material is not a commodity input — it requires controlled-environment manufacturing, multi-layer lamination at precise specifications, and ongoing process development as chip packages grow more complex.

And they are growing more complex. The AI era is not just consuming more substrate area; it is requiring substrate at specifications that are harder to manufacture and that fewer facilities can produce.

Ajinomoto has announced plans to invest at least ¥25 billion in additional ABF capacity by 2030. That investment figure is both reassuring and revealing: reassuring because it signals commitment, revealing because a 2030 investment horizon implies that the company itself does not expect this to be a near-term resolved constraint.

> The market often overestimates flexibility at the chip-design layer and underestimates rigidity at the materials-and-substrate layer.

For researchers tracking supply chain dependency concentration: ABF is arguably the single highest-concentration chokepoint in the entire AI infrastructure stack. It receives a fraction of the analytical attention that TSMC or SK Hynix receive.

## §5 The Resolution Timeline: Who Clears First, Who Doesn't

For investors and operators, the actionable question is not whether these bottlenecks exist — they do — but when each one resolves, and what that resolution sequence implies.

**CoWoS:** earliest to ease, but not soon. The gap is narrowing. But "narrowing" through 2026 still means constrained. This is the bottleneck most likely to show meaningful relief in the 2026–2027 window.

**HBM:** structurally tight through the decade. The SK Group chairman's statement about wafer shortage persisting to 2030, combined with four-to-five-year lead times for new wafer capacity, makes this the hardest constraint to reason around optimistically. SK Hynix's position will remain dominant; Micron's entry adds optionality but not near-term volume.

**Substrate and materials:** the most underappreciated source of delay. Ajinomoto's 2030 investment plan describes a constraint that is intensifying in technical difficulty even as capacity nominally expands. This is not a bottleneck that resolves when a new factory opens — it resolves when the full materials-qualification-manufacturing chain matures at the next node of complexity.

> CoWoS may ease first. HBM may remain structurally tight longer. Substrate and material constraints may be the most underappreciated source of future delay.

For investors: The non-obvious beneficiaries sit at the layers least discussed — advanced packaging equipment suppliers, specialty substrate manufacturers, and any company that successfully develops an ABF alternative or a competing interposer material.

For supply chain operators: The three metrics worth tracking are CoWoS lead times, HBM allocation terms, and ABF capacity announcements out of Ajinomoto.

The compute is real. The demand is real. But between the architecture and the datacenter floor, there is a physical world that scales on its own timeline — and right now, that timeline is slower than the one being priced into the market.
