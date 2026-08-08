---
layout: post
title: "AssumptionMiner, Explained Simply"
permalink: /assumptionminer.html
description: "A short Q&A about our paper on making the hidden assumptions in AI-generated code visible, traceable, and fixable."
---

*Our paper [AssumptionMiner](https://arxiv.org/abs/2607.22898) was written for a research audience. This post explains it in plain language, as a short Q&A — no software engineering background needed.*

## What problem are you trying to solve?

When you ask an AI tool (like ChatGPT or GitHub Copilot) to write code, you describe what you want in ordinary language: "write a program that averages a list of scores." But everyday language always leaves things out. What if the list is empty? What if a score isn't a number? Should the result be rounded?

The AI doesn't ask. It silently makes a decision about every unstated detail and builds those decisions into the code. We call these **implicit assumptions**. They're invisible, but they determine how the software actually behaves — and when an assumption doesn't match what you really wanted, you get bugs that are hard to explain, because the "decision" that caused them was never written down anywhere.

## What's your solution, in one sentence?

When an AI generates code, it should also hand you a written list of the assumptions it made — and you should be able to correct any of them and have the code update accordingly.

## How does AssumptionMiner actually work?

Three capabilities, matching the three words in the paper's title:

- **Extracting.** The system generates code *plus* a structured list of assumptions: every gap in your request and how the AI filled it. Think of it as the AI showing its work.
- **Tracing.** Each assumption is linked to the exact lines of code it affects. The system analyzes the program's structure to build this map, so you can click an assumption and see precisely which code depends on that guess.
- **Revising.** If an assumption is wrong, you fix the assumption — not the code. The system then regenerates only the code connected to it, leaving everything else untouched.

## How do you know it works?

We first had to build a way to measure it, because none existed: a benchmark of **180 intentionally ambiguous programming tasks**, with **676 assumptions annotated by hand** (a portion carefully verified by human reviewers, linking each assumption to the code it affects). The benchmark is available for other researchers to use.

Two results worth knowing:

1. Linking assumptions to the code they govern is genuinely hard. Our best method — using an AI model to do the mapping — is right about **64%** of the time, ahead of simpler keyword-matching (about 57%), but far from perfect. We report this openly: it's a new problem, and there's room to improve.
2. Fixing an assumption the targeted way changes about **2.4× less code** than broader regeneration. That matters because in software, every changed line needs to be re-read and re-tested; fewer unnecessary changes means fewer new opportunities for error.

## Why should someone outside of programming care?

Because the pattern is universal. Any time you delegate a task with incomplete instructions — to a person or to an AI — the gaps get filled by someone else's judgment. With people, you can ask "why did you do it this way?" With AI-generated code today, there's usually no answer: the reasoning is discarded and only the code remains.

As AI writes more of the world's software, "what did the AI assume?" stops being an academic question and becomes a practical one about reliability and trust. Our position is simple: those assumptions exist whether or not we look at them — so we should build tools that let us look.

## Where can I read more?

The full paper is on [arXiv](https://arxiv.org/abs/2607.22898). Questions and feedback are always welcome.
