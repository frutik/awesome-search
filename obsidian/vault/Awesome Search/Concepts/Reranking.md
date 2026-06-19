---
title: "Reranking"
aliases: ["reranker", "second-stage ranking", "re-ranking", "cross-encoder reranking", "neural reranking", "multi-stage reranking"]
tags:
  - concept
  - search
  - ranking
  - retrieval
created: 2026-05-16
---

# Reranking

## Definition

Reranking is a second-stage scoring step that takes an initial candidate set retrieved cheaply (first stage) and rescores it using a more expensive, higher-quality model. The reranker sees both the query and document together, enabling richer interaction than first-stage retrievers.

## Why Reranking Exists

First-stage retrievers ([[BM25]], [[Bi-Encoder]]) must score millions of documents quickly — they use independent query/document representations or simple term statistics. This limits their expressiveness. A reranker only needs to score ~100–1000 candidates, so it can afford deep query-document interaction.

## Standard Pipeline

```
Query
  │
  ▼
First-stage retrieval (BM25 / bi-encoder ANN)   → top-1000 candidates
  │
  ▼
Reranker (cross-encoder or LLM)                 → rescored top-1000
  │
  ▼
Final ranked list (top-10/20 served to user)
```

## Reranker Types

### Cross-Encoder (Most Common)
A [[Cross-Encoder]] processes query + document concatenated as a single sequence, producing a relevance score. Sees full interaction between query and document tokens.

- Models: `cross-encoder/ms-marco-MiniLM-L-6-v2`, Cohere Rerank, `bge-reranker-*`
- Latency: ~50–200ms for 100 candidates on GPU
- Quality: significantly better than bi-encoder for nuanced relevance

### LLM-as-Reranker
Use a large language model ([[LLM as Judge]]) to score or listwise-rank candidates. Higher quality, much higher cost.

- Pointwise: "Is this document relevant to the query? Yes/No"
- Listwise: "Rank these 10 documents by relevance"

### ColBERT Late Interaction
[[ColBERT]] / [[Late Interaction]] sits between bi-encoder speed and cross-encoder quality — efficient enough for first-stage in some setups, but also used as a reranker.

### Feature-Based (LTR) Re-ranker
A [[Learning to Rank|LTR]] model ([[LambdaMART]]) rescores the top-N using tabular features — BM25 components, popularity/CTR, price, freshness. Often deployed as an **external secondary re-ranker** outside the search engine, agnostic to retrieval. [[Metarank]] is the canonical open-source example; it trains on [[Implicit Judgments]] and serves with a ~20–30 ms latency budget. See [[Learn-to-Rank with OpenSearch and Metarank]].

## Reranking in RAG

In [[RAG]] pipelines, reranking is critical: the LLM context window is limited, so only the top 3–5 chunks are included. A reranker narrows 50–100 retrieved chunks down to the best ones before LLM generation.

## Tradeoffs

| | First-Stage | Reranker |
|---|---|---|
| Throughput | Millions of docs/sec | Hundreds of docs/sec |
| Latency | <10ms | 50–500ms |
| Quality | Good | Excellent |
| Cost | Low | Higher |

## Related Concepts
## When Reranking Becomes a System Boundary

From [[When Reranking Becomes a System Boundary]] ([[Ravindra Harige]]):

**Retrieval defines eligibility; reranking defines order.** If a document is not retrieved, no downstream stage can recover it.

### Ranking as a Projection

Reranking does not redo retrieval-time computation (term matches, field contributions, BM25 components). It operates on a compressed, lossy representation of what survived into the candidate set. This is structural — not a failure of implementation.

### Compensatory Reranking

The system crosses a boundary when performance gains come from widening the rerank window rather than improving retrieval. At that point the window size is load-bearing (not a latency knob), and reranking has become compensatory.

### Evaluation Split

| Stage | Metric | Blindspot |
|-------|--------|-----------|
| Retrieval | Recall@K | NDCG can improve while recall is weak |
| Reranking | NDCG, MRR | Metrics improve while user-visible relevance plateaus |

Retrieval (engineering) and reranking (ML/data science) are owned by different teams with different metrics. Neither dashboard shows the full picture. The gap closes only when someone is accountable for the space between them.


- [[Retrieval Pipeline]] — the multi-stage architecture reranking fits into
- [[Cross-Encoder]] — primary reranking architecture
- [[Bi-Encoder]] — first-stage retriever that feeds the reranker
- [[ColBERT]] — late interaction alternative
- [[LLM as Judge]] — LLM-based reranking
- [[RAG]] — key use case for reranking
- [[Learning to Rank]] — related family of ranking approaches
- [[MonoT5]] — T5 pointwise neural reranker
- [[RankLLaMA]] — LLaMA fine-tuned reranker
- [[RankGPT]] — listwise LLM reranker
- [[LambdaMART]] / [[Metarank]] — feature-based external secondary re-ranker
- [[Feature Store]] — serves the features an LTR re-ranker consumes

## Topics

- [[Reasoning Reranking]] — the frontier of LLM / generative / reasoning rerankers
- [[Frontier of Search 2026]]
