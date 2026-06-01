---
title: "Matryoshka Representation Learning: A Guide to Faster Semantic Search"
source: "https://ujjwalm29.medium.com/matryoshka-representation-learning-a-guide-to-faster-semantic-search-1c9025543530"
author: []
tags:
  - clippings
  - embeddings
  - matryoshka
  - semantic-search
  - performance
  - medium
concepts:
  - Matryoshka Embeddings
  - Dense Vector Retrieval
  - Semantic Search
created: 2026-05-15
---

# Matryoshka Representation Learning: A Guide to Faster Semantic Search

**Source**: https://ujjwalm29.medium.com/matryoshka-representation-learning-a-guide-to-faster-semantic-search-1c9025543530

## Summary

A practitioner's guide to [[Matryoshka Embeddings]] (MRL) focusing on the theory behind the hierarchical encoding, practical speedups, and implementation guidance for faster semantic search.

## The Core Insight: Information Hierarchy

Traditional embeddings distribute semantic information uniformly across all dimensions — there's no ordering or priority. If you truncate 768 dimensions to 128, you lose 83% of dimensions *randomly*, resulting in poor-quality embeddings.

MRL forces a priority ordering: the first D dimensions capture the *most salient* semantic information, with subsequent dimensions adding refinement.

**Analogy**: A book summary hierarchy:
- 1 sentence (most important)
- 1 paragraph (adds detail)
- 1 page (more detail)
- Full book (complete)

Each level contains all information from shorter levels, plus more.

## Mathematical Formulation

For a model producing embeddings e ∈ ℝᴰ:

Standard loss:
```
L = loss(e₁...ₑD, labels)
```

MRL loss:
```
L_MRL = Σₘ weight_m × loss(e₁...ₑm, labels)
        for m in {8, 16, 32, 64, 128, 256, 512, D}
```

The weighted sum ensures every prefix is semantically valid.

## Speedup Analysis

Cosine similarity computation scales with dimension:
- 1536-dim: baseline time T
- 256-dim: T/6 (6x faster)
- 64-dim: T/24 (24x faster)

For ANN search over 100M vectors:
| Dims | Throughput (QPS) | Accuracy vs. Full |
|------|-----------------|-------------------|
| 1536 | 72 QPS | 100% |
| 512 | 220 QPS | 99.3% |
| 256 | 580 QPS | 98.9% |
| 128 | 1200 QPS | 98.1% |

The 256-dim configuration achieves **8x throughput at 99% accuracy** — a very favorable tradeoff.

## Two-Pass Search Implementation

```python
# First pass: fast approximate search
short_query_emb = model.encode(query, dimensions=256)
candidates = index_256.search(short_query_emb, k=1000)

# Second pass: accurate reranking
full_query_emb = model.encode(query, dimensions=1536)
candidate_embs = index_1536.fetch(candidate_ids)
scores = cosine_similarity(full_query_emb, candidate_embs)
final_results = sorted(zip(candidate_ids, scores))[:10]
```

## Storage vs. Quality Tradeoff

Two storage strategies with MRL:

1. **Store only truncated** (e.g., 256-dim): save space, accept quality floor
2. **Store both** (256-dim + 1536-dim): two-pass adaptive; optimal quality/speed balance

Strategy 2 requires ~16% more storage than strategy 1 but delivers full accuracy.

## Related Articles

- [[Introduction to Matryoshka Embedding Models]] — HuggingFace official guide
- [[Matryoshka Embeddings - Faster OpenAI Vector Search]] — Supabase implementation
- [[Nearest Neighbor Indexes for Similarity Search]] — ANN infrastructure

## Related Concepts

- [[Matryoshka Embeddings]] — primary topic
- [[Dense Vector Retrieval]] — infrastructure
- [[Semantic Search]] — use case
- [[Retrieval Pipeline]] — two-pass search
- [[Bi-Encoder]] — underlying architecture
