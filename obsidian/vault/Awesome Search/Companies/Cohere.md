---
type: company
category: technology-provider
industry:
  - AI
  - NLP
  - enterprise AI
products:
  - Cohere Embed
  - Cohere Rerank (rerank-v3.5)
  - Command LLM
search_domain: embedding models, cross-encoder reranking, multilingual retrieval
tags:
  - company
  - technology-provider
  - reranking
  - embeddings
created: 2026-05-16
website: https://cohere.com
---

# Cohere

AI company specializing in enterprise NLP. Relevant to search primarily through their **reranking models** — production-grade cross-encoders used to re-score retrieval results.

## Relevance to Search

- **Rerank-v3.5**: cross-encoder reranker used in production hybrid pipelines (e.g., Elastic multilingual search)
- **Embed v3**: multilingual embedding model competitive with E5 and Qwen3
- Integrates with Elasticsearch, OpenSearch, and other search engines as a hosted inference endpoint

## Articles

- [[Multilingual Embedding Model Hybrid Search Reranking]] — Cohere rerank-v3.5 used in Elastic pipeline
- [[Hev meets Jev]] — `rerank-v3.5` benchmarked on three [[BEIR]] subsets at **0.486 mean nDCG@10** and $2.00 per 1,000 queries; an untuned general decision model ([[Jev]]) matched or beat it on all three corpora at roughly a quarter of the price

- [[rerank-3 and rerank-3-lite - the next generation of Voyage rerankers]] — Cohere Rerank v4.0 Pro and Fast as the main baselines; Voyage reports rerank-3 ahead by 2.72% and 5.74%, and by 13.84% over Pro on long documents

## Related Concepts

- [[Cross-Encoder]] · [[Reranking]] · [[Hybrid Search]] · [[Dense Vector Retrieval]]

## Related Companies

- [[Elastic]] — integrates Cohere as an inference provider
