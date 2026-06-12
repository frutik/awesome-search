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

Two tasks are **not** part of core PostgreSQL search: **embedding inference** and **neural reranking** (cross-encoder / LLM). In practice these usually run outside the database — though PostgreSQL can *orchestrate* external inference from SQL, and PL/Python can run model code in-process. See [[#What runs outside PostgreSQL]].

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

**Advantages:** no extra infrastructure, fast GIN indexes, language-specific text search configurations (dictionaries and stemmers), phrase and boolean queries, and `ts_headline` for native result snippet highlighting.

**Terminology note (Postgres vs. the wider search world):** what Lucene-based engines ([[Elasticsearch]] / [[OpenSearch]]) call an **analyzer** — one pipeline doing char-filtering → tokenization → token filters (lowercase, stemming, stopwords, synonyms) — PostgreSQL splits into separately named objects:

| Lucene/ES term                                                 | PostgreSQL equivalent                                                                                                                                 |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tokenizer                                                      | **parser** — splits text into tokens and labels each token's *type* (`asciiword`, `word`, `numword`, `email`, `url`, …); default `pg_catalog.default` |
| Token filters (stemming, stopwords, synonyms, thesaurus)       | **dictionaries** — normalize a token into a *lexeme* or drop it; types include `snowball` (stemmer), `simple`, `synonym`, `thesaurus`, `ispell`       |
| Stemmer                                                        | the **Snowball dictionary** inside a configuration                                                                                                    |
| **Analyzer** (the whole pipeline, e.g. the "english" analyzer) | **text search configuration** — the named bundle mapping each token type → an ordered dictionary chain; e.g. `to_tsvector('english', …)`              |

So Postgres has no object literally called an "analyzer"; the closest single analog is a **text search configuration**, which is itself composed of a parser plus dictionaries (including the stemmer). This article uses the Postgres terms.

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

- **[[HNSW]]** — often the stronger pgvector choice when you want a better speed–recall trade-off than IVFFlat, at the cost of slower builds and higher memory use. Builds incrementally as rows are inserted, so it needs no upfront clustering step and works even on an initially empty table.
- **[[IVF|IVFFlat]]** — smaller indexes, faster builds, lower recall. Builds via a one-time **k-means clustering pass at `CREATE INDEX`** (computing the `lists` cell centroids) over the rows already in the table, so index quality depends on clustering quality and on the amount/shape of data present when the index is built — **load representative data before building**, and a rebuild may be advisable if the corpus changes substantially. This "training" is unsupervised clustering, not model training.

**Distance/types:** cosine / L2 / inner-product operators; `halfvec`, `sparsevec`, binary vector indexing (see [[Binary Quantization]]).

**Scale-up options:** for higher throughput or larger corpora, [[pgvectorscale]] and [[VectorChord]] are drop-in replacements/complements that add faster index types (DiskANN-style, RaBitQ quantization) on top of the same SQL interface.

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
    ORDER BY ts_rank(search_vector, q) DESC
    LIMIT 100
),
semantic AS (
    SELECT id,
        row_number() OVER (ORDER BY embedding <=> :query_embedding) AS rank
    FROM products
    ORDER BY embedding <=> :query_embedding
    LIMIT 100
),
rrf AS (
    SELECT id, 1.0 / (60 + rank) AS score FROM lexical
    UNION ALL
    SELECT id, 1.0 / (60 + rank) AS score FROM semantic
)
SELECT p.*, SUM(rrf.score) AS hybrid_score
FROM rrf JOIN products p USING (id)
GROUP BY p.id  -- id should be a PRIMARY KEY
ORDER BY hybrid_score DESC
LIMIT 20;
```

**Why RRF:** lexical and vector scores live on different, query-dependent scales (BM25 is unbounded and grows with query length; cosine distance sits in [0, 2]), so naive weighted addition lets whichever leg produces larger numbers dominate. RRF fuses **ranks, not scores**, making it invariant to each leg's scale — no normalization, no calibration. The trade-off: ranks discard score *magnitudes* (a runaway top hit and a marginal one are both just "rank 1"), so tuned normalized fusion — per-leg min-max/z-score normalization plus weights fitted on relevance judgments — can outperform RRF, but it requires labeled data and an offline eval loop that most teams don't have on day one. RRF's single parameter `k` controls how steeply contribution decays with rank; `k = 60` — from Cormack, Clarke, and Büttcher (SIGIR 2009) — is the standard default, chosen because RRF is famously insensitive to the exact value. At `k = 60` adjacent ranks contribute almost equally, so RRF behaves as a cross-list consensus signal rather than "trust each leg's #1". Widely adopted: Elasticsearch, OpenSearch, Azure AI Search, and most modern retrieval pipelines ship it as the hybrid default.

---

## 5. BM25 Inside PostgreSQL — ParadeDB / pg_textsearch / psql_bm25s / vchord_bm25

PostgreSQL's native FTS does not provide [[BM25]]. Several extensions add it (and are queried in SQL):

- **[[ParadeDB]]** (`pg_search`) — BM25 + hybrid + faceting, on a Tantivy/Lucene-style engine.
- **[[pg_textsearch]]** ([[Tiger Data]] / formerly Timescale) — BM25 as a native index access method (`CREATE INDEX … USING bm25`), queried via a pgvector-style distance operator (`ORDER BY content <@> 'search terms' LIMIT k`), with [[Block-Max WAND]] top-k, parallel index builds, partitioned-table support, expression/partial indexes, and hybrid pairing with [[pgvector]] / [[pgvectorscale]]. Open-sourced in late 2025, past v1.0 and self-declared production-ready (v1.4.0-dev), young relative to ParadeDB. One operational caveat: requires `shared_preload_libraries`, which limits availability on managed Postgres (RDS, Cloud SQL, Supabase) until providers add support.
- **[[psql_bm25s]]** — BM25 as a native, WAL-logged Postgres index access method (Apache-2.0, Intelligent-Internet); transactional, replication-safe, with field-aware retrieval and BM25/vector late-fusion. Its repository reports a median **~3.97× QPS** advantage over the Python `bm25s` reference on its own PG18 15-dataset BEIR benchmark matrix (self-reported, workload-dependent), and also compares against pg_search and vchord_bm25.
- **vchord_bm25** — another Postgres BM25 extension (used as a benchmark baseline).

**What overlaps vs. what's distinctive:** all four provide BM25 ranking; ParadeDB, [[pg_textsearch]], and [[psql_bm25s]] all support BM25/vector hybrid. Where ParadeDB stands apart is **scope** — it aims to be a full Elasticsearch replacement, adding **faceting and search aggregations** on top of search, not just a BM25 scorer. [[pg_textsearch]] and psql_bm25s both take the opposite bet — a lean, native Postgres index access method rather than an embedded search engine — differing mainly in license and feature focus (psql_bm25s: field-aware retrieval, late-fusion, highlighting; pg_textsearch: [[Block-Max WAND]] performance and a pgvector-style operator interface). vchord_bm25 focuses on BM25 ranking alongside the [[VectorChord]] vector stack.

**Licensing** (decision-critical for commercial/enterprise use), from most to least permissive: **pg_textsearch** is **PostgreSQL-licensed** (the same license as Postgres itself — use it anywhere, for anything), [[psql_bm25s]] is **Apache-2.0**, vchord_bm25 is **dual-licensed under AGPLv3 or ELv2**, and [[ParadeDB]] is **AGPL-3.0 / commercial**. Note the trade-off runs roughly opposite to feature scope — the most permissive licenses currently sit on the leanest/youngest extensions.

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

If you want to keep search entirely inside PostgreSQL and avoid running a separate search cluster, the following combinations work well in practice:

**Small RAG, Documentation, and Knowledge Bases**
Stack: PostgreSQL Full-Text Search + [[pgvector]]

For smaller document collections, PostgreSQL's built-in Full-Text Search provides strong lexical retrieval, while pgvector adds semantic search capabilities. This combination is often sufficient for internal documentation, knowledge bases, and lightweight RAG applications.

**Medium-Sized Product Catalogs**
Stack: [[ParadeDB]] or pg_textsearch or [[psql_bm25s]] BM25 + [[pgvector]] + RRF

For e-commerce catalogs and larger search workloads, BM25-based retrieval typically provides better lexical ranking than PostgreSQL's native Full-Text Search. Combining BM25 retrieval with vector search and merging the results using RRF often delivers significantly better relevance than either approach alone.

**Large-Scale Search Systems**
Stack: Consider [[OpenSearch]] or [[Elasticsearch]]

While PostgreSQL can handle surprisingly large workloads, dedicated search engines become attractive when dealing with tens of millions of documents, very high query volumes, advanced search features, or teams that require independent scaling of search infrastructure.

---

## Strengths of PostgreSQL Search

Single datastore · simpler infrastructure · mature SQL ecosystem · strong transactional guarantees · good vector support · hybrid search · RRF and business-signal scoring expressed directly in SQL.

## Weaknesses compared to Elasticsearch and OpenSearch

Weaker typo tolerance · fewer analyzers · less mature faceting, search analytics, and relevance tooling · fewer merchandising features · limited explainability.

**Mitigations worth knowing:** typo tolerance can be partially addressed with [[pg_trgm]] (trigram similarity indexes, `similarity()` / `word_similarity()`) plus `unaccent` for accent-insensitive matching — not as seamless as Elasticsearch's built-in fuzziness, but often sufficient. Faceting is possible as plain `GROUP BY` queries — doable, but slower and more verbose than a dedicated faceting engine.

---

## What runs outside PostgreSQL

These steps are part of a realistic search pipeline but are **not SQL** — they are external model inference (or a different engine). Postgres consumes their *output*:

- **Embedding generation** — turning text/images into vectors is **model inference, not SQL**. The resulting vector is stored in a `vector` column or passed into the query. Three patterns:
  - **App layer** (most common) — generate embeddings in your service and `INSERT` them.
  - **PL/Python / `pgsql-http` / `pg_vectorize` calling an inference endpoint** — the *function* runs in Postgres; the inference runs in a model server **outside the DB process**, which can be **co-located on the same infrastructure** (a localhost sidecar, or an internal service like TEI / Ollama / vLLM / Triton in the same VPC/cluster) — not necessarily a third-party API. Often the best production pattern: the model is loaded once on dedicated/GPU hardware and shared across all backends (no per-connection load), while data and latency stay in-house. Orchestration is in SQL even though the math isn't.
  - **PL/Python with a local model in-process** (`plpython3u` + sentence-transformers) — inference genuinely runs **inside the Postgres backend process**, so it *is* technically doable in a function. Rarely used in production: the model loads per backend connection (heavy memory), runs CPU-bound in the DB process, needs torch + weights installed server-side, and `plpython3u` is an untrusted superuser-only language that most managed Postgres (RDS, Cloud SQL, Supabase) disallow.
  
  Either way the *embedding math* is Python/model code, not the relational engine — which is why this sits on the boundary rather than in the SQL body above.
- **Reranking** — [[Reranking|cross-encoder]] ([[Cross-Encoder]], [[MonoT5]], BGE/Qwen rerankers) and [[LLM as Judge|LLM]] rerankers run in an external model/API. A typical pipeline retrieves + fuses in Postgres (§3–§4), then sends the top ~100 to an external reranker. Hosted options: [[Cohere]] Rerank, [[Voyage AI]] Rerank.
- **Large-scale dedicated engines** — advanced faceting, typo tolerance, query rules, merchandising, and search analytics live in [[Elasticsearch]] / [[OpenSearch]], not Postgres.

---

## Related Notes

- [[Search Platforms]] — where PostgreSQL fits among search engines
- [[Elasticsearch vs OpenSearch]] — the dedicated-engine alternative
- [[PostgreSQL]] · [[pgvector]] · [[ParadeDB]] · [[psql_bm25s]] · [[pg_textsearch]] — the tools
- [[Hybrid Search]] · [[Reciprocal Rank Fusion]] · [[Full-Text Search]] · [[BM25]]
- External steps: [[Reranking]] · [[Cross-Encoder]]
