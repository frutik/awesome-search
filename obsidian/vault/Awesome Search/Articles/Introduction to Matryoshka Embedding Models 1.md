---
title: "🪆 Introduction to Matryoshka Embedding Models"
source: "https://huggingface.co/blog/matryoshka"
author:
  - "[[Tom Aarsen]]"
  - "[[Joshua (Xenova)]]"
  - "[[Omar Sanseviero]]"
published: 2024-02-23
created: 2026-05-15
description: "Introduction to Matryoshka Embedding Models — trained to produce useful embeddings at multiple dimensionalities for speed/accuracy trade-offs."
tags:
  - clippings
  - company-blog
---
# 🪆 Introduction to Matryoshka Embedding Models

Matryoshka embedding models store more important information in earlier dimensions, less important in later ones — like Russian nesting dolls. Truncated embeddings still retain useful information, unlike traditional models.

## Why use them?

1. **Shortlisting + reranking**: shrink embeddings for fast candidate retrieval, then process finalists at full dimensionality
2. **Trade-offs**: tune storage cost, speed, and performance independently

## Training

Standard training: produce embeddings → compute loss on full-size → update weights.

MRL training: produce embeddings → compute loss at **multiple dimensionalities** (e.g., 768, 512, 256, 128, 64) → sum losses → update weights. This frontloads the most important information.

```python
from sentence_transformers.losses import CoSENTLoss, MatryoshkaLoss

loss = MatryoshkaLoss(
    model=model,
    loss=CoSENTLoss(model=model),
    matryoshka_dims=[768, 512, 256, 128, 64],
)
```

## Usage

```python
model = SentenceTransformer("tomaarsen/mpnet-base-nli-matryoshka", truncate_dim=64)
embeddings = model.encode(["The weather is nice!", "It's sunny outside!"])
# shape: (2, 64)
```

Re-normalize after manual truncation if original embeddings were normalized.

## Results (STSBenchmark)

- Matryoshka model exceeds standard model at **all** dimensionalities
- **At 8.3% of embedding size (64d of 768d): 98.37% performance preserved** vs 96.46% for standard model

Significant storage savings and downstream speedups with negligible accuracy loss.


## Related Concepts

- [[Matryoshka Embeddings]]
- [[Dense Embeddings]]
- [[Embedding Fine-tuning]]
- [[Embeddings]]
- [[Semantic Search]]

## People

- [[Tom Aarsen]]
- [[Jo Kristian Bergum]]
