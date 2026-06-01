---
type: article
title: "T-SNE Explained — Math and Intuition"
source: "https://medium.com/swlh/t-sne-explained-math-and-intuition-94599ab164cf"
author:
  - "[[Achinoam Soroker]]"
published: 2020-08-04
tags: [article, dimensionality-reduction, t-SNE, KL-divergence, perplexity, visualization, medium]
concepts:
  - t-SNE
  - Dimensionality Reduction
created: 2026-06-01
---

# T-SNE Explained — Math and Intuition

**Author:** [[Achinoam Soroker]]  
**Source:** https://medium.com/swlh/t-sne-explained-math-and-intuition-94599ab164cf

## Summary

Three-stage derivation of the t-SNE algorithm, building intuition before introducing math. Covers why simple projection fails (density differences), how joint probability distributions handle it, and why Student-t solves the crowding problem.

## The Three Stages

### Stage 1: Joint probability distribution in high-dim
- Compute Euclidean distances between all pairs
- Convert distances to conditional probabilities via Gaussian centered at xᵢ (perplexity controls σᵢ)
- Symmetrize: `pᵢⱼ = (p_{j|i} + p_{i|j}) / 2N`

### Stage 2: Random low-dim dataset
- Initialize random points in target dimension (usually 2D or 3D)
- Model their similarities using **Student-t distribution** (not Gaussian)
- Why t-distribution: heavy tails prevent "crowding" — moderate high-dim distances become more extreme in low-dim, separating clusters

### Stage 3: Gradient descent
- Minimize **KL divergence** between high-dim (P) and low-dim (Q) distributions
- Cost function: `C = Σᵢⱼ pᵢⱼ log(pᵢⱼ / qᵢⱼ)`
- Convergence = a 2D/3D layout where neighborhood structure matches the original

## Perplexity

Controls σᵢ per point — a target number of effective neighbors. Robust between 5–50. Points in dense regions get smaller σᵢ (narrower Gaussian); sparse regions get larger σᵢ.

## Key Limitation

t-SNE is **non-parametric**: no reusable transform. Cannot project new points — must rerun on the full dataset. This disqualifies it for retrieval/search use.

## Related Concepts

- [[t-SNE]] — concept note
- [[Dimensionality Reduction]] — parent concept
- [[PCA]] — linear alternative that is parametric

## Related Articles

- [[t-SNE Explained - Visualising High-Dimensional Data]] — step-by-step numerical walkthrough
- [[t-SNE Clearly Explained]] — includes CNN feature map application
- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — comparative overview

## People

- [[Achinoam Soroker]]
- [[Laurens van der Maaten]] — t-SNE original author
- [[Geoffrey Hinton]] — t-SNE co-author
