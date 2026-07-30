---
title: "Score Normalization"
aliases: ["score scaling", "min-max normalization", "minMaxScaler", "sigmoid normalization", "score calibration"]
type: concept
tags:
  - concept
  - hybrid-search
  - ranking
  - retrieval
created: 2026-07-30
---

# Score Normalization

Mapping the raw scores produced by different retrieval systems onto a common scale so they can be
meaningfully combined. It is the enabling step for every score-based fusion strategy —
[[Relative Score Fusion]], [[Linear Score Combination]], and weighted blends generally — and the step
that [[Reciprocal Rank Fusion]] avoids needing by discarding scores altogether.

---

## Why it's necessary

Scores from different retrieval paths are not on comparable scales, and often not on *bounded*
scales at all:

| Source | Range | Behavior |
|---|---|---|
| [[BM25]] / lexical | **Unbounded** | Grows with term frequency, term rarity, document shortness; no ceiling |
| Cosine / [[Dense Vector Retrieval]] | Typically bounded | MongoDB's `$vectorSearch` emits 0.0–1.0 directly |
| [[ELSER]] / learned sparse | Unbounded | Sums of learned term weights |
| Domain values (price, distance, rating) | Arbitrary | Whatever the field happens to be |

Combining un-normalized scores does not degrade gracefully — it silently hands the ranking to
whichever branch has the larger numeric scale, while still returning a single plausible-looking
`_score`. See [[Hybrid Fusion Failure - BM25 Displacing Reference Documents]] for a worked failure,
and the warning under [[Hybrid Search]] about `bool`/`should` clauses summing raw scores.

## Strategies

**None** — pass raw scores through. Only defensible when the pipelines already share a scale.

**Min-max scaling** (`minMaxScaler`) — linearly map the observed `[min, max]` of a result set to
`[0, 1]`. Intuitive and preserves relative gaps, but only as stable as the extremes: a single
outlier stretches the range and flattens everything else. Because min and max are computed *per
result set*, the same document can normalize differently across queries.

**Sigmoid** — squash any real value into `(0, 1)` with a logistic curve. Bounded regardless of input
range, so it tolerates unbounded lexical scores, but it **saturates**: inputs far from the curve's
center collapse toward 0 or 1 and lose their differences. In [[Reciprocal Rank Fusion and Relative Score Fusion]] a raw distance score of 85.0 normalizes to exactly 1.0 while a rating of 4.2 becomes
~0.985 — the distance pipeline's internal gradations are erased because its scale (0–100) sits far
outside the range where sigmoid discriminates.

**Z-score / L2** — standardize by distribution rather than extremes. Steadier than min-max on noisy
corpora where outliers are common.

## Where it sits in a fusion pipeline

```
pipeline A ──→ raw scores ──→ normalize ──┐
                                          ├──→ weight ──→ combine (sum / avg / custom) ──→ final
pipeline B ──→ raw scores ──→ normalize ──┘
```

Normalization precedes weighting: weights applied to un-normalized scores compound the scale
mismatch rather than correcting it.

## Engine support

- **[[MongoDB]] Atlas** — `$scoreFusion` takes `input.normalization` of `none`, `sigmoid`, or
  `minMaxScaler`, then combines by `avg` (default) or a custom expression. The `$score` stage can
  also normalize at the pipeline level, though deferring to `$scoreFusion` is the simpler default.
- **[[OpenSearch]]** — a dedicated normalization processor in the hybrid search pipeline, ahead of
  combination.
- **[[Elasticsearch]]** — score normalization and fusion for BM25 + kNN combination; note that a
  plain `bool`/`should` query does **not** normalize.

## The RRF alternative

[[Reciprocal Rank Fusion]] sidesteps normalization entirely by using only rank position, which is why
it is robust out of the box and the usual recommendation for getting started. The cost is that it
discards magnitude: two documents at rank 1 contribute identically even when one scored far better,
and consecutively ranked documents are treated as evenly spaced when they may not be. Choosing
between the two is a choice about whether your score gaps carry real information worth normalizing
to preserve.

## Related Concepts

- [[Relative Score Fusion]] — the fusion strategy that depends on this step
- [[Reciprocal Rank Fusion]] — avoids the problem by ignoring scores
- [[Linear Score Combination]] — weighted blending, which assumes normalized inputs
- [[Hybrid Search]] — the setting where incomparable scales arise
- [[BM25]] — the canonical unbounded score
- [[Dense Vector Retrieval]] — the canonical bounded score
- [[Bayesian BM25]] — an alternative to rescaling: convert scores to calibrated probabilities instead

## Articles

- [[Reciprocal Rank Fusion and Relative Score Fusion]] — normalization options worked through with numbers
- [[Hybrid Fusion Failure - BM25 Displacing Reference Documents]] — the failure mode when it's skipped
- [[RRF is Not Enough]] — the case for keeping score magnitude
