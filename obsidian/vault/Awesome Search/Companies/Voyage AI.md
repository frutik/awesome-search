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

## People
- [[Erik Hatcher]] — used Voyage AI in Semantic Boosting demo

## Articles
- [[Hybrid Search Blueprint Series Semantic Boosting]]

## Key Concepts
- [[Dense Vector Retrieval]]
- [[Semantic Boosting]]
- [[Embeddings]]
