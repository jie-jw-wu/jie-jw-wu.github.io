---
title: Can an AI Agent Be a Growth Hacker?
description: Off-policy evaluation, a classic problem in reinforcement learning, is how companies estimate a new policy's impact from logged data instead of a live A/B test. We asked whether LLM agents can keep that code tuned on their own, and measured how often they make things better, worse, or simply break.
permalink: /blog/growthhacker.html
authors: Jie “JW” Wu*, Ayanda Patrick Herlihy*, Ahmad Saleem Mirza, Ali Afoud, Fatemeh Fard (*co-first authors)
paper:
  title: "GrowthHacker: Automated Off-Policy Evaluation Optimization Using Code-Modifying LLM Agents"
  authors: Jie “JW” Wu*, Ayanda Patrick Herlihy*, Ahmad Saleem Mirza, Ali Afoud, Fatemeh Fard (*co-first authors)
  venue: ACM Transactions on Software Engineering and Methodology (TOSEM)
  year: 2026
  url: https://doi.org/10.1145/3815588
  code: https://github.com/jie-jw-wu/ope-agent
  bibtex: |
    @article{wuherlihy2025growthhacker,
      title={GrowthHacker: Automated Off-Policy Evaluation Optimization Using Code-Modifying LLM Agents},
      author={Wu, Jie JW and Herlihy, Ayanda Patrick and Mirza, Ahmad Saleem and Afoud, Ali and Fard, Fatemeh},
      journal={ACM Transactions on Software Engineering and Methodology},
      year={2026},
      doi={10.1145/3815588}
    }
---

How can we tell whether a new decision policy will work before deploying it? This is the question behind **off-policy evaluation (OPE), a classic problem in reinforcement learning and contextual bandits**. Given data collected under one policy, OPE aims to estimate how another policy would perform. A *policy* is a rule for choosing an action, such as which item to recommend to a user.

