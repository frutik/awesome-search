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

## Weighted RRF and Choosing k (Qdrant)

[[Qdrant Vector DB|Qdrant]] parameterizes both knobs directly on the query: `k` since v1.16.0, and
per-prefetch weights (Weighted RRF) since v1.17.0. Qdrant's formula for a document at position `pos`
in one prefetch is `1/((pos+1)/weight + k − 1)`, reducing to `1/(pos+k)` at equal weights — the same
shape as above, but zero-based, so Qdrant's default `k=2` is not directly comparable to the original
RRF paper's `k=60` (one-based); porting that paper's convention requires `k=61`.

[[How to Tune Hybrid Search in Qdrant]] measured how much `k` matters across five datasets: at
`k=2`, rank 1 carries 5.50× the weight of rank 10; at `k=61`, only 1.15×. Datasets with about one
relevant document per query did best at low `k` (2 or 5); datasets with tens or hundreds of relevant
documents per query did best at high `k` (20 or 61) — on WANDS, `k=2` vs. `k=61` picked a different
top result for 42% of queries. Weight pairs are only valid for the `k` they were tuned at, and a
prefetch's own standalone score doesn't say which way to weight it — e.g. weighting the *weaker*
solo retriever higher can still win, because weights act on positions within each list, not on
absolute score quality. A weight of 0.0 keeps a prefetch's documents in the result, scored at 0.0,
rather than excluding them. Tied scores are more common at low `k`; the fix is to request more
results, sort client-side by descending score then ascending ID, and keep the first N.

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
- **[[Distribution-Based Score Fusion]] (DBSF)**: normalizes each retriever's scores by its own mean/spread rather than discarding them; Qdrant's alternative to RRF when retrievers' score magnitudes are trustworthy
- **[[Semantic Boosting]]**: inject vector results as boost clauses into a lexical query; lexical engine produces the final output, enabling native facets/highlights/pagination

## Articles

- [[Reciprocal Rank Fusion and Relative Score Fusion]] — [[Erik Hatcher]] ([[MongoDB]]) works the formula, weighting and score details through in full
- [[Survey of the Hybrid Search Landscape]] — situates RRF as fusion by relevancy *order*, ignoring computed scores
- [[RRF is Not Enough]] — [[Doug Turnbull]] on what rank-only fusion discards
- [[How to Tune Hybrid Search in Qdrant]] — [[Dylan Couzon]]; measures RRF's `k` and weight parameters against labeled data, and compares RRF to [[Distribution-Based Score Fusion|DBSF]]
- [[Hybrid Queries - Qdrant]] — Qdrant's RRF `k`/weight parameterization and DBSF documented together
