---
type: concept
title: "Maximum Inner Product Search"
aliases: ["MIPS", "kMIPS", "k-MIPS", "k-Maximum Inner Product Search", "maximum inner product search"]
tags: [concept, vector-search, recommendation, retrieval]
related_concepts:
  - "[[Vector Similarity Metrics]]"
  - "[[Approximate Nearest Neighbor Search]]"
  - "[[Brute-Force Vector Search]]"
  - "[[MMR]]"
created: 2026-10-03
---

# Maximum Inner Product Search (MIPS)

Given a set of item vectors and a query vector, **k-Maximum Inner Product Search (kMIPS)** returns the *k* items with the largest inner product ⟨p, q⟩ with the query. It is the retrieval primitive behind matrix-factorization recommenders, where users and items share a latent space and relevance *is* the inner product. The same operation underlies dot-product scoring over [[Dense Embeddings]].

---

## Definition

For an item set P ⊂ ℝᵈ, a query q ∈ ℝᵈ and k ≥ 1, find S ⊆ P with |S| = k such that ⟨p, q⟩ ≥ ⟨p′, q⟩ for every p ∈ S and p′ ∉ S.

Inner product is not a distance: it is not normalized and does not satisfy the triangle inequality. Item norms therefore matter — a long vector can outrank a closer one. This is why MIPS is usually treated as its own problem rather than as nearest-neighbour search. See [[Vector Similarity Metrics]] for how inner product relates to cosine and L2.

## Method families

A taxonomy from the DkMIPS paper's survey of the field:

- **Index-free**
  - *Scan-based* — a linear scan with pruning and skipping.
  - *Sampling-based* — approximate, with low expected cost.
- **Index-based**
  - *Tree-based* — for example the Ball-Tree, and the Ball-Cone Tree variant, which bounds inner products by ball centre and radius.
  - *[[LSH|Locality-sensitive hashing]]*
  - *[[Vector Quantization|Quantization]]*
  - *Proximity graphs* (see [[HNSW]])

The last three overlap with the general [[Approximate Nearest Neighbor Search]] toolbox. The exact baseline is a [[Brute-Force Vector Search|linear scan]] in O(nd).

Variants studied in the literature include inner-product similarity join, reverse kMIPS, and diversity-aware kMIPS.

## Diversity-aware MIPS

Plain kMIPS optimizes relevance only, so results tend to cluster. A user with broad interests gets top-k items from a narrow slice of them. **DkMIPS** adds an [[MMR]]-style penalty on pairwise inner products inside the result set, with a λ dial between relevance and diversity. It is NP-hard, and the pairwise term breaks the assumptions most MIPS indexes rely on. Its authors use greedy approximation algorithms over a Ball-Cone Tree instead of LSH, quantization or graphs. See [[Diversity-Aware k-Maximum Inner Product Search Revisited]].

## Related Concepts

- [[Vector Similarity Metrics]] — inner product vs. cosine vs. L2
- [[Approximate Nearest Neighbor Search]] — the index families MIPS borrows from
- [[Brute-Force Vector Search]] — the exact linear-scan baseline
- [[MMR]] — the relevance/diversity objective behind DkMIPS
- [[Dense Embeddings]]

## Related Topics

- [[Search Result Diversity]]
- [[Vector Search Tradeoffs]]

## Related Articles

- [[Diversity-Aware k-Maximum Inner Product Search Revisited]]
