---
title: "Poincaré Embedding"
aliases: ["Poincaré embedding", "Poincare embedding", "hyperbolic embedding", "hyperbolic embeddings"]
tags:
  - concept
  - embeddings
  - region-based-embeddings
  - representation-learning
---

# Poincaré Embedding

A [[Region-Based Representation]] (Nickel & Kiela, NIPS 2017, *Poincaré Embeddings for Learning Hierarchical Representations*) that embeds objects in **hyperbolic space** (the Poincaré ball) instead of Euclidean space. Hyperbolic geometry expands exponentially toward its boundary, so it can embed **tree-like hierarchies with low distortion in very few dimensions** — general concepts sit near the origin, specific ones near the boundary, capturing hierarchy and overlapping meanings naturally.

It is a contemporary alternative to [[Gaussian Embedding]] and a precursor to [[Box Embedding]] in the search for representations that go beyond points. Trade-off versus boxes: hyperbolic distance computations are more involved than the cheap min/max intersection of axis-aligned boxes.

## Related Concepts
- [[Region-Based Representation]] — the family this belongs to
- [[Box Embedding]] — Euclidean box alternative with cheap overlap
- [[Gaussian Embedding]] — Gaussian alternative
- [[Embeddings]] — point-vector baseline

## Articles
- [[Express Words in a Box - Understanding Box Embedding from the Basics]] — [[Shun Tsukagoshi]]; introduces Poincaré Embedding as a region-representation precursor to boxes
