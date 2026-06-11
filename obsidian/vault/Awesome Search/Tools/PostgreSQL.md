---
type: tool
title: "PostgreSQL"
aliases: ["PostgreSQL", "Postgres"]
website: "https://www.postgresql.org/"
repo: "https://github.com/postgres/postgres"
tags:
  - tool
  - database
  - search-engine
  - full-text-search
  - open-source
---

# PostgreSQL

Open-source relational database that doubles as a capable search platform. Native [[Full-Text Search]] (`tsvector`/`tsquery`, GIN indexes, `ts_rank`) plus extensions for [[Dense Vector Retrieval|vector search]] ([[pgvector]]) and [[BM25]] ([[ParadeDB]]) let teams run [[Hybrid Search]] and [[Reciprocal Rank Fusion|RRF]] inside a single datastore.

- Website: https://www.postgresql.org/

## Search capabilities

- **Native FTS** — `tsvector`, `tsquery`, `websearch_to_tsquery`, GIN indexes, `ts_rank`/`ts_rank_cd`. Stemming and language analyzers; phrase & boolean queries. Ranking is local term-statistics based, **not [[BM25]]**.
- **Vector search** — via [[pgvector]] (HNSW / IVFFlat).
- **BM25 + faceting** — via [[ParadeDB]] (`pg_search`) or [[psql_bm25s]] (native BM25 index access method).
- **Hybrid + RRF** — composable in SQL.

## Strengths vs. dedicated engines

Single datastore, simpler infra, mature SQL ecosystem, strong transactional guarantees. Weaker on typo tolerance, analyzers, faceting, merchandising, search analytics, and explainability than [[Elasticsearch]] / [[OpenSearch]].

## Related

- [[Search using PostgreSQL]] — the full topic
- [[pgvector]] · [[ParadeDB]] · [[psql_bm25s]] — search extensions
- [[Full-Text Search]] · [[Hybrid Search]] · [[Reciprocal Rank Fusion]] · [[BM25]]
- [[Search Platforms]] · [[Elasticsearch vs OpenSearch]]
