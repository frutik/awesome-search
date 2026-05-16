---
title: "Wormhole Vectors"
aliases: ["wormhole embedding", "cross-space vectors", "traversal vectors"]
tags:
  - concept
  - search
  - embeddings
  - hybrid-search
---

# Wormhole Vectors

## Definition

Wormhole Vectors are a concept introduced by [[Trey Grainger]] to describe document or query vectors that exist meaningfully in *multiple* retrieval spaces simultaneously — bridging sparse (lexical), dense (semantic), and behavioral signal spaces.

The "wormhole" metaphor: just as a wormhole connects distant points in space-time, these vectors connect distant regions of separate retrieval spaces, enabling traversal from one space to another.

## Motivation

Traditional hybrid search combines sparse + dense with fusion (RRF, linear combination). This is a late-stage merge — each system retrieves independently, and results are merged afterward.

Wormhole Vectors represent an earlier, deeper integration: a single vector that *is itself* a bridge between spaces, rather than two vectors combined after retrieval.

## Three Retrieval Spaces

Grainger identifies three spaces that a comprehensive search system operates in:

1. **Sparse/Lexical space** — term-based retrieval (BM25, [[SPLADE]])
2. **Dense/Semantic space** — embedding-based retrieval ([[Bi-Encoder]], [[ColBERT]])
3. **Behavioral space** — click-through, purchase, engagement signals

Wormhole Vectors connect nodes across all three spaces.

## Practical Implementation

[[Dima Kan]]'s implementation at Aiven demonstrates wormhole vectors in production:
- Documents at intersection of sparse high-relevance AND dense high-relevance become "wormholes"
- Traversal: start in sparse space (fast keyword lookup) → follow wormhole → arrive in dense semantic neighborhood
- Result: semantic expansion without exhaustive ANN search

## Relation to [[Bag-of-Documents Model]]

[[Daniel Tunkelang]]'s [[Bag-of-Documents Model]] is conceptually related:
- Both treat queries as distributions over document spaces
- Both enable non-obvious connections between queries and documents
- Bag-of-Documents operates probabilistically; Wormhole Vectors operate geometrically

## Comparison with Standard Hybrid Search

| Approach | Integration Point | Complexity | Quality |
|----------|------------------|------------|---------|
| [[Hybrid Search]] (RRF) | Result merge | Low | Good |
| Linear combination | Score merge | Medium | Good |
| Wormhole Vectors | Vector space | High | Potentially better |

## Related Concepts
- [[Embeddings]] — parent concept
- [[Dense Embeddings]] — the dense space wormholes bridge from/to
- [[Sparse Embeddings]] — the sparse space wormholes bridge from/to

- [[Hybrid Search]] — standard approach wormhole vectors extend
- [[Sparse Vector Retrieval]] — one space wormholes bridge
- [[Dense Vector Retrieval]] — another space
- [[Bag-of-Documents Model]] — related probabilistic framing
- [[Bi-Encoder]] — dense component
- [[SPLADE]] — sparse component

## People

- [[Trey Grainger]] — invented the Wormhole Vectors concept; "AI-Powered Search" author
- [[Dima Kan]] — Aiven; practical implementation of wormhole vectors
