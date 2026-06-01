---
type: article
title: "t-SNE Explained: Visualising High-Dimensional Data"
source: "https://medium.com/data-science-explained/t-sne-explained-visualising-high-dimensional-data-4f556041a80e"
author:
  - "[[Billy Chan]]"
published: 2025-12-26
tags: [article, dimensionality-reduction, t-SNE, KL-divergence, perplexity, visualization, Student-t, medium]
concepts:
  - t-SNE
  - Dimensionality Reduction
created: 2026-06-01
---

# t-SNE Explained: Visualising High-Dimensional Data

**Author:** [[Billy Chan]]  
**Source:** https://medium.com/data-science-explained/t-sne-explained-visualising-high-dimensional-data-4f556041a80e

## Summary

Most detailed step-by-step walkthrough of the t-SNE algorithm, working through a toy 5-point dataset numerically at every stage. Explains the "why" behind each design decision: why probabilities over distances, why perplexity, why Student-t in low-D.

## Why Probabilities Over Distances

Raw distances aren't comparable across dense vs sparse regions. Converting to probabilities **normalizes locally**: a distance of 0.5 in a dense cluster gets a different probability than the same distance in a sparse region. This lets t-SNE treat all points fairly.

## Step-by-Step Algorithm

1. Pick point i; compute Euclidean distances to all j's
2. Convert distances to Gaussian similarity scores (RBF kernel)
3. Normalize scores → conditional probabilities `p_{j|i}`
4. Choose σᵢ via perplexity: binary search for σ that gives target entropy `log(perplexity)`
5. Collect all conditional probabilities → asymmetric matrix
6. Symmetrize: `pᵢⱼ = (p_{j|i} + p_{i|j}) / 2N` — now all 10 joint probs (for 5 points) sum to 1
7. Initialize random low-dim positions yᵢ
8. Compute low-dim similarities using **Cauchy distribution** (Student-t with 1 degree of freedom)
9. Minimize KL divergence via gradient descent

## Why Student-t (Cauchy) in Low-D

In high-D, distances concentrate — most points are roughly equidistant. Gaussian tails drop too fast in low-D, causing the **crowding problem** (all points collapse together). The Student-t heavy tail keeps distant points meaningfully apart in probability terms.

## Key Warning

Between-cluster spacing in t-SNE plots is **arbitrary** — clusters can be at any distance from each other. Only within-cluster structure is meaningful. The KL divergence asymmetry means t-SNE cares much more about preserving close neighbors than about placing distant clusters correctly.

## Related Concepts

- [[t-SNE]] — concept note
- [[Dimensionality Reduction]] — parent concept

## Related Articles

- [[t-SNE Explained - Math and Intuition]] — complementary derivation, same algorithm
- [[t-SNE Clearly Explained]] — includes early exaggeration/compression tricks
- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — comparison table

## People

- [[Billy Chan]]
- [[Laurens van der Maaten]] — t-SNE original author
