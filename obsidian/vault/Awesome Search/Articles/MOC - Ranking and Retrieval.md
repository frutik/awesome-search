---
title: "MOC — Ranking and Retrieval"
tags:
  - moc
  - search
  - ranking
  - retrieval
created: 2026-05-15
---

# MOC — Ranking and Retrieval

Map of content covering lexical retrieval, learning to rank, hybrid fusion, multi-stage pipelines, and personalization.

## Lexical Retrieval

### BM25 and TF-IDF
- **Concept**: [[BM25]] — the standard for lexical retrieval; k1/b parameters; IDF saturation
- [[Understanding the BM25 Algorithm]] — clear formula breakdown with k1/b intuition
- [[Targeting Broad Queries in Search]] — Etsy: broad query challenges for BM25
- [[How Etsy Uses Thermodynamics for Search]] — entropy-based diversity for broad queries

- [[Semantic Search Without Embeddings]] — [[Doug Turnbull]]; taxonomy + BM25 as alternative to dense retrieval

### Classic Search Problems
- [[Broad and Ambiguous Search Queries]] — Tunkelang on disambiguation strategies
- [[Deconstructing E-Commerce Search - The 12 Query Types]] — Baymard's query taxonomy

## Hybrid Search

- **Concept**: [[Hybrid Search]] — sparse + dense combination
- **Concept**: [[Reciprocal Rank Fusion]] — rank-based merging, score-agnostic fusion
- [[RRF is Not Enough]] — why naive RRF fails; upstream quality matters; intent routing
- [[SPLADE for Sparse Vector Search Explained]]
- [[Hybrid Search SPLADE Sparse Encoder]]

- [[Wormhole Vectors Beyond Hybrid Search in OpenSearch]] — [[Dima Kan]]; SKG traversal bridging sparse/dense/behavioral spaces
- [[Hybrid search > sum of its parts? Berlin Buzzwords 2022]] — early hybrid search benchmarking
- [[Multilingual Embedding Model Hybrid Search Reranking]] — [[Quynh Nguyen]]; cross-lingual E5 + RRF + Cohere reranker

## Multi-Stage Ranking

- **Concept**: [[Retrieval Pipeline]] — full retrieve → rerank pipeline
- [[Multi-Stage Ranking]] — three stages: retrieval → relevance → click ranking
- [[Cross-Encoders ColBERT and LLM-Based Re-Rankers]] — when to use each
- [[Bi-encoder vs Cross-encoder When to Use Which One]]

## Learning to Rank

- **Concept**: [[Learning to Rank]] — LambdaMART, RankNet, neural rerankers
- [[How LambdaMART Works]] — Turnbull explains lambda gradients and MART
- [[Machine Learning-Powered Search Ranking of Airbnb Experiences]] — 4-stage ML progression
- [[Learning to Rank for Flight Itinerary Search]] — Skyscanner LTR case study
- [[Building a Better Search Engine for Semantic Scholar]] — LightGBM + LambdaRank

## Personalization

- **Concept**: [[Personalization]] — user embeddings, behavioral signals
- [[Patterns for Personalization]] — Eugene Yan: 5 ML patterns with industry examples
- [[Listing Embeddings in Search Ranking]] — Airbnb: real-time personalization via embeddings

## Bias and Diversity

- **Concept**: [[Position Bias]] — rank confounder in click signals
- **Concept**: [[Diversity Metrics]] — MMR, α-NDCG, APD, entropy
- [[Search at Slack]] — how Slack handles position bias in LTR training
- [[Diversity Metrics for Recommender Systems]] — diversity metrics from a RecSys perspective
- [[Maximal Marginal Relevance for Keyphrase Extraction]] — MMR applied to keyphrase selection

## Related MOCs

- [[MOC - Search Quality Assurance and Query Understanding]]
- [[MOC - Agentic Search and Embeddings]]
- [[MOC - Case Studies]]


## Additional Articles — Ranking

- [[Bayesian BM25 is Cool]] — BB25: calibrated BM25 probabilities for principled hybrid fusion
- [[Understanding BERT and Search Relevance]] — BERT dense vectors for search; storage trade-offs; black box challenge
- [[E-commerce Search and Recommendation with Vespa]] — Vespa features for e-commerce search and recs
- [[Using Approximate Nearest Neighbor Search to Find Similar Products]] — ANN with metadata filters, HNSW, real-time updates
- [[Putting Search Ranking in Perspective]] — Tunkelang on ranking priority stack
