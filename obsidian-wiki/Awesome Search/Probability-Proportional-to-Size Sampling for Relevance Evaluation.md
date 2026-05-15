---
title: "How to succeed with explicit relevance evaluation using Probability-Proportional-to-Size sampling"
source: "https://opensourceconnections.com/blog/2022/10/13/how-to-succeed-with-explicit-relevance-evaluation-using-probability-proportional-to-size-sampling/"
author:
  - "[[Nate Day]]"
published: 2022-10-13
created: 2026-05-15
description: "Practical guide to explicit relevance evaluation: why PPTSS beats simple random sampling, how many queries to start with (50), and timeline expectations."
tags:
  - clippings
---
# Explicit Relevance Evaluation with Probability-Proportional-to-Size Sampling

Explicit relevance evaluation: domain experts manually rate search result quality. Less initial investment than implicit methods (click analysis), stronger direct signal.

## Why PPTSS over simple random sampling

**Probability-proportional-to-size sampling** weights frequent queries appropriately while still including less common ones — creating samples that mirror actual user traffic patterns. Simple random sampling over-represents tail queries.

## Practical guidance

### Query sample size
**Start with 50 queries.** This aligns with TREC standards and provides sufficient initial data. Multiple batches can follow.

### Query quality validation
Manually review to eliminate:
- Generic or ambiguous terms
- Queries affected by ranking rules
- Traffic unrelated to your inventory

Aim for ~50 viable queries after filtering.

### Timeline expectations
- Defining information needs: ~1 hour with subject matter experts
- For 50 queries × 2 rankers × depth 5 (500 total judgments): ~1h40m at ~5 ratings/minute

### Tooling
Tools like **Quepid** facilitate the explicit evaluation workflow.


## Related Concepts

- [[Search Evaluation]]
- [[Judgment Lists]]
- [[NDCG]]

## People

- [[Nate Day]]
