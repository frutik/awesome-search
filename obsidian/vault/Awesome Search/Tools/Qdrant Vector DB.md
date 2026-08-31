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
- **Hybrid fusion** — [[Reciprocal Rank Fusion|RRF]] (with configurable `k` since v1.16 and per-prefetch weights since v1.17) or [[Distribution-Based Score Fusion|DBSF]] (since v1.11), combining prefetch results at query time
- **Multivectors / late interaction** — native `multivector_config` with `MultiVectorComparator.MAX_SIM` for [[ColBERT]]/[[ColPali]] rerank; see [[Late Interaction in Qdrant]]
- **Payload filtering** — rich JSON payload per vector with indexed field filtering
- **Collections** — top-level namespace; each collection has its own vector config and index
- **Memory tiers** — unified `pinned`/`cached`/`cold` setting per component (v1.19+), replacing the `on_disk`, `always_ram`, and `on_disk_payload` flags
- **Per-tenant IDF** — [[BM25]] corpus statistics scoped to a tenant inside a shared collection (v1.19+); see [[Multi-Tenancy in Search]]

## Quantization Options

| Method | Compression | Notes |
|--------|-------------|-------|
| Scalar Quantization (int8) | 4× | Near-lossless; default recommended |
| Binary Quantization | 16×–32× | Significant recall loss without oversampling |
| [[TurboQuant]] (v1.18+) | 8×–32× | Rotation-based; beats BQ by 9–24 pp recall |
| turbo4 datatype (v1.19+) | 9× on disk | Stores only the 4-bit code; no originals retained, so no rescoring |

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
- [[Reciprocal Rank Fusion]] — configurable `k`/weights fusion method
- [[Distribution-Based Score Fusion]] — Qdrant's score-preserving fusion alternative to RRF
- [[Late Interaction]] — native multivector MaxSim reranking; see [[Late Interaction in Qdrant]]
- [[MUVERA]] — fixed-dimensional approximation used as the late-interaction first stage

## Articles
- [[TurboQuant in Qdrant]]
- [[Qdrant 1.19 - Turbo4 Datatype and Memory Tiers]] — turbo4 storage datatype, memory tiers, per-tenant IDF, slice filtering
- [[Choosing a Vector Database for ANN Search at Reddit]] — head-to-head vs. Milvus at 340M vectors; Qdrant showed better raw latency at RF=1 but lost on scaling and organizational fit
- [[How to Tune Hybrid Search in Qdrant]] — [[Dylan Couzon]]; RRF vs. DBSF and RRF `k`/weight tuning, measured across five datasets
- [[Hybrid Queries - Qdrant]] — RRF and DBSF fusion query reference

## People
- [[Ivan Pleshkov]] — TurboQuant implementation
- [[Jonas Schulz]] — TurboQuant co-author
- [[Mohamed Arbi Nsibi]] — 1.19 release writeup
- [[Dylan Couzon]] — hybrid search tuning guide
