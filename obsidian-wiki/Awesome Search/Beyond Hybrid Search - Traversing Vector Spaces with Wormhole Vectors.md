---
title: "Beyond Hybrid Search: Traversing Vector Spaces with Wormhole Vectors"
source: "https://aiven.io/blog/beyond-hybrid-search-traversing-vector-spaces-with-wormhole-vectors"
author:
  - "[[Dima Kan]]"
published: 2025-12-15
created: 2026-05-15
description: "Wormhole vectors traverse between sparse and dense vector spaces via a Semantic Knowledge Graph, enabling disambiguation, explainability, and zero-result resolution."
tags:
  - clippings
---
# Beyond Hybrid Search: Traversing Vector Spaces with Wormhole Vectors

Standard hybrid search (BM25 + dense vectors + RRF) treats vector spaces as isolated silos. Wormhole vectors connect them.

## The problem

- **Sparse Space** (inverted index): high-dimensional, discrete, explainable keyword matching
- **Dense Space** (embeddings): lower-dimensional, continuous, abstract semantics

Going sparse→dense is easy (average embeddings of top results). Going dense→sparse is hard.

## Solution: Semantic Knowledge Graph (SKG)

Use statistical term distributions as bridges:
- **Foreground set**: documents retrieved by dense vector query (top 50)
- **Background set**: all remaining index documents
- **Score**: P(term | Foreground) / P(term | Background)

This surfaces terms disproportionately represented in query results — filtering out stopwords automatically.

### Disambiguation example

Dense query landing near "Java" documents:
- **Programming context** → terms: Hibernate, Scala, VM → generates: `Java AND (Hibernate OR Scala)`
- **Beverage context** → terms: Coffee, Sumatra, Roast → generates: `Java AND (Coffee OR Sumatra)`

## The Wormhole Workflow

1. **Lexical search** → top results
2. **Average embeddings** → dense intermediate vector
3. **SKG analysis** → identify distinct concept clusters
4. **Behavioral space** → query clickstream embeddings using discovered concepts

## Production value

- **Zero-result problem**: "sweet dough ring" → SKG discovers "Donut" without manual synonyms
- **Explainability**: maps dense vectors back to keywords ("Matched on concept: Pastry")

## Implementation (OpenSearch)

Uses `significant_terms` aggregations for SKG analysis, standard k-NN plugin for dense search.

```
1. Execute dense kNN query
2. Get top-k documents (Foreground)
3. Run significant_terms aggregation
4. Construct refined sparse query
5. Optionally traverse behavioral space
```

## Related Concepts
- [[Wormhole Vectors]] — the concept introduced in this article
- [[Hybrid Search]] — standard approach that wormhole vectors extend
- [[Sparse Embeddings]] — sparse space being traversed
- [[Dense Embeddings]] — dense space being traversed
- [[Embeddings]] — parent concept
- [[Semantic Search]] — semantic disambiguation via SKG
- [[Zero Results]] — wormhole vectors resolve zero-result queries without manual synonyms
- [[Query Understanding]] — disambiguation and scope expansion

## People
- [[Dima Kan]] — Aiven; wormhole vectors author