---
title: "Copper Is Running Out of Room. But Light Has a Manufacturing Problem."
date: 2026-05-07
draft: false
tags: ["silicon-photonics", "ai-infrastruture", "advanced-packaging", "semiconductors", "manufacturing"]
description: "## Why CPO is not an optics story — it is a process-integration story.*AI Infrastructure Notes | Part 2**Sinclair Huang*Everyone says AI needs more bandwidth.That part is true.As AI clusters scale fro"
canonical: "https://medium.com/@sinclairhuang/copper-is-running-out-of-room-but-light-has-a-manufacturing-problem-4a7c8f2c1dcd?source=rss-1f713d63bb6a------2"
---

## Why CPO is not an optics story — it is a process-integration story.

**AI Infrastructure Notes | Part 2**

**Sinclair Huang**

Everyone says AI needs more bandwidth.

That part is true.

As AI clusters scale from thousands of accelerators to tens of thousands, and then toward million-GPU-scale systems, the network stops being a background layer. It becomes part of the compute fabric itself. Copper reaches its distance, power, and signal-integrity limits. Optical interconnect moves closer to the switch ASIC. Co-packaged optics becomes the logical next step.

That is the easy part of the story.

The harder question is not whether light is useful.

The harder question is whether the manufacturing window survives.

In March 2025, NVIDIA announced Spectrum-X Photonics and Quantum-X Photonics, its co-packaged-optics networking switches for large-scale AI factories. TSMC has also said its COUPE-on-substrate CPO solution begins production in 2026. Broadcom has announced Tomahawk 6 Davisson, a 102.4-Tbps Ethernet switch with co-packaged optics.

The industry narrative is now clear: light is moving closer to the ASIC.

But CPO is not being delayed by a lack of optical physics. SiN waveguides, Cu-Cu bonding, and Ge photodetectors are all well-understood individually. The real problem appears when they must coexist inside one package, under BEOL-compatible thermal budgets, wafer-scale variation, and production-yield requirements.

That makes CPO a process-integration story, not an optics story.

While developing a training curriculum on advanced semiconductor manufacturing — and after working through recent literature and conversations with engineers who actually run these processes — I kept seeing the same pattern:

The bottleneck is not a single missing invention.

It is the collision of mature process modules at the integration boundary.

This article focuses on three failure modes that will decide whether CPO actually ships at scale:

1. SiN waveguide propagation-loss drift

2. EIC-PIC Cu-Cu hybrid-bonding voids

3. Ge photodetector dark-current drift

There is another real CPO issue I am deliberately bracketing here: laser-source integration and thermal management. Whether the industry standardises around external laser sources, co-packaged laser sources, or some hybrid approach remains a major architecture debate. Lasers are heat-sensitive, and that problem deserves its own article.

But even if the laser is kept outside the package, the PIC/EIC manufacturing stack still has to survive the three process windows below. That is why I focus here on the manufacturing failure modes inside the optical path and the EIC-PIC integration boundary.

## The 60-second version

&gt; CPO is often described as “optics replacing copper.”

&gt; That is directionally right, but incomplete.

&gt; The manufacturing problem is more specific:

&gt; ****CPO requires FEOL-grade process quality under a BEOL thermal budget.****

&gt; That conflict appears in three places:

&gt; ****SiN waveguides**** want low-loss, high-temperature film quality, but BEOL integration pushes them toward lower-temperature PECVD plus post-processing.

&gt; ****Cu-Cu hybrid bonding**** uses BEOL copper technology, but requires near-atomic-level surface control, especially around Cu recess and wafer-scale bonding yield.

&gt; ****Ge photodetectors**** want high-quality epitaxy and annealing, but BEOL-compatible integration caps the thermal budget below the temperatures that normally produce the best detector performance.

&gt; So the real CPO question is not:

&gt; ****Can optics beat copper?****

&gt; It is:

&gt; ****Can thin-film deposition, CMP, BEOL metallization, ion implantation, Ge epitaxy, and hybrid bonding be co-optimised inside one manufacturable window?****

&gt; That is why the integration-control point becomes uniquely valuable.

&gt; ****The physics did not suddenly change. The tolerance budget did.****

## A different way to read the CPO headlines

The market reaction to CPO has been swift.

