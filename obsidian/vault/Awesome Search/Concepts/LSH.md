---
title: "LSH"
type: concept
aliases:
  - Locality Sensitive Hashing
  - Locality-Sensitive Hashing
tags:
  - concept
  - vector-search
  - ann
created: 2026-07-05
---

# LSH — Locality Sensitive Hashing

**Locality Sensitive Hashing** is an [[Approximate Nearest Neighbor Search|ANN]] method
that hashes vectors so that **similar vectors collide into the same bucket**. This
inverts the goal of an ordinary hash function (which minimizes collisions): LSH
deliberately **maximizes** them for near-neighbors, so search can be restricted to a
small set of candidate buckets instead of the whole dataset.

## How It Works

1. Vectors are pushed through hashing functions into buckets, grouping near-neighbors together.
2. A query vector is hashed the same way, landing in (or near) a bucket.
3. The nearest bucket(s) are found via **Hamming distance**, and search scope is
   restricted to the vectors inside them — avoiding an exhaustive scan.

## Key Parameter: `nbits`

- Controls resolution of the hash and therefore the recall/speed/size trade-off.
- Must **scale with dimensionality** — in [[FAISS]] (`IndexLSH(d, nbits)`) a value like
  `d*4` is used. Higher `nbits` → better recall, but larger index and slower search.
- **Curse of dimensionality**: LSH is excellent at low dimensionality but degrades
  quickly as `d` grows (e.g. 512), where cost explodes. Best reserved for low-`d` data.

## In Practice

On Sift1M, LSH at `nbits = d*4` ran ~10× faster than exact Flat search with good recall
(see [[Choosing Indexes for Similarity Search (Faiss in Python)]]). In modern systems it
has been **largely superseded by [[HNSW]]** for high-dimensional embeddings, but remains
a useful, simple option when dimensionality is low.

## Related Concepts

- [[Approximate Nearest Neighbor Search]] — the problem LSH addresses
- [[HNSW]] · [[IVF]] — alternative ANN indexes that scale better to high `d`
- [[Dense Vector Retrieval]] — where ANN indexes are applied

## Tools

- [[FAISS]] — `IndexLSH`

## Articles

- [[Choosing Indexes for Similarity Search (Faiss in Python)]]
- [[Nearest Neighbor Indexes for Similarity Search]]

## Related Topics

- [[Vector Search Tradeoffs]] — the umbrella hub for choosing between index families
