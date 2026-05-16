---
type: company
industry: search infrastructure
products:
  - Vespa (open-source search and recommendation engine)
category: technology-provider
search_domain: open-source big data serving engine with native ML support
---

# Vespa

## What They Build

Vespa is an open-source **big data serving engine** originally developed by Yahoo and now maintained as an independent open-source project (vespa.ai). Unlike Elasticsearch (document-centric) Vespa was built with ML-native ranking in mind from the start — it supports tensor computations, native embedding models, and multi-phase ranking as first-class features.

Vespa is particularly strong for use cases that mix retrieval, ranking, and ML inference in a single platform without an external reranking tier.

## Search Contributions

### Models and Embeddings
- **ColBERT embedder** — native integration of [[ColBERT]] late-interaction model into Vespa with asymmetric binarization (32x compression with minimal quality loss). Led by [[Jo Kristian Bergum]]
- Native HNSW approximate nearest neighbor for dense vector retrieval
- BM25 + dense vector [[Hybrid Search]] as a built-in feature

### Methodology
- **LLM-as-Judge for retrieval evaluation** — demonstrated how to use LLMs to generate relevance labels and compute NDCG; showed strong correlation with human judgments (Spearman ρ ≈ 0.85–0.90). Early and influential demonstration of the [[LLM as Judge]] pattern for retrieval

### Architecture
- Multi-phase ranking: cheap first-stage rankers → expensive ML models only on candidates
- Tensor computations at serving time without external ML serving infrastructure
- Native support for structured filtering alongside dense vector search

## Position in the Ecosystem

Vespa is a direct alternative to Elasticsearch + separate ML serving tier. The value proposition: run BM25, dense vector ANN, and ML re-ranking in a single engine. The tradeoff: steeper learning curve, smaller community than Elasticsearch.

## People

- [[Jo Kristian Bergum]] — Chief Scientist, Vespa AI; author of ColBERT embedder and LLM-as-judge work

## Articles

- [[Announcing the Vespa ColBERT Embedder]]
- [[Improving Retrieval with LLM as a Judge]]

## Concepts

[[ColBERT]] · [[Late Interaction]] · [[LLM as Judge]] · [[Hybrid Search]] · [[Dense Vector Retrieval]] · [[Reranking]]
