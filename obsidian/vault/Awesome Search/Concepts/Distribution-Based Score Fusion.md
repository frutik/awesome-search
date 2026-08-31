---
title: "Distribution-Based Score Fusion"
aliases: ["DBSF"]
type: concept
tags:
  - concept
  - hybrid-search
  - ranking
  - retrieval
created: 2026-08-31
---

# Distribution-Based Score Fusion

A [[Hybrid Search]] fusion method, available in [[Qdrant Vector DB|Qdrant]] since v1.11.0, that keeps
each retriever's raw scores but normalizes their distributions before combining them — a middle
ground between [[Reciprocal Rank Fusion|RRF]] (which discards scores entirely) and plain
[[Score Normalization|min-max]] fusion (which normalizes against the observed extremes).

---

## Formula

For each retriever's returned set, DBSF computes the mean μ and sample standard deviation σ, then
rescales every score using the 3-sigma range as endpoints:

```
ŝ = (s − (μ − 3σ)) / 6σ
```

The normalized scores are then summed across retrievers. Because each retriever now contributes on
the same comparable range, differing raw score magnitudes no longer decide the outcome by
themselves.

## Behavior

- **Stateless / per-query** — the mean and standard deviation are computed from each query's own
  returned points, not from a running distribution seen across queries.
- **Not clipped to [0, 1]** — scores outside the 3-sigma range remain outside that range after the
  remap; DBSF widens the scale, it doesn't hard-bound it.
- **Degenerate case** — if every returned score is identical (or only one point is returned), DBSF
  emits 0.5 rather than dividing by zero.
- **Small-sample sensitivity** — the μ/σ statistics come from the prefetch's top-k, a small sample,
  so a single dominant outlier in that top-k can skew normalization for the query. Increasing the
  prefetch limit is the mitigation.
- **Nested vs. root-level** — in a multi-shard collection, DBSF nested inside a prefetch runs per
  shard and rescales against that shard's own candidate distribution; root-level fusion instead
  combines candidates already gathered across shards.

## DBSF vs. RRF

| Property | [[Reciprocal Rank Fusion\|RRF]] | DBSF |
|---|---|---|
| Signal used | Rank position only | Raw score, rescaled by distribution |
| Preserves score magnitude/leads | No — a rank-1 document scores the same whether it led rank-2 narrowly or widely | Yes — a wide lead in one retriever's scores survives the sum |
| Parameters | `k`, per-prefetch weights | None — takes no parameters |
| Assumption | Score scale is not trustworthy, only order is | Score magnitude carries real information |
| Qdrant default/recommended when unsure | Yes — the "safe default" without an eval set | No |

RRF reads only a document's slot in each list, so a lead in one prefetch flattens to a single rank
step; DBSF keeps the scores on a shared axis, so that lead survives the sum. Qdrant's own guidance:
"DBSF is a reasonable choice when you trust your retrievers' raw scores to carry magnitude
information. On well-calibrated retrievers DBSF can outperform tuned weighted RRF; on others
weighted RRF wins." Neither dominates the other in general — the recommendation is to compare both
against a labeled eval set.

## Measured Results (Qdrant, five BEIR/e-commerce datasets)

[[How to Tune Hybrid Search in Qdrant]] compares DBSF against default RRF (`k=2`, equal weights) on
five public datasets (5,183–100,000 documents), using all-MiniLM-L6-v2 for dense retrieval and
Qdrant's core [[BM25]] for sparse, 200 candidates from each prefetch:

| Dataset | DBSF nDCG@10 | Gain over default RRF |
|---|---|---|
| WANDS | 0.7637 | +0.0383 |
| DBPedia-entity | 0.4822 | +0.0184 |
| CodeSearchNet | 0.6716 | +0.0161 |
| SciFact | 0.7323 | +0.0148 (interval crosses zero) |
| ArguAna | 0.5171 | −0.0045 (interval crosses zero) |

DBSF beat default RRF with a 95%-interval gain excluding zero on three of the five datasets; the
SciFact and ArguAna deltas were inconclusive. DBSF also produced no tied scores at rank 10 on
SciFact, versus 12.5% of default RRF's top 10 sharing a score with an adjacent result — a side effect
of using continuous rescaled scores instead of the coarse `1/(pos+k)` values RRF produces at low `k`.

## Usage (Qdrant)

```python
from qdrant_client import QdrantClient, models

client.query_points(
    collection_name="products",
    prefetch=[dense_prefetch, sparse_prefetch],
    query=models.FusionQuery(fusion=models.Fusion.DBSF),
    limit=10,
)
```

The public API takes no `k` or `weights` for DBSF — those fields belong to `RrfQuery` only.

## Related Concepts

- [[Reciprocal Rank Fusion]] — the rank-only alternative DBSF is compared against
- [[Score Normalization]] — DBSF's μ/σ rescaling is a distribution-based normalization, in the same
  family as z-score/L2 normalization
- [[Relative Score Fusion]] — min-max/sigmoid-normalized linear fusion; a related but distinct
  score-preserving strategy
- [[Hybrid Search]] — the setting DBSF fuses within
- [[Qdrant Vector DB]] — the engine that implements DBSF

## Articles

- [[How to Tune Hybrid Search in Qdrant]] — [[Dylan Couzon]]; DBSF vs. RRF measured across five
  datasets, and the tuning workflow for choosing between them
- [[Hybrid Queries - Qdrant]] — the formula, degenerate-case handling, and per-shard behavior
