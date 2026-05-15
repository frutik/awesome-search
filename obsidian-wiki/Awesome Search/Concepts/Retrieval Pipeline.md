---
title: "Retrieval Pipeline"
aliases: ["multi-stage retrieval", "retrieval-reranking pipeline", "two-stage retrieval", "retrieve-then-rerank"]
tags:
  - concept
  - search
  - retrieval
  - pipeline
---

# Retrieval Pipeline

## Definition

A retrieval pipeline is a multi-stage architecture that cascades retrieval systems from fast-but-approximate to slow-but-accurate, progressively narrowing a large corpus to a final ranked list.

The classic two-stage pattern:
```
Full corpus (millions) 
    → [Stage 1: Fast retrieval] → top-1000 candidates
    → [Stage 2: Accurate reranking] → top-10 final results
```

## Why Multi-Stage?

A [[Cross-Encoder]] reranker is highly accurate but O(n) in corpus size — it cannot score millions of documents per query. A [[Bi-Encoder]] or BM25 first-stage retrieval is fast enough to scan millions but less accurate.

The cascade exploits this tradeoff: use fast retrieval to prune to a manageable set, then apply expensive-but-accurate reranking.

## Standard Two-Stage Architecture

### Stage 1: First-Pass Retrieval
- **BM25**: fast lexical retrieval, inverted index, sub-millisecond
- **[[Bi-Encoder]]**: ANN search over dense vectors, ~10ms
- **[[Sparse Vector Retrieval]]** (SPLADE): hybrid of lexical speed + semantic quality
- **[[Hybrid Search]]**: RRF fusion of BM25 + bi-encoder

Output: ~100–1000 candidates

### Stage 2: Reranking
- **[[Cross-Encoder]]**: jointly encodes (query, doc), most accurate
- **[[ColBERT]]**: late interaction, faster than cross-encoder, more accurate than bi-encoder
- **Learned rerankers**: MonoT5, RankLLaMA, RankGPT

Output: 10–50 final results

## Distillation: Collapsing the Pipeline

[[Daniel Tunkelang]]'s work on distilling retrieval pipelines: use a high-quality two-stage pipeline to *generate training signal* for training a single-stage model that approximates the pipeline's output.

```
[BM25 + MonoT5-3B reranker] → training labels
    → train single bi-encoder to match pipeline quality
    → single-stage inference at deployment
```

This is how [[ELSER]] was trained: ensemble teacher (MiniLM + MonoT5-3B) → compressed 100M parameter model.

**Trade-off**: Training complexity vs. serving simplicity/speed.

## [[Agentic Search]] as Dynamic Pipeline

In [[Agentic Search]], the pipeline becomes adaptive:
- Agent decides which retrieval stages to invoke
- May skip reranking for simple queries
- May invoke multiple retrieval strategies for complex queries
- Verification step may trigger pipeline re-execution with reformulated query

## Three-Stage Pipelines

For very large corpora or very high precision requirements:
```
Full corpus 
    → ANN retrieval (bi-encoder) → 1000 candidates
    → Sparse rerank (BM25 score fusion) → 100 candidates  
    → Cross-encoder rerank → 10 results
```

## Related Concepts

- [[Bi-Encoder]] — fast first-stage retrieval
- [[Cross-Encoder]] — accurate reranking
- [[ColBERT]] — efficient reranking alternative
- [[Hybrid Search]] — enhanced first stage
- [[SPLADE]] — learned sparse first stage
- [[Agentic Search]] — dynamic pipeline
- [[RAG]] — uses retrieval pipeline for generation
- [[Embedding Fine-tuning]] — can collapse pipeline via distillation

## People

- [[Daniel Tunkelang]] — pipeline distillation; QueryUnderstanding.com
- [[Jo Kristian Bergum]] — Vespa multi-stage retrieval
