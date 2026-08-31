---
type: article
title: "How to Tune Hybrid Search in Qdrant"
tags:
  - hybrid-search
  - ranking
  - retrieval
  - qdrant
source: "https://qdrant.tech/articles/how-to-tune-hybrid-search/"
author: "Dylan Couzon"
published: 2026-08-22
created: 2026-08-31
concepts:
  - Reciprocal Rank Fusion
  - Distribution-Based Score Fusion
  - Hybrid Search
  - NDCG
tools:
  - Qdrant Vector DB
---

# How to Tune Hybrid Search in Qdrant

**Source:** https://qdrant.tech/articles/how-to-tune-hybrid-search/
**Author:** [[Dylan Couzon]]

## Summary

A tuning workflow for [[Hybrid Search]] fusion in [[Qdrant Vector DB|Qdrant]]: confirm fusion beats
either prefetch alone, choose between [[Reciprocal Rank Fusion|RRF]] and
[[Distribution-Based Score Fusion|DBSF]] on labeled data, set RRF's `k` from how many relevant
documents each query tends to have, sweep per-prefetch weights last, then validate the winner on
held-out queries.

## Setup

Measurements use five public datasets (5,183–100,000 documents) — SciFact, ArguAna, WANDS,
CodeSearchNet, DBPedia-entity — with all-MiniLM-L6-v2 for dense retrieval, Qdrant's core [[BM25]]
for sparse retrieval, and 200 candidates from each prefetch, scored with [[NDCG|nDCG@10]].

## Confirm Fusion Beats Either Prefetch

Default RRF (`k=2`, equal weights — Qdrant's default) against dense-only and sparse-only retrieval:

| Dataset | Dense | Sparse | RRF (k=2) | Over the better one |
|---|---|---|---|---|
| SciFact | 0.6239 | 0.6886 | 0.7175 | +0.0289 |
| ArguAna | 0.4905 | 0.4224 | 0.5216 | +0.0311 |
| WANDS | 0.6921 | 0.7098 | 0.7254 | +0.0156 |
| CodeSearchNet | 0.6299 | 0.5126 | 0.6555 | +0.0256 |
| DBPedia-entity | 0.4677 | 0.3857 | 0.4638 | −0.0039 |

Fusion beat both prefetches on four of five datasets, with 95% intervals excluding zero; on
DBPedia-entity fusion trailed dense retrieval alone and the interval crossed zero.

## RRF vs. DBSF

RRF uses only a candidate's rank position — a document at rank 1 scores the same whether it led rank
2 by a wide or narrow margin. DBSF puts both retrievers' scores on one scale per query, using each
list's mean and spread, so a wide score lead survives into the fused ranking. Which one wins depends
on the data; the article's recommendation is to run both against a labeled query set. See
[[Distribution-Based Score Fusion]] for the formula and the article's five-dataset DBSF-vs-RRF
comparison table.

## Choosing RRF's k

Qdrant scores a document at position `pos` as `1/((pos+1)/weight + k − 1)`, which reduces to
`1/(pos+k)` at equal weights. At Qdrant's default `k=2`, rank 1 carries 5.50× the weight of rank 10;
at `k=61` (the convention from the original RRF paper, one-based `k=60`, mapped to Qdrant's
zero-based positions), rank 1 carries only 1.15× the weight.

Sweeping `k` over 1, 2, 5, 20, and 61 across the five datasets: datasets with about one relevant
document per query (ArguAna, CodeSearchNet, SciFact) did best at `k=2` or `k=5`; datasets with tens
or hundreds of relevant documents per query (DBPedia-entity, WANDS) did best at `k=20` or `k=61`. On
WANDS, `k=2` and `k=61` picked a different top result for 42% of queries while nDCG@10 rose 0.0360.

Tied scores are more common at low `k` — SciFact's default-RRF top 10 shared a score with an adjacent
result in 12.5% of queries on average, versus 2.8% at `k=61` and none under DBSF. The fix: request
more than 10 results, sort client-side by descending score then ascending ID, keep the first 10.

## Tuning Weights

A weight pair multiplies each prefetch's contribution; the pair is absolute, so (1, 2) and (2, 4) are
different settings because the formula divides position by weight. Weights are only valid for the
`k` they were tested at — on WANDS at `k=5`, (1, 2) scores 0.7390 and (2, 4) scores 0.7508, but at
`k=61` (WANDS's best `k`) equal weights win, 0.7614 vs. 0.7567. A prefetch's own standalone score
doesn't say which way to lean: on DBPedia-entity, dense scores higher solo (0.4677 vs. 0.3857) yet
the winning pair weights sparse 3× and gains 0.0060; CodeSearchNet leans the other way, weighting
dense 2× for a 0.0096 gain. A weight of 0.0 keeps a prefetch's documents in the result at score 0.0
rather than excluding them.

## Validate on Held-Out Queries

A configuration can win on the queries used to select it and still fail on held-out queries. On
SciFact's 300 queries, no tested configuration — including DBSF's +0.0148 gain — had a 95% interval
excluding zero; across 200 random splits, a selected configuration retained 67%–95% of its gain on
held-out data. Keeping the default was the correct answer on one of the five datasets.

## Tuning Order

1. Confirm fusion beats either prefetch alone.
2. Pick RRF or DBSF on labeled data.
3. Set `k` from relevant documents per query.
4. Sweep a few weight pairs at that `k`.
5. Validate the winner on held-out queries before shipping.

## Related Concepts

- [[Reciprocal Rank Fusion]]
- [[Distribution-Based Score Fusion]]
- [[Hybrid Search]]
- [[NDCG]]
- [[BM25]]

## Related Articles

- [[Hybrid Queries - Qdrant]] — the DBSF formula and API this article's DBSF results build on
- [[RRF is Not Enough]] — [[Doug Turnbull]]; the case that fusion strategy can't fix upstream
  retrieval quality, complementary to this article's premise that fusion parameters matter
