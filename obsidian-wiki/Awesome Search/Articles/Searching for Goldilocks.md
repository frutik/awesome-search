---
title: "Searching for Goldilocks"
aliases: ["Goldilocks Search Diversity", "Tunkelang Goldilocks"]
tags:
  - clippings
  - search
  - diversity
source: "https://queryunderstanding.com/searching-for-goldilocks-b7f5c66c5cff"
author: "Daniel Tunkelang"
created: 2026-05-15
concepts:
  - Diversity Metrics
  - Faceted Search
  - Search Evaluation
---

# Searching for Goldilocks

**Source:** https://queryunderstanding.com/searching-for-goldilocks-b7f5c66c5cff
**Author:** [[Daniel Tunkelang]]

## Summary

The Goldilocks problem in search diversity: too little diversity wastes result-list real estate on near-duplicates; too much pushes down the most relevant items. The optimum lies somewhere in between — "just right."

Tunkelang frames diversity through the **Wundt Curve**: user satisfaction increases with diversity up to a point, then drops as the result set becomes incoherent. The challenge is finding that peak.

### Why Diversity Matters
- Hedges against uncertainty about query intent
- Surfaces unexpected relevant items users didn't know to ask for
- Avoids redundancy in a ranked list

### NP-Hardness of Optimal Diversification
Finding the globally optimal diverse set is NP-hard. Practical approaches use greedy approximations — add items one at a time, each time choosing the next item that maximizes marginal relevance minus a diversity penalty.

### Maximal Marginal Relevance (MMR)
Classic formula:
```
score(d) = λ × rel(d, q) − (1−λ) × max_sim(d, already_selected)
```
Lambda controls the relevance-diversity trade-off.

### Tension with Precision
High-precision metrics (P@k, NDCG@k) reward near-duplicate top hits. If you optimize purely for precision, diversity suffers. Need explicit diversity-aware metrics (e.g., α-nDCG, intent-aware metrics).

## Key Concepts
- **Wundt Curve** — inverted-U relationship between diversity and user satisfaction
- **MMR (Maximal Marginal Relevance)** — greedy diversification scoring
- **NP-hardness** — exact diversity optimization is computationally intractable
- **λ trade-off** — tunable balance between relevance and novelty

## Related Concepts
- [[Diversity Metrics]]
- [[Search Evaluation]]
- [[Faceted Search]]
- [[Search Intent]]
- [[NDCG]]

## Related Articles
- [[Thoughts on Search Result Diversity]]
- [[Facets - Constraints or Preferences]]
- [[Facets, But Which Ones]]
- [[Evaluating Good Search - Measure It]]

## People
- [[Daniel Tunkelang]]
