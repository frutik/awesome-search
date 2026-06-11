---
type: tool
title: "ParadeDB"
aliases: ["ParadeDB", "pg_search"]
website: "https://www.paradedb.com/"
repo: "https://github.com/paradedb/paradedb"
tags:
  - tool
  - search-engine
  - postgresql
  - bm25
  - full-text-search
  - open-source
---

# ParadeDB

Open-source [[PostgreSQL]] extension (and distribution) that brings Elasticsearch-style search to Postgres — most notably **[[BM25]] ranking**, which native Postgres [[Full-Text Search]] lacks.

- Website: https://www.paradedb.com/
- GitHub: https://github.com/paradedb/paradedb

## What it adds

- **BM25 ranking** — proper global corpus-based relevance (vs. `ts_rank`'s local term statistics)
- **Hybrid search** — BM25 + vector ([[pgvector]]) combined, fused via [[Reciprocal Rank Fusion|RRF]]
- **Faceting** and **search aggregations**
- **Search-oriented indexes** (built on a Tantivy/Lucene-style engine)

```text
ParadeDB BM25  +  pgvector  +  RRF   →  relevance close to Elasticsearch/OpenSearch
```

## Role

The lexical/BM25 leg of a PostgreSQL search stack for product catalogs and e-commerce, where native FTS ranking is insufficient.

## Related

- [[Search using PostgreSQL]] · [[PostgreSQL]] · [[pgvector]]
- [[BM25]] · [[Full-Text Search]] · [[Hybrid Search]] · [[Reciprocal Rank Fusion]]
- Compare: [[Elasticsearch]] · [[OpenSearch]]