IDTechEx forecasts the co-packaged-optics market to exceed $20 billion by 2036, growing at a 37% CAGR from 2026 to 2036. NVIDIA and Broadcom are pulling CPO into the centre of AI networking roadmaps. Foundry roadmaps now contain CPO line items that did not exist in the mainstream conversation only a short time ago.

In public markets, “CPO exposure” is quickly becoming a narrative in itself. But a lot of that conversation still stops at roadmaps and TAM. Very little of it asks where the actual manufacturing windows are tightest.

That is the gap I kept noticing while reading the NVIDIA, Broadcom, and foundry roadmaps: the slides tell you where bandwidth is going, but they rarely tell you which tolerance budget hurts first.

Read the headlines, and the story sounds clean:

Copper runs out of room.

Light moves closer to the chip.

Photons beat electrons.

Problem solved.

But when those slides are decomposed into actual unit-process steps, the bottlenecks are not purely optical.

They sit at the boundary between process modules that each look solved on paper: thin-film deposition, CMP, ion implantation, BEOL metallization, hybrid bonding, and Ge epitaxy.

Each module has decades of engineering maturity.

The difficulty is forcing all of them to coexist under one CPO thermal, optical, electrical, and yield budget.

That is when tolerances collapse by one to two orders of magnitude.

A simple example captures the whole issue.

In conventional BEOL Cu damascene, post-CMP surface roughness of Rq ≈ 1–2 nm can be excellent. Current flowing through copper does not meaningfully care about that scale of surface variation.

But if a SiN waveguide is placed near or above that copper-integrated stack, the same surface starts interacting with telecom-wavelength light. What is invisible noise to electrons can become measurable dB/cm loss to photons. The exact magnitude depends on roughness amplitude, correlation length, sidewall versus top-surface contributions, mode overlap, waveguide geometry, and cladding design.

The point is not a single number.

The point is that the same manufactured surface receives two different verdicts from two different physical systems.

That is the CPO problem.

## Failure Mode #1: Drift in SiN waveguide propagation loss

### Where thin-film deposition and CMP jointly decide the fate of a single optical path

****Key window:**** SiN waveguide loss is not just a design variable. In reported foundry-compatible flows, it is strongly tied to film quality, CMP roughness, correlation length, and post-processing. The practical target is optical-grade roughness, not ordinary BEOL planarity.

The first leg of a CPO optical path is often a SiN waveguide. Its quality directly sets the optical power budget.

A typical CPO optical engine may start with finite laser launch power, then lose margin through modulation, routing, coupling, and detection. Every additional dB of insertion loss is a direct hit on system reliability and energy efficiency.

SiN waveguide propagation loss has three main sources:

1. Intrinsic material absorption, including Si-H and N-H bond absorption

2. Surface and sidewall scattering, especially relevant at telecom wavelengths

3. Geometric non-uniformity from lithography and etch

The second source is where process integration becomes decisive.

Scattering loss is not fixed by optics alone. It is strongly shaped by the deposition recipe, the post-deposition anneal, the CMP process, and the roughness correlation length left behind by the manufacturing flow.

A 2023 study of foundry-compatible deposited SiN showed how large the process delta can be. PECVD SiN without CMP showed a loss above 10 dB/cm, while PECVD plus CMP brought a loss below 1 dB/cm. With additional annealing, the reported loss could fall further, reaching 0.28 dB/cm with RTA and 0.06 dB/cm with furnace annealing in the reported flow.

The takeaway is simple:

Going from “PECVD as deposited” to “PECVD plus CMP plus anneal” can buy roughly two orders of magnitude in optical loss.

But that improvement is not free.

Every extra 1 dB of link loss requires about 26% more optical launch power, because 10^(0.1) ≈ 1.26. More optical power means more heat, more thermal drift, and more reliability pressure.

This is why waveguide roughness is not a cosmetic metric.

It is a system-level power and reliability variable.

### The thermal-budget conflict

LPCVD SiN can produce dense, high-quality films at around 780°C. That high temperature helps drive out hydrogen-related bonds and improves film quality.

But 780°C is incompatible with a BEOL copper environment.

PECVD SiN can be deposited at roughly 300–400°C, making it BEOL-compatible. But PECVD films typically carry higher hydrogen content, lower density, higher stress, and stronger dependence on deposition microstructure and post-processing.

