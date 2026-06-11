---
type: topic
title: "Search using PostgreSQL"
aliases: ["PostgreSQL search", "Postgres search", "search in Postgres", "Modern Search in PostgreSQL"]
related_concepts:
  - "[[Full-Text Search]]"
  - "[[BM25]]"
  - "[[Hybrid Search]]"
  - "[[Reciprocal Rank Fusion]]"
  - "[[Dense Vector Retrieval]]"
  - "[[HNSW]]"
related_topics:
  - "[[Search Platforms]]"
  - "[[E-commerce Search]]"
  - "[[Elasticsearch vs OpenSearch]]"
tags:
  - topic
  - postgresql
  - search-platforms
  - hybrid-search
  - vector-search
created: 2026-06-11
---

# Search using PostgreSQL

## Overview

PostgreSQL has evolved into a surprisingly capable search platform (2026). **Everything below runs inside PostgreSQL via SQL** — [[Full-Text Search]], [[Dense Vector Retrieval|vector search]] ([[pgvector]]), [[BM25]] (extensions), [[Hybrid Search]], [[Reciprocal Rank Fusion]] (RRF), and business-signal scoring.

Two things are **not** done in SQL and must happen outside Postgres: **generating embeddings** (model inference — you store/pass in the vector) and **cross-encoder / LLM reranking**. See [[#What runs outside PostgreSQL]].

It also still differs from dedicated engines like [[Elasticsearch]] / [[OpenSearch]] in faceting, typo tolerance, analyzers, merchandising, and relevance tooling — see [[#Weaknesses compared to Elasticsearch and OpenSearch]].

---

## 1. Native Full-Text Search

PostgreSQL ships built-in [[Full-Text Search]]: `tsvector`, `tsquery`, `websearch_to_tsquery`, GIN indexes, `ts_rank`, `ts_rank_cd`.

```sql
SELECT *
FROM products
WHERE search_vector @@ websearch_to_tsquery('english', 'wireless keyboard')
ORDER BY ts_rank(search_vector, websearch_to_tsquery('english', 'wireless keyboard')) DESC;
```

**Advantages:** no extra infrastructure, fast GIN indexes, stemming, language-specific analyzers, phrase and boolean queries.

**Limitation — not [[BM25]]:** `ts_rank` scores using local term statistics and does **not** implement the global corpus-based relevance model of Elasticsearch/OpenSearch. Often fine for simple apps; usually insufficient for sophisticated e-commerce relevance (use a BM25 extension — see §5).

---

## 2. Vector Search with pgvector

[[pgvector]] is the standard vector-search extension. The **similarity search and ANN index run in Postgres**; the query/document **embedding is generated outside** Postgres and passed in as `:query_embedding` (or written into the column). See [[#What runs outside PostgreSQL]].

```sql
ALTER TABLE products ADD COLUMN embedding vector(1536);

CREATE INDEX products_embedding_hnsw
ON products USING hnsw (embedding vector_cosine_ops);

SELECT * FROM products
ORDER BY embedding <=> :query_embedding   -- vector passed in, computed externally
LIMIT 20;
```

**Index types:**

- **[[HNSW]]** — recommended default. High recall, excellent latency. Builds incrementally as rows are inserted, so it needs no upfront clustering step and works even on an initially empty table.
- **[[IVF|IVFFlat]]** — smaller indexes, faster builds, lower recall. Requires a one-time **k-means clustering pass at `CREATE INDEX`** (computing the `lists` cell centroids) over the rows already in the table — so you must **load data before building the index**, and **REINDEX** if the data distribution later shifts. This "training" is unsupervised clustering, not model training.

**Distance/types:** cosine / L2 / inner-product operators; `halfvec`, `sparsevec`, binary vector indexing (see [[Binary Quantization]]).

---

## 3. Hybrid Search

[[Hybrid Search]] combines lexical and semantic retrieval — both legs and the fusion run in SQL:

```text
Query
  ├── Full-text search ─┐   (SQL: tsvector / BM25 extension)
  └── Vector search ────┤   (SQL: pgvector <=>)
                        ▼
                 Candidate Sets
                        ▼
                   Fusion Layer   (SQL: RRF — §4)
                        ▼
                     Results
```

---

## 4. Reciprocal Rank Fusion (RRF)

The most common fusion technique, and **pure SQL**. [[Reciprocal Rank Fusion|RRF]] scores by `1 / (k + rank)`, typically `k = 60`.

```sql
WITH lexical AS (
    SELECT id,
        row_number() OVER (ORDER BY ts_rank(search_vector, q) DESC) AS rank
    FROM products, websearch_to_tsquery('english', :query) q
    WHERE search_vector @@ q
    LIMIT 100
),
semantic AS (
    SELECT id,
        row_number() OVER (ORDER BY embedding <=> :query_embedding) AS rank
    FROM products
    LIMIT 100
),
rrf AS (
    SELECT id, 1.0 / (60 + rank) AS score FROM lexical
    UNION ALL
    SELECT id, 1.0 / (60 + rank) AS score FROM semantic
)
SELECT p.*, SUM(rrf.score) AS hybrid_score
FROM rrf JOIN products p USING (id)
GROUP BY p.id
ORDER BY hybrid_score DESC
LIMIT 20;
```

**Why RRF:** lexical and vector scores use different scales, so no normalization is needed; more robust than weighted score addition; widely adopted (Elasticsearch, OpenSearch, Azure AI Search, modern retrieval pipelines).

---

## 5. BM25 Inside PostgreSQL — ParadeDB / psql_bm25s / vchord_bm25

PostgreSQL's native FTS does not provide [[BM25]]. Several extensions add it (and are queried in SQL):

- **[[ParadeDB]]** (`pg_search`) — BM25 + hybrid + faceting, on a Tantivy/Lucene-style engine.
- **[[psql_bm25s]]** — BM25 as a native, WAL-logged Postgres index access method (Apache-2.0, Intelligent-Internet); transactional, replication-safe, with field-aware retrieval and BM25/vector late-fusion. Benchmarks ~4× the Python `bm25s` library on BEIR and compares against pg_search and vchord_bm25.
- **vchord_bm25** — another Postgres BM25 extension (used as a benchmark baseline).

**What overlaps vs. what's distinctive:** all three provide BM25 ranking; ParadeDB and [[psql_bm25s]] both also do BM25/vector hybrid. Where ParadeDB stands apart is **scope** — it aims to be a full Elasticsearch replacement, adding **faceting and search aggregations** on top of search, not just a BM25 scorer. psql_bm25s focuses on being a native, replication-safe BM25 index (with field-aware retrieval, late-fusion, highlighting); vchord_bm25 focuses on BM25 ranking alongside the VectorChord vector stack.

For relevance behavior close to Elasticsearch/OpenSearch — including faceting/aggregations — ParadeDB is the closest fit; for a lean BM25 index inside Postgres, psql_bm25s is lighter-weight.

---

## 6. Business Ranking Signals

Blending retrieval scores with business signals is **plain SQL arithmetic** over columns (cf. [[Results Boosting]], [[Signal Downboosting]]) — one of the things Postgres does most naturally, since the signals already live in your tables:

```sql
SELECT id,
         retrieval_score  * 0.7
       + popularity_score * 0.2
       + freshness_score  * 0.1   AS final_score
FROM ranked_candidates
ORDER BY final_score DESC
LIMIT 20;
```

Typical signals: popularity, CTR, conversion rate, margin, freshness, inventory availability.

---

## 7. Recommended PostgreSQL Architectures

In-Postgres stacks (no separate search cluster):

| Use case | Stack (all in Postgres) |
|---|---|
| **Small RAG / docs / KB** | PostgreSQL FTS + [[pgvector]] |
| **Medium product catalog** | [[ParadeDB]] / [[psql_bm25s]] BM25 + [[pgvector]] + RRF |

For **large-scale e-commerce** a dedicated engine ([[OpenSearch]] / [[Elasticsearch]] + vector + RRF + external reranking) is still preferable — but that moves outside Postgres; see [[#What runs outside PostgreSQL]].

---

## Strengths of PostgreSQL Search

Single datastore · simpler infrastructure · mature SQL ecosystem · strong transactional guarantees · good vector support · hybrid search · RRF and business-signal scoring expressed directly in SQL.

## Weaknesses compared to Elasticsearch and OpenSearch

Weaker typo tolerance · fewer analyzers · less mature faceting, search analytics, and relevance tooling · fewer merchandising features · limited explainability.

---

## What runs outside PostgreSQL

These steps are part of a realistic search pipeline but are **not SQL** — they are external model inference (or a different engine). Postgres consumes their *output*:

- **Embedding generation** — turning text/images into vectors is **model inference, not SQL**. The resulting vector is stored in a `vector` column or passed into the query. Three patterns:
  - **App layer** (most common) — generate embeddings in your service and `INSERT` them.
  - **PL/Python / `pgsql-http` / `pgai` / `pg_vectorize` calling an inference endpoint** — the *function* runs in Postgres; the inference runs in a model server **outside the DB process**, which can be **co-located on the same infrastructure** (a localhost sidecar, or an internal service like TEI / Ollama / vLLM / Triton in the same VPC/cluster) — not necessarily a third-party API. Often the best production pattern: the model is loaded once on dedicated/GPU hardware and shared across all backends (no per-connection load), while data and latency stay in-house. Orchestration is in SQL even though the math isn't.
  - **PL/Python with a local model in-process** (`plpython3u` + sentence-transformers) — inference genuinely runs **inside the Postgres backend process**, so it *is* technically doable in a function. Rarely used in production: the model loads per backend connection (heavy memory), runs CPU-bound in the DB process, needs torch + weights installed server-side, and `plpython3u` is an untrusted superuser-only language that most managed Postgres (RDS, Cloud SQL, Supabase) disallow.
  
  Either way the *embedding math* is Python/model code, not the relational engine — which is why this sits on the boundary rather than in the SQL body above.
- **Reranking** — [[Reranking|cross-encoder]] ([[Cross-Encoder]], [[MonoT5]], BGE/Qwen rerankers) and [[LLM as Judge|LLM]] rerankers run in an external model/API. A typical pipeline retrieves + fuses in Postgres (§3–§4), then sends the top ~100 to an external reranker. Hosted options: [[Cohere]] Rerank, [[Voyage AI]] Rerank.
- **Large-scale dedicated engines** — advanced faceting, typo tolerance, query rules, merchandising, and search analytics live in [[Elasticsearch]] / [[OpenSearch]], not Postgres.

---

## Related Notes

- [[Search Platforms]] — where PostgreSQL fits among search engines
- [[Elasticsearch vs OpenSearch]] — the dedicated-engine alternative
- [[PostgreSQL]] · [[pgvector]] · [[ParadeDB]] · [[psql_bm25s]] — the tools
- [[Hybrid Search]] · [[Reciprocal Rank Fusion]] · [[Full-Text Search]] · [[BM25]]
- External steps: [[Reranking]] · [[Cross-Encoder]]
