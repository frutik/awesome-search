---
title: "ColBERT"
aliases: ["ColBERTv2", "Contextualized Late Interaction over BERT"]
tags:
  - concept
  - search
  - neural-ir
  - embedding-model
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

## vs. Other Architectures

| Model | Interaction | Speed | Quality |
|---|---|---|---|
| [[Bi-Encoder]] | None (separate encoding) | Fast | Good |
| [[Cross-Encoder]] | Early (joint encoding) | Slow | Best |
| ColBERT | Late (token-level) | Medium | Near cross-encoder |

## Related Concepts
- [[Embeddings]] — parent concept
- [[Dense Embeddings]] — ColBERT produces per-token dense embeddings

- [[Late Interaction]] — the general principle ColBERT implements
- [[Bi-Encoder]] — simpler alternative
- [[Cross-Encoder]] — more accurate alternative
- [[Dense Vector Retrieval]] — ColBERT produces multi-vector dense representations

## Tools

- **RAGatouille** — Python library for ColBERT in RAG pipelines
- **Vespa** — native ColBERT embedder
- **FAISS** — indexing for ColBERT document vectors

## Articles

- [[Announcing the Vespa ColBERT Embedder]] — [[Jo Kristian Bergum]]
- [[What is ColBERT and Late Interaction and Why They Matter in Search]] — [[Han Xiao]]

## People

- [[Omar Khattab]] (creator)
- [[Matei Zaharia]] (co-creator)
- [[Jo Kristian Bergum]] (Vespa implementation)
- [[Han Xiao]] (Jina AI extension)
