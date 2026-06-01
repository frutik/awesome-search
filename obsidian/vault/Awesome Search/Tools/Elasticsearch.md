---
title: Elasticsearch
type: tool
tags:
  - tool
  - search-engine
  - vector-search
  - open-source
  - lucene
website: https://www.elastic.co/elasticsearch
repo: https://github.com/elastic/elasticsearch
maintainer: "[[Elastic]]"
created: 2026-05-19
---

# Elasticsearch

Dominant open-source distributed search engine built on Apache Lucene. Default backend for a large share of production search systems globally — e-commerce, log analytics, enterprise search. Maintained by [[Elastic]].

- Website: https://www.elastic.co/elasticsearch
- GitHub: https://github.com/elastic/elasticsearch

---

## What It Does

Elasticsearch indexes documents as JSON and exposes a REST API for full-text search, aggregations, filtering, and (since v8) dense vector ANN search. Horizontally scalable via sharding and replication.

Key capabilities:
- **Full-text search** — [[BM25]]-based relevance scoring (Lucene underneath)
- **Dense vector search** — `knn` query with [[HNSW]] index; supports [[Scalar Quantization]], [[BBQ|Binary Quantization (BBQ)]], [[ELSER]]
- **Hybrid search** — BM25 + kNN combination with score normalization and fusion
- **Sparse retrieval** — [[ELSER]] (Elastic Learned Sparse Encoder) for zero-shot semantic retrieval without dense embeddings
- **Aggregations** — faceted counts, histograms, metrics at scale
- **Boosting** — `function_score` query for [[Results Boosting]] (popularity, margin, recency)
- **Filtering** — pre-filter and post-filter support for `knn` queries ([[Vector Filtering]])

## Retrieval Options

| Mode | Query type | Notes |
|------|-----------|-------|
| BM25 | `match`, `multi_match` | Default; fast; no ML dependency |
| Sparse semantic | `sparse_vector` + [[ELSER]] | Zero-shot; no embedding model needed |
| Dense semantic | `knn` | Requires embedding model at index + query time |
| Hybrid | `knn` + `match` combined | Score normalization required (RRF or linear) |

## Quantization (Dense Vectors)

| Method | Compression | Notes |
|--------|-------------|-------|
| int8 Scalar Quantization | 4× | Near-lossless; default for kNN |
| [[BBQ]] (Better Binary Quantization) | 32× | Elastic's production binary quant scheme |

## Notable Use Cases in This Vault
- [[Zalando]] — base search layer
- [[Uber]] — custom Lucene-based platform
- Semantic Scholar — Elasticsearch + ML reranker

## Related Tools
- **[[Qdrant Vector DB]]** — purpose-built vector DB; stronger quantization
- **[[Weaviate Vector DB]]** — vector DB with native reranking pipeline
- **[[OpenSearch]]** — AWS fork of Elasticsearch; Apache 2.0 licensed
- **[[Elasticsearch vs OpenSearch]]** — licensing, performance, and feature comparison

## Related Concepts
- [[BM25]] — default scoring model
- [[ELSER]] — Elastic's sparse retrieval model
- [[BBQ]] — Elastic's binary quantization
- [[HNSW]] — ANN index for dense vectors
- [[Hybrid Search]] — BM25 + dense combination
- [[Results Boosting]] — `function_score` patterns
- [[Vector Filtering]] — kNN + predicate support
- [[Reciprocal Rank Fusion]] — fusion strategy for hybrid search

## Articles
- [[Elastic Learned Sparse Encoder ELSER Retrieval Performance]]
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]]
- [[Multilingual Embedding Model Hybrid Search Reranking]]
- [[Elasticsearch Personalized Search in Ecommerce - Improve Relevance]]
- [[Why Ecommerce Search Needs Governance and How It Improves Retrieval]]

## People
- [[Thomas Veasey]] — Principal Engineer; BBQ/OSQ quantization benchmarks
- [[Alexander Marquardt]] — Elastic Services Engineering
- [[Honza Král]] — Elastic
- [[Taylor Roy]] — Elastic
