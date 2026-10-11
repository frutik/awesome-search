---
title: "Voyage AI"
type: company
tags:
  - company
  - embeddings
  - vector-search
website: "https://www.voyageai.com/"
category: technology-provider
industry: AI / embeddings
products: ["Voyage AI API", "voyage-3-large", "voyage-4-large"]
search_domain: [embeddings, semantic search, vector search]
created: 2026-05-19
---

# Voyage AI

Embedding model provider. Offers high-dimensional text embedding APIs used in semantic and vector search pipelines.

Referenced in [[Erik Hatcher]]'s [[Hybrid Search Blueprint Series Semantic Boosting]] as the embedding provider for query vectorization (`voyage-4-large`, 2048 dimensions, dot product similarity).

## Models
- **voyage-3-large** — used for pre-embedding documents in the `embedded_movies` example
- **voyage-4-large** — used for query embedding at query time

- **[[Voyage rerank-3|rerank-3 / rerank-3-lite]]** — rerankers launched 2026-09-30, succeeding rerank-2.5 / rerank-2.5-lite at the same price ($0.05 / $0.02 per M tokens), with 32K context and instruction-following. Largest gains are on long documents and code.

The rerankers were built "in collaboration with the Voyage team at [[MongoDB]]" and are also served natively in MongoDB Atlas Vector Search.

## People
- [[Erik Hatcher]] — used Voyage AI in Semantic Boosting demo

## Articles
- [[Hybrid Search Blueprint Series Semantic Boosting]]
- [[Hev meets Jev]] — `rerank-3` scores **0.504 mean nDCG@10** on three [[BEIR]] subsets, at $0.50 per 1,000 queries with p50/p95 of 185 ms / 287 ms. That is second to Mixedbread's mxbai-rerank-v3.1-listwise (0.511) and a hair ahead of an untuned general decision model ([[Jev]], 0.501), with a much tighter latency tail than Jev
- [[rerank-3 and rerank-3-lite - the next generation of Voyage rerankers]] — launch post; +2.72% NDCG@10 over [[Cohere]] Rerank v4.0 Pro across 95 datasets (vendor-run), and ahead of untuned [[Jev]] in code, law and finance

## Key Concepts
- [[Dense Vector Retrieval]]
- [[Semantic Boosting]]
- [[Embeddings]]

- [[Reranking]]
