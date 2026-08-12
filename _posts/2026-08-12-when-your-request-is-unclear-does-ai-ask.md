---
title: When Your Request Is Unclear, Does AI Ask?
description: Good engineers ask questions when instructions don't add up. We built a benchmark to test whether code models do the same, and to make it something the field can actually measure.
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

The difference isn't coding ability. It's knowing when the instructions aren't good enough yet, and saying so.

## Asking is not a soft skill

We tend to file "asking questions" under communication, as though it were separate from the real technical work. In software it isn't. Most expensive engineering mistakes don't come from someone writing bad code; they come from someone writing perfectly good code for the wrong problem.

Every experienced engineer has internalized this. Given a vague ticket, they don't start typing. They notice the gap, name it, and get it resolved before writing a line. The recognizing is the skill: spotting that a sentence which *sounds* complete actually isn't.

Now consider how we use AI coding tools. You type a request in a box, and the model answers. For a long time it simply always answered: whatever you typed, precise or half-formed, consistent or self-contradictory, back came confident, well-formatted code.

That is changing, and it's worth saying so plainly. The current generation of coding assistants, Claude Code and its peers among them, will sometimes stop and ask what you meant before charging ahead. They are visibly better at this than the models in our study, and some of that improvement is by design rather than accident.

But "sometimes" is carrying a lot of weight in that sentence. Whether you get a question still depends on which model you're using, how the ambiguity happens to be phrased, and what scaffolding sits around the model. And as far as we can tell, nobody reports it as a number. Every leaderboard tracks whether the code was correct; none tracks whether the system noticed it had been handed a broken request. **If we can't say how reliably a tool distinguishes a clear request from a confused one, we can't say when it will quietly build the wrong thing.**

