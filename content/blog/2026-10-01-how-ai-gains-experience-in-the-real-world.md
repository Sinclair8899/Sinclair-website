---
title: "How AI Gains Experience in the Real World"
date: 2026-10-01
draft: false
tags: ["agentic-ai", "tacit-knowledge", "physical-ai", "spatial-intelligence", "world-models"]
description: "To work in the physical world, it also needs an environment in which it can observe, act, receive feedback, and test the results."
canonical: "https://medium.com/@sinclairhuang/how-ai-gains-experience-in-the-real-world-d63b589b00a0"
cta: "subscribe"
---

*繁體中文版：[AI 的經驗如何在真實世界養成](/blog/2026-10-01-how-ai-gains-experience-zh/)*

*Reflections on World Labs and learning through code and fieldwork*

Po-Sung (Sinclair) Huang | October 1, 2026

![Houses with sloping roofs along a residential street under a partly cloudy sky](/images/blog/2026-10-01-how-ai-gains-experience-in-the-real-world/figure1-roofs.jpg)

*Figure1. Sloping residential roofs seen during my travels brought to mind my friend’s work on site. Photograph by the author.*

## A question prompted by an acquisition

On September 28, 2026, AMD announced an agreement to acquire World Labs in an all-stock transaction valued at approximately $8.2 billion. The deal is expected to close by year-end, subject to the required approvals. After closing, Fei-Fei Li will become AMD’s executive vice president and chief scientist.[1] In her announcement, she wrote about a universe made of real things, rather than words alone.[2]

Having attended several of Li’s talks and discussions, I have long been interested in spatial intelligence and physical AI. But using AI and dealing with everyday problems has made another question more pressing for me: how does expertise develop? AI already helps me turn ideas into working tools. To work in the physical world, it also needs an environment in which it can observe, act, receive feedback, and test the results.

## AI makes it easier for me to learn by doing

A year ago, writing code in Colab often meant pasting code, running it, getting an error, and taking that error back to an AI for help. Ten or more rounds were common. With Claude Code and Codex, many debugging and revision steps can now continue within the tools. I still test and review the work, but spend much less time moving code and messages back and forth.

I have also used different AIs to help write Python and reproduce parts of the workflow I liked in EViews, which I used for my EMBA thesis. I connected database extracts to Python for statistical analysis and built a simple app called PyViews. I have cross-checked the core regressions against linearmodels, an independently developed Python library, and the coefficients matched exactly. A direct comparison with EViews is still pending, as my license has expired. I did this to learn, for enjoyment and curiosity, and to explore AI’s boundaries.

An idea can quickly become something I can use, inspect, and revise. The relatively low cost of trying again makes me more willing to experiment. Once I know what I want to solve, choosing suitable tools or agent skills can turn a small idea into a different way of working. Building and checking a tool with AI is itself a learning experience.

[![PyViews screenshot: a sidebar for choosing the sample and fiscal years, and a command window showing panel least squares regression output](/images/blog/2026-10-01-how-ai-gains-experience-in-the-real-world/figure2-pyviews-en.png)](/images/blog/2026-10-01-how-ai-gains-experience-in-the-real-world/figure2-pyviews-en.png)

*Figure2. PyViews, built with AI assistance. Choose the sample and years, type one command, and the panel regression runs. The core results match an independent Python library; a direct comparison with EViews is still pending.*

What the tool taught me came less from building it than from checking it. The first regression ran without a single error message, yet several problems were hidden in it. IBM’s income statement had never been downloaded, so the company silently dropped out of the sample. Alphabet’s two share classes were counted as two firms. Twenty healthcare companies, which I had included on the assumption that AlphaFold 3 would soon lift biotech stocks, distorted the results: a few biotechs with almost no revenue made R&D-to-revenue ratios meaningless. Even an exclusion rule written by the AI contradicted its own example and was caught only when tested against the data. The AI’s errors were found through my sense of whether the numbers made sense; my own mistaken assumption was exposed by the data. Each correction, kept with what I had expected and what I actually found, became a small version of the experience record I propose below.

## Car repairs and roofs bring me back to the field

Digital work often leaves reproducible test records. In a physical setting, a crucial condition may never have been measured, or may appear only briefly. My old car developed an intermittent electronic parking brake fault: a warning appeared, disappeared, and sometimes could not be reproduced at the workshop. I sent diagnostic screens and fault codes to an AI. Following its advice, I spent NT$23,000 on a refurbished assembly. The warning returned. The AI then shifted its suspicions toward wiring and communication between modules. After weeks of discussion, the cause remained unresolved.

The AI helped organise possibilities and suggested what evidence to retain. But a plausible hypothesis is not a confirmed diagnosis. Information may be missing; the reasoning may also be wrong. A mechanic can inspect connectors, listen, and compare the symptoms with past cases. Deciding how to obtain the right evidence is part of expertise.

