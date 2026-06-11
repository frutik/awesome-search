---
type: concept
title: "Full-Text Search"
aliases: ["full-text search", "FTS", "lexical search", "keyword search"]
tags:
  - concept
  - search
  - retrieval
  - lexical
---

# Full-Text Search

## Definition

Full-text search (FTS) retrieves documents by matching query terms against the words in a document, typically over an **inverted index**, and scores matches by term-frequency-based relevance. It is the lexical counterpart to [[Semantic Search]] / [[Dense Vector Retrieval]].

## Core machinery

- **Inverted index** — term → list of documents containing it
- **Analysis** — tokenization, stemming/lemmatization, stopword removal, language analyzers
- **Scoring** — term frequency × inverse document frequency; the dominant model is [[BM25]]

## Scoring is not always BM25

The relevance model matters. Dedicated engines ([[Elasticsearch]], [[OpenSearch]], built on Lucene) use **[[BM25]]** — a global, corpus-aware model. By contrast, [[PostgreSQL]]'s native FTS (`ts_rank`/`ts_rank_cd`) scores mainly on **local term statistics** and is *not* BM25 — adequate for simple search, often insufficient for e-commerce relevance. [[ParadeDB]] adds BM25 to Postgres to close that gap.

## Role in modern search

FTS is the lexical leg of [[Hybrid Search]], combined with vector retrieval and merged via [[Reciprocal Rank Fusion]]. Lexical and semantic retrieval have complementary failure modes — FTS nails exact terms, proper nouns, and codes; semantic handles paraphrase and intent.

## Related Concepts

- [[BM25]] — the standard FTS relevance model
- [[Hybrid Search]] — FTS + vector retrieval
- [[Semantic Search]] · [[Dense Vector Retrieval]] — the semantic counterpart
- [[Sparse Vector Retrieval]] · [[SPLADE]] — learned-sparse evolution of lexical search
- [[Query Understanding]] · [[Stopwords]] · [[Synonyms]] · [[Spelling Correction]] — analysis-stage concerns

## Topics

- [[Search using PostgreSQL]] · [[Search Platforms]]
