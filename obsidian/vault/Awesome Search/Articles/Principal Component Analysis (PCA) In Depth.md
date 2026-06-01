---
type: article
title: "Principal Component Analysis (PCA) In Depth"
source: "https://medium.com/@fraidoonomarzai99/principal-component-analysis-pca-in-depth-93c871f25dfa"
author:
  - "[[Fraidoon Omarzai]]"
published: 2024-07-20
tags: [article, dimensionality-reduction, PCA, linear-algebra, covariance-matrix, eigenvectors, medium]
concepts:
  - PCA
  - Dimensionality Reduction
created: 2026-06-01
---

# Principal Component Analysis (PCA) In Depth

**Author:** [[Fraidoon Omarzai]]  
**Source:** https://medium.com/@fraidoonomarzai99/principal-component-analysis-pca-in-depth-93c871f25dfa

## Summary

Step-by-step walkthrough of the PCA algorithm from linear algebra foundations through Python implementation. Uses a worked example (student test scores: math, English, art) to make covariance and eigendecomposition concrete.

## Algorithm Steps

1. **Standardization** — scale to mean=0, std=1 (optional but recommended)
2. **Covariance matrix** — captures how features vary together; diagonal = per-feature variance, off-diagonal = pairwise covariance
3. **Eigenvectors + eigenvalues** — eigenvectors define principal component directions; eigenvalues measure variance captured per component; sort descending
4. **Select top-k** — discard eigenvectors with lowest eigenvalues (least information)
5. **Projection** — transform data via `y = W' × x` where W is the k×n matrix of selected eigenvectors

## Key Intuitions

- **Eigenvalue = variance explained** along that component. Low eigenvalue → that dimension carries little information → safe to drop.
- **Covariance diagonal** = variance per feature; **off-diagonal** = correlation between feature pairs
- If all eigenvalues are similar, the data is already hard to compress losslessly

## Pros / Cons

**Pros**: reduces computational complexity, improves some ML model accuracy, eliminates correlated redundancy  
**Cons**: information loss is unavoidable, assumes linearity, principal components are hard to interpret in original feature terms

## Related Concepts

- [[PCA]] — concept note
- [[Dimensionality Reduction]] — parent concept
- [[Vector Quantization]] — complementary compression (reduces precision, not count)

## Related Articles

- [[Understanding Principal Component Analysis (PCA)]] — same topic, more on applications
- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — practical comparison including t-SNE and UMAP
- [[Exploring Hierarchical Navigable Small World]] — PCA as ANN speedup technique

## People

- [[Fraidoon Omarzai]]
