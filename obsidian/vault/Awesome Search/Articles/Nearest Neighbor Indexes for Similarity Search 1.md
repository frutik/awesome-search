---
title: "Nearest Neighbor Indexes for Similarity Search"
source: "https://www.pinecone.io/learn/series/faiss/vector-indexes/"
author: []
published: 
created: 2026-05-15
description: "A guide to FAISS index types — Flat, LSH, HNSW, and IVF — with benchmarks on Sift1M to guide index selection by memory, speed, and recall requirements."
tags:
  - clippings
  - company-blog
---
# Nearest Neighbor Indexes for Similarity Search

"There is no 'one-size-fits-all' in similarity search." Index selection depends on balancing accuracy, speed, and memory.

## Index types

### Flat Index
Exhaustive comparison against every vector. Perfect recall, slow for large datasets.
- **Use when**: dataset <10K vectors or quality is paramount
- L2: `IndexFlatL2` | IP: `IndexFlatIP`
- No training required

### LSH (Locality Sensitive Hashing)
Groups vectors into buckets using hash functions that maximize collisions. High sensitivity to dimensionality curse.
- **Use when**: low-dimensional vectors, small indexes
- Not suitable for 128+ dimensions or large datasets
- Parameter: `nbits` (higher = better accuracy, more memory)

### HNSW (Hierarchical Navigable Small World Graphs)
Multi-layered graph structure. Consistently top-performing for ANN search.
- **Use when**: larger, high-dimensional datasets with ample RAM
- Parameters: `M` (connections per vertex), `efSearch`, `efConstruction`
- High memory footprint (~1.6GB for Sift1M at M=128)

### IVF (Inverted File Index)
Clusters vectors via Voronoi diagrams, restricts search to relevant cells.
- **Use when**: scalable balance of metrics needed
- Parameters: `nlist` (cells/clusters), `nprobe` (cells to search)
- Addresses edge problem with `nprobe` tuning
- Requires training step

## Benchmark results (Sift1M, 128d, M1 chip)

| Index | Memory | Query Time | Recall |
|---|---|---|---|
| Flat | ~500 MB | ~18 ms | 1.0 |
| LSH | 20–600 MB | 1.7–30 ms | 0.4–0.85 |
| HNSW | 600–1600 MB | 0.6–2.1 ms | 0.5–0.95 |
| IVF | ~520 MB | 1–9 ms | 0.7–0.95 |


## Related Concepts

- [[Dense Vector Retrieval]]
- [[Embeddings]]
- [[Dense Embeddings]]
- [[Vector Quantization]]

## People

