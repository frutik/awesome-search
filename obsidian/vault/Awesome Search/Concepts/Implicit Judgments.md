---
type: concept
title: "Implicit Judgments"
aliases: ["implicit judgments", "implicit judgements", "implicit feedback", "implicit relevance labels"]
tags:
  - concept
  - ranking
  - evaluation
  - learning-to-rank
---

# Implicit Judgments

## Definition

Implicit judgments are relevance labels **derived from observed user behavior** — clicks, add-to-cart, purchases, dwell time, and (as negative signals) impressions without interaction — rather than from explicit human annotation. They are the implicit counterpart to curated [[Judgment Lists]].

## Why it matters

Behavioral labels scale far beyond manual annotation and reflect real user intent, making them the dominant training signal for production [[Learning to Rank|LTR]] models. A clicked item is a positive signal; a shown-but-ignored item is negative (e.g. [[Metarank]]'s `ImpressionInject` synthesizes these negatives). Aggregated click-through events become the implicit judgments used to train [[LambdaMART]].

**Caveat:** implicit judgments inherit [[Position Bias]] and [[Presentation Bias]] — items shown higher get more clicks regardless of relevance — so debiasing (e.g. IPS) matters before training.

## Related Concepts

- [[Judgment Lists]] — explicit, human-annotated counterpart
- [[Click Signals]] · [[Click Models]] — the raw behavioral data
- [[Learning to Rank]] · [[LambdaMART]] — what they train
- [[Position Bias]] · [[Presentation Bias]] — biases to correct for

## Articles

- [[Learn-to-Rank with OpenSearch and Metarank]] — events aggregated into implicit judgments
- [[Metarank - Personalized Ranking That Actually Reads Your Clicks]]
- [[What Is a Judgment List]]
