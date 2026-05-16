---
title: "Distilling Retrieval Pipelines to a Single Embedding Model"
source: "https://dtunkelang.medium.com/distilling-retrieval-pipelines-to-a-single-embedding-model-606f3ecf0c91"
author:
  - "[[Daniel Tunkelang]]"
published: 2026-04-20
created: 2026-05-15
description: "A bag-of-documents approach to query embedding: represent queries as distributions over relevant documents, distilling a complex hybrid+reranking pipeline into a single fine-tuned encoder."
tags:
  - clippings
---
# Distilling Retrieval Pipelines to a Single Embedding Model

**Core insight**: "A query is not just a string. It is a distribution over the results it should retrieve."

## Bag-of-Documents Model

Each query is represented as a set of relevant documents with:
- **Centroid vector**: captures canonical search intent
- **Specificity score**: mean cosine similarity between centroid and bag documents

Specificity examples:
- "laptop" → ~0.70
- "hp laptop" → ~0.81
- "hp laptop 16gb ram" → ~0.84

## Data pipeline

Built on 6M-product FAISS index (McAuley Lab Amazon Reviews 2023) with `all-MiniLM-L6-v2`.

Bag construction:
1. Hybrid retrieval (FAISS semantic + Tantivy lexical)
2. Cross-encoder relevance filtering
3. Deduplication → top 50 results

Over a third of final bag members come exclusively from keyword search — brands, model numbers, rare terms that semantic retrieval alone misses.

## Training

- Input: query text
- Target: bag centroid vector
- Loss: cosine distance minimization

Results across 74K queries:

| Metric | Before | After |
|---|---|---|
| Cosine similarity to centroid | 0.787 | **0.914** |
| Recall@10 | 0.367 | **0.506** |
| ESCI precision | 96.0% | **97.0%** |
| Complement retrieval rate | 14.2% | **7.7%** |

## Key benefit

Training: complex pipeline (hybrid retrieval + reranking + filtering).
Inference: **single embedding operation + nearest-neighbor search**.

The fine-tuned model internalizes the entire multi-stage pipeline. This is knowledge distillation applied to retrieval — or amortized pseudo-relevance feedback.

Resources available at `huggingface.co/datasets/dtunkelang/bag-of-documents` (MIT license).

## Related Concepts
- [[Embeddings]] — the representation being trained
- [[Dense Embeddings]] — the centroid vector output
- [[Bag-of-Documents Model]] — the framework this article introduces
- [[Embedding Fine-tuning]] — contrastive fine-tuning on query-document pairs
- [[Hybrid Search]] — the pipeline being distilled (FAISS + Tantivy)
- [[Dense Vector Retrieval]] — FAISS semantic retrieval component
- [[Query Specificity]] — specificity score as mean cosine similarity of bag documents

## People
- [[Daniel Tunkelang]] — author