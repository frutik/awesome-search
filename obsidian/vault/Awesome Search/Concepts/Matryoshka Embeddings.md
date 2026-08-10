---
type: concept
title: "Matryoshka Embeddings"
aliases: ["MRL", "Matryoshka Representation Learning", "Adaptive Retrieval", "Truncatable Embeddings"]
tags:
  - concept
  - search
  - embeddings
  - efficiency
created: 2026-05-16
---

# Matryoshka Embeddings

## Definition

**Matryoshka Representation Learning (MRL)** is a training technique where a single high-dimensional embedding stores meaningful representations at **multiple granularity levels** — so that truncating the vector to fewer dimensions still yields a useful embedding. Named after Russian nesting dolls.

Introduced in Kusupati et al. (2022), arXiv:2205.13147.

## How Training Works

During training, loss is computed at **multiple dimensionalities** (e.g., 768, 512, 256, 128, 64 dimensions) and summed:

```python
loss = MatryoshkaLoss(
    model=model,
    loss=base_loss,
    matryoshka_dims=[768, 512, 256, 128, 64],
)
```

This forces the model to **frontload important information** in earlier dimensions, with later dimensions adding refinement.

## Key Property

A standard model truncated to 64 dims loses most performance. A Matryoshka model truncated to 64 dims retains ~98% of performance at full dimensionality.

> At **8.3% of original size**, Matryoshka model preserves **98.37% of performance** (vs. 96.46% for a standard model).

## Contested: Truncation vs Post-hoc PCA

The "~98% at 64 dims" figure above comes from the MRL literature's own framing. An
independent benchmark by [[Dylan Castillo]] over eight [[BEIR]] subsets
([[Honey, I Shrunk the Embeddings - Matryoshka vs PCA]]) measures truncation far less
favourably, and finds a fitted [[PCA]] projection beating it at aggressive compression
even on MRL-trained models:

| Dims | `text-embedding-3-small` truncated | PCA |
|---|---|---|
| 512 | 98% | 97% |
| 128 | 86% | 90% |
| 64 | 71% | 82% |
| 32 | 46% | 65% |

Retention here is nDCG@10 at *d* dimensions over nDCG@10 at full dimensions — a
different measurement than the size-vs-performance comparison quoted above, so the two
"98%" figures are not the same quantity.

The practical reading: MRL's real advantage is **operational** — no projection matrix to
fit, store, version, and apply identically at index and query time — rather than a
guaranteed quality edge at every dimension. That advantage narrows further if Castillo's
secondary results hold: a projection fit on 1,000 documents matched one fit on the full
corpus, and a separate projection fit out of domain on [[MS MARCO]] transferred usefully
down to 64 dims on a 1,536-dim model and 128 on a 4,096-dim one. This is one study on three models with exact
search rather than ANN indexing; treat it as a reason to measure your own truncation
curve, not as a settled verdict.

## Adaptive Retrieval (Two-Pass Strategy)

MRL enables a fast two-pass search:

```
Pass 1: Search with short embeddings (e.g., 256-dim)
        → Retrieve large candidate set (8x final_k)
Pass 2: Re-rank candidates using full embeddings (e.g., 3072-dim)
        → Return top-k results
```

**Performance (Supabase benchmark on 1M vectors):**
- Single-pass 1536D: 89.2% accuracy at 670 QPS
- Two-pass (512D first): **99% accuracy at 580 QPS**

## Supported Models

- **OpenAI text-embedding-3-small** (1536D), **text-embedding-3-large** (3072D) — support `dimensions` API parameter
- **nomic-embed-text-v1.5** — production Matryoshka model (16.3M downloads)
- **sentence-transformers** — `MatryoshkaLoss` available for training custom models

## Usage Pattern

```python
# Truncate and renormalize (after truncation, must renormalize)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("...", truncate_dim=256)
embeddings = model.encode(texts)
```

## Related Concepts
- [[Embeddings]] — parent concept
- [[Dense Embeddings]] — Matryoshka is a training technique for dense embeddings

- [[Dense Vector Retrieval]] — Matryoshka embeddings are used here
- [[Embedding Fine-tuning]] — MatryoshkaLoss is a fine-tuning technique
- [[Vector Search]] — adaptive retrieval optimizes ANN search using MRL

## Articles

- [[Matryoshka embeddings - faster OpenAI vector search using Adaptive Retrieval]] — Supabase
- [[Introduction to Matryoshka Embedding Models 1]] — HuggingFace
- [[Matryoshka Representation Learning - A Guide to Faster Semantic Search 1]] — Ujjwal
- [[Honey, I Shrunk the Embeddings - Matryoshka vs PCA]] — [[Dylan Castillo]]; benchmark where PCA beats truncation at low dimensions

## People

- Kusupati et al. — original MRL paper authors
