---
title: "Matryoshka embeddings: faster OpenAI vector search using Adaptive Retrieval"
source: "https://supabase.com/blog/matryoshka-embeddings"
author:
  - "[[gregnr]]"
  - "[[egor_romanov]]"
published: 2024-02-13
created: 2026-05-15
description: "How OpenAI's text-embedding-3 models use MRL to support shortened embeddings, and how Adaptive Retrieval achieves 99% accuracy with significant speed gains using pgvector."
tags:
  - clippings
  - company-blog
---
# Matryoshka embeddings: faster OpenAI vector search using Adaptive Retrieval

OpenAI's `text-embedding-3` models can shorten dimensions via a `dimensions` API parameter, powered by **Matryoshka Representation Learning (MRL)** — a training technique that embeds information at multiple granularity levels coarse-to-fine.

## How shortening works

Truncate from the end, then re-normalize (the normalization step is critical — truncating a unit vector breaks magnitude=1).

## Adaptive Retrieval

Two-pass search exploiting the sub-vector hierarchy:

1. **First pass** (fast, low-dim): ANN search at 512d → shortlist of `match_count × 8` candidates
2. **Second pass** (accurate, high-dim): KNN re-rank at full 3072d

### Results (1M DBpedia vectors)

| Method | Accuracy | QPS |
|---|---|---|
| Single-pass ANN 1536d | 89.2% | 670 |
| Adaptive Retrieval 512d→3072d | **99%** | 580 |

## pgvector implementation

```sql
-- Functional index on 512d sub-vectors
CREATE INDEX ON documents
USING hnsw ((sub_vector(embedding, 512)::vector(512)) vector_ip_ops)
WITH (m = 32, ef_construction = 400);

-- Two-pass query: first shortlist at 512d, re-rank at 3072d
```

## Key insights

- `text-embedding-3-large @ 256d` outperforms `ada-002 @ 1536d` (MTEB 62.0 vs 61.0)
- Optimal first-pass: **512d** (likely a training granularity)
- N-pass extension = **Funnel Retrieval** (MRL paper)
- Shorter first-pass vectors aren't always faster — lower accuracy requires retrieving more records


## Related Concepts

- [[Matryoshka Embeddings]]
- [[Dense Embeddings]]
- [[Dense Vector Retrieval]]
- [[Embeddings]]

## People

- [[gregnr]]
- [[egor_romanov]]
