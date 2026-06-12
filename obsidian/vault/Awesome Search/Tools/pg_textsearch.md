---
type: tool
title: "pg_textsearch"
aliases: ["pg_textsearch", "pg textsearch"]
website: "https://www.tigerdata.com/"
repo: "https://github.com/timescale/pg_textsearch"
tags:
  - tool
  - postgresql
  - bm25
  - full-text-search
  - open-source
created: 2026-06-12
---

# pg_textsearch

[[BM25]] extension for [[PostgreSQL]] by [[Tiger Data]] (formerly Timescale). Implements BM25 as a native index access method — same architectural approach as [[psql_bm25s]], but with a pgvector-style operator interface and [[Block-Max WAND]] top-k optimization.

- GitHub: https://github.com/timescale/pg_textsearch
- License: **PostgreSQL license** — most permissive in the Postgres BM25 ecosystem; use anywhere, for anything.

## Key features

- `CREATE INDEX … USING bm25` — native index access method
- Query via distance-style operator: `ORDER BY content <@> 'search terms' LIMIT k`
- **[[Block-Max WAND]]** top-k pruning for fast retrieval
- Parallel index builds
- Partitioned-table support and expression/partial indexes
- Hybrid pairing with [[pgvector]] and pgvectorscale

## Maturity

Open-sourced late 2025. As of June 2026: past v1.0, self-declared production-ready (v1.4.0-dev), ~1,800 GitHub stars within weeks of release. Young relative to [[ParadeDB]] but no longer a preview.

**Operational caveat:** requires `shared_preload_libraries`, which limits availability on managed Postgres (RDS, Cloud SQL, Supabase) until providers add support.

## Related

- [[PostgreSQL]] · [[BM25]] · [[Block-Max WAND]] · [[pgvector]]
- [[ParadeDB]] · [[psql_bm25s]] · vchord_bm25 — other Postgres BM25 extensions; see [[Search using PostgreSQL]]
- [[Tiger Data]] — author/maintainer
