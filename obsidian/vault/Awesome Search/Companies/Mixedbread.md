---
type: company
title: "Mixedbread"
aliases: ["mixedbread.ai", "mxbai"]
tags:
  - company
  - embeddings
  - reranking
  - vector-search
  - ai-infrastructure
website: https://mixedbread.ai
created: 2026-09-19
---

# Mixedbread

**Mixedbread** is an AI infrastructure company whose platform ingests mixed document formats
(PDFs, video, code, and connected sources such as Slack and Drive) and handles parsing,
chunking, embedding, and indexing so that agents can retrieve context from them. It is best
known in the retrieval community for its open-weight `mxbai-*` model line, whose reranker
models are widely used as drop-in [[Cross-Encoder|cross-encoders]].

Website: https://mixedbread.ai

---

## Products

From the company's own site:

- **Wholembed V3** — its flagship embedding model, described as late-interaction, omnimodal,
  and covering 100+ languages (see [[Late Interaction]], [[Multimodal Embeddings]]).
- **mxbai-rerank** — the reranker line, in a listwise formulation
  ([[Listwise Relevance Evaluation]]).
- **Toast 1** — an agentic search agent that runs the retrieval loop itself
  ([[Agentic Search]]).
- **Silo** — an S3-native multi-vector database engine.

Deployment options include regional and on-premise installations.

## In This Vault

- [[Hev meets Jev]] — `mxbai-rerank-large-v2` (hosted) is one of the three purpose-built
  rerankers benchmarked, scoring **0.476 mean nDCG@10** across SciFact, NFCorpus, and FiQA at
  $3.50 per 1,000 queries — the most expensive and the lowest-scoring of the hosted rerankers
  in that particular run, though comfortably above the unreranked [[BM25]] baseline of 0.404.
  Note that the run predates the current listwise `mxbai-rerank` generation.

## Related Notes

- [[Voyage AI]] · [[Cohere]] · [[Jina AI]] — the other reranker/embedding vendors in this vault
- [[TypeSafe]] — the general decision model benchmarked against these rerankers
- [[Hev meets Jev]] — the benchmark

## Related Concepts

- [[Reranking]] · [[Cross-Encoder]] · [[Listwise Relevance Evaluation]]
- [[Embeddings]] · [[Late Interaction]] · [[Multimodal Embeddings]]
- [[Agentic Search]]

## Related Topics

- [[Reasoning Reranking]] · [[Embedding Models Compared]]
