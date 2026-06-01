---
title: "Innovating Search Experience with Amazon OpenSearch and Amazon Bedrock"
source: "https://bigdataboutique.com/blog/innovating-search-experience-with-amazon-opensearch-and-amazon-bedrock-d045bc"
author:
  - "[[Roi Tabach]]"
published: 2024-10-08
created: 2026-05-15
description: "4 approaches to improving search with LLMs: naive synonym expansion, semantic search, query-time LLM synonym expansion (winner: Claude v2), and neural sparse retrieval."
tags:
  - clippings
  - company-blog
---
# Innovating Search Experience with Amazon OpenSearch and Amazon Bedrock

## The problem

Traditional search fails with synonyms and context. "Sport" misses "Soccer." "Orange" is ambiguous (fruit, color, brand).

## 4 approaches tested

### 1. Naive synonym expansion (WordNet)
Improves on manual ontologies but lacks context — "sport" might surface "exercise" when users want soccer gear.

### 2. Semantic search (embeddings)
Amazon OpenSearch Vector Index. "Shoes for a festive dinner" matches "high heels" without exact terms. Weakness: struggles with keyword queries where common words like "dinner" produce broad associations.

### 3. Query-time LLM synonym expansion (Amazon Bedrock)
Send user keywords to an LLM → get context-aware synonyms → query OpenSearch. Domain terms provided to model ensure relevance (e.g., "dinner" means something different in a shoe store vs. restaurant).

**Winner: Claude v2** (beat Cohere command and Meta Llama v2) — seamlessly integrated via Amazon Bedrock.

Architecture: user query → Claude synonym expansion → expanded query → OpenSearch cluster.

### 4. Neural sparse retrieval
Sparse representations capturing semantic nuances. Bridges semantic gaps while handling short keyword searches with lower cost and latency than dense embeddings.

## Conclusion

LLM-driven, context-aware synonym expansion delivers tailored search experiences at the query level without reindexing.


## Related Concepts

- [[Synonyms]]
- [[Semantic Search]]
- [[Sparse Embeddings]]
- [[Hybrid Search]]
- [[Query Understanding]]
- [[Dense Embeddings]]

## People

- [[Roi Tabach]]
