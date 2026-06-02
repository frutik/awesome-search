---
type: company
tags:
  - company
  - vector-database
  - search
  - cross-encoders
  - bi-encoders
category: technology-provider
industry: vector database / AI infrastructure
products:
  - Weaviate vector database
  - Weaviate Cloud (WCD)
search_domain:
  - vector search
  - semantic search
  - reranking
  - multi-modal search
use_cases: []
people:
  - "[[Laura Ham]]"
  - "[[André Mourão]]"
  - "[[Joon-Pil (JP) Hwang]]"
---

# Weaviate

Open-source vector database company providing semantic and hybrid search infrastructure. Competes with Pinecone, Qdrant, Milvus.

## Notable Contributions

**Cross-encoder reranking** — Weaviate has documented and popularized the bi-encoder + cross-encoder two-stage pipeline for semantic search:
- **Stage 1**: Bi-encoder ANN (fast, pre-computed embeddings)
- **Stage 2**: Cross-encoder reranker (accurate, query-aware, applied to small candidate set)

**Key insight**: Bi-encoders are fast because document embeddings are computed offline; cross-encoders are accurate because query and document are encoded together but can't scale to full corpora.

Weaviate supports cross-encoder reranking as a native feature in its search pipeline.


**Block-Max WAND** — Weaviate implemented [[Block-Max WAND]] in v1.29 (technical preview), achieving 5–10x p50 keyword search speedups and 50–90% index size reduction vs. their prior WAND baseline. Implemented by [[André Mourão]] and [[Joon-Pil (JP) Hwang]].

## Key Articles

- [[Using Cross-Encoders as Reranker in Multistage Vector Search]]

- [[BlockMax WAND - How Weaviate Achieved 10x Faster Keyword Search]]

## Tools
- [[Weaviate Vector DB]]


## People

- [[Laura Ham]]
- [[André Mourão]] — search engineer; [[Block-Max WAND]] implementation
- [[Joon-Pil (JP) Hwang]] — search engineer; [[Block-Max WAND]] implementation

## Concepts

[[Block-Max WAND]] · [[WAND]] · [[Hybrid Search]] · [[Cross-Encoder]]
