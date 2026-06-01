---
type: article
title: "t-SNE clearly explained"
source: "https://medium.com/data-science/t-sne-clearly-explained-d84c537f53a"
author:
  - "[[Kemal Erdem]]"
published: 2020-04-13
tags: [article, dimensionality-reduction, t-SNE, KL-divergence, perplexity, CNN, visualization, medium]
concepts:
  - t-SNE
  - Dimensionality Reduction
  - PCA
created: 2026-06-01
---

# t-SNE clearly explained

**Author:** [[Kemal Erdem]]  
**Source:** https://medium.com/data-science/t-sne-clearly-explained-d84c537f53a

## Summary

Intuitive explanation of t-SNE including comparison with PCA, the math of the probability distributions, and two optimization tricks (early compression, early exaggeration). Ends with a CNN feature map application (Andrej Karpathy's ImageNet t-SNE).

## PCA vs t-SNE at a Glance

PCA uses the **global covariance matrix** — you can compute it once and project new data onto the same matrix. This makes PCA reusable across datasets.

t-SNE is **iterative and non-deterministic** — no reusable matrix. Each run may produce different results. You cannot apply t-SNE learned on train data to test data. This is the critical practical limitation.

## Algorithm Summary

1. Compute conditional probabilities (Gaussian in high-D, perplexity sets σᵢ)
2. Initialize random low-dim points
3. Compute low-dim similarities using **Student t-distribution** (1 degree of freedom) — heavy tails prevent crowding
4. Gradient descent minimizing KL divergence between high-D and low-D distributions

## Optimization Tricks

**Early Compression**: L2 penalty added to cost function early in training → prevents premature local clustering → keeps points mobile.

**Early Exaggeration**: Multiply pᵢⱼ by a large constant early → clusters can move more freely, don't block each other.

## CNN Application

t-SNE excels at visualizing CNN feature maps. [[Andrej Karpathy]] ran t-SNE on 50K ImageNet images (4096-dim fc7 features from a deep CNN) to produce a 2D map where visually similar images cluster together — revealing what the network considers "similar."

## Related Concepts

- [[t-SNE]] — concept note
- [[Dimensionality Reduction]] — parent concept
- [[PCA]] — the parametric, reusable alternative

## Related Articles

- [[t-SNE Explained - Math and Intuition]] — same algorithm, different derivation
- [[t-SNE Explained - Visualising High-Dimensional Data]] — step-by-step numerical walkthrough
- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — includes UMAP comparison

## People

- [[Kemal Erdem]]
- [[Laurens van der Maaten]] — t-SNE original author
- [[Geoffrey Hinton]] — t-SNE co-author
