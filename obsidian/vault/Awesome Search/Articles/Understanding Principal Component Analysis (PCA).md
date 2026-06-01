---
type: article
title: "Understanding Principal Component Analysis (PCA)"
source: "https://medium.com/@roshmitadey/understanding-principal-component-analysis-pca-d4bb40e12d33"
author:
  - "[[Roshmita Dey]]"
published: 2023-10-06
tags: [article, dimensionality-reduction, PCA, linear-algebra, machine-learning, medium]
concepts:
  - PCA
  - Dimensionality Reduction
created: 2026-06-01
---

# Understanding Principal Component Analysis (PCA)

**Author:** [[Roshmita Dey]]  
**Source:** https://medium.com/@roshmitadey/understanding-principal-component-analysis-pca-d4bb40e12d33

## Summary

Comprehensive guide covering why dimensionality reduction is needed, the mathematics of PCA, and applications across domains. Strong on motivating the curse of dimensionality before presenting the algorithm.

## Why Dimensionality Reduction

Four problems that high-dimensionality causes:
1. **Computational complexity** — resources grow exponentially with features
2. **Overfitting** — models fit noise in high-dim space, poor generalization
3. **Visualization** — impossible to visualize beyond 3D
4. **Redundancy** — correlated features carry duplicate information, safely eliminable

## PCA Steps

1. Standardize (mean=0, std=1)
2. Compute covariance matrix
3. Compute eigenvalues and eigenvectors
4. Sort by eigenvalue descending (first PC = most variance explained)
5. Select top-k eigenvectors (transformation matrix)
6. Project data into reduced space

## Eigenvalue Interpretation

- **Eigenvalue λ** = variance explained by that principal component; always non-negative
- **Eigenvector** = direction of that component in feature space; normalized to length 1
- First PC has largest eigenvalue; PCs are orthogonal (uncorrelated by construction)

## Applications

- Image compression and face recognition
- Bioinformatics (gene expression dimensionality)
- Recommendation systems (user-item matrix compression)
- Finance (trend identification in price data)

## Related Concepts

- [[PCA]] — concept note
- [[Dimensionality Reduction]] — parent concept
- [[Embeddings]] — the vectors being compressed

## Related Articles

- [[Principal Component Analysis (PCA) In Depth]] — algorithm walkthrough with worked numerical example
- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — comparison with non-linear methods

## People

- [[Roshmita Dey]]
