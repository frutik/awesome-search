---
type: article
title: "PCA vs t-SNE vs UMAP: Visualizing the Invisible in Your Data"
source: "https://medium.com/@laakhanbukkawar/pca-vs-t-sne-vs-umap-visualizing-the-invisible-in-your-data-92cb2baebdbb"
author:
  - "[[Lakhan Bukkawar]]"
published: 2025-05-05
tags: [article, dimensionality-reduction, PCA, t-SNE, UMAP, visualization, embeddings, medium]
concepts:
  - Dimensionality Reduction
  - PCA
  - t-SNE
  - UMAP
created: 2026-06-01
---

# PCA vs t-SNE vs UMAP: Visualizing the Invisible in Your Data

**Author:** [[Lakhan Bukkawar]]  
**Source:** https://medium.com/@laakhanbukkawar/pca-vs-t-sne-vs-umap-visualizing-the-invisible-in-your-data-92cb2baebdbb

## Summary

Side-by-side comparison of PCA, t-SNE, and UMAP with Python implementations on the Iris dataset. PCA maximizes variance through linear projection; t-SNE preserves local neighborhoods for cluster visualization; UMAP balances local and global structure with better speed and scalability than t-SNE.

## Technique Summaries

**PCA**: Standardize → covariance matrix → eigenvectors → project onto top-k. Linear, deterministic, fast. Preserves global variance structure. Suitable for ML preprocessing.

**t-SNE**: Models high-dim similarities as Gaussian probabilities, low-dim as Student-t, then minimizes KL divergence. Non-linear, non-parametric (can't project new points). Best for visualization only.

**UMAP**: Builds a fuzzy graph in high-dim space, optimizes low-dim layout. Preserves both local and some global structure. Fast, scalable, parametric (can project new points). Better than t-SNE for large datasets.

## Decision Framework

```
Need dimensionality reduction?
├── Modeling/preprocessing → PCA or UMAP
│   └── Interpretability needed → PCA
└── Visualization?
    ├── Small dataset → t-SNE
    └── Large + noisy → UMAP
```

## Comparison Table

| Feature | PCA | t-SNE | UMAP |
|---|---|---|---|
| Type | Linear | Non-linear | Non-linear |
| Preserves | Global | Local | Local + some global |
| Speed | Fast | Slow | Fast |
| Use in ML models | Yes | No | Yes |
| Clustering friendly | No | Yes | Yes |
| Inverse transform | Yes | No | No |

## Related Concepts

- [[Dimensionality Reduction]] — the broader category
- [[PCA]] — principal component analysis
- [[t-SNE]] — local-neighborhood visualization
- [[UMAP]] — manifold-based projection
- [[Embeddings]] — what gets reduced

## Related Articles

- [[PCA vs t-SNE - Which One Should You Use for Visualization]] — earlier PCA vs t-SNE on MNIST
- [[Principal Component Analysis (PCA) In Depth]] — PCA step-by-step
- [[t-SNE Clearly Explained]] — detailed t-SNE mechanics
- [[Exploring Hierarchical Navigable Small World]] — PCA applied to ANN speedup

## People

- [[Lakhan Bukkawar]]
