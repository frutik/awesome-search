---
title: "Measuring Search: Metrics Matter"
source: "https://jamesrubinstein.medium.com/measuring-search-metrics-matter-de124c2f6f8c"
author:
  - "[[James Rubinstein]]"
published: 2020-07-06
created: 2026-05-15
description: "A guide to search evaluation metrics: Recall, Precision, P@K, MRR, MAP, CG, DCG, nDCG — with guidance on when to use each based on query type and user task."
tags:
  - clippings
  - medium
---
# Measuring Search: Metrics Matter

"What gets measured gets managed." Different metrics optimize for different aspects of search quality.

## Binary relevance metrics

- **Recall**: proportion of relevant corpus documents appearing in results
- **Precision**: proportion of returned results that are relevant
- Inherent tradeoff: completeness vs. user effort

Most engagement happens in the **top 5 results** — metric focus should reflect this.

### P@K (Precision at K)
Relevant documents / K. Assumes you need K relevant results — breaks down for navigational queries seeking one specific result.

### MRR (Mean Reciprocal Rank)
Score = 1 / rank_of_first_relevant. Perfect for navigational queries, undervalues research tasks needing multiple documents.

### MAP (Mean Average Precision)
Adapts K to actual user behavior — measures precision up to the last engaged document. Flexible: accommodates both navigational and exploratory searches.

## Graded relevance metrics

Assign nuanced scores (e.g., 0–3: irrelevant → highly relevant). Online: clicks=1, downloads=2, shares=3.

### CG (Cumulative Gain)
Sum of relevance scores. Ignores position.

### DCG (Discounted Cumulative Gain)
Logarithmic discount by position — high-rank results more valuable. Best for ensuring top results are best.

### nDCG (Normalized DCG)
DCG / ideal DCG → 0–1. Critical limitation: **only evaluates ranking quality of returned documents** — a poor set perfectly ranked scores high. Best used comparing algorithm versions, not standalone evaluation.

## Choosing the right metric

| Query type | Best metric |
|---|---|
| Navigational (one answer) | MRR or nDCG |
| Research (multiple options needed) | P@K or CG@K |
| Good ranking + recall | DCG@K |
| Unknown task type | MAP |


## Related Concepts

- [[Search Evaluation]]
- [[NDCG]]
- [[MRR]]
- [[Precision and Recall]]
- [[Judgment Lists]]

## People

- [[James Rubinstein]]
