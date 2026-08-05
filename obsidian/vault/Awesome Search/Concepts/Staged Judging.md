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

## Caveats

- **Cheap-stage agreement is not correctness.** Two weak judges can be confidently wrong together, especially when they share a base model or training corpus. Correlated errors pass through the cascade unchallenged. Audit a sample of the auto-accepted pairs against human labels, not just the escalated ones.
- **Escalation rate is a tuning knob with a quality cost.** Driving it down saves money and quietly degrades judgment quality on exactly the hard cases you built the system for.
- **The pruning step encodes an assumption** — that behavioral signals are trustworthy. Where they are biased by position, presentation, or prior ranking, the pruning inherits the bias and hides it upstream of everything else. See [[Clicks Residual]] and [[Click Models]].

## Related Concepts

- [[LLM as Judge]] — the expensive stage this economizes
- [[Implicit Judgments]] — supplies the pruning signal
- [[Knowledge Distillation]] — closes the loop
- [[Hard Negative Mining]] — a main consumer of high-coverage judgments
- [[Reranking]] · [[Retrieval Pipeline]] — the same cascade logic in serving
- [[Judgment Lists]] · [[Search Evaluation]]

## Related Topics

- [[Search Quality Assurance]] · [[Model Selection and Fine-Tuning Evaluation]]

## Articles

- [[Towards Scalable Relevance Engineering]] — [[Andreas Wagner]]; the worked architecture at [[searchHub]] scale
- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]]; the complementary move of ensembling weak judges rather than staging them
