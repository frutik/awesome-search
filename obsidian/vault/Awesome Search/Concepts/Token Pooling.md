---
title: "Token Pooling"
aliases: ["hierarchical token pooling", "vector pooling", "patch pooling"]
type: concept
tags:
  - concept
  - neural-ir
  - late-interaction
  - embeddings
  - performance
created: 2026-05-01
---

# Token Pooling

## Definition

Token pooling is a compression technique for **multi-vector (late interaction) embeddings** that reduces the number of stored vectors per document by clustering semantically similar token/patch vectors and replacing each cluster with its mean.

Originally proposed in the [[ColPali]] paper for visual document retrieval, applicable to any late interaction model including [[ColBERT]].

> [!info] Not to be confused with the other kinds of pooling
> "Pooling" names six unrelated operations in IR. This note covers **token pooling** —
> multi-vector compression. For sequence pooling (mean/CLS/max collapse into one vector),
> vocabulary pooling ([[SPLADE]]), judgment pooling ([[Judgment Lists]]), behavioral
> pooling, or MaxSim's score-matrix pooling ([[Late Interaction]]), start at [[Pooling]].

## How It Works

1. After encoding a document into token-level vectors `[v₁, v₂, ..., vₙ]`, group similar vectors using a clustering algorithm (e.g., hierarchical clustering)
2. For each cluster, compute the mean of all member vectors
3. Replace the cluster with this single aggregated vector
4. Result: `n` vectors → `n / pool_factor` vectors

```python
from colpali_engine.compression.token_pooling import HierarchicalTokenPooler

pooler = HierarchicalTokenPooler(pool_factor=3)
pooled = pooler.pool_embeddings(tensor)  # ~66.7% fewer vectors
```

## Pool Factor Guidelines

| Pool Factor | Vector Reduction | Performance Retention |
|-------------|-----------------|----------------------|
| 3 (recommended default) | 66.7% | 97.8% (ColPali paper) |
| High (100–200) | ~95%+ | ~5–10 vectors per doc — viable for nested HNSW indexing |

**Caveat**: Performance varies by dataset. Dense, text-heavy documents (e.g., "Shift" dataset) degrade more rapidly as pool factor increases — visual patch diversity matters.

## Why It's Useful

For [[ColPali]], each document page produces ~1000 vectors, making large-scale indexing prohibitively expensive. Token pooling makes the vector count manageable for production workloads without resorting to the full information loss of average-vector compression.

At high pool factors (100–200), the result is 5–10 vectors per document — small enough to index as nested dense vectors and leverage HNSW for first-stage retrieval, bridging the gap between average-vector compression and full late interaction.

## Relationship to Average Vectors

Average vector = token pooling with pool_factor = ∞ (one vector for the entire document). Token pooling offers a continuum from full [[Late Interaction]] fidelity down to single-vector [[Bi-Encoder]]-like representations.

## Related Concepts

- [[Late Interaction]] — the multi-vector architecture that creates the need for compression
- [[ColPali]] — primary use case; model that generates ~1000 vectors/page
- [[ColBERT]] — text-domain late interaction model, also benefits from pooling
- [[HNSW]] — can index pooled vectors when count is reduced enough (~5–10 per doc)
- [[Knowledge Distillation]] — adjacent compression strategy (model-level vs. representation-level)

- [[Pooling]] — the parent concept and the other four senses of the word
- [[Bi-Encoder]] — sequence pooling collapses to one vector; token pooling stops short of that

## Articles

- [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]]
