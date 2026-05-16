---
title: "RRF is Not Enough"
tags:
  - clippings
  - search
  - hybrid-search
  - ranking
source: "https://softwaredoug.com/blog/2024/11/03/rrf-is-not-enough"
author: "Doug Turnbull"
created: 2026-05-15
concepts:
  - Reciprocal Rank Fusion
  - Hybrid Search
  - Query Understanding
---

# RRF is Not Enough

**Source:** https://softwaredoug.com/blog/2024/11/03/rrf-is-not-enough
**Author:** [[Doug Turnbull]]

## Summary

Argues that [[Reciprocal Rank Fusion]] is not a silver bullet for [[Hybrid Search]]. Simply combining lexical and vector results through RRF will underperform when the underlying retrieval systems lack precision. "RRF'ing bad search into good search will just drag down the good search."

## Core Argument

RRF assumes both retrieval sources contribute relevant results. When BM25 returns poor results (e.g., bag-of-words matches unrelated documents), merging degrades the stronger vector results. The problem is upstream quality, not fusion strategy.

## Evidence

Real query examples with ranking tables showing:
- Strong vector search results degraded after naïve RRF with poor BM25
- Improved BM25 (phrase matching instead of bag-of-words) rescues the fusion

## Proposed Alternatives

1. **Enhance each source separately** — improve BM25 precision with phrase search before fusion
2. **Intent-based routing** — probabilistically determine user intent and allocate result budget accordingly (e.g., "80% semantic, 20% phrase")
3. **[[Query Understanding]] framework** — think in terms of solving user problems, not blending technologies

## Key Insight

> "Move beyond thinking in terms of search technologies toward systems solving the user's specific problems."

Fusion is a downstream step; upstream retrieval quality is the real lever.

## Related Concepts

- [[Reciprocal Rank Fusion]]
- [[Hybrid Search]]
- [[BM25]]
- [[Dense Vector Retrieval]]
- [[Query Understanding]]

## Related Articles

- [[Hybrid Search SPLADE Sparse Encoder]]
- [[SPLADE for Sparse Vector Search Explained]]
