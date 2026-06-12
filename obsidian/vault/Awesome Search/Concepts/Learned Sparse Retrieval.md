---
title: "Learned Sparse Retrieval"
aliases: ["LSR", "neural sparse retrieval", "learned sparse encoding"]
tags:
  - concept
  - search
  - retrieval
  - sparse-retrieval
  - neural-ir
related_concepts:
  - Sparse Vector Retrieval
  - SPLADE
  - ELSER
  - BM25
  - Dense Vector Retrieval
  - Hybrid Search
created: 2026-06-12
---

# Learned Sparse Retrieval

## Definition

Learned Sparse Retrieval (LSR) is the family of neural retrieval methods that represent queries and documents as **sparse vectors in vocabulary space** — where weights are produced by a trained model rather than counted from term frequencies. Unlike [[BM25]] or TF-IDF, LSR models learn which terms (including terms *not present* in the original text) should carry weight for a given input.

The key distinction from classical sparse retrieval: weights are *learned* via neural networks; from dense retrieval: representations remain *sparse* and inverted-index compatible.

---

## Why "Learned" Matters

Classical [[BM25]] assigns weights via hand-crafted formulas (TF, IDF, document length normalization). LSR replaces this with a trained transformer that:

1. **Expands vocabulary** — a document about "heart attack" also gets weight on "myocardial infarction", "cardiac arrest"
2. **Suppresses noise** — stopwords and irrelevant terms are pushed to zero by regularization
3. **Captures context** — the same word "bank" gets different term weights in financial vs. river contexts

This bridges the vocabulary mismatch gap that cripples BM25 without abandoning the inverted-index infrastructure that makes sparse retrieval fast.

---

## Training Paradigms

### Knowledge Distillation
Most modern LSR models are trained by distilling a stronger teacher (cross-encoder or dense retriever) into the sparse model:
- **Margin MSE loss**: minimize difference between teacher and student score margins
- **KL-divergence**: match teacher's full score distribution over candidates

### Regularization for Sparsity
Without explicit constraints, transformer MLM heads produce dense activation patterns. LSR training enforces sparsity via:
- **FLOPS regularizer** (used by SPLADE): penalizes the expected number of FLOPs at retrieval time — acts as learned stopword removal
- **L1 regularization**: directly penalizes the number of non-zero dimensions

### Contrastive Learning with Hard Negatives
Effective LSR training mines **hard negatives** — documents that are superficially relevant but not truly relevant — to force the model to learn fine-grained term discrimination.

---

## Model Family

| Model | Origin | Key Feature |
|---|---|---|
| [[SPLADE]] | NAVER LABS Europe | BERT MLM + Log-ReLU + MaxPool; term expansion |
| SPLADE++ | NAVER LABS Europe | Ensemble distillation, better sparsity/effectiveness tradeoff |
| SPLADE-v3 | NAVER LABS Europe | Updated checkpoints; Hugging Face release (2024) |
| [[ELSER]] | Elastic | SPLADE-based; zero-shot, production-tuned for Elasticsearch |
| uniCOIL | Castorini Lab | Scalar weights per existing token only; no expansion; fast |
| DeepImpact | Castorini Lab | Token-level importance without expansion |
| Neural Sparse | OpenSearch/AWS | Open-source SPLADE-style model for OpenSearch |

[[SPLADE]] and [[ELSER]] are the dominant production-grade LSR models. uniCOIL and DeepImpact trade effectiveness for speed.

---

## Mechanism (SPLADE Canonical Example)

```
Input text
  → Transformer (BERT backbone)
  → MLM head → 30,522-dim vocabulary logits per token
  → Log(1 + ReLU(logits))      ← log-saturation activation
  → MaxPool over all tokens     ← aggregate across positions
  → Sparse vector (~100–300 non-zero dims)
```

The resulting vector is stored in a standard inverted index. At retrieval time, scoring is a dot product over matching vocabulary dimensions — effectively an augmented BM25 with learned weights.

---

## Comparison

| | BM25 | Learned Sparse (SPLADE) | Dense ([[Bi-Encoder]]) |
|---|---|---|---|
| Term weighting | Counted (TF-IDF) | Learned (neural) | N/A (continuous) |
| Term expansion | Manual synonyms only | Learned automatically | Implicit in embedding |
| Interpretability | High | High (vocabulary terms) | Low |
| Infrastructure | Inverted index | Inverted index | ANN index |
| Zero-shot generalization | Poor (vocab mismatch) | Good | Good |
| Latency | ~1–5ms | ~5–20ms | ~5–20ms |

---

## Role in Hybrid Search

LSR is the sparse leg of [[Hybrid Search]], replacing or augmenting [[BM25]]:

```
Query → LSR model → sparse vector → inverted index → top-k sparse results
Query → Bi-Encoder → dense vector → ANN index     → top-k dense results
                                          ↓
                              Reciprocal Rank Fusion
```

LSR typically outperforms raw BM25 in the sparse leg, improving the overall hybrid pipeline quality.

---

## Benchmarks

LSR models are primarily evaluated on **BEIR** (Benchmarking IR) — 18 heterogeneous retrieval datasets:
- [[SPLADE]] achieves state-of-the-art among sparse-only models
- [[ELSER]] shows +17% average NDCG@10 over BM25 across 12 BEIR datasets

---

## Related Concepts

- [[Sparse Vector Retrieval]] — the retrieval mechanism LSR powers
- [[Sparse Embeddings]] — the representation type LSR produces
- [[SPLADE]] — primary LSR model
- [[ELSER]] — Elastic's production LSR model
- [[BM25]] — classical sparse baseline that LSR improves upon
- [[Dense Vector Retrieval]] — complementary approach; combined in [[Hybrid Search]]
- [[Cross-Encoder]] — often used as teacher model for LSR distillation
- [[Hybrid Search]] — LSR as the sparse leg

## Related Articles

- [[SPLADE for Sparse Vector Search Explained]]
- [[Hybrid Search SPLADE Sparse Encoder]]
- [[Elastic Learned Sparse Encoder (ELSER) Retrieval Performance]]
- [[SPLADE - Sparse Bi-Encoder BERT Model for First-Stage Ranking]]

## People

- [[Thibault Formal]] — SPLADE co-inventor, NAVER LABS Europe
- [[Stéphane Clinchant]] — SPLADE co-inventor, NAVER LABS Europe
- [[Thomas Veasey]] — ELSER, Elastic
