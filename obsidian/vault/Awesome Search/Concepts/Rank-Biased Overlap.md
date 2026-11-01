---
type: concept
title: "Rank-Biased Overlap"
aliases: ["RBO", "Ranked-Biased Overlap"]
tags:
  - concept
  - search-evaluation
  - metrics
created: 2026-10-30
---

# Rank-Biased Overlap

**Rank-Biased Overlap (RBO)** measures how much two ranked result lists differ, without needing any relevance labels. [[Search golden sets are anything but]] lists it among approaches for measuring how thoroughly a new algorithm shuffles results — not good or bad, just quantity of change — and links the RBO paper at https://dl.acm.org/doi/10.1007/978-3-031-15037-1_11.

---

## Role in Evaluation

It compares two orderings directly, so it works where [[Judgment Lists]] are sparse or biased. It tells you that results changed and by how much, not whether they got better; pair it with a quality signal such as side-by-side review, unit-test-style checks or [[Session-Based Evaluation]]. For another label-free ordering comparison see [[Kendall Rank Correlation]].

## Related Concepts
- [[Kendall Rank Correlation]] · [[NDCG]] · [[NDCG-f]] · [[Search Evaluation]]

## Related Articles
- [[Search golden sets are anything but]]