The same question matters across applications, including **recommendation, advertising, healthcare, and robotics**. In healthcare, researchers may want to evaluate a treatment policy using records of past clinical decisions. In robotics, they may want to assess a control policy from previously collected interaction data before testing it on physical hardware. These settings share a practical constraint: trying every candidate policy directly can be costly, slow, or risky. This gives [OPE a role across multiple application domains](https://proceedings.mlr.press/v238/li24l/li24l.pdf) and motivates reliable software for carrying it out.

I encountered the practical motivation for this problem during my years on a growth team. A new recommendation strategy might look promising, but evaluating it online meant implementing the change, checking it carefully, and waiting for enough user data. With many ideas competing for limited experimentation time, deciding what to test could itself become a bottleneck.

OPE connects that practical need to a long-standing research problem. A recommendation team can use logs from its current system to estimate the value of a different policy before exposing users to it. Those estimates can help prioritize online experiments, although their reliability depends on the available data and the assumptions behind the estimator.

That creates a software engineering problem: someone has to select, configure, and maintain the code that produces those estimates. Could an LLM agent help with that work by proposing changes, running the code, and measuring the results?

Our TOSEM paper, [*GrowthHacker: Automated Off-Policy Evaluation Optimization Using Code-Modifying LLM Agents*](https://doi.org/10.1145/3815588), investigates this question. The name comes from the iterative nature of growth experimentation: make a change, measure its effect, and decide whether to keep it. Here, we study a specific part of that process: improving OPE code.

## Why OPE is a useful test for coding agents

The connection to reinforcement learning gives this task a broader motivation: improving the software used to evaluate decision policies from logged data. GrowthHacker approaches that problem through the implementation, asking whether agents can improve existing OPE code through measured, iterative edits.

For a coding agent, optimizing an OPE implementation is more demanding than producing code that runs. An edit can be syntactically valid yet worsen the evaluation metric or introduce numerical instability. This gives us a concrete setting in which to ask whether agents can make useful changes to scientific software, and how reliably they do so.

We therefore examined three separate outcomes: whether the modified code executed successfully, whether it improved the selected metric, and how large that improvement or degradation was.

## From code edits to measured results

GrowthHacker gives an LLM-based system an existing OPE implementation and asks it to improve a specified evaluation metric. The system proposes code changes, executes the modified implementation on benchmark data, and compares the result with the original.

<figure class="post-figure">
  <a href="{{ '/assets/img/blog/gh-loop.png' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/img/blog/gh-loop.png' | relative_url }}" alt="Diagram of the GrowthHacker loop: an LLM-based agent takes the original OPE code as input, produces modified code, both versions are executed on OBP or Scope-RL datasets, and the new results are compared with the original to decide whether the metric improved before the next iteration.">
  </a>
  <figcaption>The GrowthHacker workflow. Agents modify OPE code, execute the candidate, and compare its evaluation metric with the original implementation. <em>(click to enlarge)</em></figcaption>
</figure>

We evaluated four configurations using the same underlying model, **Gemini 2.5 Flash**:

- **Default:** a single LLM without an agent framework.
- **AutoGen and CrewAI:** two general-purpose multi-agent frameworks.
- **two_agent:** a small workflow we developed for this task. An analyzer writes instructions for a proposed change, and a coder implements them. Each iteration starts from the original code, and a final selection step chooses the best candidate from the batch.

The benchmark contains **18 OPE notebooks** from [Open Bandit Pipeline](https://github.com/st-tech/zr-obp) and [Scope-RL](https://github.com/hakuhodo-technologies/scope-rl), covering recommendation and advertising scenarios. Healthcare and robotics motivate the broader relevance of OPE, but were not evaluated in this study. Across frameworks and experimental settings, the evaluation involved hundreds of runs. The changes focused on hyperparameters and small function modifications.

The optimization objective depended on the library: reducing estimator error in Open Bandit Pipeline, or increasing estimated policy value in Scope-RL. These objectives need to be interpreted separately. A lower estimation error indicates a more accurate estimate under the benchmark's evaluation, whereas a higher estimated policy value does not, by itself, establish a better policy in deployment.

## What improved, and how often?

The clearest result was the reliability of the constrained two-agent workflow. It completed more runs successfully and improved the selected metric more often than the other configurations.

| Configuration | Runs that executed successfully | Runs with an improved metric (Scope-RL) |
|---|---|---|
| Default | 89.5% | 65% |
| AutoGen | 92.6% | 65% |
| CrewAI | 90.1% | 63% |
| two_agent | 98.1–100% | 78% |

*Execution rates cover both libraries; the execution rate for two_agent varied across settings. Improvement rates come from the Scope-RL experiments, where the objective was estimated policy value, and count only genuine improvements, not extreme values.*

Execution failures often involved ordinary coding mistakes: syntax errors, misplaced parameters, or, in AutoGen's case, diff markup appearing in an output that should have been a complete source file. These errors matter because a promising optimization is unusable if the resulting program cannot run.

Among runs that improved the metric, **two_agent had a median gain of 4.4%**. CrewAI had the highest mean improvement, 37.9%, but a median of 1.6%. That gap between the mean and median shows why a single average can be misleading: a few large gains can make a configuration look stronger than its typical successful attempt.

Extreme values also occurred. We flagged any change larger than 9,999% in either direction as extreme, because a jump that large reflects a parameter explosion rather than a genuine improvement. Default, AutoGen, and two_agent each produced extreme values in about 1% of runs. Numerical instability in continuous action spaces was a common cause. CrewAI produced no extreme values in the observed runs, although this does not establish that it is immune to them.

Taken together, the results favor two_agent for execution reliability and improvement frequency in our evaluation. They also show that no configuration was best on every measure.

## A smaller workflow worked better in this setting

One useful finding was that a narrowly defined workflow outperformed the more general agent frameworks on several measures. The analyzer and coder had distinct responsibilities, edits were limited in scope, and each candidate began from the original implementation. This structure made the task more controlled.

We also tried giving agents the history of earlier iterations. The models got confused by the extra context, and this led to failures, so the final design kept each iteration independent of the previous ones.

These observations suggest that workflow design deserves as much attention as model choice. They do not establish that smaller agent systems always win, or that history is generally unhelpful. They show that adding coordination or context does not automatically improve performance on a concrete code optimization task.

## What the experiments establish, and what remains open

The results demonstrate that LLM agents can propose useful OPE code changes in a bounded experimental setting. Several limits matter when interpreting that finding:

- **Scope.** We used one model, Python code, and 18 notebooks from two libraries. Results may differ with other models, libraries, and workloads.
- **Benchmark design.** We developed both two_agent and the benchmark. Independent evaluations would help assess how well the comparison generalizes.
- **Imperfect reliability.** About 22% of two_agent's Scope-RL outcomes left the metric unchanged, made it worse, or produced an extreme value. Successful execution was not a guarantee of a useful change.
- **Quality beyond the metric.** We did not evaluate readability, computational efficiency, or maintainability. A metric improvement alone is insufficient to judge the overall quality of a code change.
- **Edit scope.** The study focused on conservative modifications. Broader rewrites failed more often and remain a harder problem.

A practical use of this approach would be to present candidate changes and their measured effects for human review. Before adopting a candidate, a team would still need to check whether the edit preserves the intended evaluation and whether the improvement holds beyond the data used to select it.

## Toward automated maintenance of evaluation code

This work grew out of [AutoOffAB]({{ '/assets/AutoOffAB-fse-camare-ready.pdf' | relative_url }}), my 2024 vision paper on systematically updating offline A/B testing. GrowthHacker takes a step toward that goal by implementing and evaluating a loop for modifying OPE code.

A longer-term direction is to integrate such a loop into software maintenance: rerun evaluations as data or dependencies change, propose adjustments, and submit the evidence for review. Our experiments do not yet demonstrate continuous production maintenance, but they provide a benchmark for studying the code modification component of that process.

For us, the main contribution is both empirical and practical. We show where code-modifying agents help, document where they fail, and provide a benchmark for comparing future approaches. The code, data, and scripts to reproduce our results are public. The next challenge is to make improvements robust enough that a better benchmark result becomes a change a developer can confidently accept.

**This is joint work with Ayanda Patrick Herlihy (co-first author), Ahmad Saleem Mirza, Ali Afoud, and Prof. Fatemeh Fard at the University of British Columbia, Kelowna.**
