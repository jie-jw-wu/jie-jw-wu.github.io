---
layout: post
title: "The Questions Your AI Coding Assistant Never Asks"
permalink: /assumptionminer.html
description: A walkthrough of my paper AssumptionMiner — what happens when you ask AI for code and it quietly answers questions you never posed.
published: false
---

*An accessible introduction to my paper, [AssumptionMiner: Extracting, Tracing, and Revising Implicit Assumptions in LLM Code Generation](https://arxiv.org/abs/2607.22898). No software engineering background required.*

## An experiment you can try

Open ChatGPT and type: *"Write a program that lets users register with a username and password."*

You will get working code in seconds. Now look closer — not at what you asked for, but at what you *didn't* ask for, and got anyway:

- **Is there a minimum password length?** You didn't say. The AI picked one (or didn't).
- **What happens if the username is already taken?** You didn't say. The AI decided.
- **Is the password stored in plain text or encrypted?** You didn't say. The AI chose — and this one is a security decision.
- **Where are users stored — in memory, a file, a database?** You didn't say. The AI guessed.

Each of these is a real decision embedded in the code you received. You made none of them. And unless you read the code carefully — which many users of AI tools don't, or can't — you don't know what was decided in your name.

Researchers call your request an *underspecified prompt*, and the AI's silent gap-filling choices *implicit assumptions*. My paper is about dragging those assumptions into the light.

## The core idea: code should come with a "decisions receipt"

The system I built, **AssumptionMiner**, changes what the AI hands back. Instead of just code, you get code plus an explicit list of every assumption the AI made — what I call an *assumption layer*. For the example above, it might read:

1. *Assumed passwords must be at least 8 characters* — input validation
2. *Assumed duplicate usernames are rejected with an error message* — error handling
3. *Assumed passwords are hashed before storage* — security
4. *Assumed users are stored in a local file* — data storage

Think of it as an itemized receipt: not just the product, but every decision that went into it.

The paper organizes these assumptions into six recurring categories — input validation, data format, error handling, data storage, performance, and security — based on where AI models most often have to fill gaps. To check that these categories are meaningful and not just my own invention, two developers independently categorized assumptions from the benchmark and agreed with each other the vast majority of the time.

## From reading to fixing

A receipt is only useful if you can dispute the charges. In AssumptionMiner, every assumption is reviewable: you confirm the ones you like and revise the ones you don't. Suppose you change assumption 4 — "actually, store users in a database."

Here's the part I find most satisfying as a researcher. AssumptionMiner builds a dependency map between each assumption and the specific parts of the code it shaped (using the code's underlying structure, called an abstract syntax tree). So when you revise one assumption, the system regenerates *only the code governed by that assumption*. The password rules you already approved stay untouched. This matters because wholesale regeneration is how you lose work: ask an AI to "change one thing" and it often quietly changes five.

## Measuring it

Claims like "we surface assumptions" need evidence, so the paper contributes a benchmark: **180 ambiguous programming tasks with 676 annotated assumptions**, including a human-verified subset for testing whether assumptions can be traced to the right lines of code. I evaluated the approach across four AI models — GPT-4o and three open-source code models — measuring how completely and precisely each surfaces the assumptions a task actually requires, and whether combining models does better than any single one.

## The bigger picture

There's a popular idea that as AI gets better, we'll simply describe what we want and get correct software. I think my paper points at the flaw in that dream: *describing what you want is the hard part.* Human requests are always incomplete; something must fill the gaps. Today the AI fills them silently. The question is whether the filling happens invisibly — or on the record, where you can inspect and override it.

Making AI's assumptions explicit won't just produce better code. It changes the relationship: from "trust whatever the AI decided" to "review the decisions, keep the good ones, fix the rest." That's how we already work with human collaborators. AI should meet the same bar.

*The paper is on [arXiv](https://arxiv.org/abs/2607.22898); code and benchmark are [openly available](https://doi.org/10.5281/zenodo.21535058).*
