---
layout: post
title: "What Is the AI Assuming? (A Short Introduction to AssumptionMiner)"
permalink: /assumptionminer.html
description: A short Q&A-style introduction to my paper on the hidden assumptions behind AI-generated code.
published: false
---

*A short, plain-language Q&A about my paper, [AssumptionMiner: Extracting, Tracing, and Revising Implicit Assumptions in LLM Code Generation](https://arxiv.org/abs/2607.22898).*

**Q: What problem does this paper tackle?**

When you ask an AI like ChatGPT to write a program, your request is never complete. The paper's running example: *"Implement a user authentication system that checks credentials and returns a session token."* That one sentence leaves open how passwords are protected, whether login tokens expire, what happens after failed attempts, where sessions are stored, and how fast any of it needs to be. The AI can't ship code with question marks in it — so it silently picks answers to all the questions you never asked. Those silent picks are called **implicit assumptions**, and they decide how your program actually behaves.

The result can be what I call *working-but-wrong* code: it runs, it passes tests, and it still violates your intent — say, by protecting passwords with MD5, an algorithm broken for decades. In my benchmark, every task carried at least two hidden assumptions; most carried three or four.

<figure style="margin: 28px 0; text-align: center;">
  <img src="assets/img/blog/am-fig1-teaser.png" alt="Before and after AssumptionMiner: five hidden assumptions in generated login code, invisible on the left, surfaced as an editable list on the right" style="max-width: 100%; border: 1px solid #e5e5e5; border-radius: 6px;">
  <figcaption style="font-size: 13px; color: #888; margin-top: 8px;">Five silent decisions in AI-generated login code — invisible on the left, surfaced and editable on the right (figure from the paper).</figcaption>
</figure>

**Q: What's the proposed fix?**

A system I call **AssumptionMiner**. The idea fits in one sentence: *when the AI writes code, it must also hand over the list of assumptions it made.* The code arrives with a structured, human-readable record — an "assumption layer" — of every gap-filling decision, sorted into six categories: input validation, data format, error policy, persistence, performance, and security. Each entry names the decision, the AI's rationale, and realistic alternatives it could have chosen instead.

**Q: Okay, I can see the list. Then what?**

You act on it. Each assumption is a card you can accept, edit, or reject:

<figure style="margin: 28px 0; text-align: center;">
  <img src="assets/img/blog/am-interface.png" alt="The AssumptionMiner interface: code with highlighted regions on the left, assumption cards with Accept, Edit, and Reject buttons on the right" style="max-width: 100%; border: 1px solid #e5e5e5; border-radius: 6px;">
  <figcaption style="font-size: 13px; color: #888; margin-top: 8px;">The review interface: each assumption links to the exact code it produced (figure from the paper).</figcaption>
</figure>

Because AssumptionMiner maps each assumption to the exact code regions it produced (via the code's underlying structure, called an abstract syntax tree), revising one assumption regenerates *only the code it touched* — everything you already approved stays put. It turns "regenerate and hope" into something closer to a conversation: the AI proposes, you dispose.

**Q: How do you know it works?**

The paper builds a benchmark of **180 intentionally ambiguous programming tasks with 676 annotated assumptions**, including a subset verified line-by-line by professional developers. An ensemble of two open-source models recovers hidden assumptions with an F1 score of 0.816 — about 3.6× the strongest baseline. And when you revise a single decision, targeted regeneration changes less than half as much code as regenerating the whole program:

<figure style="margin: 28px 0; text-align: center;">
  <img src="assets/img/blog/am-chart-edit.svg" alt="Bar chart: edit distance 0.24 for AssumptionMiner versus 0.31 to 0.57 for in-place edits, full regeneration, and manual reprompting" style="max-width: 100%;">
</figure>

Not everything is solved: pinpointing the *exact* decision (rather than its general category) remains hard for current models, and targeted edits occasionally leave the code inconsistent. The paper treats both as open problems, not footnotes.

**Q: Why should someone outside software care?**

Because the pattern is universal. Any time you delegate a task described in ordinary language — to an AI or a person — the gaps in your description get filled by someone else's judgment. Good collaborators surface their judgment calls; bad ones bury them. Right now, AI buries them. This paper is a case study in forcing those judgment calls into the open, in a domain (code) where we can be precise about which decision shaped which outcome.

**Q: Where can I read more?**

The full paper is on [arXiv](https://arxiv.org/abs/2607.22898), and the benchmark, code, and replication package are [openly available](https://doi.org/10.5281/zenodo.21535058). If you have thoughts or questions, I'd love to hear them.
