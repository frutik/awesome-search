---
type: concept
title: "Staged Judging"
aliases: ["cascaded judging", "staged relevance judging", "judge cascade", "tiered LLM judging"]
tags:
  - concept
  - search-evaluation
  - llm-judge
  - scalability
created: 2026-08-05
---

# Staged Judging

## Definition

Staged judging applies cascade architecture to **relevance evaluation** rather than to retrieval. Cheap first-stage judges resolve the large, easy majority of query-document pairs; only pairs where the cheap judges disagree or express low confidence escalate to an expensive [[LLM as Judge]].

It is the same economic logic as [[Multi-Stage Ranking]] — spend compute in proportion to difficulty — pointed at the evaluation pipeline instead of the serving pipeline.

## The Problem It Solves

[[LLM as Judge]] works well and does not scale. At web or large e-commerce volumes — billions of annual searches, hundreds of billions of query-document pairs — running a frontier model over every pair is economically impossible, regardless of how good the judgments are.

The usual response is to sample: judge a few thousand pairs and generalize. That works for tracking aggregate quality but fails for tasks that need coverage rather than an estimate — mining [[Hard Negative Mining|hard negatives]] across a full catalogue, or detecting per-query regressions in the tail.

## The Architecture

1. **Prune first.** Most pairs do not need judging at all. [[Implicit Judgments|Behavioral signals]] identify *easy positives* — results already performing well, where a judgment would tell you nothing you don't know — and *candidate hard negatives*, the underperforming pairs actually worth examining. This reduction is the largest single lever, capable of removing the overwhelming majority of the problem space before any model runs.
2. **Cheap judges next.** Quantized [[Bi-Encoder|bi-encoder]] models score the surviving pairs at CPU speed. Where an ensemble of cheap judges agrees confidently, accept their verdict.
3. **Escalate disagreement.** Only pairs where the cheap stage is split or uncertain go to the full LLM. Disagreement is a good proxy for genuine difficulty.
4. **Distill the result.** LLM judgments become training data. A small model fine-tuned on them via [[Knowledge Distillation]] absorbs much of the judge's behaviour at production-serving cost, closing the loop so the next cycle needs fewer escalations.

## Why It Works

The distribution of difficulty is extremely skewed. Most query-document pairs are obviously relevant or obviously irrelevant, and a small model settles them as well as a large one. The expensive model's advantage only appears on genuinely ambiguous pairs — which are a small fraction of the total, but the fraction that determines whether your judgments are any good.

Cascading exploits that skew directly. It is the same reason [[Reranking]] works in serving: cheap recall over everything, expensive precision over a shortlist.

## Measuring the Bands, Not the Metric

The pattern is usually justified with an accuracy or F1 figure, which is the wrong quantity. What
a staged setup actually buys is **queue reduction at an acceptable loss rate**, and that needs its
own table.

[[Adapting Jev to Your Domain with GEPA]] reports one, on literature screening rather than
relevance judging, and the framing transfers directly. Thresholds are picked on a validation set,
then the fresh test set is described in the terms an operator cares about:

| Prompt | Cutoff | In review | Deprioritized | Positives deferred | Positive retention |
|---|---|---|---|---|---|
| Original | 0.400 | 106 | 194 | 4 | 93.4% |
| Optimized | 0.400 | 78 | 222 | 6 | 90.2% |

The optimized prompt is better on every classification metric — F1 69.1% → 79.7% — and *worse* on
the quantity that decides whether it ships, since it defers two more true positives. Whether 28
fewer items to read is worth those two is a policy question, and the metric table cannot answer
it.

One practical note from the same study. The threshold signal is only as fine as the validation
positives: with 21 of them, deferring one clears a 95% retention target and deferring two fails
it, so the cutoff is being chosen on a very coarse grid — and the optimized prompt, chosen at a
cutoff that met the bar on validation, then retained 90.2% on the held-out split.
## Caveats

- **Cheap-stage agreement is not correctness.** Two weak judges can be confidently wrong together, especially when they share a base model or training corpus. Correlated errors pass through the cascade unchallenged. Audit a sample of the auto-accepted pairs against human labels, not just the escalated ones.
- **Escalation rate is a tuning knob with a quality cost.** Driving it down saves money and quietly degrades judgment quality on exactly the hard cases you built the system for.
- **Whether the cascade inherits the judge's biases is unstudied.** The architecture is validated on accuracy — does the cheap stage label like the expensive one — but a distilled student can reproduce a teacher's systematic errors as faithfully as its correct calls, and then serve them at production scale. Nothing in the cascade design detects that. See [[Adversarial Relevance Judgment]].
- **The headline pruning numbers are one team's production figures.** The ~93% pruned and 75-85% auto-settled rates come from a single deployment, reported by its author, and have not been replicated elsewhere.
- **The pruning step encodes an assumption** — that behavioral signals are trustworthy. Where they are biased by position, presentation, or prior ranking, the pruning inherits the bias and hides it upstream of everything else. See [[Clicks Residual]] and [[Click Models]].

## Related Concepts

- [[LLM as Judge]] — the expensive stage this economizes
- [[Implicit Judgments]] — supplies the pruning signal
- [[Knowledge Distillation]] — closes the loop
- [[Hard Negative Mining]] — a main consumer of high-coverage judgments
- [[Reranking]] · [[Retrieval Pipeline]] — the same cascade logic in serving
- [[Adversarial Relevance Judgment]] — the open question of whether cascades inherit exploitable weaknesses
- [[Levels of Judge Agreement]] — what the cascade's quality should actually be validated against
- [[Judgment Lists]] · [[Search Evaluation]]
- [[Brier Score]] · [[Expected Calibration Error]] — whether the band boundaries mean what they claim

## Related Topics

- [[Search Quality Assurance]] · [[Model Selection and Fine-Tuning Evaluation]]

## Articles

- [[Towards Scalable Relevance Engineering]] — [[Andreas Wagner]]; the worked architecture at [[searchHub]] scale
- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]]; the complementary move of ensembling weak judges rather than staging them
- [[Do LLM Judges Actually Agree With Us]] — [[Andrew Kornilov]]; positions judge economics as an axis orthogonal to judge quality, and flags inherited bias as open
- [[Using TypeSafe's Jev for Evals]] — the escalation bands expressed as cutoffs on a calibrated probability: act on the confident tail, route the ambiguous middle to a human, discard the rest
- [[Jev - The Most Interesting Model Released This Year]] — the same escalation shape inside an agent loop; see [[Jevals]] for the implementation
- [[Adapting Jev to Your Domain with GEPA]] — [[Praneeth Paikray]]; the bands reported as a review-policy table rather than an F1 number