A friend in the United States who does small construction and plumbing jobs gave me another perspective. After he took on a bathroom project, I saw his hand-drawn plan on the table. His son had studied civil engineering and used tools such as AutoCAD, but my friend preferred to measure on site and draw by hand. He confidently told me that, in his view, AI would not replace his practical work.

Walking through the neighbourhood with him, I listened as he pointed out sloping roofs he had repaired and maintained. Looking at the one- and two-story homes, I imagined a robot clumsily climbing onto a roof. The picture amused me. At that moment, it felt far removed from everyday life.

The difference between a hand sketch and a computer drawing does not fully explain his confidence. What interests me is how he connects measurements, plans, and actual construction. A drawing still has to work under the conditions on site. Could AI help him organise estimates and past cases, reduce some of the burden, and make his experience easier to preserve?

Michael Polanyi’s The Tacit Dimension describes how what we know can exceed what we can articulate.[3] Skill and judgment do not always fit neatly into manuals. Yet experience can still be recorded in part. A repair report that only says “part replaced” is inadequate for the next decision. It should also explain why the part was replaced, what improvement was expected, and whether that improvement occurred.

## Practice from a machine and guidance from a coach

During a walk in a Seattle park, I came across a tennis court where a sister and brother were practising with a ball machine. A female coach stood nearby and later fed balls herself and joined them on court. They thought I was waiting to use the court. I took the opportunity to ask about the machine, including whether it could coach. She smiled and said perhaps in the future, but for now a coach was still needed to identify a learner’s blind spots and weaknesses and provide focused guidance.

The encounter helped me see how practice opportunities and useful feedback belong together. The machine supplies balls; the coach watches the players and adjusts the focus. Counting repetitions is not enough. We also need to know what is improving and which mistakes keep recurring.

## The litter box could not smell what we could not tolerate

The remaining litter could no longer cover the waste, and the machine smelled; another cat would not go in. After smelling it, I judged that this litter could not stay, and I dumped it. Pressing Cycle to sift out the clumps would have been another option. The machine can carry out either command, but it cannot smell the odour or know whether that odour has become intolerable to the people living with it. An AI explanation afterwards described the buttons and called the unit fully automatic; it did not supply that on-site judgment. The motion can be delegated. The sense of which motion is required still belongs to a person there.

![An automatic litter box with an orange cat curled up inside the drum](/images/blog/2026-10-01-how-ai-gains-experience-in-the-real-world/figure3-litter-box.jpg)

*Figure3. My son’s automatic litter box. The machine carried out the command; it could not smell whether the litter had become intolerable. Photograph by the author.*

## A concrete proposal: checkable experience records

I have long wondered whether perception, localisation, and navigation methods from self-driving cars could be adapted to drones, letting AI observe the world through a vehicle and build observation logs. The methods share common ground, but three-dimensional motion and sensing conditions differ, so adaptation and validation remain necessary. Whatever the vehicle, though, a more basic question remains: in what form should experience be kept?

Children learn through exploration and feedback. Experts develop by facing varied cases, identifying failures, and changing their approach. AI needs appropriate tasks and evaluation conditions too. Repetition alone does not guarantee improvement; poor feedback may reinforce errors.

What I want to propose is a checkable experience record. At a minimum, it should do four things: preserve the environment and original data; separate actual observations from model inferences; record the action taken and what was expected at the time; and compare that expectation with the actual outcome. When results differ, it gives grounds to ask whether evidence was missing, the judgment was wrong, or the conditions had changed. Had my car repair been recorded this way from the start, weeks of back-and-forth would not have kept circling back to possibilities already ruled out. Improvement must also be measured, rather than simply narrated fluently by an AI.

A family member told me that his company requires installation and maintenance reports to be entered into an AI system. Engineers can search practical cases from customer factories around the world, alongside installation procedures and principles. Site photographs and videos have not yet been included. Connecting those images to equipment conditions, interventions, and outcomes could make the records more useful. Searchable reports do not mean the AI has acquired practical skills, but they help people retrieve experience and judge its relevance.

## Simulation and the need for real testing

World Labs is developing such training environments. In September 2026, it introduced Atlas, covering spatial reconstruction, spacetime simulation, and robotic Real-to-Sim workflows. In July, it reported work that builds simulations from real tasks and tests policies learned there on physical robots.[4][5] These are the company’s reported capabilities and results; their scope depends on the tasks and test conditions. A world model supplies representations and simulation. Physical action also requires sensing, control, and execution systems.

Drone research offers concrete examples. The 2023 Swift system combined simulation training with real flight data to correct errors before competing on a real racecourse.[6] A separate 2021 study trained policies entirely in simulation and transferred them successfully to previously unseen real environments.[7] Not every training step must take place in the field, but reliability still needs real testing.

This reminds me of computation and wet experiments in drug development: models propose candidates and predictions, while experiments provide evidence for revision. A 2026 molecular discovery study connected algorithmic design, synthesis, and biological testing to choose the next round of exploration.[8] There is no shortcut here: plausible reasoning cannot substitute for checking actual effects. Simulation and automation can accelerate that process.

