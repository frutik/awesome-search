---
title: "Matryoshka Embeddings"
aliases: ["MRL", "Matryoshka Representation Learning", "Adaptive Retrieval", "Truncatable Embeddings"]
tags:
  - concept
  - search
  - embeddings
  - efficiency
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
- [[Introduction to Matryoshka Embedding Models]] — HuggingFace
- [[Matryoshka Representation Learning - A Guide to Faster Semantic Search]] — Ujjwal

## People

- Kusupati et al. — original MRL paper authors
