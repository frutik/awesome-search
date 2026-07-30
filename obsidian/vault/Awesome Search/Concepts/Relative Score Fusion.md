---
title: "Relative Score Fusion"
aliases: ["RSF", "score fusion", "relative score combination"]
type: concept
tags:
  - concept
  - hybrid-search
  - retrieval
  - ranking
created: 2026-05-19
---

# Relative Score Fusion

A hybrid search fusion strategy that normalizes scores from multiple retrieval systems to a common scale and combines them linearly, preserving score magnitude information that [[Reciprocal Rank Fusion]] (RRF) discards.

Part of the "classic hybrid search techniques" alongside RRF, as described in [[Erik Hatcher]]'s MongoDB hybrid search series.

---

## How It Works

1. Retrieve results from each retrieval system (e.g., BM25, dense vector)
2. Normalize each system's scores to [0, 1] using min-max or other normalization
3. Combine normalized scores: `final = α × score_lexical + (1 − α) × score_dense`

## Normalization is the whole game

The combination step is trivial; the [[Score Normalization]] step decides the outcome. Engines typically
offer three modes:

| Mode | Behavior | Risk |
|---|---|---|
| `none` | Raw scores combined as-is | Only safe when pipelines already share a scale |
| `minMaxScaler` | Linear map of observed `[min, max]` to `[0, 1]` | One outlier stretches the range and flattens the rest |
| `sigmoid` | Logistic squash into `(0, 1)` | Bounded for any input, but **saturates** — values far from the curve's center collapse to 0 or 1 |

Saturation is the non-obvious failure. In [[Erik Hatcher]]'s worked example, one pipeline's scores
span 0–100 and the other's span 0–5; sigmoid maps a raw 85.0 to exactly **1.0**, erasing every
gradation within that pipeline, while the 0–5 pipeline retains its resolution. The fusion then
averages a flattened signal against a live one. Knowing each pipeline's actual range is a
prerequisite, not a refinement.

## Combination

Once normalized and weighted, values are combined either by **averaging** (the usual default) or by
a custom expression. Note the ordering: normalize → weight → combine. Weights applied to
un-normalized scores compound the scale mismatch instead of correcting it.

## RRF vs RSF

| Property | RRF | RSF |
|----------|-----|-----|
| Uses score values | No (rank only) | Yes |
| Score normalization required | No | Yes |
| Sensitive to score outliers | No | Yes |
| Preserves score magnitude | No | Yes |
| Parameter-free | Yes (except k) | No (requires α) |

## Limitations
- Requires score normalization across systems with incompatible scales
- Score distributions can differ per query, making normalization unstable
- Needs α weight tuning, unlike RRF which is robust out of the box
- Min-max normalization is only as stable as the extremes: one outlier lexical score stretches the range and flattens everything else. L2 is steadier on noisy corpora.
- **Omitting the normalization step doesn't degrade gracefully** — it silently hands the ranking to whichever branch has the larger scale. See [[Hybrid Fusion Failure - BM25 Displacing Reference Documents]].

## Related Concepts
- [[Reciprocal Rank Fusion]] — rank-based alternative; simpler, more robust
- [[Hybrid Search]] — the context where RSF is applied
- [[Linear Score Combination]] — closely related approach
- [[Semantic Boosting]] — alternative two-phase approach; avoids list merging entirely

## In MongoDB

`$scoreFusion` takes `input.normalization` (`none` / `sigmoid` / `minMaxScaler`) and
`combination.method` (`avg` by default, or a custom expression). Where a pipeline doesn't naturally
emit a score, the `$score` stage computes one into `$meta.score` — but `$search` and `$vectorSearch`
already provide scores, so `$score` isn't used with them.

The asymmetry that matters: `$vectorSearch` scores already sit in 0.0–1.0, whereas lexical `$search`
[[BM25]] scores have no defined range at all. Normalizing the lexical leg is almost always warranted.

## Articles
- [[Reciprocal Rank Fusion and Relative Score Fusion]] — RSF worked end-to-end with `$score`, `$scoreFusion` and score details
- [[Survey of the Hybrid Search Landscape]] — introduces RSF as fusion by sensible score range normalization
- [[Hybrid Search Blueprint Series Semantic Boosting]] — series that covers RSF alongside RRF and Semantic Boosting
