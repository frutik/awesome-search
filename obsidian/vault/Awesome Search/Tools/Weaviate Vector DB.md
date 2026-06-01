---
title: Weaviate Vector DB
type: tool
tags:
  - tool
  - vector-database
  - vector-search
  - open-source
  - reranking
website: https://weaviate.io/
repo: https://github.com/weaviate/weaviate
maintainer: "[[Weaviate]]"
created: 2026-05-19
---

# Weaviate Vector DB

Open-source vector database providing semantic and hybrid search infrastructure. Supports native multi-stage retrieval pipelines including ANN retrieval and cross-encoder reranking. Maintained by [[Weaviate]] (the company).

- Website: https://weaviate.io/
- GitHub: https://github.com/weaviate/weaviate
- Cloud: Weaviate Cloud (WCD) — managed hosted service

---

## What It Does

Weaviate stores objects with vector representations and exposes search via GraphQL and REST APIs. It integrates vectorization and reranking as first-class pipeline stages rather than requiring external tooling.

Key capabilities:
- **ANN search** — [[HNSW]]-based index
- **Hybrid search** — combines dense and sparse (BM25) retrieval with fusion
- **Native reranking** — cross-encoder reranking built into the search pipeline (no separate service)
- **Vectorizer modules** — pluggable embedding providers (OpenAI, Cohere, HuggingFace, etc.) called at import and query time
- **Multi-modal** — image + text vectors in the same collection
- **GraphQL API** — declarative query syntax for retrieval, filtering, aggregation

## Two-Stage Pipeline

Weaviate's canonical retrieval pattern:

1. **Stage 1 — Bi-encoder ANN**: fast candidate retrieval using pre-computed embeddings ([[Bi-Encoder]])
2. **Stage 2 — Cross-encoder reranking**: accurate reranking of top-K candidates using query-aware scoring ([[Cross-Encoder]])

This separates scalability (stage 1) from accuracy (stage 2).

## Related Tools
- **[[Qdrant Vector DB]]** — competing vector database; stronger quantization options (TurboQuant)
- **Pinecone** — managed-only competitor
- **FAISS** — library only; no pipeline features

## Related Concepts
- [[HNSW]] — ANN index used
- [[Hybrid Search]] — dense + sparse fusion
- [[Cross-Encoder]] — reranker Weaviate integrates natively
- [[Bi-Encoder]] — first-stage retriever
- [[Reranking]] — the two-stage pattern Weaviate popularized
- [[Dense Vector Retrieval]] — primary retrieval mode

## Articles
- [[Using Cross-Encoders as Reranker in Multistage Vector Search]]

- [[Choosing a Vector Database for ANN Search at Reddit]] — Reddit qualitatively scored Weaviate; not tested quantitatively due to time constraints; single-node-type architecture noted as a concern

## People
- [[Laura Ham]] — cross-encoder pipeline explainer
