---
layout: post
title: "What Your AI Coding Assistant Isn't Telling You"
permalink: /assumptionminer.html
description: "Why AI-generated code is full of silent guesses — and how our new tool, AssumptionMiner, makes them visible."
---

*This post introduces our recent paper, [AssumptionMiner: Extracting, Tracing, and Revising Implicit Assumptions in LLM Code Generation](https://arxiv.org/abs/2607.22898), written for readers without a background in software engineering research.*

## A story about a bookshelf

Imagine you ask a carpenter to "build me a bookshelf." A week later, a bookshelf arrives. It's five feet tall, made of pine, with four fixed shelves.

You never said how tall it should be. You never mentioned the material. You never said whether the shelves should be adjustable. The carpenter had to decide all of that — and every one of those decisions was a *guess* about what you wanted. Maybe good guesses. Maybe not. The problem is that unless you ask, you'll never know which parts of the bookshelf came from your request and which parts came from the carpenter's imagination.

This is exactly what happens when people ask AI to write code.

## AI fills in the blanks — silently

Tools like ChatGPT and GitHub Copilot can turn a plain-English request into working code. But a short request like *"write a function that reads a list of scores and returns the average"* leaves an enormous amount unsaid. What if the list is empty? What if a score is negative, or not a number at all? Should the result be rounded?

The AI doesn't stop to ask. It quietly picks an answer to every one of these questions and bakes those answers into the code. We call these silent choices **implicit assumptions**: decisions that are nowhere in your request but everywhere in the code's behavior.

Most of the time you never see them. They surface later — as a bug, a crash, or software that does something you never intended. And because the assumptions were never written down, it's hard to even notice they were made.

## Our idea: make the guesses visible

In our paper, we propose a simple shift in perspective: when an AI generates code, **the assumptions it made should be part of the output, just like the code itself.**

We built a system called **AssumptionMiner** that does three things:

1. **Extract.** Alongside the generated code, it produces a written list of the assumptions the AI made — a record of every gap in your request and how the AI chose to fill it. ("I assumed the list is never empty." "I assumed scores are whole numbers.")

2. **Trace.** Each assumption is linked to the exact lines of code it affects. Click on an assumption, and you can see precisely which part of the program depends on that guess.

3. **Revise.** If an assumption is wrong — say, the list *can* be empty — you correct that one assumption, and the system regenerates only the code that depends on it, leaving the rest untouched.

In the bookshelf analogy: the carpenter now hands you the bookshelf *and* a note that says "I assumed pine, five feet, fixed shelves." You cross out "fixed" and write "adjustable," and only the shelves get rebuilt — not the whole bookshelf.

## Does it work?

To study this properly, we built a benchmark: 180 programming tasks that are deliberately ambiguous, the way real requests are, with 676 assumptions carefully annotated by hand. This gives researchers a shared way to measure how well systems handle unstated decisions.

Two findings stand out:

- **Tracing assumptions to code is doable but not trivial.** Our best method, which uses an AI model to map each assumption to the code it governs, gets it right about 64% of the time — better than simpler keyword-matching approaches, but with clear room to grow.
- **Targeted fixing pays off.** When a user corrects one assumption, our regeneration approach changes about **2.4× less code** than regenerating without that targeting. Less churn means less new code to review — and fewer chances for new mistakes to sneak in.

## Why this matters beyond programmers

You might not write code, but AI-made guesses affect you anyway. As more of the software around us is written with AI assistance, the question "what did the AI assume?" becomes a quality and safety question for everyone. A system that keeps its assumptions hidden is a system nobody can fully check.

The deeper principle is one that applies far beyond code: **when an AI fills in the blanks in your request, you deserve to see what it filled in.** AssumptionMiner is our attempt to build that principle into how AI writes software.

---

*The paper is available on [arXiv](https://arxiv.org/abs/2607.22898). Comments and questions are welcome — feel free to reach out.*
