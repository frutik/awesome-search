---
title: "HNSW"
aliases: ["Hierarchical Navigable Small World", "HNSW index", "HNSW graph"]
tags:
  - concept
  - vector-search
  - ann
  - performance
---

# HNSW — Hierarchical Navigable Small World

Graph-based approximate nearest neighbor (ANN) index. **Malkov & Yashunin, 2018** (arXiv:1603.09320). The dominant ANN index structure for high-recall, low-latency dense vector search. Used by Elasticsearch, Qdrant, Weaviate, [[pgvector]], FAISS, and most production vector stores.

## Structure

HNSW builds a multi-layer proximity graph:

```
Layer 2 (top):   few nodes, long-range links   ← coarse navigation
Layer 1:         more nodes, medium-range links
Layer 0 (base):  all nodes, short-range links  ← fine-grained search
```

Each node in layer 0 holds up to `M` bidirectional links to its nearest neighbors. Higher layers are subsampled probabilistically; a given node exists in layer `l` with probability `e^(-l / mL)`.

**Search** starts at the entry point in the top layer, greedily descends to layer 0, then explores a beam of candidates at the base layer using a priority queue (greedy beam search).

**Insert** follows the same path to find the best neighbors at each layer, then adds edges. Existing edges may be pruned to stay within the `M` budget (heuristic neighbor selection prefers diverse neighbors over closer ones).

## Key Parameters

| Parameter | Role | Typical range |
|-----------|------|---------------|
| `M` | Max edges per node per layer | 8–64 (16 is common) |
| `ef_construct` | Beam width during index build | 64–512 |
| `ef_search` (efSearch) | Beam width at query time | 16–512 |

- Higher `M`: better recall, more memory (each link is typically a stored neighbour ID, ~4 bytes)
- Higher `ef_construct`: better graph quality (slower build, same query memory)
- Higher `ef_search`: better recall at query time, slower queries — the main runtime knob

## Recall / Speed / Memory

| Metric | Characteristic |
|---|---|
| Recall | 95–99%+ achievable with reasonable ef_search |
| Query latency | Sub-millisecond on CPU for typical dims |
| Build time | O(n log n) approximately |
| Memory | Raw vectors + graph links — see below |
| Compression | Combine with [[Scalar Quantization]] or [[Binary Quantization]] / [[TurboQuant]] to reduce memory |

### Memory, from first principles

Quote memory only alongside a dimensionality — the vector payload dominates, and it scales with `d`:

```
bytes ≈ n × (d × bytes_per_component)   ← vectors
      + n × (~2M × 4)                   ← graph links (one ~4-byte neighbour ID each)
```

Layer 0 holds up to `2M` links per node and higher layers `M`, so `~2M` links per node is the
usual working estimate. Worked at float32:

| Corpus | Vectors | Links (M=16) | Links (M=128) | Total |
|---|---|---|---|---|
| 1M × 128 dims | 512 MB | 128 MB | 1.02 GB | ~0.6–1.5 GB |
| 1M × 768 dims | 3.07 GB | 128 MB | 1.02 GB | ~3.2–4.1 GB |

The first row reproduces the measured 600–1600 MB range reported for Sift1M in
[[Nearest Neighbor Indexes for Similarity Search 1]] (which attributes the ~1.6 GB top end to
`M=128`), so the estimate is calibrated rather than theoretical.

Two things fall out. **The graph is not the expensive part** at realistic dimensionality — at 768
dims and a sane `M`, links are a few percent of the total, so "HNSW uses a lot of memory" is mostly
a statement about storing float32 vectors at all. And **compression therefore dominates the memory
question**:
[[Scalar Quantization]] at int8 cuts the 3.07 GB payload to ~0.77 GB, [[Binary Quantization]] to
~0.1 GB, while the link overhead is unchanged. See
[[Dimensionality Reduction vs Quantization]] and [[Vector Search Tradeoffs]].

