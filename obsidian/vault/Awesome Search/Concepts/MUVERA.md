---
title: "MUVERA"
aliases: ["Multi-Vector Retrieval via Fixed Dimensional Encodings", "Fixed Dimensional Encoding", "FDE"]
tags:
  - concept
  - search
  - neural-ir
  - multi-vector
  - late-interaction
---

# MUVERA

## Definition

**MUVERA** (Multi-Vector Retrieval via Fixed Dimensional Encodings) collapses a [[Late Interaction]] multi-vector representation (e.g. [[ColBERT]]'s per-token matrix) into a **single fixed-dimensional vector** that approximates the MaxSim score under an ordinary inner product. This lets a multi-vector document be retrieved with standard single-vector ANN ([[HNSW]]) in the first stage, sidestepping the cost of full MaxSim during candidate generation.

## Why It Matters

The central problem of late interaction is that MaxSim compares every query vector against every document vector — too expensive for first-stage retrieval over a large corpus. MUVERA provides a cheap, ANN-indexable proxy:

1. **Stage 1** — encode query and documents as fixed-dimensional MUVERA vectors, retrieve top-k candidates with fast single-vector ANN.
2. **Stage 2** — rerank those candidates with the full multi-vector MaxSim ([[ColBERT]]).

This is the single-vector "approximation of the multivector" that plays the same role as Elastic's **average vectors** — a compressed stand-in for the first stage.

## In Practice

[[Qdrant Vector DB]] supports MUVERA as a first-stage `prefetch` representation, then reranks with a ColBERT multivector field in the same Query API call (`using="muvera"` → `using="colbert"`). See [[Late Interaction in Qdrant]].

## Related Concepts

- [[Late Interaction]] — the architecture MUVERA accelerates
- [[ColBERT]] — the multi-vector model MUVERA approximates
- [[HNSW]] — single-vector ANN index MUVERA makes usable for late interaction
- [[Token Pooling]] — alternative multi-vector compression (clusters vectors rather than collapsing to one)
- [[Bi-Encoder]] — the single-vector baseline MUVERA imitates for stage 1

## Related Topics

- [[Late Interaction in Qdrant]] — where MUVERA is used as the prefetch stage
- [[Late Interaction in Elasticsearch]] — "average vectors" play the analogous role there
