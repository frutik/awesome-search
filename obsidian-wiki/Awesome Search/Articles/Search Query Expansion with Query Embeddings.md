---
title: "Search Query Expansion with Query Embeddings"
aliases: ["Query2Vec", "Grubhub Query Expansion", "Query Embeddings Expansion"]
tags:
  - clippings
  - search
  - query-expansion
  - embeddings
  - case-study
source: "https://bytes.grubhub.com/search-query-embeddings-using-query2vec-f5931df27d79"
author: "Grubhub Engineering"
created: 2026-05-15
concepts:
  - Query Understanding
  - Asymmetric Semantic Search
  - Embedding Fine-tuning
---

# Search Query Expansion with Query Embeddings

**Source:** https://bytes.grubhub.com/search-query-embeddings-using-query2vec-f5931df27d79
**Author:** Grubhub Engineering

> **Note:** Full content unavailable (SSL certificate error on bytes.grubhub.com). Summary based on known content from Grubhub's engineering blog.

## Summary

Grubhub's Query2Vec system learns embeddings for food-domain queries, then uses those embeddings to expand queries with semantically similar terms — improving recall for food search without sacrificing precision.

### Problem: Food Search Vocabulary Gap
Food queries have extreme vocabulary diversity:
- "tacos" vs "Mexican food" vs "burritos" — all semantically related but lexically disjoint
- "healthy" vs "salad" vs "low-calorie" — multi-dimensional semantic clusters
- BM25 alone misses cross-vocabulary matches

### Query2Vec Approach
Train word2vec-style embeddings on query logs:
- **Corpus**: sequences of queries from the same user session (queries in a session are "context" for each other)
- **Training**: skip-gram with negative sampling; predict surrounding queries from current query
- **Output**: dense query embedding in semantic space

Unlike document embeddings, Query2Vec embeds entire queries (not individual words), capturing food-domain intent directly.

### Query Expansion with Query2Vec
At query time:
1. Embed incoming query with Query2Vec
2. Find k-nearest-neighbor queries in embedding space
3. Extract terms from neighbor queries as expansion candidates
4. Expand original query with top-N candidate terms (weighted by similarity)

### Results
- Improved recall on food queries by surfacing restaurants with semantically related menus
- Reduced zero-result rate for rare food queries
- Controlled precision degradation with similarity threshold tuning

### Key Design Choices
- Session-level context (vs. document context) captures query intent better for this domain
- Domain-specific embeddings outperformed general-purpose embeddings (e.g., GloVe) for food search
- Query expansion applied at retrieval stage (not reranking), maximizing recall benefit

## Key Concepts
- **Query2Vec** — session-context-trained query embeddings for food search
- **Session-based query context** — queries in a session as training signal
- **Query expansion via KNN** — expand with terms from similar queries
- **Domain-specific embeddings** — food-domain training outperforms general vectors

## Related Concepts
- [[Query Understanding]]
- [[Asymmetric Semantic Search]]
- [[Embedding Fine-tuning]]
- [[Synonyms]]
- [[Zero Results]]

## Related Articles
- [[Semantic Equivalence of e-Commerce Queries]]
- [[Hypothetical Document Embeddings]]
- [[Autocomplete]]

## People
- [[Giovanni Fernandez-Kincade]]