## Preserving experience and remembering human worth

This changes how I think about personal AI. If it preserves my cases, interventions, and subsequent outcomes, it can reduce repeated guessing and help distinguish rejected hypotheses from those still lacking evidence. General knowledge becomes more useful when connected to an individual history. Keeping data on a personal device or in a private environment does not automatically improve judgment. Complete records, suitable retrieval, and continued correction are still needed.

Using AI to build tools makes learning and experimentation easier. The work of my friend and the engineers reminds me to test judgment against results. I want to connect these experiences: make it easier to try, and retain enough about successes and failures to inform the next attempt.

On another occasion, a friend’s wife attended a dance class. Watching a Ukrainian teacher and a group of eager students, I felt the beauty of human spirit and artistic expression. For a moment, I set AI aside and simply enjoyed watching people learn and express themselves.

Reading Ephesians over the past two days also made me pause. Its description of us as God’s handiwork (2:10) prompted a personal question: as AI does more work, am I still measuring human worth by output and efficiency? My faith reminds me that people deserve to be valued in themselves. I want to use AI to help people learn and ease their burdens. As tools become more capable, I need greater discernment, honesty about their results and limitations, and attention to how they affect the people around me.

Experience is valuable precisely because it comes from real people trying and taking responsibility in the real world. AI can help us record that experience more completely, but its owner remains human.

## Sources

[1] AMD (September 28, 2026). AMD to Acquire World Labs to Advance the Future of AI Compute. [Source](https://ir.amd.com/news-events/press-releases/detail/1299/amd-to-acquire-world-labs-to-advance-the-future-of-ai-compute)

[2] Fei-Fei Li (September 28, 2026). To Seek a Newer World. [Source](https://drfeifei.substack.com/p/worldlabs-joining-amd)

[3] Polanyi, M. (2009; originally published 1966). The Tacit Dimension. University of Chicago Press. [Source](https://press.uchicago.edu/ucp/books/book/chicago/T/bo6035368)

[4] World Labs (September 1, 2026). Atlas: A World Model for Spatial Intelligence. [Source](https://www.worldlabs.ai/blog/atlas)

[5] World Labs (July 28, 2026). Building Worlds That Train Robots. [Source](https://www.worldlabs.ai/blog/real-to-sim-to-real)

[6] Kaufmann, E., et al. (2023). Champion-level drone racing using deep reinforcement learning. Nature, 620, 982–987. [Source](https://pmc.ncbi.nlm.nih.gov/articles/PMC10468397/)

[7] Loquercio, A., et al. (2021). Learning High-Speed Flight in the Wild. Science Robotics, 6(59), eabg5810. [Source](https://arxiv.org/abs/2110.05113)

[8] Piticari, A.-S., et al. (2026). Algorithm-driven, phenotype-directed bioactive molecular discovery. Communications Chemistry, 9, 267. [Source](https://www.nature.com/articles/s42004-026-02066-8)

## Further Reading

Li, F.-F. (2025). From Words to Worlds: Spatial Intelligence is AI’s Next Frontier. Li’s full case for spatial intelligence and world models. [Source](https://drfeifei.substack.com/p/from-words-to-worlds-spatial-intelligence)

Li, F.-F. (2023). The Worlds I See: Curiosity, Exploration, and Discovery at the Dawn of AI. Flatiron Books. Li’s memoir, tracing the path that led her to spatial intelligence.

Sennett, R. (2008). The Craftsman. Yale University Press. On how hand and mind together form practical judgment.

Crawford, M. B. (2009). Shop Class as Soulcraft. Penguin Press. A philosophy PhD turned motorcycle mechanic reflects on the knowledge embedded in manual work.

## Disclaimer

This essay shares the author’s personal experience and views. It is not automotive repair, investment, or other professional advice. Companies and transactions are mentioned only as context, not as investment recommendations. Descriptions of AI capabilities are based on public sources and may change as the technology develops. AI tools assisted with organising and proofreading this essay; the experiences, photographs, and views are the author’s own.

## Keywords

Spatial Intelligence, Physical AI, World Models, World Labs, Tacit Knowledge, Agentic AI, Experience Records, Human–AI Collaboration

## About the Author

Po-Sung (Sinclair) Huang is a retired executive, now a consultant and independent researcher with about 30 years of cross-industry experience in Taiwan’s electronics, chemical, and life sciences sectors. He holds an EDBA from HEC Liège and serves as Special Advisor to the Chairman at Continental Carbon Co., Ltd. His research interests include AI and semiconductors, industrial competitiveness, and technology valuation.

ORCID: 0009–0007–8173–5672 | Website: sinclairhuang.org

---

*This article was originally published on Medium. [Read the full version with charts and figures →](https://medium.com/@sinclairhuang/how-ai-gains-experience-in-the-real-world-d63b589b00a0)*