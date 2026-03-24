---
title: "What Are CoWoS, HBM, and ABF - And Why Do They Matter So Much in the AI Era?"
date: 2026-03-24
description: "A plain-language walkthrough of CoWoS, HBM, and ABF — what they actually are, why they are always mentioned together, and how they map onto Taiwan's role in the global AI supply chain."
tags: ["AI", "Semiconductors", "HBM", "CoWoS", "ABF", "Supply Chain", "Taiwan"]
---

Why is everyone suddenly talking about CoWoS, HBM, and ABF whenever AI, NVIDIA, or AI servers come up? Many people know they are important, but still get stuck the first time they run into these terms.

This essay is a plain‑language walkthrough of what they actually are, why they are always mentioned together, and how they map onto Taiwan's role in the global AI supply chain.

When Google, Amazon, and Tesla are all designing their own chips, is Taiwan's manufacturing ecosystem still structurally important — or just enjoying a temporary window?

To answer that, we have to go from GPUs to memory, to advanced packaging, to high‑end substrates, and see what it actually takes for AI compute to become physical, shippable infrastructure.

---

## From GPU to HBM, CoWoS, and ABF

Any time you hear about NVIDIA, AI servers, or "scaling up compute," you almost always see three acronyms show up: CoWoS, HBM, and ABF.

People sense these are critical, but often still ask very reasonable questions:

- Isn't CoWoS just "packaging"?
- How is a high‑end substrate different from a regular PCB?
- How many layers of substrates up to now?
- Can Taiwan actually produce HBM?
- If Google, Amazon, and Tesla all design their own chips, doesn't that mean the advantage of Taiwan's supply chain is just temporary?

These are good questions, because AI compute doesn't become real just because you have a GPU. It takes an entire stack working together.

If we use a simple analogy:

- The GPU is the brain.
- HBM is ultra‑high‑speed short‑term memory.
- CoWoS is the integration technology that tightly connects the brain to that memory.
- ABF and substrates are the structural base that carries the whole complex system.

Once you internalise that sentence, you already have the big picture.

---

## 1. What is HBM?

HBM stands for High Bandwidth Memory. You can think of it as the ultra‑fast data warehouse sitting right next to an AI chip.

Training and running AI models means constantly moving huge amounts of data. If memory bandwidth cannot keep up, even the most powerful GPU will sit idle waiting for data. HBM is therefore not just about having more capacity; what really matters is:

- Extremely high data transfer rates (multi‑hundred GB/s per stack, moving toward >1 TB/s)
- Very wide I/O interfaces (thousands of bits)
- TSV‑stacked DRAM dies with very short internal distances
- Architected for high‑performance computing workloads

In other words, HBM's job is to keep the GPU from waiting around.

If the GPU is the brain, HBM is the ultra‑fast working memory sitting right beside it. No matter how strong your brain is, if working memory is too slow, overall performance gets bottlenecked.

Commercial HBM production today remains heavily concentrated in just a few DRAM players. Recent market data puts SK Hynix at roughly the mid‑50%–60% range of HBM market share, with Samsung and Micron making up most of the rest — a very concentrated market rather than a broad, commoditised one.

> **For investors:** a concentrated HBM market with multi‑year qualification cycles suggests sustained pricing power and relatively visible capex paths for leading vendors, but also the risk of a classic "super‑cycle then correction" once capacity finally catches up.

---

## 2. What is CoWoS?

CoWoS is an advanced packaging technology. The acronym stands for Chip on Wafer on Substrate.

If HBM is high‑bandwidth memory, then CoWoS is the way you tightly, densely, and at very high speed integrate the GPU with that HBM.

CoWoS usually involves:

- Large silicon interposers approaching multi‑reticle sizes
- Thousands to tens of thousands of micro‑bumps between the GPU and HBM stacks
- Very fine line/space routing on the interposer to carry wide, high‑speed interfaces

Even if HBM is fast on paper, if you don't connect it to the GPU closely enough, with high‑density wiring and efficient signal paths, you cannot unlock that performance in the real system. CoWoS is not "just wrapping chips." Its value is enabling GPU and HBM to operate as one coherent high‑performance system.

> Without CoWoS, it is very hard to fully integrate the performance of the GPU and HBM.

TSMC explicitly positions CoWoS as an AI/HPC integration platform under its 3DFabric portfolio. On recent earnings calls, TSMC has discussed aggressive efforts to expand CoWoS capacity — in some cases nearly doubling capacity over 2025–2027 — yet demand from NVIDIA and custom AI ASICs still keeps the line effectively sold out.

> **For investors:** when AI accelerator deployment is gated more by CoWoS slots than by GPU tape‑outs, part of the value capture shifts from GPU vendors toward those who control advanced packaging and associated substrate capacity.

---

## 3. What is ABF / a Substrate?

ABF stands for Ajinomoto Build‑up Film — an insulating build‑up film material used in high‑end package substrates.

Returning to our analogy:

- GPU = brain
- HBM = ultra‑fast working memory
- CoWoS = high‑complexity integration technology
- ABF / substrate = the structural base that carries this entire complex system

As packaging becomes more complex, wiring becomes denser, and signal integrity more demanding, the materials and substrates underneath have to be upgraded as well. Modern AI/HPC substrates use multiple build‑up layers, single‑digit‑micron line/space, and careful CTE/warpage control to keep very large packages within spec.

