---
title: "t-SNE"
aliases: ["t-distributed Stochastic Neighbor Embedding", "t-distributed stochastic neighbor embedding", "TSNE", "tSNE"]
tags:
  - concept
  - dimensionality-reduction
  - visualization
  - ml
created: 2026-06-01
---

# t-SNE (t-distributed Stochastic Neighbor Embedding)

## Definition

t-SNE is a non-linear dimensionality reduction algorithm that converts high-dimensional distances into probabilities and then finds a low-dimensional layout that best preserves those probabilities. Introduced by [[Laurens van der Maaten]] and [[Geoffrey Hinton]] in 2008.

## How It Works

1. **Compute pairwise Gaussian similarities** in high-D — convert Euclidean distances to probabilities; σᵢ set by perplexity
2. **Symmetrize** into joint distribution P: `pᵢⱼ = (p_{j|i} + p_{i|j}) / 2N`
3. **Initialize random low-dim positions** yᵢ
4. **Model low-dim similarities** using Student-t distribution (1 degree of freedom = Cauchy) — not Gaussian
5. **Minimize KL divergence** between P and Q via gradient descent

## Why Student-t in Low-D

In high-dim space, most points are roughly equidistant (distance concentration). If a Gaussian were used in low-D, all moderately distant points would collapse together (**crowding problem**). The heavy tail of the Student-t distribution keeps distant points meaningfully far apart in probability terms.

## Perplexity

A hyperparameter interpreted as the "effective number of neighbors." Controls σᵢ per point via binary search on Shannon entropy. Each point adapts its own σᵢ: dense regions use smaller σᵢ, sparse regions larger. Typical range: 5–50.

## Key Limitations

| Limitation | Implication |
|---|---|
| Non-parametric | Cannot project new points; must rerun on full dataset |
| Non-deterministic | Different runs → different layouts |
| Visualization only | Between-cluster spacing is meaningless |
| Slow | O(n²) naive; O(n log n) with Barnes-Hut approximation |
| No inverse transform | Cannot reconstruct original vectors |

**Not suitable for search/retrieval** — only for visualization and exploratory analysis.

## Related Concepts

- [[Dimensionality Reduction]] — parent concept
- [[PCA]] — linear, parametric alternative; suitable for search preprocessing
- [[UMAP]] — non-linear but parametric and faster; better for large datasets
- [[Matryoshka Embeddings]] — training-time flexible-dimension approach

## Articles

- [[t-SNE Explained - Math and Intuition]] — three-stage algorithm derivation
- [[t-SNE Explained - Visualising High-Dimensional Data]] — step-by-step numerical walkthrough
- [[t-SNE Clearly Explained]] — intuitive explanation with optimization tricks
- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — comparison table
- [[PCA vs t-SNE - Which One Should You Use for Visualization]] — MNIST comparison

## People

- [[Laurens van der Maaten]] — original author (2008)
- [[Geoffrey Hinton]] — co-author
