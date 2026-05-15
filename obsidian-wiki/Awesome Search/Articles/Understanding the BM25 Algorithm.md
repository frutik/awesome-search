---
title: "Understanding the BM25 Full Text Search Algorithm"
tags:
  - clippings
  - search
  - retrieval
  - classic
source: "https://emschwartz.me/understanding-the-bm25-full-text-search-algorithm/"
author: "Evan Schwartz"
created: 2026-05-15
concepts:
  - BM25
---

# Understanding the BM25 Full Text Search Algorithm

**Source:** https://emschwartz.me/understanding-the-bm25-full-text-search-algorithm/
**Author:** Evan Schwartz

## Summary

Clear explanation of [[BM25]]'s formula, parameters, and key design decisions. One of the most accessible introductions to BM25 mechanics.

## Formula Components

```
BM25(q, d) = Σ IDF(qi) × (TF(qi, d) × (k1 + 1)) / (TF(qi, d) + k1 × (1 - b + b × |d|/avgdl))
```

### 1. IDF — Inverse Document Frequency
Rare terms get higher weight than common terms:
```
IDF(qi) = ln((N - n(qi) + 0.5) / (n(qi) + 0.5))
```

### 2. TF — Term Frequency with Saturation
Diminishing returns on repeated terms, controlled by k1.

### 3. Length Normalization
Prevents longer documents from dominating, controlled by b.

## Key Parameters

| Parameter | Typical Value | Effect |
|---|---|---|
| **k1** | 1.2–2.0 | Controls TF saturation — how quickly repeated terms lose incremental value |
| **b** | 0.75 | Controls length normalization strength (0 = disabled) |

## Key Design Insight

BM25 drops probability-calculation terms that don't affect document ordering, and crucially **assumes most documents are not relevant** (R=r=0). This makes it practical without pre-existing relevance data.

## Important Limitation

BM25 scores cannot be compared **across** different collections or time periods — only within the same collection for the same query.

## Related Concepts

- [[BM25]]
- [[Hybrid Search]]
- [[Reciprocal Rank Fusion]]
- [[Sparse Vector Retrieval]]

## Related Articles

- [[SPLADE for Sparse Vector Search Explained]]
- [[RRF is Not Enough]]
