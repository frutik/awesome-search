---
title: "Bi-Encoder"
aliases: ["Two-Tower Model", "Dual Encoder", "Bi-encoder Architecture", "Siamese Network"]
tags:
  - concept
  - search
  - neural-ir
  - embedding-model
---

# Bi-Encoder

## Definition

A **bi-encoder** uses **two independent encoders** — one for queries, one for documents — producing separate dense vector embeddings. Relevance is computed as the similarity (cosine or dot product) between the query embedding and pre-computed document embeddings.

## How It Works

```
Query  → Encoder_Q → q_vec ──┐
                               → similarity(q_vec, d_vec) → score
Doc    → Encoder_D → d_vec ──┘
```

Documents are encoded **offline** (pre-computed and stored). At search time, only the query is encoded and compared against the index.

## Key Properties

| Property | Value |
|---|---|
| Query encoding | Online (at search time) |
| Document encoding | Offline (pre-computed) |
| Interaction | None — similarity computed post-encoding |
| Speed | Very fast (dot product / cosine against ANN index) |
| Quality | Good for general tasks; limited for nuanced relevance |

## Training

Trained with **contrastive loss** (e.g., MultipleNegativesRankingLoss):
- Maximize similarity of relevant (query, document) pairs
- Minimize similarity of irrelevant pairs
- Positive pairs from click data, relevance judgments, or NLI datasets

## When to Use

**Best for:**
- Large-scale first-stage retrieval (millions/billions of docs)
- Any task where pre-computing document embeddings is feasible
- Real-time applications requiring low latency

**Less suited for:**
- Nuanced relevance where query-document interaction matters
- Small candidate sets where [[Cross-Encoder]] reranking is feasible

## vs. Related Architectures

- [[Cross-Encoder]] — processes query+document jointly; slower but more accurate
- [[ColBERT]] — uses per-token vectors with late interaction; balance of speed and quality
- [[Late Interaction]] — generalization of ColBERT's token-level interaction idea

## Related Concepts
- [[Embeddings]] — what the bi-encoder produces
- [[Dense Embeddings]] — the specific representation type output by bi-encoders

- [[Dense Vector Retrieval]] — bi-encoders produce the dense vectors used here
- [[Hybrid Search]] — bi-encoder retrieval often combined with BM25
- [[Semantic Search]] — bi-encoders enable semantic matching
- [[Asymmetric Semantic Search]] — bi-encoders with asymmetric query/doc encoding (e.g., MS MARCO models)

## Articles

- [[Bi-encoder vs Cross-encoder When to Use Which One]]

## Normalization Note

Also called: dual encoder, two-tower model, Siamese network (when same encoder for both). All refer to the same architecture.
