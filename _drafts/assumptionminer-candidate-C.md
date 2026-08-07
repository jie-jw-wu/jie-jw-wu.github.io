---
layout: post
title: "What Is the AI Assuming? (A Short Introduction to AssumptionMiner)"
permalink: /assumptionminer.html
description: A short Q&A-style introduction to my paper on the hidden assumptions behind AI-generated code.
published: false
---

*A short, plain-language Q&A about my paper, [AssumptionMiner: Extracting, Tracing, and Revising Implicit Assumptions in LLM Code Generation](https://arxiv.org/abs/2607.22898).*

**Q: What problem does this paper tackle?**

When you ask an AI like ChatGPT to write a program, your request is never complete. "Build me a to-do list app" doesn't say what happens when the list is empty, whether tasks are saved after you close the app, or what counts as a valid task name. The AI can't ship code with question marks in it — so it silently picks answers to all the questions you never asked. Those silent picks are called **implicit assumptions**, and they decide how your program actually behaves. Sometimes they're fine. Sometimes they're the reason the program fails, or isn't secure. Either way, you were never told.

**Q: What's the proposed fix?**

A system I call **AssumptionMiner**. The idea fits in one sentence: *when the AI writes code, it must also hand over the list of assumptions it made.* The code comes with a structured, human-readable record — an "assumption layer" — of every gap-filling decision: how inputs are checked, how errors are handled, how data is stored and formatted, and what was assumed about performance and security.

**Q: Okay, I can see the list. Then what?**

You act on it. Each assumption can be confirmed ("yes, that's what I meant") or revised ("no — do this instead"). And because AssumptionMiner tracks which parts of the code each assumption produced, revising one assumption regenerates only the code it touched, leaving everything you already approved alone. It turns "regenerate and hope" into something closer to a conversation: the AI proposes, you dispose.

**Q: How do you know it works?**

The paper builds a benchmark of **180 intentionally ambiguous programming tasks** with **676 carefully annotated assumptions** — a test set for the question "did the AI notice everything it was assuming?" I evaluated several AI models on extracting assumptions, linking them to the right code, and supporting revision. A human-verified subset checks the hardest part: whether an assumption can be traced to the exact lines of code it shaped.

**Q: Why should someone outside software care?**

Because the pattern is universal. Any time you delegate a task described in ordinary language — to an AI or a person — the gaps in your description get filled by someone else's judgment. Good collaborators surface their judgment calls; bad ones bury them. Right now, AI buries them. This paper is a case study in forcing the judgment calls into the open, in a domain (code) where we can be mathematically precise about which decision influenced which outcome.

**Q: Where can I read more?**

The full paper is on [arXiv](https://arxiv.org/abs/2607.22898), and the code and benchmark are [openly available](https://doi.org/10.5281/zenodo.21535058). If you have thoughts or questions, I'd love to hear them.
