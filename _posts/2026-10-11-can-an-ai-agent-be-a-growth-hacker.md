---
title: Can an AI Agent Be a Growth Hacker?
description: Off-policy evaluation, a classic problem in reinforcement learning, is how companies estimate a new policy's impact from logged data instead of a live A/B test. We asked whether LLM agents can keep that code tuned on their own, and measured how often they make things better, worse, or simply break.
permalink: /blog/growthhacker.html
authors: Jie JW Wu*, Ayanda Patrick Herlihy*, Ahmad Saleem Mirza, Ali Afoud, Fatemeh Fard (*co-first authors)
paper:
  title: "GrowthHacker: Automated Off-Policy Evaluation Optimization Using Code-Modifying LLM Agents"
  authors: Jie JW Wu*, Ayanda Patrick Herlihy*, Ahmad Saleem Mirza, Ali Afoud, Fatemeh Fard (*co-first authors)
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

Every product team has more ideas than it can test. A new ranking model for the feed, a different order for friend suggestions, a tweak to the ad auction. The bottleneck is rarely the idea. It's proving the idea works before you bet real users on it.

The standard way to prove it is an **online A/B test**: ship the change to a slice of users, wait, and compare. I spent years on a growth team doing exactly this, and I can tell you where the time goes. Building the variant to production standards. Getting sign-off, because a buggy variant hurts real people. Then waiting weeks for enough data to say anything, often through several rounds. Good ideas sit in a queue behind the test calendar.

There is a cheaper route. **Offline A/B testing**, which researchers call *off-policy evaluation* (OPE), uses the logs you already have to *estimate* how a new policy would have performed, without ever deploying it. No user harm, no weeks of waiting. The catch is that the estimate is only as good as the estimator code behind it: which method you use, how it's configured, which hyperparameters you picked. In practice that code gets written once, tuned by hand, and then left alone while the data underneath it keeps changing.

It's worth pausing on how much rides on that code. OPE is not a niche trick for A/B testing. It is a classic, heavily studied problem in reinforcement learning and bandits: given data collected under one decision policy, estimate how a different policy would have done. Recommender systems, ad auctions, search ranking, and increasingly healthcare and robotics all lean on it, because in each of those settings trying every candidate policy live is too slow, too expensive, or too dangerous. Any improvement in how well, and how reliably, OPE code is maintained pays off across all of them. That is why we think a benchmark for *automatically optimizing OPE code* is worth building, independent of the growth-hacker framing.

In industry, the person who refuses to leave it alone has a name: a **growth hacker**. Someone who relentlessly tweaks, measures, keeps what helps, and throws away what doesn't. Our question in this paper was simple. *Can an AI agent do that job?*

## The loop

The setup is a loop. An LLM, or a team of LLM agents, reads the OPE code, modifies it, runs it on real benchmark data, and checks whether the evaluation metric got better. Then it tries again.

<figure class="post-figure">
  <a href="{{ '/assets/img/blog/gh-loop.png' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/img/blog/gh-loop.png' | relative_url }}" alt="Diagram of the GrowthHacker loop: an LLM-based agent takes the original OPE code as input, produces modified code, both versions are executed on OBP or Scope-RL datasets, and the new results are compared with the original to decide whether the metric improved before the next iteration.">
  </a>
  <figcaption>The GrowthHacker loop: the agent edits the estimator code, runs it, compares the result against the original, and iterates. <em>(click to enlarge)</em></figcaption>
</figure>

We tried four ways of running that loop, all on the same underlying model (Gemini 2.5 Flash):

- **Default**: a single LLM with no agent framework at all.
- **AutoGen** and **CrewAI**: two popular general-purpose multi-agent frameworks.
- **two_agent**: a deliberately small framework we built ourselves. One *analyzer* agent writes an instruction file saying what to change; one *coder* agent makes the change. Every iteration starts again from the original code, not from the previous attempt, and a final step picks the best iteration out of the batch.

