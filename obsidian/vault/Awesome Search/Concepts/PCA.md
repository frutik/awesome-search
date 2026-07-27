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

## Measured Cost on Real Embeddings

[[Doug Turnbull]] measured recall against brute-force ground truth after PCA-compressing
MiniLM (384-dim) embeddings of the [[MS MARCO]] passage corpus, fitting PCA on 100K vectors
([[Principal Component Analysis - an embedding shrink-ray]]):

| Dims | Compression | Eigenvalue % | Recall |
|---|---|---|---|
| 200 | 1.9× | 88.5 | 0.879 |
| 100 | 3.8× | 64.05 | 0.5714 |
| 50 | 7.7× | 42.04 | 0.2029 |

The degradation is steeply non-linear — roughly halving dimensions is survivable, but pushing
to 7.7× collapses recall. Eigenvalue % (`np.sum(eigenvalues[:k]) / np.sum(eigenvalues)`) is the
share of variance retained, and it tracks recall loosely rather than predicting it exactly.

### The Flat-Spectrum Diagnostic

PCA only pays off where there is redundancy to harvest. If an embedding model already spreads
information evenly across dimensions, the eigenvalue spectrum is flat and nothing compresses:

> "Imagine the 1st eigenvalue is 15 and the 384th is 13 you're not going to get much effective
> shrinkage with PCA."

Inspect the explained-variance curve **before** committing to PCA — a steep drop after k
components means good compressibility; a flat curve means pick a different technique.
Compressibility also depends on the corpus, not just the model.

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
- [[MS MARCO]] — the corpus the compression numbers above were measured on

## Related Topics

- [[Dimensionality Reduction vs Quantization]] — how PCA compares to bit-level compression
- [[PCA vs t-SNE for Retrieval]] — why PCA's orthogonality makes it retrieval-safe where t-SNE is disqualified

## Articles

- [[Principal Component Analysis - an embedding shrink-ray]] — practical walkthrough with measured recall on [[MS MARCO]]
- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — comparison with all three
- [[Principal Component Analysis (PCA) In Depth]] — step-by-step with worked example
- [[Understanding Principal Component Analysis (PCA)]] — applications focus
- [[PCA vs t-SNE - Which One Should You Use for Visualization]] — MNIST comparison
- [[Exploring Hierarchical Navigable Small World]] — PCA as ANN preprocessing option