## vs. IVF

| | HNSW | [[IVF]] |
|---|---|---|
| Structure | Graph | Inverted lists (clusters) |
| Recall at same nprobe/ef | Higher | Lower |
| Memory | Higher (edge storage) | Lower |
| Update | Supports inserts without rebuild | Rebuild needed for significant updates |
| Best for | Quality-critical, moderate scale | Very large scale, memory-constrained |

## Filtering

Standard HNSW ignores metadata — filters are applied post-search (post-filter: fast but low recall when filters are selective) or pre-filter (accurate but slow). Purpose-built solutions like Qdrant's [[Vector Filtering]] integrate predicates into graph traversal.

Four strategies ranked by filter selectivity:
1. **Post-filter** — ANN search runs normally, filter applied to hits; can return 0 results
2. **Pre-filter** — only filter-passing nodes counted in search; degrades as selectivity increases
3. **Pre-filter, check first** — skip distance computations for non-matching nodes; [[ACORN-1]] extends this with multi-hop neighborhoods to avoid getting stuck
4. **Exact search fallback** — triggered when filtering fraction drops below a threshold

## Steering the Traversal

The hop-selection function is a seam, not a fixed part of the algorithm. Vanilla HNSW picks the next neighbour by similarity to the query vector alone; replacing that criterion changes which region of the graph the walk reaches, and therefore what the index can return at all — a stronger intervention than filtering or reranking the output.

- [[Vector Filtering]] / [[ACORN-1]] — fold metadata predicates into the hop decision
- **Relevance feedback** — [[Qdrant]] 1.17 scores each hop by a combination of query similarity and feedback from a previous retrieval round, distilling a reranker's judgement into the traversal itself. See [[Relevance Feedback]] and [[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]].

Both are only possible for engines that own their index — a recurring argument against treating search engines as black boxes.

## Related Concepts
- [[Dense Vector Retrieval]] — HNSW is the dominant index used here
- [[IVF]] — alternative cluster-based ANN index
- [[LSH]] — hash-bucket ANN index; simpler but superseded by HNSW at high dimensionality
- [[FAISS]] — library exposing HNSW as `IndexHNSWFlat`
- [[Vector Quantization]] — compresses stored vectors; HNSW graph edges remain float32 or quantized
- [[Scalar Quantization]] — often combined with HNSW (quantized storage + graph traversal)
- [[Binary Quantization]] — extreme compression combined with HNSW; recall recovered via rescoring
- [[TurboQuant]] — rotation-based quantization designed to work with HNSW (MSE variant chosen for symmetric scoring compatibility)
- [[Vector Filtering]] — metadata-aware HNSW traversal
- [[ACORN-1]] — HNSW extension for aggressive filtered ANN search using multi-hop neighborhoods
- [[ANN]] — parent concept
- [[pgvector]] — exposes HNSW indexing inside [[PostgreSQL]]; see [[Search using PostgreSQL]]

## Articles

- [[Exploring Hierarchical Navigable Small World]] — Vespa intern deep-dive; covers graph quality metrics, disconnected components, edge density, dimensionality reduction, and ACORN-1 comparison
- [[Choosing a Vector Database for ANN Search at Reddit]] — Reddit's benchmark of Milvus vs Qdrant at 340M vectors; HNSW M=16, efConstruction=100 was the primary tested index configuration
- [[Exploring Vector Databases with Milvus]] — deep dive into HNSW and quantization-based indexing in Milvus; n_probe tradeoffs; filtering strategies A–E
- [[Choosing Indexes for Similarity Search (Faiss in Python)]] — James Briggs video benchmarking HNSW vs Flat, LSH, and IVF on Sift1M

## Videos

- [[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]] — [[Berlin Buzzwords]] 2026; modifying the hop-selection function to carry relevance feedback

## Related Topics

- [[Vector Search Tradeoffs]] — where HNSW's recall/memory/update position sits among the other axes