ABF is not a trivial material — it is one of the foundations that determine whether high‑end packages can be manufactured reliably at all.

Ajinomoto's share in high‑performance semiconductor insulating films is above 90–95%, and the company has announced multi‑year investment plans — on the order of tens of billions of yen — to expand ABF production through 2030.

> **For investors:** concentrated material supply, long equipment lead times, and package‑specific substrate designs mean that "invisible" ABF bottlenecks can decide who actually ships AI hardware on time — and at what margin.

---

## 4. Why Are These Three Always Discussed Together?

Because in the AI era, they are not three isolated topics. They form one tightly coupled system:

- **HBM** determines whether data can be delivered to the GPU fast enough.
- **CoWoS** determines whether the GPU and HBM can be integrated at very high density and bandwidth.
- **ABF / substrates** determine whether that complex package can be mechanically and electrically supported in volume.

The real question is therefore not any single component, but: *Can the entire AI chip system be built reliably and at scale?*

That is why you can no longer talk about AI compute just by looking at the GPU chip itself. You have to think about memory, packaging, substrates, and materials. A bottleneck at any layer can delay shipments and cap actual delivered performance.

---

## 5. One‑Sentence Summary

Without HBM, the GPU cannot be fed fast enough. Without CoWoS, the GPU and HBM cannot be tightly integrated. Without ABF / high‑end substrates, the entire complex package cannot be mechanically or electrically supported.

CoWoS, HBM, and ABF matter not because they are fashionable buzzwords, but because together they decide whether AI compute can physically land in data centres and devices.

---

## Frequently Asked Questions

**Q1. "Isn't CoWoS just packaging? Why is everyone treating it like such a big deal?"**

You can say yes — CoWoS is an advanced packaging technology — but it is very different from the intuitive idea of "put the die in a package and protect it." Traditional packaging is more about protecting the chip and getting signals off‑chip into a PCB. CoWoS, by contrast, uses a large silicon interposer with very fine line/space, thousands of micro‑bumps, and tight power/signal constraints to tie together one or more large logic dies and multiple HBM stacks.

*CoWoS looks like packaging on the surface, but in practice, it is the core integration technology for AI chip systems.*

---

**Q2. "What's the difference between a package substrate and a regular PCB?"**

A regular PCB connects various components on the board, usually with line/space in the tens of microns. A high‑end package substrate sits directly under the chip package and has to handle far higher I/O density, single‑digit‑micron line/space, tight impedance control, and tougher warpage targets.

- A PCB is the road network of an electronic system.
- A high‑end substrate is the ultra‑precise interchange right under the chip package.

---

**Q3. "How many layers are high‑end substrates at now?"**

The more important trend is that AI/HPC substrates are moving toward more build‑up layers (into the mid‑20s and beyond), finer line/space in the single‑digit‑micron range, larger body sizes to accommodate multi‑chiplet and multi‑HBM packages, and higher I/O counts. It is not just "making more layers," but making the whole stack significantly more difficult from a process‑control and yield‑management standpoint.

---

**Q4. "Can Taiwan produce HBM?"**

Taiwan is not one of the "big three" branded HBM suppliers today, but it is a central manufacturing and integration base in the HBM ecosystem — strong in leading‑edge foundry, CoWoS packaging, high‑end ABF substrates, OSAT and test. That means you can get exposure to the HBM build‑out not only through memory names, but also via foundry, advanced packaging, testing, and substrate companies.

---

**Q5. "Why can't just anyone start making HBM?"**

Because HBM isn't "just memory." The hard parts include stacking multiple DRAM dies with TSVs at acceptable yields, managing heat and power density in very tall stacks, and passing strict, time‑consuming qualification with major GPU vendors. The real barrier is: *process technology + yield management + long customer qualification cycles + accumulated system‑level experience.*

---

## Extended Question: If Google, Amazon, and Tesla Design Their Own Chips, Does Taiwan Still Matter?

"Designing your own chip" usually means defining your own architecture and optimising it for your workload. It does not automatically mean you control leading‑edge wafer manufacturing, CoWoS at scale, HBM supply, high‑end ABF substrates, or high‑volume ramp experience.

*Design rights can decentralise. The manufacturing ecosystem is much harder to clone.*

A more accurate framing:

> Over the visible medium term, Taiwan remains one of the hardest‑to‑replace cores of the AI supply chain, especially where leading‑edge wafers, HBM‑class memory integration, CoWoS, and ABF substrates intersect.

A more realistic scenario is that Taiwan gradually shifts from "the" absolute centre to one of the dominant centres — still with outsized influence in key bottleneck steps.

> **For investors:** the key trade is not "own anything with 'AI' in the ticker." It is to identify which parts of the stack remain structurally scarce — leading‑edge wafers, HBM, CoWoS, ABF — and which companies can convert that scarcity into sustainable returns on heavy capex, without over‑building into the next down‑cycle.

---

*Note: None of this is a guarantee that "anything tied to HBM/CoWoS/ABF will automatically make money." These are structural lenses for thinking about risk, capacity, and where bargaining power might reside — not stock recommendations or investment advice.*
