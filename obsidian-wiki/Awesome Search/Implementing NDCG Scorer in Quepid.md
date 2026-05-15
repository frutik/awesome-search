---
title: "How to Implement a Normalized Discounted Cumulative Gain (NDCG) Ranking Quality Scorer in Quepid"
source: "https://opensourceconnections.com/blog/2018/02/26/ndcg-scorer-in-quepid/"
author:
  - "[[Bertrand Rigaldies]]"
published: 2018-02-26
created: 2026-05-15
description: "Step-by-step guide to implementing a custom NDCG@10 scorer in Quepid using JavaScript — with the DCG, ideal DCG, and nDCG calculation approach."
tags:
  - clippings
---
# Implementing NDCG Scorer in Quepid

**Quepid** is a Test-Driven Relevancy Dashboard for relevancy practitioners — enables examining individual queries and system-level monitoring across test cases.

## Quepid scorer components

1. Descriptive name
2. JavaScript code computing query scores
3. Rating scale (default 1–10)
4. Optional rating labels

## NDCG@10 mathematics

**CG**: sum of ratings through rank position p

**DCG**: `Σ rating(i) / log₂(i + 1)` — logarithmic position discounting

**nDCG**: `DCG / ideal_DCG` → 0.0–1.0 scale, enabling cross-query comparison

## Implementation steps

1. Mock Quepid objects (`docs`, `bestDocs`) in JSFiddle/CodePen for debugging
2. Create helper functions for rating retrieval and log calculations
3. Implement `actualRatings()` and `idealRatings()` functions
4. Compute DCG for both result sets
5. Return ratio via `setScore()`

## Quepid integration

1. Navigate to Custom Scorers → Add New
2. Name (e.g., "NDCG@10")
3. Paste JavaScript implementation
4. Select scorer in case settings
5. Re-run evaluations

**Note**: "Number of Results to Show" setting must accommodate the desired rank position parameter; `bestDocs` capped at 10 results maximum.


## Related Concepts

- [[NDCG]]
- [[Search Evaluation]]
- [[Judgment Lists]]

## People

- [[Bertrand Rigaldies]]
