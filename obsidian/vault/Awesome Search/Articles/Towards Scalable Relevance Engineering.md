---
type: article
title: "Towards Scalable Relevance Engineering"
source: "https://www.linkedin.com/pulse/towards-scalable-relevance-engineering-andreas-wagner-s3akf/"
author:
  - "[[Andreas Wagner]]"
published: 2026-08-04
created: 2026-08-05
concepts:
  - "[[Staged Judging]]"
  - "[[LLM as Judge]]"
  - "[[Implicit Judgments]]"
  - "[[Knowledge Distillation]]"
  - "[[Hard Negative Mining]]"
  - "[[Scalar Quantization]]"
topics:
  - "[[Search Quality Assurance]]"
  - "[[E-commerce Search]]"
companies:
  - "[[searchHub]]"
tags:
  - article
  - llm-judge
  - search-evaluation
  - scalability
  - embeddings
---

# Towards Scalable Relevance Engineering

**Source**: https://www.linkedin.com/pulse/towards-scalable-relevance-engineering-andreas-wagner-s3akf/
**Author**: [[Andreas Wagner]] ([[searchHub]])

## Summary

[[Andreas Wagner]] addresses a problem the [[LLM as Judge]] literature mostly avoids: the approach is economically impossible at real e-commerce scale. At [[searchHub]]'s volume — upwards of 10 billion searches annually, and hundreds of billions of query-document pairs — running a frontier model over every pair is not a budgeting difficulty but a non-starter.

The article is an architecture for making it viable anyway, in three moves. Together they form the worked example behind [[Staged Judging]].

## The Core Problem

Most published work on LLM judges optimizes **judgment quality** — how closely a model agrees with human raters. See [[Classic ML to Cope with Dumb LLM Judges]] and [[Improving Retrieval with LLM as a Judge]]. Wagner's constraint is different and orthogonal: given a fixed, adequate judge, how do you afford to run it across a catalogue?

Sampling is the usual answer, and it is insufficient here. A sampled judgment set tracks aggregate quality but cannot support tasks that need coverage — mining [[Hard Negative Mining|hard negatives]] across the full catalogue, or catching per-query regressions in the tail.

## Move 1: Radical Problem Reduction

The largest lever is not making judging cheaper but **judging far less**.

Implicit user feedback partitions the pair space before any model runs:

- **Easy positives** — results already performing well behaviorally. Re-evaluating them yields no information.
- **Potential hard negatives** — underperforming pairs where something may genuinely be wrong. These are worth real analysis.

Pruning on this basis reportedly removes **~93%** of the problem space. No model architecture delivers a comparable saving; the cheapest judgment is the one never made. See [[Implicit Judgments]].

## Move 2: Staged Judging

The survivors go through a cascade rather than straight to an LLM.

Lightweight first-stage judges built on embedding models — `intfloat/multilingual-e5-large` under INT8 [[Scalar Quantization|quantization]], and `BAAI/bge-m3` — resolve **75–85%** of remaining pairs on their own. Only pairs where the cheap judges disagree escalate to a full LLM, on the reasoning that disagreement is a serviceable proxy for genuine difficulty.

This is [[Multi-Stage Ranking]] logic relocated from serving to evaluation: cheap coverage over everything, expensive precision over the residual.

## Move 3: Distillation Into Production

Roughly **100,000** LLM judgments become training data. Fine-tuning `intfloat/multilingual-e5-small` on them via [[Knowledge Distillation]] yields a model with **sub-20ms CPU inference** — cheap enough to run continuously in production rather than as a periodic offline batch.

This closes the loop. The distilled judge handles routine cases, the LLM is reserved for the genuinely hard residual, and each cycle needs fewer escalations. It is the same manoeuvre [[Daniel Tunkelang]] describes in [[Distilling Retrieval Pipelines to a Single Embedding Model]], applied to the judge rather than the retriever.

## Why It Matters

The vault's LLM-judge cluster is almost entirely about **judge quality**. This article is the **judge economics** counterpart, and the distinction is load-bearing: a judge that is 95% accurate and unaffordable produces no judgments at all, which is strictly worse than a 90% judge you can actually run over the catalogue.

The pattern generalizes well beyond searchHub's scale. Any team whose evaluation ambitions exceed its budget — which is most of them — can apply the same sequence: prune with behavioral signal, cascade by difficulty, distill what the expensive model taught you.

## Caveats Worth Holding

- The 93% pruning figure depends entirely on trusting behavioral signals. Where those are distorted by position bias or prior ranking, the pruning inherits the distortion and hides it upstream of everything downstream. See [[Clicks Residual]] and [[Click Models]].
- Cheap-judge agreement is not correctness. Two quantized embedding models can be confidently wrong together, particularly on the ambiguous pairs that motivated the system.
- Figures are as reported by the author from production at searchHub; there is no external replication.

## Related

- [[Staged Judging]] — the concept this article instantiates
- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]] on ensembling weak judges; complementary attack on the same wall
- [[Search Quality Assurance with AI as a Judge]] · [[Using LLMs to Amplify Human Labeling and Improve Dash Search Relevance]]
- [[Embedding Models Compared]] — the models used as first-stage judges
- [[Three Pillars of Search Quality - Findability]] — Wagner's other framework in the vault