This is the first core CPO conflict:

****The optical layer wants high-temperature film quality. The package integration stack allows only low-temperature processing.****

The practical industry answer is PECVD plus post-processing:

Low-temperature deposition → CMP planarization → low-thermal-budget anneal.

The process window is narrow because the result depends on multiple tools that historically were not optimised as one optical system.

### Why CMP becomes the hinge

In standard BEOL copper CMP, the objective is planarity and residue removal. Rq below 1 nm is already high-end work.

But SiN waveguide CMP moves toward optical-grade flatness. The draft process targets discussed in the literature and engineering conversations are closer to Rq &lt; 0.3 nm, with sidewall roughness, correlation length, and particles all contributing to loss.

That implies three simultaneous requirements:

1. Smaller abrasive particle size

2. Lower scratch generation during pad conditioning

3. Near-zero post-CMP particle contamination

This is CMP being asked to behave like optical polishing, but at semiconductor wafer throughput.

That combination is the hard part.

## Failure Mode #2: Voids at the EIC-PIC Cu-Cu hybrid-bonding interface

### Where BEOL copper damascene recess control determines CPO’s electro-optical conversion fate

****Key window:**** the Cu surface cannot simply be “flat.” In reported hybrid-bonding experiments, the useful recess window sits in the few-nanometer range: too shallow risks Cu protrusion and failed dielectric bonding; too deep risks insufficient Cu contact and void formation after anneal.

TSMC COUPE’s important manufacturing idea is not simply that it uses silicon photonics. It is that the electronic IC and photonic IC can be brought extremely close together through advanced 3D integration.

This interface matters because photonic chips need area, while electronic drivers and SerDes circuits benefit from advanced logic nodes. A long copper path between them defeats much of the energy and latency benefit.

That is why wafer-scale EIC-PIC hybrid bonding becomes a key CPO control point.

The problem is that hybrid bonding turns copper from “just a conductor” into a structural and electro-optical interface.

### The counterintuitive Cu recess window

The critical pre-step in hybrid bonding is CMP.

The wafer surface contains both dielectric and exposed copper. Before bonding, the dielectric surfaces must make intimate contact. During annealing, copper expands upward and completes the electrical connection.

That means the copper must sit slightly below the dielectric surface before bonding.

Too high, and the dielectric surfaces cannot bond properly.

Too low, and the copper does not make good contact after annealing.

In the cited bonding literature, the practical optimal window is only a few nanometers wide: Cu recess around 3–5 nm, with failure modes appearing when recess becomes too shallow or too deep.

That is the second core CPO conflict:

****Hybrid bonding uses BEOL copper, but demands FEOL-grade surface precision.****

Conventional copper damascene CMP can tolerate a wider process window. CPO hybrid bonding tightens the problem dramatically because the target must be hit across a large number of pads on a 300 mm wafer.

This is not only a resistance issue.

It is a yield issue.

And in CPO, yield compounds brutally.

For illustration, if a package integrates 36 optical paths and each path has a 99% yield, the package-level yield is 0.99³⁶, or about 70%, before counting any other package defect.

That is why a “small” per-element process miss becomes a system-level manufacturing problem.

### The other hidden failure points

Cu recess is only the first issue.

Copper surface oxidation can introduce a thin CuO layer before bonding. A low-temperature anneal may not fully remove that interface layer, raising resistance and weakening the bond.

Interface voids can appear due to grain structure, non-uniform bonding, local contamination, or thermal cycling. Voids are not just electrical defects. They are stress concentrators.

CTE mismatch between the EIC, PIC, dielectric layers, and metal stack creates long-term reliability risk.

Electromigration also changes the meaning at a hybrid-bonding interface. The interface is not a conventional continuous copper line; it is a non-native Cu-Cu interface that may behave differently under high current density and thermal stress.

In older BEOL thinking, copper was evaluated mainly as a current path.

In CPO, copper becomes an electro-optical integration surface.

That is a different standard.

## Failure Mode #3: Dark-current drift in Ge photodetectors

### Where ion implantation and defect management decide whether the optical signal can be heard

****Key window:**** the detector must simultaneously hit dark-current, responsivity, bandwidth, and BEOL thermal-budget targets. That is hard because the best Ge material quality usually wants more temperature than the BEOL stack is willing to give.

