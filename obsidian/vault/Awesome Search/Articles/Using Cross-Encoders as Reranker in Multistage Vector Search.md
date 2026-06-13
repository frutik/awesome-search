---
created: 2026-05-16
type: article
tags: [article, cross-encoder, bi-encoder, reranking, two-stage-ranking, weaviate, company-blog]
source: "https://weaviate.io/blog/cross-encoders-as-reranker"
author: [Laura Ham]
company: [Weaviate]
concepts: [Cross-Encoder, Bi-Encoder, Dense Vector Retrieval, Retrieval Pipeline]
topics: [Conversational and Agentic Search]
---

# Using Cross-Encoders as Reranker in Multistage Vector Search

**[[Laura Ham]]** (Weaviate) explains the bi-encoder / cross-encoder tradeoff and how to combine them in a two-stage pipeline.

## Bi-Encoders

- Encode query and documents **independently** into dense vectors
- Similarity = cosine/dot product between pre-computed vectors
- **Fast** (ANN lookup at query time, embeddings pre-computed at index time)
- **Less accurate** — query context doesn't inform document encoding

## Cross-Encoders

- Take **(query, document) pair** as input; output a relevance score 0-1
- Full attention over both texts together — much more accurate
- **Cannot be pre-computed** — must run at query time for every candidate
- **Slow** — impractical to run against millions of documents

## Two-Stage Pipeline (The Fisherman Analogy)

```
All documents
    → Bi-encoder ANN → top-k candidates (fast, high recall)
        → Cross-encoder reranker → top-n results (slow, high precision)
```

Step 1 trades some precision for speed. Step 2 recovers precision on the small candidate set.

## Pre-trained Models

Available on HuggingFace under `cross-encoder/` namespace. MS MARCO-trained models work well for general natural language search. Fine-tune for out-of-domain data.

## Key Takeaway

Bi-encoders are the right choice for large-scale retrieval; cross-encoders are the right choice for precision reranking of a small candidate set. Combining them gets both at scale.

## Related Concepts

[[Cross-Encoder]] · [[Bi-Encoder]] · [[Dense Vector Retrieval]] · [[Retrieval Pipeline]]
