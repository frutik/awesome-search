---
title: "Nearest Neighbor Indexes for Similarity Search"
source: "https://www.pinecone.io/learn/series/faiss/vector-indexes/"
author: ["James Briggs"]
tags:
  - clippings
  - vector-search
  - ann
  - faiss
  - infrastructure
  - company-blog
concepts:
  - Dense Vector Retrieval
  - Semantic Search
  - Bi-Encoder
created: 2026-05-15
---

# Nearest Neighbor Indexes for Similarity Search

**Source**: https://www.pinecone.io/learn/series/faiss/vector-indexes/  
**Author**: [[James Briggs]] (Pinecone)

## Summary

[[James Briggs]] explains the major ANN (Approximate Nearest Neighbor) index types available in FAISS, their tradeoffs, and guidance on choosing the right index for different scale and quality requirements.

## The ANN Problem

Exact nearest neighbor search over millions of vectors is O(n × d) — too slow for real-time queries. ANN algorithms trade a small accuracy loss for massive speedups.

## Index Types

### Flat (Exact Search)
```python
import faiss
index = faiss.IndexFlatL2(dimension)  # exact L2 search
index.add(vectors)
distances, indices = index.search(query, k=10)
```
- **Accuracy**: 100% (exact)
- **Speed**: Slowest — O(n)
- **Use when**: Small dataset (<100K), or as quality baseline

### IVF (Inverted File Index)
```python
quantizer = faiss.IndexFlatL2(d)
index = faiss.IndexIVFFlat(quantizer, d, nlist=100)  # 100 clusters
index.train(vectors)
index.add(vectors)
index.nprobe = 10  # search 10 clusters at query time
```
- **Accuracy**: ~95–99% (tunable via nprobe)
- **Speed**: Fast — searches only `nprobe` clusters
- **Use when**: Medium dataset (100K–10M), need GPU support

### HNSW (Hierarchical Navigable Small World)
```python
index = faiss.IndexHNSWFlat(d, M=16)  # M = connections per node
index.hnsw.efConstruction = 40
index.add(vectors)
index.hnsw.efSearch = 16
```
- **Accuracy**: 95–99% (tunable via efSearch)
- **Speed**: Very fast — graph traversal
- **Memory**: Higher than IVF (stores graph structure)
- **Use when**: Low latency requirement, CPU-only, no batch training needed

### IVF + PQ (Product Quantization)
```python
index = faiss.IndexIVFPQ(quantizer, d, nlist=100, m=8, nbits=8)
```
Compresses vectors from float32 to quantized codes:
- 4–8x memory reduction
- Small accuracy loss
- **Use when**: Very large dataset (>100M), memory-constrained

### LSH (Locality Sensitive Hashing)
Hashes similar vectors to the same buckets:
- Very fast but lower accuracy
- Largely superseded by HNSW in practice

## Index Selection Guide

| Dataset Size | Quality Priority | Recommended Index |
|-------------|-----------------|------------------|
| <100K | Exact | Flat |
| 100K–1M | High | HNSW |
| 1M–100M | Balanced | IVF-Flat |
| >100M | Memory constrained | IVF-PQ |
| GPU available | Speed | IVF (GPU) |

## Pinecone's Managed Index

Pinecone handles index selection automatically and adds:
- Native [[Vector Filtering]] (metadata predicates alongside ANN)
- Automatic scaling
- Real-time upsert/delete

## Quality Metrics

**Recall@k**: fraction of true top-k results returned by ANN.  
HNSW with efSearch=64 typically achieves Recall@10 > 0.99 at good throughput.

## Related Articles

- [[The Missing WHERE Clause in Vector Search]] — same author, filtering
- [[SPLADE for Sparse Vector Search Explained]] — same author, sparse complement
- [[Matryoshka Embeddings - Faster OpenAI Vector Search]] — dimension reduction for speed
- [[How to Choose the Best Model for Semantic Search]] — what you're indexing

## Related Concepts

- [[Dense Vector Retrieval]] — primary topic
- [[Semantic Search]] — use case
- [[Bi-Encoder]] — produces the vectors being indexed
- [[Matryoshka Embeddings]] — dimension reduction for faster ANN
- [[Vector Filtering]] — metadata filtering alongside ANN
- [[Hybrid Search]] — ANN is one leg of hybrid

## People

- [[James Briggs]] — author (Pinecone)
