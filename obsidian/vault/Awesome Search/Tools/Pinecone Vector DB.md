---
type: tool
title: "Pinecone Vector DB"
aliases: ["Pinecone", "Pinecone Vector DB"]
website: "https://www.pinecone.io/"
tags:
  - tool
  - vector-database
  - ann
  - hybrid-search
---

# Pinecone Vector DB

Managed (SaaS) vector database for [[Dense Vector Retrieval|dense vector]] / [[Semantic Search|semantic]] retrieval at scale, maintained by [[Pinecone]]. Also supports native sparse/term search, enabling [[Hybrid Search]] from a single instance.

- Website: https://www.pinecone.io/

## Notes

- Used as the vector retriever alongside a Lucene engine in a multi-retriever [[Hybrid Search]] setup, with [[Metarank]] fusing the result sets via [[Learning to Rank]] — see [[Hybrid Search and Learning-to-Rank with Metarank]].
- Pinecone's Learn blog is a frequent source of search/IR explainers in this vault.

## Related Tools

- [[Qdrant Vector DB]] · [[Weaviate Vector DB]] · [[Milvus Vector DB]] — alternative vector databases

## Related Concepts

- [[Dense Vector Retrieval]] · [[Hybrid Search]] · [[HNSW]] · [[Semantic Search]]

## Articles

- [[Hybrid Search and Learning-to-Rank with Metarank]]
