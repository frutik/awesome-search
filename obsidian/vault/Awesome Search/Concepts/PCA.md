---
title: "PCA"
aliases: ["Principal Component Analysis", "principal component analysis", "PCA", "eigenvector projection"]
tags:
  - concept
  - dimensionality-reduction
  - linear-algebra
  - embeddings
  - ml
created: 2026-06-01
---

# PCA (Principal Component Analysis)

## Definition

PCA is a linear dimensionality reduction technique that projects data onto a new coordinate system whose axes (principal components) are ordered by the amount of variance they explain. The first principal component captures the most variance; each subsequent one captures the next most, orthogonal to all previous.

## How It Works

1. **Standardize** — subtract mean, divide by std per feature
2. **Covariance matrix** — n×n matrix summarizing pairwise feature correlations
3. **Eigendecomposition** — eigenvectors = principal component directions; eigenvalues = variance explained
4. **Sort eigenvectors** by eigenvalue descending
5. **Project** — multiply original data by the top-k eigenvectors matrix → reduced representation

## Properties

| Property | Value |
|---|---|
| Type | Linear |
| Preserves | Global variance structure |
| Speed | Fast (one-pass, deterministic) |
| Parametric | Yes — reusable on new data |
| Inverse transform | Yes (lossy) |
| Suitable for ML | Yes |

## Relevance to Search

- Can reduce embedding dimensions (e.g., 768→256) before ANN indexing, cutting memory and speeding up search with modest quality loss
- Useful when embedding dimensions have near-zero variance (exploited in [[HNSW]] with PCA preprocessing)
- Alternative to [[Vector Quantization]]: DR reduces the *number* of dimensions; quantization reduces *bits per* dimension — both are often combined

## Limitations

- **Linear only** — cannot capture non-linear manifolds in the data
- Information loss is unavoidable (unless eigenvalues are zero)
- Principal components are hard to interpret in original feature terms

## Related Concepts

- [[Dimensionality Reduction]] — parent concept; also covers t-SNE, UMAP, Matryoshka
- [[t-SNE]] — non-linear alternative for visualization
- [[UMAP]] — non-linear alternative with parametric option
- [[Matryoshka Embeddings]] — training-time alternative; dimension-flexible without projection
- [[Vector Quantization]] — complementary compression approach
- [[HNSW]] — ANN index that benefits from reduced dimensionality

## Articles

- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — comparison with all three
- [[Principal Component Analysis (PCA) In Depth]] — step-by-step with worked example
- [[Understanding Principal Component Analysis (PCA)]] — applications focus
- [[PCA vs t-SNE - Which One Should You Use for Visualization]] — MNIST comparison
- [[Exploring Hierarchical Navigable Small World]] — PCA as ANN preprocessing option
