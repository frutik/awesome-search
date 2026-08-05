---
type: concept
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
created: 2026-05-16
---

# Dense Vector Retrieval

## Definition

**Dense vector retrieval** uses dense numerical embeddings (produced by neural models) to represent queries and documents, then finds the most similar documents via **approximate nearest neighbor (ANN)** search. Unlike sparse retrieval (keyword matching), it captures semantic relationships.

## How It Works

```
Documents → Encoder → dense vectors → ANN Index ([[HNSW]]/[[IVF]]/...)

Query → Encoder → query vector → ANN search → top-k similar docs
```

## Index Types (FAISS / ANN)

Memory figures below are for **1M vectors at 128 dimensions in float32** — the Sift1M shape used in
the FAISS index-comparison articles, where the raw vectors alone are 1M × 128 × 4 B = 512 MB. They
do **not** transfer to typical text-embedding dimensionality: at 768 dims the payload is 3.07 GB
before any index overhead, so scale the memory column by `d / 128`. See [[HNSW]] for the arithmetic.

| Index | Speed | Recall | Memory (1M × 128-dim) | Best For |
|---|---|---|---|---|
| **[[Brute-Force Vector Search\|Flat]]** (brute force) | Slowest | 100% | ~500MB | Small datasets |
| **HNSW** | Fastest | 95%+ | 600-1600MB | Quality-focused |
| **IVF** | Fast | 70-95% | ~520MB | Balanced, scalable |
| **LSH** | Variable | 40-85% | 20-600MB | Low-dimensional |

**[[HNSW]]** (Hierarchical Navigable Small World) is the most widely used:
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

- [[Brute-Force Vector Search]] — the exact scan; frequently sufficient below ~1M vectors
- [[Zero-Shot Retrieval]] — whether a dense model survives a change of domain
- [[Vector Quantization]] — compressing embeddings for memory and speed
- [[Scalar Quantization]] — int8/int4 per coordinate; 4–8× compression
- [[Binary Quantization]] — 1-bit per coordinate; 32× compression; needs rescoring
- [[BBQ]] — Elasticsearch's binary + scalar quantization approach
- [[HNSW]] — the dominant index structure for dense retrieval
- [[IVF]] — cluster-based alternative; lower memory

## Articles

- [[Nearest Neighbor Indexes for Similarity Search 1]]
- [[The Missing WHERE Clause in Vector Search 1]]
- [[Migrating to Elasticsearch with dense vector for Carousell Spotlight 1]]
- [[Matryoshka embeddings - faster OpenAI vector search using Adaptive Retrieval]]

- [[Understanding BERT and Search Relevance]]
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]] — [[Thomas Veasey]]; OSQ 10-40x faster via integer SIMD
- [[Why Are Embeddings So Cheap]] — [[Piotr Mazurek]]; compute-bound; ~$0.01/1M tokens at scale
- [[Dense Retrieval at Vinted]] — [[Vinted]]; multilingual-CLIP two-tower, hybrid (ANN supplements lexical), HNSW on [[Vespa]] at billion scale
- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]]; the three adoption mistakes — no fine-tuning, out-of-domain single-vector models, unpriced ANN tradeoffs
- [[Just brute force your embeddings]] — [[Doug Turnbull]]; ~1m vectors scanned with one NumPy dot product