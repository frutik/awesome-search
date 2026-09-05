---
title: Manticore Search
type: tool
aliases: ["Manticore", "Manticore Search", "manticoresearch"]
tags:
  - tool
  - search-engine
  - full-text-search
  - vector-search
  - hybrid-search
  - open-source
website: https://manticoresearch.com/
repo: https://github.com/manticoresoftware/manticoresearch
created: 2026-09-05
---

# Manticore Search

Open-source C++ search database combining [[Full-Text Search|full-text]], vector and [[Hybrid Search|hybrid]] retrieval behind a SQL-first interface. Created in 2017 as a continuation of **Sphinx Search** — described by its maintainers as "a nearly complete rewrite of its predecessor" — it is the one engine in this vault from the Sphinx lineage rather than the Lucene one.

- Website: https://manticoresearch.com/
- Manual: https://manual.manticoresearch.com/
- GitHub: https://github.com/manticoresoftware/manticoresearch

Licensed GPL-3.0, which is a stricter constraint than [[Solr]]'s Apache-2.0 and worth checking before embedding it in a commercial product.

---

## The Distinguishing Choice: SQL as the Native Syntax

Manticore is **SQL-first and MySQL-compatible**, using SQL as the native query syntax, with an HTTP JSON API alongside it. That is the architectural fact that separates it from everything else in this section: [[Elasticsearch]] and [[OpenSearch]] expose a bespoke query DSL over HTTP and [[Solr]] its own Lucene/eDisMax query syntax, and the Postgres extensions ([[ParadeDB]], [[VectorChord]], [[pgvector]]) reach SQL by living *inside* a general-purpose RDBMS. Manticore is a purpose-built search engine that happens to speak SQL, which is a third position.

It also supports JOINs across tables, real-time inserts, and transactions — features usually surrendered when moving search out of the database.

## Full-Text

Over 20 full-text operators and over 20 ranking factors with custom ranking expressions, plus the standard analysis chain: stemming, lemmatization, [[Stopwords|stopwords]], [[Synonyms|synonyms]], highlighting, fuzzy search and query [[Autocomplete|autocomplete]].

## Vector Search

[[HNSW]], supplied by the Manticore Columnar Library. Index-time settings are `knn_type` (only `hnsw` today), `knn_dims`, and `hnsw_similarity` — `L2`, `IP` or `COSINE`, with vectors normalized on insertion under cosine. Graph construction is tuned by `hnsw_m` (default 16) and `hnsw_ef_construction` (default 200).

Query time exposes `ef` (default 10) plus a set of accuracy/latency knobs that are unusually explicit for an engine of this size: `oversampling` (default 3.0) widens the candidate pool, `rescore` recomputes distances against full-precision vectors and is on by default, `early_termination` stops graph traversal adaptively, and `prefilter` chooses whether filters apply during or after traversal — the [[Vector Filtering|pre- vs post-filter]] decision, made configurable rather than fixed.

[[Vector Quantization|Quantization]] comes in three forms: `8bit` [[Scalar Quantization|scalar]], `1bit` [[Binary Quantization|binary]] using asymmetric 4-bit queries against 1-bit storage, and a faster, less accurate `1bitsimple`.

## Hybrid

Full-text and vector retrieval combine in a single query rather than through two calls and a fusion step — in SQL, a `knn()` predicate alongside `match()`; in JSON, a `knn` object beside a `query` object. Contrast [[ParadeDB]], where [[Hybrid Search|hybrid]] means BM25 and [[pgvector]] fused externally via [[Reciprocal Rank Fusion|RRF]].

## Storage and Distribution

Row-wise, columnar and docstore layouts for different access patterns; automatic secondary indexes built on a Piecewise Geometric Model (PGM) index; [[Sharding|sharded tables]] for distributed reads and writes; and virtually-synchronous multi-master replication built on Galera, with load balancing.

## On the Benchmark Claims

The project publishes head-to-head figures against Elasticsearch — 3.85× on 100M+ Hacker News comments, 5.03× on DevOps queries over 10M Nginx logs, and a large ingestion gap in both CPU and RAM. These are **the project's own numbers on workloads it selected**, with the tuning applied to the Elasticsearch baseline unspecified, and no independent replication located. Treat them as a claim to verify on your own corpus, not as a measured comparison — the standard caution in [[Retrieval Benchmarks and Leaderboards]] applies with extra force to vendor self-reporting.

## Related

- Compare: [[Elasticsearch]] · [[OpenSearch]] · [[Solr]] — the Lucene family it positions against
- Compare: [[ParadeDB]] · [[VectorChord]] — the other route to SQL-accessible search
- [[Full-Text Search]] · [[BM25]] · [[Hybrid Search]] · [[HNSW]] · [[Approximate Nearest Neighbor Search]]
- [[Vector Quantization]] · [[Binary Quantization]] · [[Scalar Quantization]] · [[Vector Filtering]]
- [[Search Platforms]] · [[Migration between Search Engines]] · [[Vector Search Tradeoffs]]
