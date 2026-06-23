---
title: "Search Architecture"
aliases: ["search pipeline architecture", "search system design", "search infrastructure"]
tags:
  - concept
  - search
  - architecture
created: 2026-05-15
---

# Search Architecture

End-to-end design of a production search system, covering ingestion, indexing, retrieval, ranking, and serving layers.

## Canonical Pipeline

```
Query Input
    ↓
Query Understanding (normalization, intent, segmentation)
    ↓
Retrieval (BM25 / ANN / Hybrid)
    ↓
First-Stage Ranking (fast scoring)
    ↓
Reranking (cross-encoder / LTR model)
    ↓
Post-processing (dedup, diversity, personalization)
    ↓
Results Served
```

## Ingestion Side

```
Raw Content
    ↓
Parsing / Normalization
    ↓
Chunking (if needed)
    ↓
Embedding (if dense)
    ↓
Index (inverted / ANN / both)
```

## Key Design Decisions

| Decision | Options |
|---|---|
| Retrieval strategy | BM25, dense, hybrid, sparse |
| Index type | Inverted, HNSW, IVF, Flat |
| Reranker | Cross-encoder, ColBERT, LLM-based |
| Fusion | RRF, linear combination, learned |
| Personalization | User embeddings, contextual signals |

## Latency Budget

Multi-stage pipelines must budget latency across stages:
- Retrieval: ~50ms
- Reranking (top 100): ~50–100ms
- Total P99: <200ms for most UX

## Industry Implementations

- **Canva**: two-phase search pipeline (Part I: retrieval, Part II: ranking)
- **Carousell**: migrated from keyword to dense vector with Elasticsearch
- **Slack**: full-text + entity-aware search at scale
- **Netflix**: federated graph-based search (distinct from [[Federated Search]] over multiple collections) — see [[Knowledge Graph Search]]

- **Uber Eats**: geosharding (H3 hex grid), document layout optimization (60% latency cut), ETD range indexing — see [[Optimizing Search at Uber Eats]]
- **Zalando**: layered architecture (Base Search → NER → Catalog API → Search API); self-DoS via facet aggregation — see [[The Day Our Own Queries DoSed Us - Zalando Search]]

## Related Concepts

- [[Retrieval Pipeline]]
- [[BM25]]
- [[Dense Vector Retrieval]]
- [[Hybrid Search]]
- [[Learning to Rank]]
- [[Reciprocal Rank Fusion]]
- [[Query Understanding]]
- [[Knowledge Graph Search]]

- [[Netflix Elasticsearch Indexing Strategy in AMP]]
- [[Twitter Search Stability and Scalability]]
- [[Thoughts about Managing Search Teams]]
- [[Search Product Management - The Most Misunderstood Role]]
