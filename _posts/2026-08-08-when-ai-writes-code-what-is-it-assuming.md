---
title: When AI Writes Code, What Is It Assuming?
description: AI coding tools don't ask questions when your request is vague — they guess, silently. Our new paper makes those guesses visible.
permalink: /blog/what-is-ai-assuming.html
---

Imagine you hire a contractor and say, "I'd like more counter space in my kitchen." They nod, disappear for a week, and return having removed your stove. Technically: more counter space. But a good contractor would have *asked* before deciding.

Millions of programmers now work with an AI "contractor": tools like ChatGPT and GitHub Copilot that write code from a plain-English request. These tools are remarkably capable, but they share the flaw above — **when your request leaves something unsaid (and real requests almost always do), they don't ask. They guess.**

In our new paper, we call these guesses *implicit assumptions*, and we measured just how common they are. Consider this innocent one-sentence request:

> "Implement a user authentication system that checks credentials and returns a session token."

A typical AI response — fewer than a dozen lines of code — silently makes at least **five** decisions you never agreed to: it scrambles passwords with MD5 (a method security experts have considered broken since the mid-2000s), issues session tokens that never expire, keeps all sessions in temporary memory that vanishes on restart, and more.

<img src="{{ '/assets/img/blog/am-assumptions-before-after.png' | relative_url }}" alt="Left: five implicit assumptions hidden in AI-generated authentication code. Right: AssumptionMiner surfaces them as an explicit, editable list." style="width: 100%; max-width: 780px; display: block; margin: 24px auto;">

<p style="text-align: center; font-size: 13px; color: #888; margin-top: -12px;">Left: five assumptions hide silently in a dozen lines of AI-generated code. Right: AssumptionMiner surfaces them as an explicit, editable list.</p>

The concerning part: this code *works*. It runs, it passes tests, it looks professional. As we put it in the paper, generated code can pass its tests while violating the developer's intent. Across the 180 programming tasks in our benchmark, 86% involved silent decisions about input checking and 81% about error handling. Security assumptions were rare (3%) — but those are the ones that hurt the most.

## Making the guesses visible

Our tool, **AssumptionMiner**, makes the AI show its work. Three steps:

1. **Extract** — alongside the code, produce a structured list of every assumption made: what was decided, how risky it is, and what the alternatives were.
2. **Trace** — link each assumption to the exact lines of code it shaped, using a map of the code's structure.
3. **Revise** — let you accept, edit, or reject each assumption. Reject "MD5" and the tool regenerates *only* the affected code, leaving the rest untouched.

<img src="{{ '/assets/img/blog/am-interface.png' | relative_url }}" alt="Screenshot of the AssumptionMiner web interface: generated code on the left, a reviewable list of assumption records on the right, each with Accept, Edit, and Reject buttons." style="width: 100%; max-width: 780px; display: block; margin: 24px auto; border: 1px solid #e5e5e5; border-radius: 4px;">

<p style="text-align: center; font-size: 13px; color: #888; margin-top: -12px;">The AssumptionMiner interface: generated code on the left, the assumptions behind it on the right — each one reviewable like a checklist.</p>

## Does it work?

Using only open-source AI models, AssumptionMiner reaches an F1 score of 0.816 at spotting *what kind* of hidden decision the AI made — roughly, it catches most of them with few false alarms, and about **3.6× better** than the best method that uses no AI at all. One striking comparison: reading the code's own comments recovers almost none of these decisions, because *developers and AIs simply don't write their assumptions down*. And when you revise an assumption, targeted regeneration changes less than half as much code as regenerating from scratch.

We're equally upfront about what's unsolved. Under a stricter test that also requires naming the *specific* decision rather than just its category, the best open-source score falls to 0.66 — pinpointing exactly what the AI decided remains an open problem. And cascading edits, where fixing one assumption invalidates another, still trip the system up. That's the honest frontier of this research.

## Why this matters beyond programmers

AI-written software is entering your banking app, your car, your hospital. "Does the code run?" is no longer the right question. The right question is: **"What did the AI assume?"** — and we believe every AI coding tool should eventually answer it, the way a good contractor walks you through the plan before tearing out walls.

This continues our group's work on trustworthy AI-generated code: we previously showed that AI models rarely ask clarifying questions ([HumanEvalComm](https://arxiv.org/pdf/2406.00215), TOSEM 2025) and trained models to ask instead of guess ([ClarifyCoder](https://arxiv.org/abs/2504.16331)). AssumptionMiner covers the other side: when the AI has already guessed, drag the guesses into the light.

---

📄 Paper: [arXiv:2607.22898](https://arxiv.org/abs/2607.22898) · 💾 Benchmark, code, and tool: [Zenodo](https://doi.org/10.5281/zenodo.21535058)
