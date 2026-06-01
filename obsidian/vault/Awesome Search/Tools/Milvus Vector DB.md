---
title: Milvus Vector DB
type: tool
tags:
  - tool
  - vector-database
  - vector-search
  - open-source
website: https://milvus.io
repo: https://github.com/milvus-io/milvus
created: 2026-06-01
---

# Milvus Vector DB

Open-source vector database built for efficient large-scale similarity search and AI applications. Initially published in the 2021 SIGMOD paper "Milvus: A Purpose-Built Vector Data Management System." Built on top of Facebook FAISS with added scalability, dynamic data management, and a distributed architecture.

- Website: https://milvus.io
- GitHub: https://github.com/milvus-io/milvus
- Documentation: https://milvus.io/docs

---

## What It Does

Milvus stores vectors alongside structured metadata (attributes) and supports multiple query types over large-scale dynamic vector collections.

Key capabilities:
- **Multiple index types** — HNSW (graph-based), IVF_FLAT, IVF_SQ8, IVF_PQ, and more (quantization-based); extensible interface for new indexes
- **Attribute filtering** — five strategies (A–E); partition-based Strategy E outperforms cost-based approaches
- **Multi-vector queries** — aggregated similarity over composite objects (Vector Fusion and Iterative Merging approaches)
- **Dynamic data** — insertions and deletions via LSM structure; snapshot isolation for consistent reads
- **Hybrid search** — dense + sparse (BM25 full-text search, 4× faster than Elasticsearch per Milvus 2.6 benchmarks)
- **Quantization** — support for scalar quantization, binary quantization (RaBitQ 1-bit in 2.6: 72% lower memory, 4× faster)
- **Multi-tenant** — supports 100K+ collections (Milvus 2.6)

## Architecture

Milvus uses a heterogeneous multi-node architecture with three layers:
1. **Coordinator layer** — metadata, sharding, load-balancing
2. **Computing layer** (Kubernetes): separate nodes for queries, ingestion, and indexing; auto-scaling readers; WAL-based writer
3. **Storage layer** — Amazon S3 (high availability)

This separation means ingest load does not interfere with query traffic — a key differentiator vs. homogeneous architectures like Qdrant.

## Version History Notes

- **Milvus 2.4** — version used in Reddit's evaluation
- **Milvus 2.5** — improved full-text BM25 search
- **Milvus 2.6** — RaBitQ 1-bit quantization (72% memory reduction, 4× faster); tiered storage (50% cost reduction); 4× faster BM25 vs Elasticsearch; 100× faster JSON filtering; 100K+ collection support; zero-disk architecture

## Related Tools
- **[[Qdrant Vector DB]]** — competing vector database; homogeneous architecture; Rust-based; tested head-to-head at Reddit
- **[[Weaviate Vector DB]]** — competing vector database; single-node-type architecture (similar to Qdrant)
- **[[Elasticsearch]]** — general search engine; Milvus 2.6 claims 4× faster BM25 full-text search

## Related Concepts
- [[HNSW]] — primary graph-based ANN index
- [[IVF]] — quantization-based ANN index family
- [[Vector Quantization]] — core indexing technique
- [[Dense Vector Retrieval]] — primary use case
- [[Vector Filtering]] — attribute filtering during ANN search
- [[Hybrid Search]] — combined dense + sparse retrieval

## Case Studies
- [[Reddit - Vector Database Selection]] — Reddit chose Milvus over Qdrant for ~340M vectors after head-to-head evaluation

## Articles
- [[Choosing a Vector Database for ANN Search at Reddit]]
- [[Exploring Vector Databases with Milvus]]
- [[Milvus - Unlocking Your Data's Hidden Relationships]]
