---
type: concept
title: "ColBERT"
aliases: ["ColBERTv2", "Contextualized Late Interaction over BERT"]
tags:
  - concept
  - search
  - neural-ir
  - embedding-model
created: 2026-05-16
---

# ColBERT

## Definition

**ColBERT** (**Col**aborative **BERT** / Contextualized Late Interaction over BERT) is a neural retrieval model that represents queries and documents as sets of **per-token vectors** rather than single pooled vectors. Relevance is computed via the **MaxSim** operator — the sum of maximum dot products across query-document token pairs.

Created by [[Omar Khattab]] and [[Matei Zaharia]] at Stanford University, published at SIGIR 2020.

## Architecture

```
Query tokens → BERT → [q1, q2, ..., qm]   (query token vectors)
Doc tokens   → BERT → [d1, d2, ..., dn]   (doc token vectors)

Score = Σᵢ max_j (qᵢ · dⱼ)    (MaxSim)
```

**Special tokens:**
- `[Q]` prefix for queries (padded with `[mask]` tokens)
- `[D]` prefix for documents

## Versions

| Version | Year | Key Innovation |
|---|---|---|
| ColBERT v1 | 2020 | Original late interaction model |
| ColBERTv2 | 2021 | Denoised supervision + residual compression (6-10x storage reduction) |
| jina-colbert-v1-en | 2024 | Extended to 8192 tokens ([[Han Xiao]] / Jina AI) |

## Key Advantages

1. **Quality near cross-encoders** — token-level interaction captures nuanced relevance
2. **Scalability of bi-encoders** — documents pre-encoded offline, only queries at runtime
3. **Explainability** — MaxSim scores reveal which tokens drove retrieval (unlike dense embeddings)
4. **Training efficiency** — fewer labeled examples than single-vector models

## Compression (Vespa implementation)

Asymmetric binarization by [[Jo Kristian Bergum]]:
- Query vectors: float (full precision)
- Document vectors: int8 (compressed)
- Result: **32x compression** with minimal accuracy loss

### An earlier, more aggressive compression — and what it cost

Before the binarized embedder, [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]]
deployed a distilled MiniLM ColBERT: **22M parameters** (vs 110M), **32 dimensions per wordpiece**
(vs 128), stored as bfloat16, with query and document caps of 32 and 180 wordpieces. It reranked the
top 2,000 BM25 hits.

The result is a caution about compressing multi-vector models. This model scored **0.363 average
nDCG@10 across 13 BEIR datasets — below BM25's 0.453** — and the article states that compression and
distillation showed a *greater* impact zero-shot than in-domain. Two specific failures:

- **Catastrophic on some domains**: HotpotQA 0.298 vs BM25's 0.623; FEVER 0.534 vs 0.751; CLIMATE-FEVER
  0.067 vs 0.207
- **The query length cap binds**: CLIMATE-FEVER queries average 20.2 words against the 32-wordpiece limit

It still earned its place in a hybrid, which reached 0.481 — late interaction's value here was
complementarity with BM25, not standalone quality. See [[Hybrid Search]] and [[Zero-Shot Retrieval]].

## vs. Other Architectures

| Model | Interaction | Speed | Quality |
|---|---|---|---|
| [[Bi-Encoder]] | None (separate encoding) | Fast | Good |
| [[Cross-Encoder]] | Early (joint encoding) | Slow | Best |
| ColBERT | Late (token-level) | Medium | Near cross-encoder |

### Out-of-Domain Generalization

A further advantage, separate from peak quality: multi-vector representations transfer better
across domains than pooled single vectors. [[Jo Kristian Bergum]]'s position in
[[Three mistakes when introducing embeddings and vector search]] is that models like ColBERT
*"generalize much better than single-vector representations"* — a [[Bi-Encoder]] must decide at
training time which distinctions survive [[Pooling|pooling]] into one vector, and that decision is made
against the training query distribution. Deferring matching to query time keeps more of the
signal available when the distribution shifts. See [[Zero-Shot Retrieval]].

## Related Concepts
- [[Embeddings]] — parent concept
- [[Dense Embeddings]] — ColBERT produces per-token dense embeddings
- [[Zero-Shot Retrieval]] — where late interaction's transfer advantage shows up

- [[Late Interaction]] — the general principle ColBERT implements
- [[Bi-Encoder]] — simpler alternative
- [[Cross-Encoder]] — more accurate alternative
- [[Dense Vector Retrieval]] — ColBERT produces multi-vector dense representations
- [[Relational Transformer]] — ColBERTv2 used as a comparison point on RT's FLOPs-vs-NDCG@10 chart

## Tools

- **RAGatouille** — Python library for ColBERT in RAG pipelines
- **Vespa** — native ColBERT embedder
- **FAISS** — indexing for ColBERT document vectors

## Articles

- [[Announcing the Vespa ColBERT Embedder]] — [[Jo Kristian Bergum]]
- [[What is ColBERT and Late Interaction and Why They Matter in Search]] — [[Han Xiao]]
- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]]; recommends multi-vector models for out-of-domain robustness

## People

- [[Omar Khattab]] (creator)
- [[Matei Zaharia]] (co-creator)
- [[Jo Kristian Bergum]] (Vespa implementation)
- [[Han Xiao]] (Jina AI extension)

- [[ColBERT-Zero - To Pre-train Or Not To Pre-train ColBERT Models]] — [[Antoine Chaffin]] et al.; multi-vector pre-training beats KD-only; SOTA on BEIR <150M
- [[ColBERT Comes to Apache Solr]] — [[Nicolò Rinaldi]]; ColBERT reranking implementation in Apache Solr
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — [[Jo Kristian Bergum]]; a distilled 22M ColBERT losing to BM25 standalone and still lifting a hybrid to 0.481 on BEIR