I first made this argument back in 2023, in a short position paper at the MAPS workshop titled [*Large Language Models Should Ask Clarifying Questions to Increase Confidence in Generated Code*](https://arxiv.org/pdf/2308.13507.pdf). It was written at a moment when the field's attention was almost entirely on making models generate more code, faster. The paper had no experiments, just an argument from software engineering practice that we were optimizing the wrong thing, and that a model which asks a good question is often more useful than one which produces a confident answer.

The obvious objection to a position paper is that it might be wrong. So the next step was to find out.

## Putting a number on it

Complaining that models don't ask enough questions is easy. Measuring it is harder, and until you can measure something you can't tell whether it's improving, or by how much.

So we built a benchmark. We took HumanEval, a standard set of 164 programming problems widely used to test AI coding ability, and rewrote every problem description by hand to introduce a specific defect. Three kinds, drawn from how real requirements actually fail:

- **Ambiguity**: the description allows more than one reasonable reading
- **Inconsistency**: parts of the description contradict each other
- **Incompleteness**: something essential is simply missing

We also combined them in pairs, which yielded 762 modified problem descriptions in total. We called the result **HumanEvalComm**. It inverts the usual test: on this benchmark, writing code immediately is often the *wrong* response. The right response is a question.

<figure class="post-figure">
  <a href="{{ '/assets/img/blog/hec-methodology.png' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/img/blog/hec-methodology.png' | relative_url }}" alt="Methodology diagram: 164 HumanEval problems, a taxonomy of ambiguity, inconsistency and incompleteness, then evaluation on communication rate, good question rate, and pass rates.">
  </a>
  <figcaption>Each of 164 standard problems was rewritten by hand to introduce ambiguity, inconsistency, or incompleteness. We then measured whether models ask instead of guess. <em>(click to enlarge)</em></figcaption>
</figure>

## What we found

**More than 60% of the time, the models wrote code anyway.** Handed a description that contradicted itself or omitted something essential, most produced a confident solution instead of a question.

How often a model asked varied widely, and not in a reassuring way. CodeQwen1.5-Chat asked in 4.82% of cases, roughly one time in twenty. CodeLlama managed 10.16%, ChatGPT 14.21%. The most talkative model we tested, DeepSeek Chat, reached 37.93%: still silent in nearly two out of three broken requests.

The silence has a price. Given the flawed descriptions, ChatGPT's accuracy fell from 65.58% to 31.34%, **less than half**, with a similar drop in how many tests its code passed. Nothing about the programming got harder. The model simply answered a question nobody asked, and never noticed.

<figure class="post-figure">
  <a href="{{ '/assets/img/blog/hec-results.png' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/img/blog/hec-results.png' | relative_url }}" alt="Results table comparing models on Pass@1, test pass rate, communication rate, and good question rate on HumanEval versus HumanEvalComm.">
  </a>
  <figcaption>Accuracy drops sharply once descriptions are flawed (compare the HmEval and HmEvalComm columns), while communication rates stay low across the board. <em>(click to enlarge)</em></figcaption>
</figure>

There's a quieter finding worth pausing on. Models were most likely to ask when information was outright *missing*, and least likely when the description was subtly ambiguous or self-contradictory. That's exactly backwards from what's useful. A missing input is the failure mode a developer is most likely to catch unaided. A description that reads smoothly while meaning two different things is the one that slips through review, and it's precisely where the models stay quiet.

## How much can you delete before it notices?

The result that stayed with us came from a simple stress test. Instead of carefully rewriting a description, we just deleted parts of it at random (10% of the words, then 20%, and so on) and watched for the point at which the model would stop and ask what was going on.

It took far longer than expected.

**With half the description deleted, 95% of responses were still code.** Not a question, not a flag. A confident solution to a problem whose statement had been cut in half. Even after removing **90%** of the description, leaving barely a fragment of a sentence, the models still wrote code 46% of the time.

<figure class="post-figure">
  <a href="{{ '/assets/img/blog/hec-removal.png' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/img/blog/hec-removal.png' | relative_url }}" alt="Line chart showing communication rate stays near zero until about half the problem description is removed, rising to only 54% at 90% removed, while test pass rate declines steadily.">
  </a>
  <figcaption>The blue line is how often the model asks a question; it stays near zero until half the description is gone. The red line is code correctness, falling the whole way. For most of that decline, the model never says anything is wrong. <em>(click to enlarge)</em></figcaption>
</figure>

Look at the gap between the two lines. Correctness starts falling immediately: the model is already producing worse answers by the time 20% is missing. But the questions don't start until much later, if at all. For most of the range, the model is quietly getting things wrong and telling you nothing.

That gap is the whole problem in one picture.

## A note on when this was measured

Dates matter for a result like this, so here they are. **We ran these experiments in the first half of 2024**, and the first version of the paper went up on arXiv in June 2024. The journal version appeared in TOSEM in 2025, and the work was presented at FSE in 2026, but the numbers themselves come from those 2024 runs.

The models were the strong options available at that moment. "ChatGPT" here means `gpt-3.5-turbo-0125`, the frozen January 2024 snapshot, which we pinned deliberately so the results would stay reproducible rather than drifting under us. The four open-source models were 2023–2024 releases in the 7B–13B range: CodeLlama-13B-Instruct, CodeQwen1.5-7B-Chat, DeepSeek Coder 6.7B, and DeepSeek LLM 7B. We were limited to that size range by the GPUs we had, which is worth stating plainly too.

That is several generations ago. Models have improved enormously since, and today's frontier systems are far stronger coders that would very likely score better here. Please read the specific percentages as a measurement of that 2024 cohort, not as a claim about what current models do.

What we don't yet know is whether the *behavior* changed along with the capability. Being a better coder and knowing when to stop and ask are different skills, and improvements in the first don't automatically deliver the second. That's precisely why the benchmark is public: re-running it on current models is a small experiment that would settle the question, and we'd genuinely like to know the answer.

## Why this matters beyond programming

Code generation is where this is easiest to measure, but it isn't where the problem ends. The same pattern shows up wherever we hand an underspecified request to an AI system and receive a fluent answer: the fluency is not evidence that the system understood you.

As these tools take on more autonomy, writing larger changes, running for longer, acting with less review, the cost of a silent misunderstanding compounds. A wrong guess in ten lines of code is a nuisance. The same wrong guess propagated through an afternoon of autonomous work is expensive, and much harder to trace back to the sentence that caused it.

We think "did it ask when it should have?" belongs alongside "was the answer correct?" as a standard measure of these systems. It's currently almost never reported.

**Can it be fixed?** Encouragingly, yes, at least partly, and without new model training. As a proof of concept we built a simple agent, Okanagan, that separates writing code from judging whether there was enough information to write it. Just splitting those two steps raised the rate of asking substantially. We don't present it as a strong solution; it's a rough prototype, and roughly half the questions it asks aren't useful. What it demonstrates is headroom: models are more capable of recognizing missing information than their default behavior suggests. They mostly aren't asked to.

That's the real message of this work. Not that today's AI can't clarify, but that we haven't been measuring whether it does, or building systems that expect it to.

This is part of a longer line of work in our group on making AI coding tools honest about what they don't know: from the [2023 position paper](https://arxiv.org/pdf/2308.13507.pdf) arguing models should ask, to this benchmark measuring whether they do, to [ClarifyCoder](https://arxiv.org/abs/2504.16331) training them to prefer asking over answering, to [AssumptionMiner]({{ '/blog/what-is-ai-assuming.html' | relative_url }}) surfacing the silent guesses a model already made when it didn't ask.

**This is joint work with Prof. Fatemeh H. Fard at the University of British Columbia, Kelowna.** The benchmark, code, and evaluation scripts are public, and we'd like others to build on this.
