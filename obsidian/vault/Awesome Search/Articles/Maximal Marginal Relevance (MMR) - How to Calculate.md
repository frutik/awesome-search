---
title: "Understanding Hit Rate, MRR, and MMR Metrics"
source: "https://www.analyticsvidhya.com/blog/2024/07/hit-rate-mrr-and-mmr-metrics/#h-how-to-calculate-mmr"
author:
  - "[[Badrinarayan M]]"
published: 2024-07-12
created: 2026-05-15
description: "How to calculate Maximum Marginal Relevance (MMR) — a re-ranking strategy balancing relevance and diversity using the λ parameter."
tags:
  - clippings
---
# Maximum Marginal Relevance (MMR)

MMR is a re-ranking strategy that balances **relevance** and **diversity** — ensuring "items returned are both relevant and sufficiently varied to address all facets of the query."

## Formula

MMR score = λ × Sim(document, query) − (1−λ) × max Sim(document, previously_selected)

- **λ → 1**: prioritizes relevance
- **λ → 0**: emphasizes diversity

## How it works (iterative selection)

For each iteration, pick the candidate with the highest MMR score — balancing similarity to the query against similarity to already-selected documents.

Example: nodes [N2, N3, N1] for query Q1:
1. Select N1 first (highest relevance: 0.9)
2. Compute MMR scores for N2, N3 penalizing similarity to N1
3. Select N3
4. Final order: [N1, N3, N2]

## Key benefit

Minimizes redundancy — the top N results provide meaningful variety, eliminating clustering of similar items. Enables comprehensive answers addressing multiple query dimensions.


## Related Concepts

- [[Diversity Metrics]]
- [[Search Evaluation]]
- [[Retrieval Pipeline]]

## People

- [[Badrinarayan M]]
