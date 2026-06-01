---
title: "UMAP"
aliases: ["Uniform Manifold Approximation and Projection", "uniform manifold approximation", "umap"]
tags:
  - concept
  - dimensionality-reduction
  - visualization
  - manifold-learning
  - ml
created: 2026-06-01
---

# UMAP (Uniform Manifold Approximation and Projection)

## Definition

UMAP is a non-linear dimensionality reduction algorithm based on manifold learning and topological data analysis. It builds a fuzzy graph representation of the high-dimensional data and optimizes a low-dimensional layout to match it. Faster than [[t-SNE]] and parametric (can project new points).

## How It Works

1. **Build a fuzzy k-NN graph** in high-dim space — each point connected to its k nearest neighbors with weighted edges based on distance
2. **Construct a fuzzy simplicial set** — a topological representation of the local structure
3. **Optimize low-dim layout** — find an embedding that minimizes cross-entropy between the high-dim and low-dim fuzzy graph structures

## Properties

| Property | Value |
|---|---|
| Type | Non-linear |
| Preserves | Local + some global structure |
| Speed | Fast (much faster than t-SNE) |
| Parametric | Yes — can project new points |
| Inverse transform | No (parametric UMAP extension exists) |
| Suitable for ML | Yes |

## UMAP vs t-SNE

| | UMAP | t-SNE |
|---|---|---|
| Speed | Fast | Slow |
| New data | Yes (parametric) | No |
| Global structure | Partially preserved | Largely lost |
| Cluster spacing | More meaningful | Arbitrary |
| Hyperparameter sensitivity | Lower | Higher |

## Relevance to Search

UMAP's parametric nature makes it more practical than t-SNE for embedding compression pipelines where new vectors must be projected at query time. However, PCA remains the default for linear compression due to its speed, reversibility, and interpretability.

## Key Parameters

- `n_neighbors` — controls local vs global structure balance (like perplexity in t-SNE)
- `min_dist` — minimum distance between points in low-dim space; lower = tighter clusters
- `n_components` — target dimensionality

## Related Concepts

- [[Dimensionality Reduction]] — parent concept
- [[t-SNE]] — slower non-parametric alternative
- [[PCA]] — linear, even faster alternative
- [[Matryoshka Embeddings]] — training-time flexible-dimension approach

## Articles

- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — comparison table with code
