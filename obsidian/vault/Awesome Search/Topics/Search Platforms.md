---
type: topic
aliases:
  - search engine
  - search backend
  - search infrastructure
  - vector database
  - search platform
tags:
  - topic
  - search-platforms
  - elasticsearch
  - solr
  - vespa
  - qdrant
  - weaviate
  - algolia
  - pinecone
  - opensearch
  - search-engine
related_concepts:
  - "[[Hybrid Search]]"
  - "[[BM25]]"
  - "[[Vector Search]]"
  - "[[Inverted Index]]"
  - "[[HNSW]]"
  - "[[Sparse Embeddings]]"
related_topics:
  - "[[E-commerce Search]]"
  - "[[Enterprise Search]]"
  - "[[Conversational and Agentic Search]]"
created: 2026-05-31
---

# Search Platforms

## Overview

A search platform is the engine that stores, indexes, and retrieves content at query time. Choosing a platform is one of the earliest and most consequential infrastructure decisions for a search team — it determines what retrieval methods are available, how much operational overhead the team carries, and what the cost structure looks like at scale.

Platforms split along two axes:

- **Open source vs. proprietary** — open-source engines give full control over the stack and data; proprietary SaaS solutions trade that control for faster onboarding, managed infrastructure, and vendor-provided relevance tooling.
- **Self-hosted vs. SaaS** — even open-source engines (e.g. Elasticsearch, OpenSearch) are available as managed cloud services; pure SaaS products (Algolia, Pinecone) are only available hosted.

## Lucene-Based

Engines built on Apache Lucene. Lucene provides a full-featured foundation: inverted index and BM25 for lexical retrieval, but also native support for vector fields (HNSW) and hybrid search. These engines are not limited to keyword search — they are increasingly used as unified retrieval backends.

- **[[Elasticsearch]]** — the dominant choice for production search; rich query DSL, extensive ecosystem. Available open-source (self-hosted) and as Elastic Cloud (SaaS).
- **Apache Solr** — the other major Lucene-based engine; older, more configuration-heavy, common in enterprise and media.
- **OpenSearch** — AWS-led fork of Elasticsearch (post-7.x licensing split); fully open-source, available managed on AWS.

## Vector / Semantic Search

Purpose-built for dense embedding retrieval. These engines index high-dimensional vectors (via HNSW or similar ANN structures) and return results by similarity rather than keyword overlap. Most support hybrid search combining keyword and vector scores.

- **[[Qdrant Vector DB]]** — open-source, Rust-based, strong filtering performance; available self-hosted and as Qdrant Cloud (SaaS).
- **[[Weaviate Vector DB]]** — open-source, GraphQL API, built-in vectorization modules; available self-hosted and as Weaviate Cloud (SaaS).
- **Pinecone** — proprietary SaaS-only vector database; no self-hosting option; known for operational simplicity.
- **Milvus / Zilliz** — open-source vector DB (Milvus) with a managed SaaS layer (Zilliz Cloud).
- **Chroma** — lightweight open-source vector store popular in RAG prototyping.

## Full-Featured / Hybrid Platforms

Engines designed from the ground up with relevance, hybrid retrieval, and production scale as first-class concerns.

- **Vespa** — open-source, self-hosted (or Vespa Cloud SaaS); uniquely combines BM25, dense vector, and structured attribute matching in a single engine with built-in ranking expressions. Strong choice for complex ranking pipelines. See [[From Elasticsearch to Vespa]].
- **Typesense** — open-source, self-hosted or Typesense Cloud; developer-friendly, fast, opinionated defaults; positioned as a simpler alternative to Elasticsearch for search-heavy apps.
- **Meilisearch** — open-source, self-hosted or Meilisearch Cloud; optimized for instant search UX, typo tolerance, and ease of setup.

## SaaS / Proprietary Platforms

Fully managed, proprietary offerings where the engine is not available for self-hosting.

- **Algolia** — the dominant SaaS search platform for product and site search; strong relevance-tuning UI, extensive front-end SDKs, high price point at scale.
- **Coveo** — enterprise SaaS search with ML-based ranking and personalization; targets large organizations.

## Specialized / Vertical Platforms

Some platforms are not general-purpose search engines but focus on a specific domain or problem layer, typically sitting on top of an underlying engine.

- **[[searchHub]]** ([[Andreas Wagner]]) — e-commerce-focused SaaS platform for search optimization and query understanding. Covers query rewriting, A/B testing, analytics, and spell correction (SmartQuery). Also released the Open Commerce Search Stack (OCSS) as an open-source reference implementation for retail search. See [[Three Pillars of Search Quality - Findability]] and [[Common Pitfalls of Onsite Search Experimentation]].
- **[[Hornet]]** ([[Jo Kristian Bergum]], [[Lester Solbakken]]) — retrieval infrastructure platform purpose-built for AI agents. Focuses on high-precision context delivery for agentic workloads, where query patterns differ fundamentally from human search (longer queries, web-search operators, multi-turn compounding). See [[This Is What Agentic Retrieval Looks Like]] and [[Mutually Assured Distraction]].
- **Empathy.co** — e-commerce search and discovery platform; SaaS, focused on search UX, analytics, and personalization.
- **Constructor.io** — SaaS product discovery platform for e-commerce; combines search, recommendations, and browse with ML-driven ranking.

## Database-Embedded Search (SQL)

Search run inside an existing database rather than a dedicated engine — increasingly viable for small-to-medium workloads, eliminating a separate search cluster.

- **[[PostgreSQL]]** — native [[Full-Text Search]] (`tsvector`, GIN, `ts_rank`), plus [[pgvector]] for vector search and [[ParadeDB]] for [[BM25]]; supports [[Hybrid Search]] + [[Reciprocal Rank Fusion|RRF]] in SQL. See [[Search using PostgreSQL]].

## Key Trade-offs When Choosing a Platform

| Dimension | Open Source / Self-Hosted | SaaS / Proprietary |
|---|---|---|
| Control | Full (data, config, infra) | Limited |
| Ops burden | High | Low |
| Cost at scale | Lower (infra only) | Higher (per-query or per-record pricing) |
| Vendor lock-in | None | High |
| Time to first result | Slower | Fast |

## Related Notes

- [[E-commerce Search]] — platform choice is a recurring theme in ecommerce search case studies
- [[Enterprise Search]] — enterprise teams frequently operate Elasticsearch or Vespa at scale
- [[Hybrid Search Blueprint Series Semantic Boosting]] — hybrid retrieval patterns that span Lucene and vector platforms
- [[From Elasticsearch to Vespa Rebuilding the Kleinanzeigen Homepage Feed — Part 1]] — real migration case study
- [[Conversational and Agentic Search]] — agentic workloads impose distinct retrieval requirements; Hornet is built specifically for this use case
- [[Search using PostgreSQL]] — running modern search inside Postgres (FTS + pgvector + ParadeDB + RRF)
