---
type: concept
title: "Implicit Judgments"
aliases: ["implicit judgments", "implicit judgements", "implicit feedback", "implicit relevance labels"]
tags:
  - concept
  - ranking
  - evaluation
  - learning-to-rank
created: 2026-06-11
---

# Implicit Judgments

## Definition

Implicit judgments are relevance labels **derived from observed user behavior** — clicks, add-to-cart, purchases, dwell time, and (as negative signals) impressions without interaction — rather than from explicit human annotation. They are the implicit counterpart to curated [[Judgment Lists]].

## Why it matters

Behavioral labels scale far beyond manual annotation and reflect real user intent, making them the dominant training signal for production [[Learning to Rank|LTR]] models. A clicked item is a positive signal; a shown-but-ignored item is negative (e.g. [[Metarank]]'s `ImpressionInject` synthesizes these negatives). Aggregated click-through events become the implicit judgments used to train [[LambdaMART]].

**Caveat:** implicit judgments inherit [[Position Bias]] and [[Presentation Bias]] — items shown higher get more clicks regardless of relevance — so debiasing (e.g. IPS) matters before training.

## As a Pruning Signal, Not Just a Label Source

A second use, distinct from supplying training labels: implicit signals can decide **which pairs are worth evaluating at all**.

Partitioning query-document pairs by behavioral performance separates *easy positives* — results already performing well, where a judgment adds no information — from *candidate hard negatives*, the underperforming pairs where something may genuinely be wrong. Only the latter need expensive evaluation. At e-commerce scale this pruning has been reported to remove ~93% of the pair space before any model runs, which is a far larger saving than any efficiency gain in the judge itself. See [[Staged Judging]] and [[Towards Scalable Relevance Engineering]].

The same bias caveat applies with more force here. When behavioral signals are distorted by [[Position Bias|position]] or [[Presentation Bias|presentation]], the distortion no longer merely skews training weights — it removes pairs from evaluation entirely, so the resulting blind spot is invisible to everything downstream.

## Related Concepts

- [[Judgment Lists]] — explicit, human-annotated counterpart
- [[Click Signals]] · [[Click Models]] — the raw behavioral data
- [[User Behavior Insights]] — open standard (UBI) for capturing the query/event stream these labels are derived from
- [[Learning to Rank]] · [[LambdaMART]] — what they train
- [[Position Bias]] · [[Presentation Bias]] — biases to correct for

## Articles

- [[Learn-to-Rank with OpenSearch and Metarank]] — events aggregated into implicit judgments
- [[Metarank - Personalized Ranking That Actually Reads Your Clicks]]
- [[What Is a Judgment List]]
