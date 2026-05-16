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

Graph-based approximate nearest neighbor (ANN) index. **Malkov & Yashunin, 2018** (arXiv:1603.09320). The dominant ANN index structure for high-recall, low-latency dense vector search. Used by Elasticsearch, Qdrant, Weaviate, pgvector, FAISS, and most production vector stores.

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

- Higher `M`: better recall, more memory (each edge is a stored ID + distance)
- Higher `ef_construct`: better graph quality (slower build, same query memory)
- Higher `ef_search`: better recall at query time, slower queries — the main runtime knob

## Recall / Speed / Memory

| Metric | Characteristic |
|---|---|
| Recall | 95–99%+ achievable with reasonable ef_search |
| Query latency | Sub-millisecond on CPU for typical dims |
| Build time | O(n log n) approximately |
| Memory | ~600–1600 MB / 1M 768-dim float32 vectors (edge overhead on top of raw vectors) |
| Compression | Combine with [[Scalar Quantization]] or [[Binary Quantization]] / [[TurboQuant]] to reduce memory |

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

## Related Concepts
- [[Dense Vector Retrieval]] — HNSW is the dominant index used here
- [[IVF]] — alternative cluster-based ANN index
- [[Vector Quantization]] — compresses stored vectors; HNSW graph edges remain float32 or quantized
- [[Scalar Quantization]] — often combined with HNSW (quantized storage + graph traversal)
- [[Binary Quantization]] — extreme compression combined with HNSW; recall recovered via rescoring
- [[TurboQuant]] — rotation-based quantization designed to work with HNSW (MSE variant chosen for symmetric scoring compatibility)
- [[Vector Filtering]] — metadata-aware HNSW traversal
- [[ANN]] — parent concept
