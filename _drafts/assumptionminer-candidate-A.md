---
layout: post
title: "When AI Writes Code, It Also Makes Decisions You Never See"
permalink: /assumptionminer.html
description: An accessible introduction to my paper AssumptionMiner, on surfacing the hidden assumptions AI makes when it writes code.
published: false
---

*This post introduces my recent paper, [AssumptionMiner: Extracting, Tracing, and Revising Implicit Assumptions in LLM Code Generation](https://arxiv.org/abs/2607.22898), for readers without a background in software engineering research.*

## The contractor who never asks questions

Imagine hiring a contractor to renovate your kitchen. You say, "I'd like new cabinets and more counter space." The contractor nods, disappears for a week, and comes back with a finished kitchen.

It looks great — until you notice the details. The cabinets are walnut (you wanted white). The outlets are hidden behind the coffee machine. The drawers open the wrong way for a left-handed cook.

None of these were mistakes, exactly. You never said what you wanted. The contractor had to decide *something*, so they decided quietly, and you only discovered their decisions after everything was built.

This is precisely what happens when AI writes code today.

## AI fills in the gaps — silently

Tools like ChatGPT and GitHub Copilot can write working programs from a plain-English request. But a plain-English request is almost never a complete specification. Here is the example that runs through my paper. Ask an AI to:

> *"Implement a user authentication system that checks credentials and returns a session token."*

Sounds complete, right? Yet a typical AI-generated implementation quietly makes at least five decisions you never asked for:

1. It scrambles passwords with **MD5** — a method broken for decades (a modern choice would be bcrypt).
2. Session tokens are plain random strings with **no expiry**.
3. After three failed logins it just **crashes with a raw error**.
4. Sessions live **in memory** — everyone is logged out when the server restarts.
5. It checks users with a **slow linear scan** that won't survive real traffic.

<figure style="margin: 28px 0; text-align: center;">
  <img src="assets/img/blog/am-fig1-teaser.png" alt="Before and after AssumptionMiner: the same generated code, with five hidden assumptions either invisible (left) or surfaced as an explicit, editable list (right)" style="max-width: 100%; border: 1px solid #e5e5e5; border-radius: 6px;">
  <figcaption style="font-size: 13px; color: #888; margin-top: 8px;">The same AI-generated login code. Left: five silent decisions buried in the code. Right: AssumptionMiner surfaces them as an explicit, editable list (figure from the paper).</figcaption>
</figure>

In the paper I call these **implicit assumptions**: choices absent from your request that nonetheless shape how the code behaves. The insidious part is that this code *works*. It runs, it passes tests, it looks right in a demo. I call this failure mode **working-but-wrong**. And it is not rare: in the benchmark I built for the paper, every single task contained at least two hidden assumptions — about 3.8 per task on average.

A human colleague would ask, "Hey, how should passwords be stored?" The AI just decides, and the decision is buried in code you may never read closely.

## Making the invisible visible

My paper proposes a system called **AssumptionMiner**, built around a simple idea: when AI generates code, the assumptions should come out with it, as a first-class part of the output.

Instead of handing you code alone, AssumptionMiner hands you code *plus* an explicit "assumption layer": a structured, readable list of every gap-filling decision the AI made. Studying 180 tasks, I found these decisions cluster into six recurring categories: how inputs are checked, how data is formatted, how errors are reported, how data is stored, how performance is handled, and how security is handled. The last two are the rarest — appearing in only 3–4% of tasks — but the highest-stakes: a single bad security assumption, like MD5, can invalidate an otherwise perfect program.

Then comes the useful part: the list is interactive. Each assumption appears as a card you can **accept**, **edit**, or **reject**.

<figure style="margin: 28px 0; text-align: center;">
  <img src="assets/img/blog/am-interface.png" alt="The AssumptionMiner interface: generated code on the left with highlighted regions, assumption cards on the right with Accept / Edit / Reject buttons" style="max-width: 100%; border: 1px solid #e5e5e5; border-radius: 6px;">
  <figcaption style="font-size: 13px; color: #888; margin-top: 8px;">The developer-facing interface: each assumption is a reviewable card, linked to the exact code it produced (figure from the paper).</figcaption>
</figure>

Behind the scenes, AssumptionMiner keeps a dependency map linking each assumption to the exact regions of code it shaped. When you revise one — say, flipping MD5 to bcrypt — the system regenerates only the affected code. Your other confirmed choices stay untouched.

In effect, the AI contractor finally shows you their notebook: "Here's everything I decided on your behalf. Want to change any of it?"

## Does it work?

To measure this, the paper contributes a benchmark of **180 deliberately ambiguous programming tasks with 676 annotated assumptions**, including a human-verified subset. The headline result: an ensemble of two open-source models recovers hidden assumptions with an F1 score of 0.816 — about 3.6× better than the strongest baseline that works only from code comments.

<figure style="margin: 28px 0; text-align: center;">
  <img src="assets/img/blog/am-chart-extraction.svg" alt="Bar chart: AssumptionMiner ensemble reaches F1 0.82, versus 0.23 for reading code comments and 0.08 for rule-based pattern matching" style="max-width: 100%;">
</figure>

Targeted regeneration also pays off: revising one decision changes less than half as much code as regenerating the whole program. To be clear, the problem is far from solved — under a stricter test that requires naming the *exact* decision, not just its category, the best open-source score drops to 0.66, and targeted edits occasionally leave the program inconsistent. The paper reports these limits openly; they're what makes this a research problem rather than a product feature.

## Why this matters beyond programmers

AI is increasingly doing work for people who cannot easily check that work. The gap between "what you asked for" and "what you got" is where trust breaks down — in code, and arguably everywhere else AI is used.

I think the principle behind AssumptionMiner generalizes: **whenever AI fills gaps in your request, it should tell you what it filled in.** Code is simply a domain where we can enforce this precisely, because every decision can be traced to concrete lines and revised one at a time.

If you'd like to dig deeper, the paper is on [arXiv](https://arxiv.org/abs/2607.22898) and the benchmark, code, and replication package are [openly available](https://doi.org/10.5281/zenodo.21535058).
