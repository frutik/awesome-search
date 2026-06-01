---
title: Thoughts on Search Result Diversity
aliases:
  - Search Result Diversity
  - Tunkelang Diversity
tags:
  - clippings
  - search
  - diversity
  - medium
source: https://dtunkelang.medium.com/thoughts-on-search-result-diversity-1df54cb5bf4a
author: Daniel Tunkelang
created: 2026-05-15
concepts:
  - Diversity Metrics
  - Search Evaluation
  - Learning to Rank
---

# Thoughts on Search Result Diversity

**Source:** https://dtunkelang.medium.com/thoughts-on-search-result-diversity-1df54cb5bf4a
**Author:** [[Daniel Tunkelang]]

## Summary

A deeper treatment of diversity in ranked retrieval. Tunkelang distinguishes diversity as **ambiguity hedging** (the query might mean multiple things) versus **novelty seeking** (redundancy reduction even for unambiguous queries).

### Two Reasons to Diversify

1. **Ambiguity** — "jaguar" could be the car, the animal, or the OS. A diverse list covers multiple intents.
2. **Redundancy** — Even for clear queries, near-duplicate results waste rank positions.

### KL-Divergence Approach
One framing: the ideal result list should match the distribution of relevant documents across subtopics. Measure divergence between the list's topic distribution and the corpus's topic distribution using KL-divergence.

### Greedy Reranking
Practical implementation:
1. Retrieve top-N with standard relevance ranking
2. Greedily reorder: at each position, pick the next item that maximizes relevance + novelty (MMR-style)
3. Optionally cap items per subtopic (categorical diversity)

### Subtopic Coverage Metrics
- **α-nDCG** — penalizes redundant relevant documents at lower ranks
- **ERR-IA** — intent-aware Expected Reciprocal Rank
- **D-measure** — explicit intent coverage

### Hard vs. Soft Diversity
- **Hard**: limit N results per category (e.g., max 2 results per domain)
- **Soft**: score-based MMR with tunable λ

### Relationship to Facets
Diversity and faceted search are complementary: facets let users explicitly constrain intent; diversity hedges when they don't.

## Key Concepts
- **Ambiguity hedging** — covering multiple interpretations
- **Redundancy reduction** — avoiding near-duplicate results
- **KL-divergence** — measuring topic distribution mismatch
- **Greedy reranking** — practical MMR implementation
- **α-nDCG** — diversity-aware evaluation metric

## Related Concepts
- [[Diversity Metrics]]
- [[Search Evaluation]]
- [[Search Intent]]
- [[Learning to Rank]]
- [[NDCG]]
- [[Faceted Search]]

## Related Articles
- [[Searching for Goldilocks]]
- [[Facets - Constraints or Preferences]]
- [[Evaluating Good Search - Measure It]]

## People
- [[Daniel Tunkelang]]
