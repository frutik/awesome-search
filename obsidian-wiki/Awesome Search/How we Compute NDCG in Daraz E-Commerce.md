---
title: "How we Compute NDCG in Daraz (E-Commerce)"
source: "https://medium.com/@hassam.chundrigar520/how-we-compute-ndcg-in-daraz-e-commerce-9a103b444c9f"
author:
  - "[[Hassam Chundrigar]]"
published: 2022-10-17
created: 2026-05-15
description: "Daraz's (Alibaba Group) NDCG implementation for e-commerce search — using purchase/cart/click relevance weights, top-10 evaluation, and Python/SQL implementation."
tags:
  - clippings
---
# How we Compute NDCG in Daraz (E-Commerce)

NDCG evaluates ranking quality through three principles: relevance hierarchy, position weighting, and query independence. Selected as "the most simple and widely used measure in ranking evaluation."

## Relevance weights from user funnel

| Action | Score |
|---|---|
| Purchase | 5 |
| Add to Cart | 2 |
| Click | 1 |

## Implementation assumptions

1. **Top-10 only** — lower positions yield negligible impact
2. **Clicked-only instances** — focus on searches with at least one product interaction
3. **A/B-test ready** — supports comparison across multiple ranking algorithms

## Calculation

- **DCG**: weighted relevance sum with position-based discount factors
- **IDCG**: same calculation on perfectly-ranked items based on actual user behavior
- **NDCG** = DCG / IDCG

Implementation: Python UDFs for individual search instance calculation + SQL aggregation across datasets.


## Related Concepts

- [[NDCG]]
- [[Search Evaluation]]
- [[Click Signals]]
- [[Judgment Lists]]

## People

- [[Hassam Chundrigar]]
