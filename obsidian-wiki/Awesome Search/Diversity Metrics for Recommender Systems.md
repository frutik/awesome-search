---
title: "Diving into Diversity Metrics: Elevate Your Recommender Systems in a Snap!"
source: "https://shunya-vichaar.medium.com/diving-into-diversity-metrics-elevate-your-recommender-systems-in-a-snap-57637de380e1"
author:
  - "[[Shunya Vichaar]]"
published: 2024-04-23
created: 2026-05-15
description: "Three diversity metrics for recommender systems: Coverage, Effective Catalog Size (ECS from Netflix), and Gini-Simpson Diversity Index."
tags:
  - clippings
---
# Diversity Metrics for Recommender Systems

"Diversity in recommendation systems can enrich user experience, but if not carefully managed, it may lead to information overload and decreased relevance."

## 1. Coverage

Breadth of unique items presented to users from the available pool.

```
Coverage (%) = (Unique items recommended / Total items available) × 100
```

Example: 10,000 titles, 2,000 unique recommendations → 20% coverage.

## 2. Effective Catalog Size (ECS)

From Netflix. Measures how many items represent typical streaming hours, accounting for individual viewing patterns and catalog dispersion.

Uses proportions (p) of streaming hours per item:

Example: 3 videos with 10, 6, 3 hours (19 total) → proportions 0.526, 0.316, 0.158 → ECS ≈ 2.263 items per typical hour.

## 3. Gini-Simpson Diversity Index

Population diversity on 0–1 scale. Higher = more diverse, lower = more concentrated.

```
D = Σ[nᵢ(nᵢ−1)] / N(N−1)
Simpson's Diversity Index = 1 − D
```

Example: 3 items with populations 300, 335, 365 → diversity index = 0.67 (substantial diversity).


## Related Concepts

- [[Diversity Metrics]]
- [[Search Evaluation]]
- [[Personalization]]

## People

- [[Shunya Vichaar]]
