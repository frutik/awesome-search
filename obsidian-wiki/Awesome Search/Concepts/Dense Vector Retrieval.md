---
title: Dense Vector Retrieval
aliases:
  - Dense Retrieval
  - Vector Search
  - ANN Search
  - Approximate Nearest Neighbor
  - ANNS
  - ANN
  - KNN
  - K-Nearest Neighbors
  - Approximate Nearest Neighbor Search
  - nearest neighbor search
tags:
  - concept
  - search
  - embeddings
  - vector-search
---

# Dense Vector Retrieval

## Definition

**Dense vector retrieval** uses dense numerical embeddings (produced by neural models) to represent queries and documents, then finds the most similar documents via **approximate nearest neighbor (ANN)** search. Unlike sparse retrieval (keyword matching), it captures semantic relationships.

## How It Works

```
Documents → Encoder → dense vectors → ANN Index (HNSW/IVF/...)

Query → Encoder → query vector → ANN search → top-k similar docs
```

## Index Types (FAISS / ANN)

| Index | Speed | Recall | Memory | Best For |
|---|---|---|---|---|
| **Flat** (brute force) | Slowest | 100% | ~500MB/1M | Small datasets |
| **HNSW** | Fastest | 95%+ | 600-1600MB | Quality-focused |
| **IVF** | Fast | 70-95% | ~520MB | Balanced, scalable |
| **LSH** | Variable | 40-85% | 20-600MB | Low-dimensional |

**HNSW** (Hierarchical Navigable Small World) is the most widely used:
- Graph-based multi-layer structure
- Key params: `M` (connections), `efSearch`, `efConstruction`

## Key Models Producing Dense Vectors

- **[[Bi-Encoder]]** models (e.g., sentence-transformers, OpenAI ada, E5)
- **[[ColBERT]]** — multi-vector dense (per-token)
- **[[Matryoshka Embeddings]]** — truncatable dense vectors

## The Filtering Problem

Standard ANN indexes don't support metadata filters efficiently:
- **Pre-filter + brute-force:** Accurate but slow
- **Post-filter:** Fast but may return too few results
- **Single-stage (Pinecone):** Merges metadata + vector index — best of both

See: [[Vector Filtering]]

## Symmetric vs. Asymmetric Retrieval

- **Symmetric** — query and document are similar length/type (e.g., duplicate question detection)
- **Asymmetric** — short query retrieves long documents (e.g., question → Wikipedia passage)

See: [[Asymmetric Semantic Search]]

## Related Concepts
- [[Vector Similarity Metrics]] — cosine similarity, dot product, Euclidean distance; how similarity is computed
- [[Embeddings]] — what embeddings are; how they're trained
- [[Dense Embeddings]] — the representation type this retrieval method indexes

- [[Bi-Encoder]] — produces single dense vectors
- [[ColBERT]] — produces multi-vector dense representations
- [[Matryoshka Embeddings]] — optimized dense vectors
- [[Hybrid Search]] — dense + sparse combined
- [[Sparse Vector Retrieval]] — complementary approach
- [[Vector Filtering]] — adding metadata filters to ANN search
- [[RAG]] — dense retrieval is core to RAG

- [[Vector Quantization]] — compressing embeddings for memory and speed
- [[BBQ]] — Elasticsearch's binary + scalar quantization approach

## Articles

- [[Nearest Neighbor Indexes for Similarity Search]]
- [[The Missing WHERE Clause in Vector Search]]
- [[Migrating to Elasticsearch with dense vector for Carousell Spotlight]]
- [[Matryoshka embeddings - faster OpenAI vector search using Adaptive Retrieval]]

- [[Understanding BERT and Search Relevance]]
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]] — [[Thomas Veasey]]; OSQ 10-40x faster via integer SIMD
- [[Why Are Embeddings So Cheap]] — [[Piotr Mazurek]]; compute-bound; ~$0.01/1M tokens at scale