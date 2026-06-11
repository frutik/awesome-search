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
  - "[[Reranking]]"
  - "[[Cross-Encoder]]"
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

PostgreSQL has evolved into a surprisingly capable search platform (2026). Within a single datastore you can implement [[Full-Text Search]], [[Dense Vector Retrieval|vector search]], [[Hybrid Search]], [[Reciprocal Rank Fusion]] (RRF), [[Semantic Search|semantic retrieval]], and [[Cross-Encoder|cross-encoder]] [[Reranking]].

It still differs from dedicated engines like [[Elasticsearch]] / [[OpenSearch]] in faceting, typo tolerance, analyzers, merchandising, and relevance tooling — see [[#Weaknesses Compared to Elasticsearch and OpenSearch]].

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

**Limitation — not [[BM25]]:** `ts_rank` scores using local term statistics and does **not** implement the global corpus-based relevance model of Elasticsearch/OpenSearch. Often fine for simple apps; usually insufficient for sophisticated e-commerce relevance.

---

## 2. Vector Search with pgvector

[[pgvector]] is the standard vector-search extension for PostgreSQL.

```sql
ALTER TABLE products ADD COLUMN embedding vector(1536);

CREATE INDEX products_embedding_hnsw
ON products USING hnsw (embedding vector_cosine_ops);

SELECT * FROM products
ORDER BY embedding <=> :query_embedding
LIMIT 20;
```

**Index types:**

- **[[HNSW]]** — recommended default. High recall, excellent latency. Builds incrementally as rows are inserted, so it needs no upfront clustering step and works even on an initially empty table.
- **[[IVF|IVFFlat]]** — smaller indexes, faster builds, lower recall. Requires a one-time **k-means clustering pass at `CREATE INDEX`** (computing the `lists` cell centroids) over the rows already in the table — so you must **load data before building the index**, and **REINDEX** if the data distribution later shifts. This "training" is unsupervised clustering, not model training.

**Newer pgvector features:** HNSW, IVFFlat, cosine / L2 / inner-product distance, `halfvec`, `sparsevec`, binary vector indexing (see [[Binary Quantization]]).

---

## 3. Hybrid Search

[[Hybrid Search]] combines lexical and semantic retrieval:

```text
Query
  ├── Full-text search ─┐
  └── Vector search ────┤
                        ▼
                 Candidate Sets
                        ▼
                   Fusion Layer
                        ▼
                     Results
```

---

## 4. Reciprocal Rank Fusion (RRF)

The most common fusion technique. [[Reciprocal Rank Fusion|RRF]] scores by `1 / (k + rank)`, typically `k = 60`.

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

PostgreSQL's native FTS does not provide [[BM25]]. Several extensions add it:

- **[[ParadeDB]]** (`pg_search`) — BM25 + hybrid + faceting, on a Tantivy/Lucene-style engine.
- **[[psql_bm25s]]** — BM25 as a native, WAL-logged Postgres index access method (Apache-2.0, Intelligent-Internet); transactional, replication-safe, with field-aware retrieval and BM25/vector late-fusion. Benchmarks ~4× the Python `bm25s` library on BEIR and compares against pg_search and vchord_bm25.
- **vchord_bm25** — another Postgres BM25 extension (used as a benchmark baseline).

**What overlaps vs. what's distinctive:** all three provide BM25 ranking; ParadeDB and [[psql_bm25s]] both also do BM25/vector hybrid. Where ParadeDB stands apart is **scope** — it aims to be a full Elasticsearch replacement, adding **faceting and search aggregations** on top of search, not just a BM25 scorer. psql_bm25s focuses on being a native, replication-safe BM25 index (with field-aware retrieval, late-fusion, highlighting); vchord_bm25 focuses on BM25 ranking alongside the VectorChord vector stack.

```text
ParadeDB BM25  +  pgvector  +  RRF
```

For relevance behavior close to Elasticsearch/OpenSearch — including faceting/aggregations — ParadeDB is the closest fit; for a lean BM25 index inside Postgres, psql_bm25s is lighter-weight.

---

## 6. Reranking

```text
Stage 1: retrieve 100–300 candidates
Stage 2: apply reranker
Stage 3: return top 10–20 results
```

Typical pipeline: BM25 + Vector Search → [[Reciprocal Rank Fusion|RRF]] → top 100 → [[Cross-Encoder]] → top results.

**Common rerankers:**
- Open-source: BGE Reranker, Qwen Reranker, [[MonoT5]], [[Cross-Encoder]] models
- Hosted APIs: [[Cohere]] Rerank, [[Voyage AI]] Rerank
- LLM-based: GPT, Claude (expensive; only for small candidate sets — cf. [[LLM as Judge]])

---

## 7. Business Ranking Signals

Production systems blend retrieval scores with business signals (cf. [[Results Boosting]], [[Signal Downboosting]]):

```text
Final Score = Retrieval + Popularity + CTR + Conversion + Margin + Freshness + Inventory
```

```sql
final_score = retrieval_score * 0.7 + popularity_score * 0.2 + freshness_score * 0.1
```

---

## 8. Recommended Architectures

| Use case | Stack |
|---|---|
| **Small RAG / docs / KB** | PostgreSQL FTS + [[pgvector]] |
| **Medium product catalog** | [[ParadeDB]] BM25 + [[pgvector]] + RRF |
| **Large-scale e-commerce** | [[OpenSearch]] / [[Elasticsearch]] + vector + RRF + [[Cross-Encoder]] |

The large-scale engines remain preferable when you need advanced faceting, typo tolerance, query rules, merchandising, relevance tooling, and search analytics.

---

## Strengths of PostgreSQL Search

Single datastore · simpler infrastructure · mature SQL ecosystem · strong transactional guarantees · good vector support · hybrid search · RRF via SQL.

## Weaknesses Compared to Elasticsearch and OpenSearch

Weaker typo tolerance · fewer analyzers · less mature faceting, search analytics, and relevance tooling · fewer merchandising features · limited explainability.

---

## Recommendation

A practical modern PostgreSQL search stack:

```text
Lexical:    PostgreSQL FTS or ParadeDB BM25
Semantic:   pgvector (HNSW)
Fusion:     Reciprocal Rank Fusion (RRF)
Reranking:  BGE / Qwen / Cohere / Voyage
Business:   Popularity + Freshness + Inventory
```

For many product catalogs and internal search systems this is sufficient and can eliminate the need for a separate search cluster.

## Related Notes

- [[Search Platforms]] — where PostgreSQL fits among search engines
- [[Elasticsearch vs OpenSearch]] — the dedicated-engine alternative
- [[PostgreSQL]] · [[pgvector]] · [[ParadeDB]] · [[psql_bm25s]] — the tools
- [[Hybrid Search]] · [[Reciprocal Rank Fusion]] · [[Full-Text Search]] · [[Reranking]]
