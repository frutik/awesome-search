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

## Related Concepts
- [[Reciprocal Rank Fusion]] — rank-based alternative; simpler, more robust
- [[Hybrid Search]] — the context where RSF is applied
- [[Linear Score Combination]] — closely related approach
- [[Semantic Boosting]] — alternative two-phase approach; avoids list merging entirely

## Articles
- [[Hybrid Search Blueprint Series Semantic Boosting]] — series that covers RSF alongside RRF and Semantic Boosting