After light travels through the waveguide and crosses the integrated optical path, it must be converted back into an electrical signal.

That conversion is typically done with Ge or SiGe photodetectors.

Ge is attractive because silicon does not absorb telecom wavelengths efficiently, while germanium can absorb 1310 nm and 1550 nm light and remains Group IV, making it more CMOS-compatible than III-V materials such as InGaAs.

But the defining metric is not just responsivity.

It is dark current.

Dark current is the current that flows even when no light is present. It raises the noise floor, reduces sensitivity, and consumes optical-link margin.

### The lattice-mismatch problem

Ge-on-Si has a fundamental materials problem: the lattice mismatch between Ge and Si is about 4.2%.

That mismatch generates threading dislocations during epitaxy. Each dislocation can act as a recombination centre and contribute to dark current.

Typical threading-dislocation-density ranges can vary by orders of magnitude depending on the epitaxy and anneal process. In broad terms, unoptimized epi can sit around 1⁰⁸–1⁰⁹ cm⁻², optimised SiGe buffer and cyclic anneal flows can move toward 1⁰⁶–1⁰⁷ cm⁻², and leading research demonstrations can push below 1⁰⁵ cm⁻².

That is why the detector problem is not purely optical.

It is materials and defect engineering.

### Ion implantation versus in-situ doping

Ge photodetectors need doped regions. There are two broad routes.

Ion implantation plus RTA gives precise placement and concentration control and fits mainstream CMOS thinking. But implantation damage in Ge can be severe, and end-of-range defects can become dark-current centres.

In-situ doping during epitaxy avoids implantation damage, but profile control, process stability, and EHS controls become more difficult.

A 2021 **Optics Express** paper cited in the draft found that in-situ As doping during Ge seed-layer growth produced dramatically lower dark current than the ion-implant route.

That is not an optics breakthrough.

It is a doping-process breakthrough.

### The BEOL thermal-budget squeeze

The hardest case is BEOL-compatible Ge detector integration.

High-quality Ge epitaxy often wants temperatures around 700°C. Dislocation annealing can want even higher temperatures. Dopant activation can also require temperatures above what BEOL copper and low-k materials can comfortably tolerate.

But BEOL integration forces the process below roughly 450°C.

That is the third core CPO conflict:

****Ge detectors want high-temperature material quality, but CPO integration caps the temperature budget.****

So the detector may be forced to operate below its theoretical performance ceiling, not because detector physics is poorly understood, but because the integration stack will not allow the ideal process.

## The underlying conflict

Put the three failure modes side by side, and the pattern becomes clear.

CPO requires FEOL-grade process quality at BEOL thermal budget.

SiN waveguides need low-loss film quality, but CPO pushes them toward low-temperature deposition and post-processing.

Cu-Cu bonding uses BEOL metallization, but demands a few-nanometer recess window and wafer-scale uniformity.

Ge detectors want high-temperature epitaxy and annealing, but BEOL integration limits the thermal budget.

This cannot be solved by a single better optical component.

It requires cross-module process co-design:

Deposition with CMP.

CMP with hybrid bonding.

Epitaxy with ion implantation.

Thermal budget with optical loss.

Package yield with device-level variation.

That is why CPO is a process-integration story.

And that is why the integration-control point becomes unusually valuable.

The early production phase of CPO should favour players that can see and control the FEOL, BEOL, 3D integration, and advanced-packaging boundary at the same time.

That does not mean one player owns the entire chain.

Optical-component vendors, switch-ASIC companies, laser suppliers, packaging houses, foundries, and system integrators all remain critical.

But the party that can make the cross-module tradeoffs has a different kind of leverage.

CPO is not won by the component that looks best alone.

It is won by the integration window that survives production.

## What this means for investors

When evaluating CPO-exposed companies, do not only ask whether a company “has silicon photonics.”

That question is too broad.

The sharper question is whether the company controls a manufacturing window that becomes harder as CPO moves from roadmap to production.

Ask more specific questions:

Does it have long-running SiN process R&amp;D capability?

Does it understand PECVD/LPCVD optical-quality tradeoffs?

Does it control CMP at optical-grade roughness?

Does it have production-scale hybrid-bonding experience?

