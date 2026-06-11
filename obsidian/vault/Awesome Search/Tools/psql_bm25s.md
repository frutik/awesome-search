---
type: tool
title: "psql_bm25s"
aliases: ["psql_bm25s", "psql bm25s"]
website: "https://github.com/Intelligent-Internet/psql_bm25s"
repo: "https://github.com/Intelligent-Internet/psql_bm25s"
tags:
  - tool
  - postgresql
  - bm25
  - full-text-search
  - open-source
---

# psql_bm25s

[[PostgreSQL]] extension implementing [[BM25]]-family lexical retrieval as a **native index access method**. Inspired by the Python `bm25s` library, but reimplemented as a real Postgres index (not a port) so it gains index persistence inside the database, transactional writes, crash recovery, physical replication, planner-visible SQL access, and maintenance under row churn. Maintained by the **Intelligent-Internet** org; Apache-2.0.

- GitHub: https://github.com/Intelligent-Internet/psql_bm25s
- Releases: https://github.com/Intelligent-Internet/psql_bm25s/releases
- Docker: `ghcr.io/intelligent-internet/psql_bm25s:pg18`
- Docs: `/docs` (architecture, API, performance, hybrid search, maintenance)

## What it does

- **True BM25 ranking** in Postgres (vs. native FTS `ts_rank`, which is *not* BM25 — see [[Full-Text Search]]).
- **Index types / columns**: `text`, `varchar`, `text[]`, `varchar[]`, `int4[]`; WAL-logged native index pages; full physical-replication compatibility.
- **Maintenance**: mutable index handling INSERT/UPDATE/DELETE with three consistency modes — realtime, eventual, manual.
- **Query interfaces**: `psql_bm25s_query_ids()` / `psql_bm25s_query_tokens()` canonical APIs; `@@` (match) and `<=>` (BM25 ordering) operators; `psql_bm25s_query()` / `psql_bm25s_query_prepared()` helpers.
- **Text processing**: tokenization, normalization, optional stopwords, English stemming, Latin-diacritic folding.
- **Advanced**: multicolumn fusion indexes, field-aware retrieval with query-time weights, **hybrid BM25/vector late-fusion** (pairs with [[pgvector]]), token highlighting/snippeting.

```sql
CREATE EXTENSION psql_bm25s;
CREATE INDEX docs_bm25_idx ON docs USING psql_bm25s (body);
SELECT * FROM psql_bm25s_query('docs_bm25_idx'::regclass, 'search query', 5);
```

## Performance claims

On the BEIR suite (15 datasets): median **~3.97× QPS** vs. Python `bm25s` for IDs retrieval (~3.93× for `text[]`); faster on 12/15 (IDs) and 11/15 (`text[]`) datasets. On `msmarco` (8.8M docs): **96.67 QPS vs. 1.61** for the Python reference. The repo's `docs/performance` also compares against [[ParadeDB|pg_search]] and `vchord_bm25` (the two other Postgres BM25 extensions).

## Where it fits

An alternative to [[ParadeDB]] (`pg_search`) for adding [[BM25]] to a [[Search using PostgreSQL|PostgreSQL search stack]] — pair with [[pgvector]] for [[Hybrid Search]] fused via [[Reciprocal Rank Fusion|RRF]].

## Related

- [[Search using PostgreSQL]] · [[PostgreSQL]] · [[pgvector]] · [[ParadeDB]]
- [[BM25]] · [[Full-Text Search]] · [[Hybrid Search]] · [[Reciprocal Rank Fusion]]
- Compare: [[ParadeDB]] (pg_search), vchord_bm25, Elasticsearch/OpenSearch BM25
