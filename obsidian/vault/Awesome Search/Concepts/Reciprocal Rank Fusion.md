---
title: "Reciprocal Rank Fusion"
aliases: ["RRF", "rank fusion", "result merging"]
type: concept
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

## Weighting, and why the constant matters

The constant is not decoration. Because it dominates the denominator at low ranks, it also sets the *scale* of the output, which is why raw RRF scores come
out as small, hard-to-read numbers that barely separate. Weights fix both problems at once.

In [[MongoDB]]'s `$rankFusion`, where `k = 60` is a fixed built-in, a weight of **30 on each of two
pipelines** rescales the summed score into a comfortable ~0.0–1.0 range: each pipeline contributes at
most ~0.5, and a document ranked first in both lists lands at ~1.0.

Equal weights also produce **structural ties**: a document at rank 1 in list A and a document at
rank 1 in list B score identically, since rank is all RRF sees. Assigning *different* weights per
pipeline is the way to break them — and doubles as the knob for expressing that one retrieval path
should count for more than another, which plain unweighted RRF cannot do.

Worked end-to-end with numbers in [[Reciprocal Rank Fusion and Relative Score Fusion]].

## Explainability

Because the contribution of each list is just `w × 1/(k + rank)`, RRF is unusually easy to explain.
Engines can expose the per-pipeline rank, weight, and resulting term — including a marker for lists
the document did *not* appear in — making a fused score fully reconstructible. See
[[Search Results Explainability]].

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
- [[Federated Search]] — RRF is the standard merger when fanning out across multiple collections/engines

- **[[Relative Score Fusion]] (RSF)**: normalize scores to [0,1] and combine linearly; preserves score magnitude but requires calibration
- **[[Semantic Boosting]]**: inject vector results as boost clauses into a lexical query; lexical engine produces the final output, enabling native facets/highlights/pagination

## Articles

- [[Reciprocal Rank Fusion and Relative Score Fusion]] — [[Erik Hatcher]] ([[MongoDB]]) works the formula, weighting and score details through in full
- [[Survey of the Hybrid Search Landscape]] — situates RRF as fusion by relevancy *order*, ignoring computed scores
- [[RRF is Not Enough]] — [[Doug Turnbull]] on what rank-only fusion discards
