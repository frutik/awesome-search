---
title: "Introduction to Matryoshka Embedding Models"
source: "https://huggingface.co/blog/matryoshka"
author: ["Hugging Face"]
tags:
  - clippings
  - embeddings
  - matryoshka
  - huggingface
  - machine-learning
concepts:
  - Matryoshka Embeddings
  - Embedding Fine-tuning
  - Bi-Encoder
created: 2026-05-15
---

# Introduction to Matryoshka Embedding Models

**Source**: https://huggingface.co/blog/matryoshka  
**Publisher**: Hugging Face

## Summary

Hugging Face's official introduction to Matryoshka Representation Learning (MRL) — the technique enabling dimension-flexible embeddings — covering the theory, training with `sentence-transformers`, and practical deployment.

## Matryoshka Representation Learning (MRL)

MRL, introduced by Kusupati et al. (2022), trains embedding models so that **any prefix of the embedding vector is itself a valid, semantically meaningful embedding**.

Like Russian nesting dolls (matryoshka), the full embedding contains smaller embeddings within it:
```
[dim 1..8] ← 8-dim embedding
[dim 1..16] ← 16-dim embedding
[dim 1..32] ← 32-dim embedding
...
[dim 1..1536] ← full embedding
```

Each prefix independently ranks documents correctly.

## Training with MatryoshkaLoss

Standard training: minimize loss for a single embedding dimension.  
MRL training: minimize a *sum of losses* across multiple dimensions simultaneously.

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.losses import MatryoshkaLoss, MultipleNegativesRankingLoss

model = SentenceTransformer("bert-base-uncased")

inner_loss = MultipleNegativesRankingLoss(model)
loss = MatryoshkaLoss(
    model, 
    loss=inner_loss, 
    matryoshka_dims=[64, 128, 256, 512, 768]  # train at all these dims
)
```

During training, the loss is computed at each specified dimension, forcing the model to encode information in a hierarchical, prefix-compatible way.

## Supported Dimensions

For `nomic-embed-text-v1.5` (example):
- 768 → full quality
- 512 → ~99.5% quality
- 256 → ~99% quality
- 128 → ~98% quality
- 64 → ~96% quality

The quality loss is surprisingly small even at aggressive truncation.

## Why It Works

Standard embeddings pack information across all dimensions uniformly. MRL forces the model to prioritize: put the most important semantic information in the *earliest* dimensions, and refine/add detail in later dimensions.

This is analogous to how JPEG compression works — the coarse structure is encoded first, fine details added by later bits.

## Use Cases

1. **Adaptive retrieval**: fast first pass (truncated) → accurate rerank (full)
2. **Tiered serving**: low-latency tier (small dims), high-quality tier (full dims)
3. **Cost reduction**: store smaller embeddings when quality constraints allow
4. **Mobile/edge**: deploy small embedding for on-device search

## Models Supporting MRL

| Model | Full Dims | Min Dims | Notes |
|-------|----------|---------|-------|
| text-embedding-3-small | 1536 | 8 | OpenAI |
| text-embedding-3-large | 3072 | 8 | OpenAI |
| nomic-embed-text-v1.5 | 768 | 64 | Open source |
| mxbai-embed-large-v1 | 1024 | 64 | Open source |

## Related Articles

- [[Matryoshka Embeddings - Faster OpenAI Vector Search]] — practical implementation
- [[Matryoshka Representation Learning - A Guide to Faster Semantic Search]] — deeper theory
- [[Fine-Tuning Text Embeddings For Domain-Specific Search]] — related fine-tuning

## Related Concepts

- [[Matryoshka Embeddings]] — primary concept
- [[Bi-Encoder]] — architecture being fine-tuned
- [[Embedding Fine-tuning]] — MRL is a fine-tuning technique
- [[Dense Vector Retrieval]] — downstream use
- [[Retrieval Pipeline]] — two-pass adaptive search
