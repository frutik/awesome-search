---
title: "Reciprocal Rank Fusion"
aliases: ["RRF", "rank fusion", "result merging"]
tags:
  - concept
  - search
  - ranking
created: 2026-05-15
---

# Reciprocal Rank Fusion

A score-based result merging algorithm that combines ranked lists from multiple retrieval systems without requiring calibrated scores.

## Formula

For each document d across k ranked lists:

```
RRF(d) = Σ 1 / (rank(d, list_i) + c)
```

Where `c` is a constant (typically 60) that dampens the impact of high-ranked documents.

## Why RRF

- **Score-agnostic**: BM25 and dense vectors use incomparable scales; RRF only uses rank positions
- **Simple**: No learned weights, no calibration
- **Robust**: Consistently beats more complex fusion approaches in practice

## Limitations

- Treats all systems equally — no way to weight one retrieval path more than another
- Loses fine-grained score signal; two items at rank 1 contribute identically even if scores differ greatly
- Does not account for query-type variance (some queries may benefit more from lexical vs. semantic)
- Criticized in *RRF is Not Enough* for losing signal in hybrid search contexts

## In Hybrid Search

RRF is also implementable directly in SQL — see [[Search using PostgreSQL]] for a [[PostgreSQL]] hybrid query fusing [[Full-Text Search|FTS]] and [[pgvector]] results.

RRF is the default fusion method in [[Hybrid Search]] pipelines combining:
- [[BM25]] (lexical) scores
- [[Dense Vector Retrieval]] (semantic) scores
- [[Sparse Vector Retrieval]] scores (e.g., [[SPLADE]])

## Alternatives

- **Linear combination**: `α * dense_score + (1-α) * sparse_score` — requires score normalization
- **Learned fusion**: train a model to optimally weight retrieval paths per query type (e.g. [[LambdaMART]] via [[Metarank]])
- **[[Interleaving]]**: zip-merge ranked lists; a simple cold-start baseline and online-eval method
- **[[Wormhole Vectors]]**: bridge across representation spaces at embedding level

## Related Concepts

- [[Hybrid Search]]
- [[BM25]]
- [[Dense Vector Retrieval]]
- [[Sparse Vector Retrieval]]
- [[Learning to Rank]]
- [[Retrieval Pipeline]]

- **[[Relative Score Fusion]] (RSF)**: normalize scores to [0,1] and combine linearly; preserves score magnitude but requires calibration
- **[[Semantic Boosting]]**: inject vector results as boost clauses into a lexical query; lexical engine produces the final output, enabling native facets/highlights/pagination
