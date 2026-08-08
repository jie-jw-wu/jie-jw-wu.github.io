---
layout: post
title: "The Hidden Decisions Inside AI-Generated Code"
permalink: /assumptionminer.html
description: "A walkthrough of AssumptionMiner: a system that turns the silent guesses in AI-generated code into something you can see, check, and change."
---

*This post is a plain-language introduction to our paper, [AssumptionMiner: Extracting, Tracing, and Revising Implicit Assumptions in LLM Code Generation](https://arxiv.org/abs/2607.22898).*

## Try this experiment

Ask an AI assistant to do the following:

> "Write a function that takes a list of student scores and returns the average."

You'll get working code in seconds. Now look closer, because in that one sentence, you left at least four questions unanswered:

- What happens if the list is **empty**? (Return zero? Report an error?)
- What if a score is **not a number** — someone typed "N/A"?
- What if a score is **negative** or above 100?
- Should the average be **rounded**, and to how many places?

The AI answered every one of these questions for you — without telling you. Its answers are hidden inside the code. If the AI decided that an empty list should cause an error, and your data sometimes contains empty lists, your program will crash in production. Not because the AI made a mistake, but because it made a *choice* you never got to see.

Researchers call your one-sentence request an *incomplete specification*, and the AI's silent choices *implicit assumptions*. Every vague request forces the AI to make them. The question our paper asks is: **why do we let those choices stay hidden?**

## What AssumptionMiner does

Our system, **AssumptionMiner**, changes the output of AI code generation from "here's your code" to "here's your code, *and here's what I assumed to write it*." It works in three steps.

**Step 1: Extract the assumptions.** Along with the code, the system produces a structured list of every gap it had to fill:

> - A1: Assumed the score list is never empty.
> - A2: Assumed all scores are numeric values.
> - A3: Assumed the average is returned unrounded.

This list is not documentation written after the fact — it is generated as a first-class output, at the same time as the code.

**Step 2: Trace each assumption to the code it controls.** Behind the scenes, AssumptionMiner analyzes the structure of the generated program and builds a map from each assumption to the specific lines it governs. Select assumption A1, and the tool highlights exactly the lines that only work if the list is non-empty. This turns a vague worry ("did the AI guess right?") into something concrete you can inspect.

**Step 3: Revise, and regenerate only what changed.** Suppose A1 is wrong — empty lists do happen in your data. You edit that single assumption ("if the list is empty, return None"), and the system rewrites *only the code tied to A1*. The rest of the program — the parts you may have already read, tested, or trusted — stays exactly as it was.

## How we measured it

Claims are cheap; here's how we evaluated ours.

First, there was no good test set for this problem, so we built one: a benchmark of **180 deliberately ambiguous programming tasks with 676 hand-annotated assumptions**, including a human-verified subset where each assumption is linked to the code it affects. It's public, so other researchers can measure their own systems against it.

On that benchmark:

- The hardest step turns out to be tracing — figuring out *which code an assumption governs*. Our best approach, which uses an AI model as the mapper, gets this right **64.2%** of the time, beating a simpler keyword-based method (56.9%). Good, and honest evidence that this problem isn't solved yet.
- The payoff shows up at revision time: when a user corrects one assumption, targeted regeneration changes about **2.4× less code** than regenerating more broadly. In software, less unnecessary change is a real virtue — every changed line is a line someone has to re-check.

## The bigger picture

There's a growing conversation about *trust* in AI: can we rely on what these systems produce? Much of that conversation focuses on whether the output is right or wrong. Our paper argues for a complementary question: **what did the system decide on its own along the way?**

For AI-generated code, the answer used to be: nobody knows, it's all buried in the code. AssumptionMiner is a step toward a different answer — one where the AI's guesses are written down, connected to their consequences, and open to correction by the human who has to live with the result.

---

*Read the full paper on [arXiv](https://arxiv.org/abs/2607.22898).*
