---
type: tool
title: "GEPA"
aliases: ["Genetic-Pareto", "GEPA optimizer", "gepa"]
tags:
  - tool
  - llm
  - prompting
  - optimization
  - open-source
repo: https://github.com/gepa-ai/gepa
website: https://arxiv.org/abs/2507.19457
related_concepts:
  - "[[Prompt Optimization]]"
  - "[[Prompt Sensitivity]]"
  - "[[Brier Score]]"
created: 2026-09-20
---

# GEPA

**GEPA** — "Genetic-Pareto" — is a prompt optimizer that learns from evaluation feedback and
automatically revises a model's instructions. Proposed by Agrawal et al. in *GEPA: Reflective
Prompt Evolution Can Outperform Reinforcement Learning* (arXiv:2507.19457, accepted to ICLR
2026), and distributed as a Python package.

🔗 https://github.com/gepa-ai/gepa · https://arxiv.org/abs/2507.19457

## How It Works

The loop is reflective rather than gradient-based:

1. A **generative model inspects examples and failures** from the current instruction and
   proposes revisions.
2. Subsequent evaluations on held-out examples decide whether a revision actually helped.
3. **Pareto selection** keeps multiple candidates alive — those that perform well on *different*
   examples — rather than collapsing to a single best-so-far, so the search does not commit
   early to one local optimum.

The framework handles minibatch sampling, candidate acceptance, Pareto parent selection and
validation scoring. Crossover between candidates is available and can be disabled.

Crucially, the model being *optimized* and the model doing the *reflecting* are different
things. The optimizer needs a generative model to write revisions; the system under optimization
does not have to be generative at all.

## Optimizing a Non-Generative Model

That separation is what makes [[Adapting Jev to Your Domain with GEPA]] possible, and it is the
most interesting property of GEPA for this vault. [[Jev]] generates no text and cannot reflect
on its own failures — but it does return a probability, which is all an optimization metric
needs. [[Praneeth Paikray]] pointed GEPA at a [[Jev]] instruction with an assistant supplying
the four candidate revisions and [[Jev]]'s squared errors supplying the score.

The objective choice is the instructive part: **minimize [[Brier Score|Brier score]]**, not
maximize accuracy. Optimizing the probability quality rather than the label improved the labels
anyway — F1 rose 10.62 points and Brier fell 44.9% on a fresh test set.

The search there was deliberately small: 4 proposals, 20 reflection examples per round,
crossover disabled, capped at 700 metric calls and using 660 across 100 training and 100
validation examples. Validation Brier by candidate ran 0.1250 (the original) → 0.0915 → **0.0839
(selected)** → 0.0899 → 0.1029 — later proposals getting worse, which is the shape a Pareto
front is meant to survive.

What the winning revision did was name the failure modes explicitly: require an identifiable
drug, a specific harmful effect, and a stated relation between them; forbid reconstructing
context from outside the sentence or inferring toxicities the model happened to know. The
optimizer, in other words, diagnosed the two error families from the evaluation feedback and
wrote them out of the instruction. The prompt grew from 503 to 2,020 characters, raising mean
input tokens per request by about 64%.

## Why It Matters Here

Every relevance judge is a prompt, and [[Prompt Sensitivity]] says that prompt is part of the
measuring instrument. GEPA is one of the few concrete answers: if rewording moves the numbers,
optimize the wording against a metric instead of authoring it. That reframing is the same one
[[DSPy]] makes structurally, and the same reason a [[LLM as Judge|judge]] rubric deserves a
held-out set of its own.

The caveat is the one [[Praneeth Paikray]] states himself: an optimizer fit to a labelled corpus
may learn that corpus's **annotation conventions** rather than the underlying truth, and nobody
independently adjudicated the labels it was fit to. The gains are real on the held-out split and
unvalidated beyond it.

## Related Concepts

- [[Prompt Optimization]] — the category
- [[Prompt Sensitivity]] — the problem it answers
- [[Brier Score]] — the objective used in the one worked example here
- [[Calibrated Relevance Probability]] — what optimizing for Brier actually improves
- [[LLM as Judge]] — the judge rubrics this technique applies to

## Related Tools

- [[DSPy]] — the other framework in this vault built on "the prompt is a parameter, not a constant"
- [[Jev]] — optimized by GEPA in the worked example, despite generating no text itself

## Related Articles

- [[Adapting Jev to Your Domain with GEPA]] — [[Praneeth Paikray]]; GEPA applied to a System One model
