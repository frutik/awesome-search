---
type: article
title: "Hybrid Queries - Qdrant"
tags:
  - hybrid-search
  - ranking
  - retrieval
  - qdrant
  - documentation
source: "https://qdrant.tech/documentation/search/hybrid-queries/#distribution-based-score-fusion-dbsf"
created: 2026-08-31
concepts:
  - Distribution-Based Score Fusion
  - Reciprocal Rank Fusion
tools:
  - Qdrant Vector DB
---

# Hybrid Queries - Qdrant

**Source:** https://qdrant.tech/documentation/search/hybrid-queries/#distribution-based-score-fusion-dbsf

Reference documentation for [[Qdrant Vector DB|Qdrant]]'s query-level fusion methods for combining
prefetch results ([[Hybrid Search]]).

## Reciprocal Rank Fusion (RRF)

Scores a document by position rather than raw score: `score(d) = Σ 1/(k + r_d)`. Recommended as the
safe default when there is no evaluation set to compare against.

- **Setting the constant `k`** (available as of v1.16.0) — configurable via `query.rrf.k`; the
  documentation's own example sets `k=60`.
- **Weighted RRF** (available as of v1.17.0) — `query.rrf.weights` assigns a relative weight per
  prefetch, since one retriever is often stronger than the other for a given workload (e.g. dense
  favoring natural-language queries, BM25 favoring identifier-heavy ones). A weight of 3.0 on the
  first prefetch and 1.0 on the second means a document ranked third in the first prefetch scores
  the same as a document ranked first in the second; on non-overlapping result sets this returns
  three results from the first prefetch for every one from the second. The number of weights must
  match the number of prefetches. Guidance for setting them: with an eval set, split queries in two,
  tune weights on the first half, measure on the second (a `tune_rrf_weights` grid-search helper is
  provided in Qdrant's "Choosing a Fusion Method" notebook); without an eval set, leave weights at
  the default (1.0, 1.0) — hand-tuned weights without measurement are unlikely to beat the default
  reliably. Retune when retrievers change (new embedding model, new chunking), when the corpus drifts
  substantially, or on a fixed cadence with a fresh eval sample.

## Distribution-Based Score Fusion (DBSF)

Available as of v1.11.0. Full treatment in [[Distribution-Based Score Fusion]]; summary here for
context alongside RRF.

DBSF keeps each retriever's raw scores but normalizes their distributions before combining them. For
each retriever's returned set it computes the mean μ and sample standard deviation σ, then rescales
every score using the 3-sigma extremes as endpoints:

```
ŝ = (s − (μ − 3σ)) / 6σ
```

Normalized scores are summed across retrievers, so differing score magnitudes no longer dominate.
DBSF is stateless — normalization limits come from each query's own returned points, not from scores
seen across queries. Scores are not clipped to [0, 1]; values outside the 3-sigma range stay outside
after the remap. If all returned scores are identical (or only one point is returned), DBSF emits 0.5
instead of dividing by zero.

DBSF takes no parameters — `k` and weights belong to `RrfQuery` only. It is "a reasonable choice when
you trust your retrievers' raw scores to carry magnitude information. On well-calibrated retrievers
DBSF can outperform tuned weighted RRF; on others weighted RRF wins" — neither dominates in general,
so the recommendation is to choose using an eval set. Two caveats: the μ/σ statistics come from the
prefetch top-k, a small sample, and a single dominant outlier in that top-k can skew normalization
for that query — increasing the prefetch limit is the mitigation for unstable rankings.

### Example

```python
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")
client.query_points(
    collection_name="{collection_name}",
    prefetch=[
        models.Prefetch(
            query=models.SparseVector(indices=[1, 42], values=[0.22, 0.8]),
            using="sparse",
            limit=20,
        ),
        models.Prefetch(
            query=[0.01, 0.45, 0.67],
            using="dense",
            limit=20,
        ),
    ],
    query=models.FusionQuery(fusion=models.Fusion.DBSF),
)
```

## Selection Guidance

- Use weighted RRF with tuning if an evaluation dataset is available.
- Use DBSF if the retrievers' scores are well-calibrated.
- Use RRF as the default otherwise.

## Related Concepts

- [[Distribution-Based Score Fusion]]
- [[Reciprocal Rank Fusion]]
- [[Hybrid Search]]

## Related Articles

- [[How to Tune Hybrid Search in Qdrant]] — [[Dylan Couzon]]; measures RRF vs. DBSF and RRF's `k`/weight
  parameters against labeled data using the fusion methods documented here
