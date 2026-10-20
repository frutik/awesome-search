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

## Multi-Vector Embeddings and MUVERA

Since **1.31**, Weaviate can encode multi-vector embeddings ([[ColBERT]], [[ColPali]]) with [[MUVERA]] so [[HNSW]] indexes one fixed-size vector per object, tuned with `k_sim`, `d_proj` and `r_reps` (no final projection). On LoTTE lifestyle with colbertv2.0, memory dropped from ~12 GB to under 1 GB and import from 20+ minutes to 3–6 minutes, at the cost of recall that needs a higher `ef` (above 512 for 80%+) to recover. See [[More Efficient Multi-Vector Embeddings with MUVERA]].

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

- [[More Efficient Multi-Vector Embeddings with MUVERA]] — MUVERA support in 1.31, LoTTE memory/import/recall benchmark

## People
- [[Laura Ham]] — cross-encoder pipeline explainer

- [[Roberto Esposito]] · [[Joon-Pil (JP) Hwang]] — MUVERA implementation post
