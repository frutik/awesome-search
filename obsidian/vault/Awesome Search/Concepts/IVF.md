---
title: "IVF"
aliases: ["Inverted File Index", "IVF index", "IVF-Flat", "IVF-PQ", "IVF-SQ", "nlist", "nprobe"]
tags:
  - concept
  - vector-search
  - ann
  - performance
---

# IVF — Inverted File Index (Vectors)

Cluster-based approximate nearest neighbor (ANN) index. The classic ANN approach in FAISS before graph-based methods dominated. Still preferred for very large datasets where [[HNSW]]'s memory overhead is prohibitive, and for combining with [[Vector Quantization]] variants (IVF-PQ, IVF-SQ).

## Structure

**Build:**
1. Run k-means on a sample of the dataset → `nlist` centroids (cluster centers)
2. Assign every vector to its nearest centroid
3. Store each vector in the inverted list for its cluster

**Query:**
1. Compute distance from query to all `nlist` centroids (coarse quantizer) — fast since nlist is small (typically 100–65536)
2. Select the `nprobe` closest centroids
3. Brute-force search within those `nprobe` lists
4. Return top-k overall

```
Query vector
  → compare to all nlist centroids (cheap)
    → enter nprobe closest lists
      → brute-force within lists → top-k results
```

## Key Parameters

| Parameter | Role | Typical values |
|-----------|------|---------------|
| `nlist` | Number of clusters | sqrt(n) rule: ~1000 for 1M vecs |
| `nprobe` | Clusters searched per query | 1–nlist; tune for recall vs speed |
| Training size | Vectors used for k-means | ≥ 39 × nlist recommended |

- `nprobe=1`: fastest, lowest recall
- `nprobe=nlist`: exact search (equivalent to brute force)
- Recall improves roughly as nprobe/nlist

## Variants

| Variant | Storage | Notes |
|---------|---------|-------|
| **IVF-Flat** | float32 | Exact within probed lists; high memory |
| **IVF-SQ** | int8 | [[Scalar Quantization]] inside each list; 4× smaller |
| **IVF-PQ** | sub-vectors | [[Vector Quantization]] (Product Quantization); 32–64× smaller; some recall loss |
| **IVF-HNSW** | float32 | Uses [[HNSW]] as the coarse quantizer instead of flat k-means |

## vs. HNSW

| | [[HNSW]] | IVF |
|---|---|---|
| Structure | Graph | Inverted lists |
| Recall at equivalent settings | Higher | Lower |
| Memory | Higher (edge storage) | Lower |
| Updates | Supports incremental inserts | Centroids fixed after training; partial rebuild for large updates |
| Build cost | O(n log n), slower | Fast after training |
| Best for | Quality-critical use cases | Very large corpora, memory-constrained |

## When to Prefer IVF

- Dataset too large for HNSW memory budget (billions of vectors)
- Combining with Product Quantization (IVF-PQ is the standard FAISS recipe for billion-scale search)
- Batch/offline search workloads (high nprobe acceptable)
- When recall requirements are moderate (80–90% sufficient)

## Related Concepts
- [[Dense Vector Retrieval]] — IVF is one of the main index types used here
- [[HNSW]] — the alternative graph-based ANN index; usually higher recall at same memory
- [[Vector Quantization]] — IVF-PQ and IVF-SQ combine IVF with quantization
- [[Scalar Quantization]] — used in IVF-SQ variant
- [[Binary Quantization]] — can be used inside IVF lists
- [[ANN]] — parent concept
- [[pgvector]] — its IVFFlat index is the IVF-Flat variant inside [[PostgreSQL]]; see [[Search using PostgreSQL]]
