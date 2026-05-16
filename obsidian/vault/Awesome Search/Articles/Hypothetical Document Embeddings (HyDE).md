---
title: "Hypothetical Document Embeddings (HyDE)"
source: "https://docs.haystack.deepset.ai/docs/hypothetical-document-embeddings-hyde"
author: []
published: 
created: 2026-05-15
description: "HyDE improves retrieval by generating hypothetical documents for a query, embedding them, and averaging to create a retrieval vector — useful when domain data differs from retriever training data."
tags:
  - clippings
---
# Hypothetical Document Embeddings (HyDE)

HyDE addresses embedding retriever generalization problems by using an instruction-following LLM to generate "hypothetical documents" that capture relevant patterns from a query.

## When to use it

- Retrieval performance is poor (low Recall)
- Your pipeline queries against large document collections
- Your domain data differs substantially from the retriever's training data

## How it works

1. LLM generates ~5 hypothetical documents for the query
2. Each hypothetical document is encoded into an embedding vector
3. Vectors are averaged into a single consolidated embedding
4. That embedding is used for vector similarity search against real documents

The averaged embedding captures the semantic space of relevant content rather than the query string itself.

## Haystack implementation

Components needed:
- OpenAI generator (configured for multiple outputs)
- Prompt builder
- Output adapter
- Document embedder
- Custom component to compute mean of hypothetical document embeddings


## Related Concepts

- [[HyDE]]
- [[Dense Embeddings]]
- [[Embeddings]]
- [[RAG]]
- [[Semantic Search]]

## People

