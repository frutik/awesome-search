---
type: article
title: "PCA vs t-SNE: which one should you use for visualization"
source: "https://medium.com/analytics-vidhya/pca-vs-t-sne-17bcd882bf3d"
author:
  - "[[Namratesh Shrivastav]]"
published: 2019-12-28
tags: [article, dimensionality-reduction, PCA, t-SNE, visualization, MNIST]
concepts:
  - Dimensionality Reduction
  - PCA
  - t-SNE
created: 2026-06-01
---

# PCA vs t-SNE: which one should you use for visualization

**Author:** [[Namratesh Shrivastav]]  
**Source:** https://medium.com/analytics-vidhya/pca-vs-t-sne-17bcd882bf3d

## Summary

Practical comparison of PCA and t-SNE on the MNIST dataset (60K training images, 784 dimensions per sample). Walks through both implementations step by step, showing where each method's output diverges.

## Core Distinction

**PCA** preserves large pairwise distances and maximizes variance — it captures global structure. Projects data linearly onto eigenvectors of the covariance matrix.

**t-SNE** preserves only local similarities. Points with high similarity in high-dimensional space remain close; non-similar points are pushed apart. It is non-linear and adapts to different regions of the data.

## Key Steps: PCA

1. Calculate mean per column; center data
2. Compute covariance matrix
3. Compute eigendecomposition (eigenvectors = principal directions)
4. Project onto top-k eigenvectors

## Key Insight

t-SNE is "incredibly flexible and often finds structure where other algorithms can't" — especially for non-linearly separable data. But it cannot be reused: there is no parametric transform to apply to new points.

## Related Concepts

- [[PCA]] — linear projection
- [[t-SNE]] — non-linear local-structure visualization
- [[Dimensionality Reduction]] — parent concept

## Related Articles

- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — extends comparison to UMAP
- [[t-SNE Explained - Math and Intuition]] — KL divergence and perplexity deep dive
- [[Understanding Principal Component Analysis (PCA)]] — detailed PCA math

## People

- [[Namratesh Shrivastav]]
