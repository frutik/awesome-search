---
title: Qdrant Vector DB
type: tool
tags:
  - tool
  - vector-database
  - vector-search
  - open-source
website: https://qdrant.tech/
repo: https://github.com/qdrant/qdrant
maintainer: "[[Qdrant]]"
created: 2026-05-19
---

# Qdrant Vector DB

Open-source vector database and similarity search engine optimized for high-performance ANN retrieval in production ML workloads. Maintained by [[Qdrant]] (the company).

- Website: https://qdrant.tech/
- GitHub: https://github.com/qdrant/qdrant

---

## What It Does

Qdrant stores dense vectors alongside payload (structured metadata) and supports filtered ANN search — combining vector similarity with attribute predicates efficiently via graph-integrated filtering.

Key capabilities:
- **ANN search** — [[HNSW]]-based index; high recall/speed tradeoff
- **Filtered search** — predicates integrated into graph traversal (not post-filter), avoiding recall loss on selective filters
- **Quantization** — [[Scalar Quantization]] (int8, 4×), [[Binary Quantization]] (1-bit, 32×), [[TurboQuant]] (rotation-based, 8×–32×, Qdrant 1.18+)
- **Sparse + dense** — supports sparse vectors alongside dense for hybrid retrieval
- **Payload filtering** — rich JSON payload per vector with indexed field filtering
- **Collections** — top-level namespace; each collection has its own vector config and index

## Quantization Options

| Method | Compression | Notes |
|--------|-------------|-------|
| Scalar Quantization (int8) | 4× | Near-lossless; default recommended |
| Binary Quantization | 16×–32× | Significant recall loss without oversampling |
| [[TurboQuant]] (v1.18+) | 8×–32× | Rotation-based; beats BQ by 9–24 pp recall |

## Related Tools
- **[[Weaviate Vector DB]]** — competing vector database; native cross-encoder reranking support
- **Pinecone** — managed-only competitor
- **FAISS** — library (not a service); no filtering, no persistence

## Related Concepts
- [[HNSW]] — the ANN index Qdrant uses
- [[Vector Quantization]] — compression family
- [[TurboQuant]] — Qdrant's latest quantization (1.18)
- [[Dense Vector Retrieval]] — primary use case
- [[Vector Filtering]] — Qdrant's predicate-in-graph approach
- [[Hybrid Search]] — combining sparse and dense retrieval

## Articles
- [[TurboQuant in Qdrant]]

## People
- [[Ivan Pleshkov]] — TurboQuant implementation
- [[Jonas Schulz]] — TurboQuant co-author
