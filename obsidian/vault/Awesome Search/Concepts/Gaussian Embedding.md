---
title: "Gaussian Embedding"
aliases: ["Gaussian embedding", "Gaussian embeddings", "word2gauss"]
tags:
  - concept
  - embeddings
  - region-based-embeddings
  - representation-learning
---

# Gaussian Embedding

A [[Region-Based Representation]] (Vilnis & McCallum, ICLR 2015, *Word Representations via Gaussian Embedding*) that represents each word as a **Gaussian distribution** rather than a point. The mean places the word in space; the **variance encodes the spread / specificity** of its meaning — semantically narrow words get low-variance Gaussians, broad words get high-variance ones. This lets the representation express uncertainty and (asymmetric) containment that a point vector cannot.

It predates [[Box Embedding]] as a way to capture hierarchy and overlap. The trade-off versus boxes: computing **overlap between Gaussians is more expensive** than the per-dimension min/max intersection of axis-aligned boxes, which is a major reason box methods became more widely applied.

## Related Concepts
- [[Region-Based Representation]] — the family this belongs to
- [[Box Embedding]] — box-shaped alternative with cheaper overlap
- [[Poincaré Embedding]] — hyperbolic alternative for hierarchy
- [[Embeddings]] — point-vector baseline

## Articles
- [[Express Words in a Box - Understanding Box Embedding from the Basics]] — [[Shun Tsukagoshi]]; introduces Gaussian Embedding as a precursor to boxes

## People
- [[Luke Vilnis]] — lead author (also Box Lattice)
