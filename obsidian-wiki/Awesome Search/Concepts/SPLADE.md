---
title: "SPLADE"
aliases: ["Sparse Lexical and Dense Expansion", "SParse Lexical AnD Expansion"]
tags:
  - concept
  - search
  - sparse-retrieval
  - neural-ir
---

# SPLADE

## Definition

**SPLADE** (**Sp**arse **L**exical **a**n**d** **E**xpansion / **SP**arse **L**exical **A**n**D** **E**xpansion) is a neural sparse retrieval model that creates **learned sparse embeddings** via BERT's Masked Language Model (MLM) head. It combines semantic understanding from transformers with the efficiency of inverted-index retrieval.

Developed by [[Thibault Formal]], [[Stéphane Clinchant]], and Benjamin Piwowarski at NAVER LABS Europe.

## Core Mechanism

```
Input text → BERT → MLM head → 30,522-dim vocabulary distribution per token
→ Log-ReLU activation
→ Max-pool across tokens
→ Sparse vector (≈100-200 non-zero entries out of 30,522)
```

For each token in the input, the MLM head predicts probability over the entire vocabulary — enabling **term expansion** (predicting relevant terms not in the original text) and **compression** (suppressing uninformative terms).

**Example:** For document about binary numbers, SPLADE:
- Expands: adds "computing", "digit" (semantically related)  
- Compresses: removes conjunctions and articles
- Result: 23-term sparse vector from a 60-term passage

## Key Technical Components

**Log saturation:** Prevents single terms from dominating scores.

**FLOPS regularizer:** Penalizes computation cost to encourage sparsity, acts as implicit stop-word removal.

## Versions

| Version | Innovation |
|---|---|
| SPLADE v1 | Original: both query & document expansion |
| SPLADE v2 | Max pooling; document-only expansion (faster queries) |
| SPLADE-V3 (2024) | Updated models; Hugging Face release |

## vs. BM25 and Dense Retrieval

| | BM25 | SPLADE | Dense ([[Bi-Encoder]]) |
|---|---|---|---|
| Vocabulary | Fixed (term frequency) | Expanded (learned) | None (continuous) |
| Semantics | None | Good (via BERT) | Excellent |
| Speed | Very fast | Fast (inverted index) | Fast (ANN) |
| Interpretability | High | High (vocabulary terms) | Low |
| Domain adaptation | Manual | Learned | Learned |

## Advantages Over Dense Retrieval

- No [[Vector Search]] infrastructure needed — works with standard inverted indexes
- Interpretable representations (vocabulary-dimension vectors)
- Strong zero-shot performance
- Easier integration into existing [[Hybrid Search]] pipelines

## Related Concepts
- [[Embeddings]] — parent concept
- [[Sparse Embeddings]] — SPLADE is a learned sparse embedding model

- [[Sparse Vector Retrieval]] — SPLADE is the leading learned sparse model
- [[ELSER]] — Elastic's SPLADE-based model
- [[Hybrid Search]] — SPLADE complements dense retrieval
- [[Cross-Encoder]] — used as teacher model for SPLADE distillation

## Articles

- [[SPLADE for Sparse Vector Search Explained]] — [[James Briggs]]
- [[Hybrid Search SPLADE Sparse Encoder]] — Sowmiya Jaganathan
- [[SPLADE - Sparse Bi-Encoder BERT Model for First-Stage Ranking]] — [[Stéphane Clinchant]], [[Thibault Formal]]
- [[Elastic Learned Sparse Encoder ELSER Retrieval Performance]] (ELSER as SPLADE variant)

## People

- [[Thibault Formal]]
- [[Stéphane Clinchant]]