Does it have low-thermal-budget Ge epitaxy and detector IP?

Can it explain package-level yield, not just device-level performance?

The credible list becomes much shorter when asked this way.

This is also why I would separate ****product exposure**** from ****process-control exposure****.

Product exposure is easier to see: optical engines, switch ASICs, pluggable modules, CPO roadmaps, and customer announcements.

Process-control exposure is easier to miss: low-temperature deposition, optical-grade CMP consumables, post-CMP cleaning, hybrid-bonding tools, wafer-level inspection, in-line metrology, and reliability qualification.

The market often prices the first category faster because it is easier to narrate.

But if CPO is fundamentally a process-integration problem, the second category may control the yield windows that decide who can actually ship.

That does not make every equipment, materials, or metrology supplier a “CPO winner.”

It means the right due diligence question changes.

Do not only ask who has the best optical story.

Ask who controls the process window that the optical story depends on.

## What this means for process engineers

CPO is not a foreign technology.

It is the extreme application of skills that already exist in thin-film deposition, CMP, BEOL metallization, ion implantation, etch, epitaxy, metrology, and reliability engineering.

The difference is that the success criteria have moved.

One thing I have noticed in conversations with BEOL and CMP engineers is that some of them initially do not think of themselves as “photonics people.” Then CPO arrives, and the boundary moves: their roughness, recess, cleaning, and reliability windows suddenly become optical-link variables.

A surface that is good enough for electrons may not be good enough for photons.

A thermal budget that is acceptable for copper may not be sufficient for Ge.

A CMP window that is respectable for BEOL may be too loose for hybrid bonding.

That is why the photonic era may end up rewarding process engineers more than people expect — especially the ones who are willing to think across modules instead of defending a single process silo.

A note on metrology: when I ask about AFM roughness, I do not mean AFM is the only high-volume answer. AFM is often a process-characterization and excursion-analysis tool, not a fast in-line screen for every wafer. At scale, the better question becomes whether the company has a wafer-level metrology loop that connects AFM sampling, OCD or scatterometry, ellipsometry, defect inspection, test structures, microring maps, and optical cut-back data into one process-control system.

## Closing: the real winners of the photonic era are process engineers

In a keynote deck, CPO looks like an optical story.

When you open the manufacturing flow, it becomes something else.

The optics has been clear for decades.

What decides mass production is whether the process stack can simultaneously deliver:

- SiN waveguide CMP roughness low enough for optical loss targets

- Cu recess control tight enough for hybrid bonding

- Ge detector dark current low enough under BEOL thermal budget

- Wafer-scale uniformity and package-level yield high enough for commercial deployment

The more I study AI infrastructure, the more I think the least glamorous questions are often the most revealing ones.

The next time a company claims it is ready for CPO production, the most useful question may not be about bandwidth.

It may be this:

****What does your SiN waveguide AFM roughness distribution look like?****

The companies that can answer immediately are the ones that are actually close — and they rarely lead with bandwidth slides.

## Further reading

For readers who want to go deeper, these are the references and topic areas I would start with:

1. ****NVIDIA Spectrum-X Photonics / Quantum-X Photonics**** — official announcements and technical materials on co-packaged optics for AI networking.

2. ****TSMC COUPE / SoIC / 3DFabric materials**** — public disclosures on compact universal photonic engines, hybrid bonding, and advanced packaging integration.

3. ****Broadcom Tomahawk 6 Davisson**** — public materials on CPO Ethernet switch architecture and early customer availability.

4. ****IDTechEx CPO market forecast**** — useful for understanding the commercial timeline and market-size expectations around co-packaged optics.

5. ****Ultra-low-loss silicon nitride photonics**** — papers on PECVD / LPCVD SiN waveguides, CMP planarization, annealing, and propagation-loss reduction.

6. ****Cu-Cu hybrid bonding reliability**** — literature on Cu recess control, interface voids, surface oxidation, electromigration, and wafer-scale hybrid bonding.

7. ****Ge-on-Si photodetectors for BEOL photonics**** — papers on Ge epitaxy, threading dislocation density, dark current, in-situ doping, implantation damage, and low-thermal-budget integration.

8. ****BEOL copper interconnect reliability**** — background on copper damascene, low-k integration, electromigration, and post-Cu interconnect scaling.

