---
title: "Distilling Retrieval Pipelines to a Single Embedding Model"
source: "https://dtunkelang.medium.com/distilling-retrieval-pipelines-to-a-single-embedding-model-606f3ecf0c91"
author: ["Daniel Tunkelang"]
tags:
  - clippings
  - retrieval
  - distillation
  - embeddings
  - search
concepts:
  - Retrieval Pipeline
  - Embedding Fine-tuning
  - Bag-of-Documents Model
  - Dense Vector Retrieval
created: 2026-05-15
---

# Distilling Retrieval Pipelines to a Single Embedding Model

**Source**: https://dtunkelang.medium.com/distilling-retrieval-pipelines-to-a-single-embedding-model-606f3ecf0c91  
**Author**: [[Daniel Tunkelang]]

## Summary

[[Daniel Tunkelang]] argues that multi-stage retrieval pipelines (BM25 → cross-encoder reranker) can be distilled into a single high-quality embedding model, achieving most of the pipeline's quality at single-stage serving cost.

## The Serving Cost Problem

A typical high-quality [[Retrieval Pipeline]]:
```
Query → BM25 (1ms) → top-1000 → Cross-encoder reranker (500ms) → top-10
```

The cross-encoder dominates latency. For production systems:
- 500ms is unacceptable for interactive search
- Scaling cross-encoders is expensive (no pre-computation)
- Yet BM25-only retrieval misses ~15% of relevant documents

## Knowledge Distillation as Solution

The pipeline itself generates high-quality training signal:

```
Step 1: Run BM25 + Cross-encoder on training queries
    → high-quality (query, relevant_doc) pairs with pipeline-quality labels

Step 2: Train a bi-encoder to match pipeline's relevance judgments
    → student learns to approximate the teacher pipeline

Step 3: Deploy student bi-encoder alone
    → single-stage, fast, approximates pipeline quality
```

This is the same approach used to train [[ELSER]]: teacher ensemble (MiniLM + MonoT5-3B) → compressed 100M parameter student.

## Bag-of-Documents as Training Signal

Tunkelang frames this using the [[Bag-of-Documents Model]]:
- The pipeline estimates P(d | q) for training queries
- The student bi-encoder learns to reproduce this distribution
- The student's embedding space effectively encodes the pipeline's relevance judgments

## Quality vs. Speed Tradeoff

| System | Latency | NDCG@10 | Notes |
|--------|---------|---------|-------|
| BM25 alone | 1ms | 0.228 | Baseline |
| Dense bi-encoder | 10ms | 0.253 | Trained generally |
| Distilled bi-encoder | 10ms | 0.263 | Trained on pipeline output |
| Full pipeline | 500ms | 0.271 | Gold standard |

The distilled model captures ~87% of the pipeline's improvement over BM25 at 10ms latency.

## Limitations

1. **Distribution shift**: distilled model trained on pipeline's output; may not generalize to out-of-distribution queries
2. **Pipeline quality ceiling**: student can't exceed teacher quality
3. **Static**: distilled model needs retraining when pipeline improves

## Relation to Constructing Query Vectors

Distillation can be seen as an offline form of [[Hypothetical Document Embeddings]]:
- HyDE: at query time, generate what a relevant document looks like
- Distillation: at training time, teach the model what relevant documents look like per query type

## Related Articles

- [[Agentic Search as an Agile Engineering Process]] — same author on retrieval evolution
- [[Elastic Learned Sparse Encoder ELSER Retrieval Performance]] — distillation in production
- [[SPLADE - Sparse Bi-Encoder BERT Model for First-Stage Ranking]] — SPLADE++ uses distillation

## Related Concepts

- [[Retrieval Pipeline]] — what is being distilled
- [[Embedding Fine-tuning]] — distillation is a training technique
- [[Bag-of-Documents Model]] — theoretical framing
- [[Dense Vector Retrieval]] — deployment target
- [[Cross-Encoder]] — teacher in the distillation
- [[Bi-Encoder]] — student being trained

## People

- [[Daniel Tunkelang]] — author
