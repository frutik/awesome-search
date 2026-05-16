---
title: "Multi-Stage Ranking"
tags:
  - clippings
  - search
  - ranking
source: "https://medium.com/better-ml/multi-stage-ranking-e0dacd81ac4"
author: "Jaideep Ray"
created: 2026-05-15
concepts:
  - Retrieval Pipeline
  - Learning to Rank
---

# Multi-Stage Ranking

**Source:** https://medium.com/better-ml/multi-stage-ranking-e0dacd81ac4
**Author:** [[Jaideep Ray]] (Sr. Staff ML Engineer)

## Summary

Practical explanation of how production search and recommendation systems break ranking into sequential ML stages, each optimizing different objectives with different speed/quality trade-offs.

## The Three Stages

### Stage 1 — Retrieval
**Goal**: Maximize recall, minimize latency.
**Method**: Gradient boosted decision trees with few high-quality features.
**Scale**: Thousands of candidates → hundreds.

### Stage 2 — Relevance Ranking
**Goal**: Optimize document/author quality and relevance.
**Method**: Stacked ensembles using human-judged training data.
**Scale**: Hundreds → tens of candidates.

### Stage 3 — Click Ranking
**Goal**: Maximize engagement via learned user behavior.
**Method**: Deep neural networks (Wide & Deep), abundant click data.
**Scale**: 10-100 candidates → final ranked list.

## Key Trade-offs

**Benefits:**
- Performance optimization at each scale
- Latency management per stage
- Decoupled development — teams iterate independently

**Drawbacks:**
- "Makes overall system hard to debug"
- Cascading failures — errors in Stage 1 propagate
- "Hard to maintain and iterate on" across stages

## Engineering Considerations

- Feature versioning prevents cascade failures
- Data linting at each stage catches feature distribution drift
- Fast offline testing enables rapid model iteration
- A/B testing validates major architecture changes

## Related Concepts

- [[Retrieval Pipeline]]
- [[Learning to Rank]]
- [[Cross-Encoder]]
- [[ColBERT]]
- [[Position Bias]]
- [[NDCG]]

## Related Articles

- [[Cross-Encoders ColBERT and LLM-Based Re-Rankers]]
- [[How LambdaMART Works]]
- [[Canva Search Pipeline Part II]]
