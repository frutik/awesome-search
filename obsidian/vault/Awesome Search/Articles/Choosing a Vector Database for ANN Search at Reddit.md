---
created: 2026-06-01
type: article
title: "Choosing a Vector Database for ANN Search at Reddit"
source: "https://milvusio.medium.com/choosing-a-vector-database-for-ann-search-at-reddit-1c9464518c96"
author: "[[Chris Fournie]]"
published: 2025-11-28
tags:
  - article
  - vector-database
  - ann
  - case-study
  - evaluation
  - medium
concepts:
  - HNSW
  - Hybrid Search
  - Vector Filtering
  - Vector Quantization
topics:
  - Search Platforms
  - E-commerce Search
---

# Choosing a Vector Database for ANN Search at Reddit

Reddit's 2025 engineering evaluation of vector databases for ANN search, concluding with the selection of **Milvus** over Qdrant and others after rigorous qualitative and quantitative testing at Reddit-scale workloads (~340M vectors).

---

## Context

In 2024 Reddit used fragmented solutions: Google Vertex AI Vector Search, Apache Solr ANN, and Facebook FAISS (in vertically-scaled sidecars). In 2025, the team ran a company-wide evaluation to select a single broadly-supported ANN vector search solution that was cost-effective and could scale to Reddit-sized data.

## Evaluation Methodology

**Step 1: Collect requirements from teams** — functional (hybrid search, range search, metadata filtering) and non-functional (100M+ vectors, <100ms P99 latency, Kubernetes-hostable). Key discipline: challenge solution bias — one team requesting 10K results per query turned out to really need metadata filtering, not bulk retrieval.

**Step 2: Qualitative scoring** — scored 11 solutions on ~60 weighted criteria (0–3 per criterion × importance 1–3). Starting candidates: Milvus, Qdrant, Weaviate, OpenSearch, Pgvector, Redis, Cassandra, Solr, Vespa, Pinecone, Vertex AI.

**Step 3: Quantitative benchmarking** — Qdrant v1.12 vs Milvus v2.4 at 340M Reddit post vectors (384 dimensions, HNSW M=16, efConstruction=100). Load tested with Grafana K6. Key tests: filtering latency, ingestion + query interaction, result diversity queries, and scaling with RF=2.

**Step 4: Final selection** — Milvus.

## Qualitative Scores (top contenders)

| Solution | Overall Score |
|---|---|
| Qdrant | 292 |
| Milvus 2.4 | 281 |
| Cassandra | 264 |
| Weaviate | 250 |
| Solr | 242 |
| Vertex AI | 173 |

Hard requirements that eliminated solutions: **open-source** (eliminated Vertex AI and Pinecone), healthy community, evidence of 100M+ vector deployments.

## Key Quantitative Findings

- **Filtering**: Adding filters increased latency more for Milvus than Qdrant at RF=1
- **Ingest + query interaction**: Qdrant's homogeneous architecture caused more interference between ingest and query load than Milvus (which separates these into distinct node types)
- **Result diversity**: Milvus had worse latency than Qdrant for diversity-constrained queries at 100 QPS
- **Scaling with replication**: At RF=2, Milvus sustained higher throughput with acceptable latency; Qdrant's p99 improved but couldn't reach 400 QPS reliably

## Why Milvus Won

1. **Organizational fit**: Written in Go (Reddit's preferred backend language); easier to contribute to than Rust-based Qdrant
2. **Architecture**: Heterogeneous node types (query/ingest/index separation) → better isolation; automatic rebalancing when increasing replication factor (Qdrant open-source requires manual shard management)
3. **Project velocity**: Stronger open-source momentum at time of evaluation
4. **Requirements coverage**: Supported multiple index types; better metadata handling

## Key Lessons

- Challenge stated requirements — teams often describe workarounds, not actual needs
- Use scoring to structure discussion, not as a final decision mechanism
- Quantitative testing reveals operational realities beyond benchmark numbers
- Organizational fit (language, architecture patterns, contribution path) matters as much as raw performance

---

## Related Concepts
- [[HNSW]] — primary index tested
- [[Hybrid Search]] — key evaluation criterion
- [[Vector Filtering]] — filtering latency was a key differentiator
- [[Vector Quantization]] — evaluated across candidates

## Related Articles
- [[Exploring Vector Databases with Milvus]] — deep technical architecture of Milvus
- [[Milvus - Unlocking Your Data's Hidden Relationships]] — introductory Milvus overview

## People
- [[Chris Fournie]] — author; Staff Software Engineer at Reddit

## Companies
- [[Reddit]] — evaluating organization