## References

1. NVIDIA, “[NVIDIA Announces Spectrum-X Photonics, Co-Packaged Optics Networking Switches to Scale AI Factories to Millions of GPUs](https://nvidianews.nvidia.com/news/nvidia-spectrum-x-co-packaged-optics-networking-switches-ai-factories),” March 18, 2025.

2. TSMC, “[TSMC Debuts A13 Technology at 2026 North America Technology Symposium](https://pr.tsmc.com/english/news/3302),” April 23, 2026.

3. Broadcom, “[Broadcom Announces Tomahawk 6 — Davisson, the Industry’s First 102.4-Tbps Ethernet Switch with Co-Packaged Optics](https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-tomahawkr-6-davisson-industrys-first-1024),” October 8, 2025.

4. IDTechEx, “[Co-Packaged Optics (CPO) 2026–2036](https://www.idtechex.com/en/research-report/co-packaged-optics-cpo/1138).”

5. Ji, X. et al., “[Ultra-Low-Loss Silicon Nitride Photonics Based on Deposited Films Compatible with Foundries](https://arxiv.org/abs/2301.03053),” 2023.

6. Bose, D. et al., “[Anneal-free ultra-low loss silicon nitride integrated photonics](https://www.nature.com/articles/s41377-024-01503-4),” **Light: Science &amp; Applications**, 2024.

7. Cheemalamarri, H. K. et al., “[Void-free Cu/dielectric hybrid bonding at low-temperature enabled by ultrathin metal passivation engineering for 3D-IC applications](https://www.nature.com/articles/s44172-026-00649-w),” **Communications Engineering**, 2026.

8. Lu, T.-F. et al., “[Effect of Cu Film Thickness on Cu Bonding Quality and Bonding Mechanism](https://www.mdpi.com/1996-1944/17/9/2150),” **Materials**, 2024.

9. Lin, Y. et al., “[Low-power and high-detectivity Ge photodiodes by in-situ heavy As doping during Ge-on-Si seed layer growth](https://opg.optica.org/abstract.cfm?uri=oe-29-3-2940),” **Optics Express**, 2021.

10. Marzen, S. et al., “[High performance germanium on silicon photodiodes for back-end-of-line photonic integration](https://pubs.aip.org/aip/apl/article/123/11/111105/2910867/High-performance-germanium-on-silicon-photodiodes),” **Applied Physics Letters**, 2023.

11. Edelstein, D., “27 Years of Copper Interconnects and Beyond: BEOL for Current and Future Technology Nodes,” **IEDM**, 2024.

## Author note

I develop technical training materials on semiconductor manufacturing, with a focus on connecting unit processes — deposition, lithography, etch, CMP, implantation, BEOL, and process integration — to advanced packaging and AI hardware infrastructure.

This article is part of my ongoing attempt to translate semiconductor process details into strategic language for engineers, investors, and technology operators. The goal is not to review every paper in the CPO literature, but to identify the manufacturing constraints that are most likely to matter when a technology moves from roadmap slides to high-volume production.

All views are my own.

## Disclaimer

This article is for research and educational purposes only. It is not investment advice, technical qualification advice, legal advice, or a recommendation to buy or sell any security.

The analysis is based on publicly available academic papers, company disclosures, conference materials, industry reports, non-confidential technical context, and my personal interpretation of those materials.

Any company, technology, or process mentioned may have internal capabilities, production data, or design choices that are not publicly disclosed. Actual production specifications may differ across vendors, process generations, and customer programs.

Errors or omissions are my own. Corrections with public citations are welcome.

## Disclosure

No company mentioned in this article has reviewed, sponsored, approved, or compensated me for this work.

This article is based on publicly available information, non-confidential technical context, and my personal analysis and opinions. It does not rely on proprietary, confidential, or material non-public information.

I may currently hold, and may buy or sell, securities of companies mentioned in this article or in the broader AI infrastructure and semiconductor ecosystem at any time without further notice.

Nothing in this article constitutes investment advice, a financial recommendation, or a solicitation to buy or sell any security. Readers should conduct their own due diligence.

## Comments invitation

Comments and disagreements are welcome — especially if you can point me to public papers, conference proceedings, or vendor disclosures I missed. I would rather be corrected with an open citation than confirmed with a private one.