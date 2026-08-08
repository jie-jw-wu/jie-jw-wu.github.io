---
layout: post
title: "The Questions Your AI Coding Assistant Never Asks"
permalink: /assumptionminer.html
description: A walkthrough of my paper AssumptionMiner — what happens when you ask AI for code and it quietly answers questions you never posed.
published: false
---

*An accessible introduction to my paper, [AssumptionMiner: Extracting, Tracing, and Revising Implicit Assumptions in LLM Code Generation](https://arxiv.org/abs/2607.22898). No software engineering background required.*

## An experiment you can try

Open ChatGPT and type the request my paper uses as its running example:

> *"Implement a user authentication system that checks credentials and returns a session token."*

You will get working code in seconds. Now look closer — not at what you asked for, but at what you *didn't* ask for, and got anyway:

- **How are passwords protected?** You didn't say. A typical answer scrambles them with MD5 — an algorithm considered broken for decades. This is a security decision, made for you.
- **What do session tokens look like? Do they expire?** You didn't say. The AI picked plain random strings with no expiry.
- **What happens after repeated failed logins?** You didn't say. The code just raises a raw error — no lockout, no useful message.
- **Where are sessions stored?** You didn't say. The AI kept them in memory, so every user is logged out whenever the server restarts.
- **Will this be fast enough?** You didn't say. The AI chose a slow linear scan.

Each of these is a real decision embedded in the code you received. You made none of them. Researchers call your request an *underspecified prompt*, and the AI's silent gap-filling choices *implicit assumptions*. The worst part: the code runs and passes basic tests, so nothing forces the decisions into view. In the paper I call this failure mode **working-but-wrong**, and it's the norm, not the exception — in my benchmark of 180 tasks, every task hid at least two such assumptions (3.8 on average).

<figure style="margin: 28px 0; text-align: center;">
  <img src="assets/img/blog/am-fig1-teaser.png" alt="Before and after AssumptionMiner: five hidden assumptions in generated login code, invisible on the left, surfaced as an editable list on the right" style="max-width: 100%; border: 1px solid #e5e5e5; border-radius: 6px;">
  <figcaption style="font-size: 13px; color: #888; margin-top: 8px;">Five silent decisions in AI-generated login code — invisible on the left, surfaced and editable on the right (figure from the paper).</figcaption>
</figure>

## The core idea: code should come with a "decisions receipt"

The system I built, **AssumptionMiner**, changes what the AI hands back. Instead of just code, you get code plus a structured record of every assumption behind it — what the paper calls an *assumption layer*. Think of it as an itemized receipt: not just the product, but every decision that went into making it.

Each recorded assumption carries a plain-language description, the AI's rationale, realistic *alternatives* it could have chosen instead, and a severity level. The paper sorts these decisions into a six-category taxonomy — input validation, data format, error policy, persistence, performance, and security. Interestingly, the first four each show up in roughly three-quarters of tasks, while persistence and security appear in under 5% — rare, but by far the highest-stakes when they do (one MD5 is enough to sink a program). To check the categories aren't just my own invention, two developers independently categorized the human-verified assumptions and agreed almost perfectly (Cohen's κ = 0.85).

## How it works, in one picture

<figure style="margin: 28px 0; text-align: center;">
  <img src="assets/img/blog/am-architecture.png" alt="AssumptionMiner architecture: prompt ingestion, code generation, assumption extraction, dependency mapping, and incremental regeneration in a loop with the developer" style="max-width: 480px; width: 100%; border: 1px solid #e5e5e5; border-radius: 6px;">
  <figcaption style="font-size: 13px; color: #888; margin-top: 8px;">The five-component pipeline: generate code, extract assumptions, map each one to the code it governs, and regenerate only what a revision touches (figure from the paper).</figcaption>
</figure>

The pipeline has five parts. Your request goes to the AI as usual, and code comes back. An *extractor* then interrogates that code: "list every design decision here that the request did not require — and for each, name a realistic alternative." A *dependency mapper* links each assumption to the specific code regions it shaped, by analyzing the code's underlying grammatical structure (its *abstract syntax tree*). Finally, an *incremental regenerator* waits for you.

You review the assumptions in an interactive panel — each one a card you can **accept**, **edit**, or **reject**:

<figure style="margin: 28px 0; text-align: center;">
  <img src="assets/img/blog/am-interface.png" alt="The AssumptionMiner interface: code with highlighted regions on the left, assumption cards with Accept, Edit, and Reject buttons on the right" style="max-width: 100%; border: 1px solid #e5e5e5; border-radius: 6px;">
  <figcaption style="font-size: 13px; color: #888; margin-top: 8px;">The review interface. Hovering an assumption highlights the code it produced; editing one triggers regeneration of just that region (figure from the paper).</figcaption>
</figure>

Suppose you edit the security assumption: "switch MD5 to bcrypt." Because the system knows exactly which lines that decision governs, it regenerates *only the password-hashing region* — the session logic, error handling, and everything else you already accepted stay untouched. This matters because wholesale regeneration is how you lose work: ask an AI to "change one thing" and it often quietly changes five.

## Measuring it

The paper evaluates three claims separately: can assumptions be *found*, can they be *traced* to the right code, and does tracing make *revision* safer. The benchmark: **180 ambiguous programming tasks with 676 annotated assumptions**, including a 30-task subset verified line-by-line by professional developers.

On finding assumptions, an ensemble of two open-source models reaches an F1 score of 0.816 — roughly 3.6× the strongest baseline that mines code comments:

<figure style="margin: 28px 0; text-align: center;">
  <img src="assets/img/blog/am-chart-extraction.svg" alt="Bar chart: AssumptionMiner ensemble F1 0.82 versus 0.23 for reading code comments and 0.08 for rule-based pattern matching" style="max-width: 100%;">
</figure>

On revision, targeted regeneration changes less than half as much code as the alternatives:

<figure style="margin: 28px 0; text-align: center;">
  <img src="assets/img/blog/am-chart-edit.svg" alt="Bar chart: edit distance 0.24 for AssumptionMiner versus 0.31 to 0.57 for in-place edits, full regeneration, and manual reprompting" style="max-width: 100%;">
</figure>

The paper is equally upfront about what's unsolved. Under a stricter test — did the system name the *exact* decision, not just its category? — the best open-source score falls to 0.66. And targeted edits occasionally leave the program internally inconsistent (83% of revisions compile, versus 100% for regenerate-everything), because changing one assumption can invalidate another linked to the same code. Both are marked as the next problems to attack.

## The bigger picture

There's a popular idea that as AI improves, we'll simply describe what we want and receive correct software. I think this work points at the flaw in that dream: *describing what you want is the hard part.* Human requests are always incomplete; something must fill the gaps. Today the AI fills them silently. The question is whether that filling happens invisibly — or on the record, where you can inspect and override it.

Making AI's assumptions explicit changes the relationship: from "trust whatever the AI decided" to "review the decisions, keep the good ones, fix the rest." That's how we already work with human collaborators. AI should meet the same bar.

*The paper is on [arXiv](https://arxiv.org/abs/2607.22898); the benchmark, code, and replication package are [openly available](https://doi.org/10.5281/zenodo.21535058).*
