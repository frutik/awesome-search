---
title: "Choosing Your Search Relevance Evaluation Metric"
source: "https://opensourceconnections.com/blog/2020/02/28/choosing-your-search-relevance-metric/"
author:
  - "[[Nate Day]]"
published: 2020-02-28
created: 2026-05-15
description: "When to use Precision, Average Precision, CG, DCG, and nDCG — and how result display format (grid vs. list) should drive the choice."
tags:
  - clippings
---
# Choosing Your Search Relevance Evaluation Metric

"Each metric tells you something different about how search is satisfying your users." No universal best — depends on your situation.

## Metrics overview

| Scale | Metric | Measures | Drawback |
|---|---|---|---|
| Binary | Precision (P) | Relevance of entire results set | Ignores position |
| Binary | Average Precision (AP) | Relevance for sequential scanning | Large impact of low-rank results |
| Graded | Cumulative Gain (CG) | Information gain from results | Ignores position |
| Graded | DCG | Information gain with positional weighting | Hard to compare across queries |
| Graded | nDCG | How close to best possible | No longer shows raw information gain |

## Binary metrics

- **Precision**: relevant / total returned. Ignores ordering.
- **Average Precision**: computes precision at each relevant document position, then averages. Rewards early placement. Works well for list-format displays; may not suit grids.

## Graded scale (TREC Newstrack: 0–4)

- **CG**: sum of relevance grades. Ignores rank.
- **DCG**: CG with logarithmic discount by position (log₂(rank+1)). High-rank documents weighted more.
- **nDCG**: DCG / ideal DCG → 0–1 scale. Enables cross-query comparison. Blind spot: "nDCG reports values normalized to the best possible" — poor results can score 1.0 if they're the best available.

## How to choose

- **Grid display** (users browse multiple results): ranking less critical → Precision-based
- **List display** (sequential scanning): position matters → Average Precision or nDCG
- Use combination for best coverage — no single metric perfectly summarizes search performance

## Related Concepts
- [[Search Evaluation]] — metric selection is central to evaluation strategy
- [[NDCG]] — nDCG explained with pros and cons
- [[Precision and Recall]] — Precision and Average Precision explained
- [[Judgment Lists]] — judgment grades are input to all these metrics
- [[Diversity Metrics]] — grid display reduces need for positional weighting

## People
- [[Nate Day]] — OpenSource Connections; author