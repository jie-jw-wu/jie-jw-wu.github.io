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

It looks great — until you notice the details. The cabinets are walnut (you wanted white). The outlets are behind the coffee machine. The drawers open the wrong way for a left-handed cook.

None of these were mistakes, exactly. You never said what you wanted. The contractor had to decide *something*, so they decided quietly, and you only discovered their decisions after everything was built.

This is precisely what happens when AI writes code today.

## AI fills in the gaps — silently

Tools like ChatGPT and GitHub Copilot can now write working programs from a plain-English request. But a plain-English request is almost never a complete specification. Suppose you ask an AI to "write a program that saves user scores for a game." You've left a lot unsaid:

- Where should scores be saved — a file, a database?
- What if two players have the same name?
- What if the saved file gets corrupted?
- Should scores be validated, or accepted as-is?

The AI cannot leave these questions unanswered, because the code has to do *something* in each case. So it picks answers — reasonable-sounding ones — and bakes them into the code without telling you. In the paper, I call these **implicit assumptions**: choices absent from your request that nonetheless shape how the code behaves, and often whether it is correct or secure.

The dangerous part is not that the AI makes assumptions. Any developer would, too. The dangerous part is that they are *invisible*. A human colleague might ask, "Hey, what should happen if the file is corrupted?" The AI just decides, and the decision is buried in code you may never read closely.

## Making the invisible visible

My paper proposes a system called **AssumptionMiner**, built around a simple idea: when AI generates code, the assumptions should come out with it, as a first-class part of the output.

Instead of handing you code alone, AssumptionMiner hands you code *plus* an explicit "assumption layer" — a structured, readable list of every gap-filling decision the AI made. Each assumption falls into one of six categories that cover where these silent choices tend to hide: how inputs are checked, how data is formatted, how errors are handled, how data is stored, how performance is treated, and how security is handled.

Then comes the useful part: the list is interactive. You can go through each assumption and confirm it ("yes, saving to a file is fine") or revise it ("no, use a database"). Behind the scenes, AssumptionMiner keeps a map that links each assumption to the exact parts of the code it influenced. When you revise an assumption, the system regenerates only the affected code — not the whole program — so your other choices stay intact.

In effect, the AI contractor finally shows you their notebook: "Here's everything I decided on your behalf. Want to change any of it?"

## Does it work?

To study this rigorously, the paper introduces a benchmark: 180 deliberately ambiguous programming tasks, annotated with 676 assumptions that an AI would need to make to complete them. Using this benchmark, I evaluated how well AssumptionMiner extracts assumptions, ties them to the right code, and supports revision — across several AI models, both commercial (GPT-4o) and open-source.

The details are in the paper, but the headline is: assumptions *can* be surfaced systematically, categorized reliably, and traced to the code they govern — which turns a silent risk into something a developer can actually review.

## Why this matters beyond programmers

AI is increasingly doing work for people who cannot easily check that work. The gap between "what you asked for" and "what you got" is where trust breaks down — in code, and arguably everywhere else AI is used.

I think the principle behind AssumptionMiner generalizes: **whenever AI fills in gaps in your request, it should tell you what it filled in.** Code is simply a domain where we can enforce this precisely, because we can trace each decision to concrete lines and fix them one at a time.

If you'd like to dig deeper, the paper is on [arXiv](https://arxiv.org/abs/2607.22898) and the code is [openly available](https://doi.org/10.5281/zenodo.21535058).
