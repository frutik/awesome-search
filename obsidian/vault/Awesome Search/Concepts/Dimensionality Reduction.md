---
title: "Dimensionality Reduction"
aliases: ["dimensionality reduction", "PCA", "principal component analysis", "t-SNE", "UMAP", "dimension reduction", "embedding compression", "vector compression"]
tags:
  - concept
  - search
  - embeddings
  - ml
created: 2026-05-16
---

# Dimensionality Reduction

## Definition

Dimensionality reduction transforms high-dimensional vectors (e.g., 768-dim BERT embeddings) into lower-dimensional representations while preserving as much structure as possible. In search, this reduces storage, speeds up ANN search, and enables visualization.

## Why It Matters for Search

Dense embedding models produce vectors of 768–4096 dimensions. At scale:
- 1B documents × 768 dims × 4 bytes = **3TB** of vectors
- ANN index build time and memory scale with dimensionality
- Reducing to 256 dims can cut storage 3× with modest quality loss

Alternative: [[Vector Quantization]] reduces *precision* per dimension; dimensionality reduction reduces the *number* of dimensions.

## Main Techniques

### PCA (Principal Component Analysis)
Linear projection onto the axes of maximum variance. Fast, deterministic, reversible.
- Good for: moderate compression, preserving global structure
- Limitation: linear only — can't capture non-linear manifolds

### t-SNE (t-distributed Stochastic Neighbor Embedding)
Non-linear projection optimized for preserving *local* neighborhoods. Produces beautiful 2D/3D visualizations.
- Good for: **visualization only** — not suitable for retrieval (non-parametric, can't project new points)
- Limitation: slow on large datasets, non-deterministic

### UMAP (Uniform Manifold Approximation and Projection)
Non-linear projection that preserves both local and global structure better than t-SNE. Faster and parametric (can project new points).
- Good for: visualization + moderate retrieval use
- Increasingly used to compress embeddings for search

### Matryoshka / Truncation
[[Matryoshka Embeddings]] are trained so that the first N dimensions already form a good representation — just truncate to reduce dimensionality without any projection. The cleanest approach for models that support it.

## Dimensionality Reduction vs. Quantization

| | Dimensionality Reduction | [[Vector Quantization]] |
|---|---|---|
| What changes | Number of dimensions | Bits per dimension |
| Storage savings | Proportional to compression ratio | 4–32× (float32 → int8/binary) |
| Quality loss | Moderate | Low to moderate |
| ANN speed gain | High | High |
| Requires retraining | No (PCA/UMAP) / Yes (Matryoshka) | No |

## Related Concepts

- [[Embeddings]] — what gets compressed
- [[Dense Vector Retrieval]] — benefits from smaller vectors
- [[Vector Quantization]] — complementary compression approach
- [[Matryoshka Embeddings]] — built-in dimensionality flexibility
- [[Dense Embeddings]] — primary target of dimensionality reduction
