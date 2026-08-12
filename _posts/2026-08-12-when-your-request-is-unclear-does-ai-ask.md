---
title: When Your Request Is Unclear, Does AI Ask?
description: We built a benchmark to test whether code LLMs ask clarifying questions when requirements are broken. Most of the time, they don't.
permalink: /blog/does-ai-ask.html
coauthors: Prof. Fatemeh H. Fard (University of British Columbia)
paper:
  title: "HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent"
  authors: Jie JW Wu, Fatemeh H. Fard
  venue: ACM Transactions on Software Engineering and Methodology (TOSEM), presented at FSE 2026
  year: 2025
  url: https://doi.org/10.1145/3715109
  code: https://github.com/jie-jw-wu/human-eval-comm
  bibtex: |
    @article{wu2025benchmarking,
      author = {Wu, Jie JW and Fard, Fatemeh H.},
      title = {HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent},
      journal = {ACM Trans. Softw. Eng. Methodol.},
      year = {2025},
      doi = {10.1145/3715109},
      url = {https://doi.org/10.1145/3715109}
    }
---

Picture a new engineer joining your team. On their first day you send a one-line message: *"Add an export button to the reports page."*

A good hire writes back within the hour: Export to CSV or PDF? Just the current view, or all reports? What should happen if the report is still loading? A weaker hire says nothing, disappears for two days, and returns with something you have to throw away.

The difference isn't coding ability. It's knowing when the instructions aren't good enough yet — and saying so.

This is the gap between today's AI coding tools and strong software engineers. The models write code impressively well. But when your request is unclear, incomplete, or self-contradictory, do they raise a hand? We built a benchmark to find out, and the short answer is: **usually not.**

## Measuring something nobody was measuring

There's no shortage of benchmarks for whether AI writes *correct* code. There was none for whether it asks *good questions*. So we made one.

We started from HumanEval, a standard set of 164 programming problems used throughout the field, and rewrote each problem description by hand to introduce a specific defect. We used three categories, drawn from how real requirements actually go wrong:

- **Ambiguity** — the description permits more than one reasonable reading
- **Inconsistency** — parts of the description contradict each other
- **Incompleteness** — something essential is simply missing

We also combined them in pairs, so each original problem yields several broken variants. The result is **HumanEvalComm**: a benchmark where the right answer is often *not* to write code, but to ask.

<figure class="post-figure">
  <a href="{{ '/assets/img/blog/hec-methodology.png' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/img/blog/hec-methodology.png' | relative_url }}" alt="Methodology diagram: 164 HumanEval problems, a taxonomy of ambiguity, inconsistency and incompleteness, then evaluation of Code LLMs and the Okanagan agent on communication rate, good question rate, and pass rates.">
  </a>
  <figcaption>How HumanEvalComm is built and evaluated: rewrite each of 164 problems to introduce a defect, then measure whether models ask instead of guess. <em>(click to enlarge)</em></figcaption>
</figure>

Then we needed to score behavior, not just output. We used four measures: how often a model asks anything at all (**communication rate**), whether the question is actually useful (**good question rate**), and two standard correctness measures (**Pass@1** and **test pass rate**).

## What we found

**More than 60% of the time, code LLMs wrote code anyway.** Faced with a description that contradicted itself or left out something essential, most models produced a confident answer rather than a question.

The specific numbers vary a lot by model, which is itself interesting. CodeQwen1.5-Chat asked in only 4.82% of cases. CodeLlama managed 10.16%, ChatGPT 14.21%. The best of the plain models, DeepSeek Chat, reached 37.93% — still fewer than two questions asked for every five broken requests.

And the silence is costly. When ChatGPT was given the flawed descriptions, its Pass@1 accuracy fell from 65.58% to 31.34% — **less than half** — with test pass rate dropping from 76.42% to 49.39%. The model didn't fail because the coding got harder. It failed because it answered the wrong question and never checked.

<figure class="post-figure">
  <a href="{{ '/assets/img/blog/hec-results.png' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/img/blog/hec-results.png' | relative_url }}" alt="Results table comparing ChatGPT, CodeLlama, CodeQwen1.5 Chat, DeepSeek Coder, DeepSeek Chat and Okanagan on Pass@1, test pass rate, communication rate, and good question rate.">
  </a>
  <figcaption>Accuracy drops sharply on broken descriptions, while communication rates stay low — until Okanagan. <em>(click to enlarge)</em></figcaption>
</figure>

## Teaching a model to ask

Knowing the gap exists is only useful if it can be closed. So we built **Okanagan**, an agent approach that restructures the interaction into three rounds: draft an initial solution, then step back and decide whether clarifying questions are needed, then regenerate using the answers.

The key move is separating "write the code" from "judge whether you had enough information to write it." A single prompt conflates those two jobs, and models overwhelmingly default to producing something.

<figure class="post-figure">
  <a href="{{ '/assets/img/blog/hec-okanagan.png' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/img/blog/hec-okanagan.png' | relative_url }}" alt="Diagram of the Okanagan agent: round one generates code, round two decides whether to ask clarifying questions, round three regenerates code using the answers.">
  </a>
  <figcaption>Okanagan's three rounds: generate, then decide whether to ask, then regenerate with the answers. <em>(click to enlarge)</em></figcaption>
</figure>

It works. Okanagan raised the communication rate from ChatGPT's 14.21% to **72.73%**, and improved accuracy on the broken descriptions along with it — Pass@1 from 31.34% to 39.62%, test pass rate from 49.39% to 56.98%. Asking questions didn't slow the model down in any way that mattered; it made the eventual code better.

We're honest that this is a first step, not a solved problem. Okanagan's good question rate is 52.24% — roughly half its questions are genuinely useful, and the other half are noise a developer would have to wade through. A tool that asks too many unhelpful questions is its own kind of annoying.

## Why this matters

The default assumption in AI coding tools today is that your prompt is complete. It rarely is. Every human collaboration involves a back-and-forth to establish what's actually wanted, and we've built a generation of tools that skip that step entirely and paper over the gap with confident guesses.

This work measures the problem. Our follow-up work attacks it from both ends: [ClarifyCoder](https://arxiv.org/abs/2504.16331) fine-tunes models to prefer asking over answering, and [AssumptionMiner]({{ '/blog/what-is-ai-assuming.html' | relative_url }}) surfaces the silent guesses a model already made when it didn't ask. Different angles on one question: how do we make AI coding tools honest about what they don't know?

**This is joint work with Prof. Fatemeh H. Fard at the University of British Columbia, Kelowna.** The benchmark, code, and evaluation scripts are all public — we'd like others to build on this, and to beat our numbers.
