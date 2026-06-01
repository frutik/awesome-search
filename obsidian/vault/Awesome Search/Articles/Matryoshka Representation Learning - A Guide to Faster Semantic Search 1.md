---
title: "Matryoshka representations: A guide to faster semantic search"
source: "https://ujjwalm29.medium.com/matryoshka-representation-learning-a-guide-to-faster-semantic-search-1c9025543530"
author:
  - "[[Ujjwal]]"
published: 2024-02-12
created: 2026-05-15
description: "Practical guide to MRL-powered semantic search: two-phase filtering with shortened embeddings achieves ~10x speedup on a 45K movie dataset."
tags:
  - clippings
  - medium
---
# Matryoshka Representations: A Guide to Faster Semantic Search

OpenAI's `text-embedding-3` models support dynamic embedding dimension adjustment via MRL (Matryoshka Representation Learning).

## Two-phase search strategy

Rather than comparing full embeddings against all indexed vectors:

1. **Phase 1**: Compare shortened query embeddings (256d) against truncated database embeddings
2. **Phase 2**: Re-rank top candidates using full-length embeddings

## Implementation (45K movie dataset)

Indexed ~45K movies (title + overview + genre) via OpenAI API with multithreading. Total cost: under $0.08.

Utility: `take the long embeddings, chop them off and normalize them` → shortened variants for phase 1.

## Results

| Query | Non-MRL | MRL |
|---|---|---|
| "the godfather" | 0.34s | 0.045s |

**~10x faster** while maintaining comparable result relevance.

Despite MRL having extra steps and 2 cosine similarity computations, shorter first-pass vectors dramatically reduce the search space.

## Key takeaway

MRL eliminates the need to maintain multiple models for different filtering levels — a single model serves both coarse and fine-grained search.


## Related Concepts

- [[Matryoshka Embeddings]]
- [[Dense Embeddings]]
- [[Embeddings]]
- [[Dense Vector Retrieval]]

## People

- [[Ujjwal]]