The playground was 18 real OPE notebooks from two widely used open-source libraries, [Open Bandit Pipeline](https://github.com/st-tech/zr-obp) and [Scope-RL](https://github.com/hakuhodo-technologies/scope-rl), covering recommendation and advertising scenarios. The agents' goal was to lower the estimators' error, or raise the estimated policy value, depending on the library. Across frameworks and settings this came to hundreds of runs.

## What happened

Three questions matter for an automated growth hacker: does it break things, does it help, and by how much?

**Does it break things?** The general-purpose frameworks produced code that failed to run roughly one time in ten. Default completed 89.5% of runs, CrewAI 90.1%, AutoGen 92.6%. The failures were mostly mundane: syntax errors, parameters placed in the wrong spot, and in AutoGen's case, diff-style markup leaking into what was supposed to be a whole file. Our constrained two_agent framework completed 98.1% to 100% of runs.

**Does it help?** When a run did complete, two_agent improved the metric 78% of the time. AutoGen and Default each managed 65%, CrewAI 63%. The rest of the time the agent either changed nothing measurable or made the estimator worse.

**By how much?** Here the averages and the medians tell different stories, and both are worth reading. Among improved runs, two_agent's *median* gain was 4.4%: a modest, dependable nudge. CrewAI had the highest *average* improvement at 37.9%, driven by a few spectacular wins, but a median of only 1.6%. CrewAI was also the only framework that never produced an "extreme" failure, where a change blew the metric up by orders of magnitude. The other three did so in about 1% of runs. Numerical explosions in continuous action spaces were the usual culprit: a hyperparameter nudged past a cliff the agent didn't know was there.

## The lesson we didn't expect

Going in, I assumed the more sophisticated frameworks would win. They didn't. **More machinery did not mean better results.** The two-agent setup, which does less, was the most reliable, and its reliability came from constraints: a narrow job for each agent, a fresh start every iteration, and a strong bias toward edits that today's models can execute dependably.

One detail makes this concrete. We tried giving the agents the history of their previous iterations, so they could learn from what had already been tried. It made things worse. The models got confused by the extra context and failed more often. Restarting from the original code each time, which looks wasteful, was the setting that worked.

That matches a broader pattern we keep seeing in our lab: the gap between an LLM that *can* do a task and a system that does it *reliably* is mostly closed by constraints, not by capability.

## What we are not claiming

Being upfront about the boundaries of this result matters more than the headline numbers.

- We tested one model, Gemini 2.5 Flash, in one language, Python, on 18 notebooks from two libraries. The experiments were run in 2025. Other models, and newer ones, may behave differently.
- We built two_agent, and it is the best performer on a benchmark we also built. Read that comparison with the appropriate skepticism.
- Even for two_agent, about 22% of attempts changed nothing or made the estimator worse. This is a tool for proposing improvements, not for silently applying them.
- We measured only the OPE metric. Whether the modified code is readable, efficient, or maintainable, we did not score.
- The edits were deliberately conservative: hyperparameters and small function changes. Broader rewrites failed more often, and we don't yet know how to make them safe.

For anything high-stakes, we recommend a human in the loop. The agent should hand you a ranked list of candidate changes with their measured effect; you decide what ships.

## Why this matters

The reason to care isn't that an agent can shave a few percent off an estimator's error. It's what the loop makes possible once it runs on its own. Offline evaluations today are snapshots: computed once, trusted for months, quietly drifting from the data they were built on. An agent that re-runs and re-tunes them continuously, inside the same CI/CD pipeline that already runs your tests, turns a snapshot into a live signal. That is the "silent growth hacker" we have in mind, and this paper is our evidence that it is feasible, with the caveats above.

This work grew out of a short [vision paper]({{ '/assets/AutoOffAB-fse-camare-ready.pdf' | relative_url }}) I wrote in 2024, AutoOffAB, arguing that offline A/B testing needed exactly this kind of systematic, automated updating. GrowthHacker is the first serious attempt to build it, and the benchmark, code, and all run data are public so that others can try to do better.

**This is joint work with Ayanda Patrick Herlihy (co-first author), Ahmad Saleem Mirza, Ali Afoud, and Prof. Fatemeh Fard at the University of British Columbia, Kelowna.**
