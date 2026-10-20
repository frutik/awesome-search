---
type: article
created: 2026-10-20
title: "MUVERA — Qdrant Multi-Vector Search Course (Module 3)"
source: "https://qdrant.tech/course/multi-vector-search/module-3/muvera/"
author: "[[Qdrant]]"
concepts: ["[[MUVERA]]", "[[Late Interaction]]", "[[HNSW]]", "[[Reranking]]", "[[LSH]]"]
topics: ["[[Late Interaction in Qdrant]]"]
tags: [multi-vector, muvera, qdrant, fastembed, late-interaction, course]
---

# MUVERA in Qdrant — Multi-Vector Search Course

A written lesson (with a Colab notebook) in [[Qdrant]]'s multi-vector search course, Module 3 "Scalability and Optimization". It explains why [[MUVERA]] is needed and how to use it in [[Qdrant Vector DB]] through [[FastEmbed]].

---

## Why HNSW Struggles with Multi-Vectors

The lesson argues that MaxSim is "inherently asymmetric and non-metric", so [[HNSW]] graph navigation works poorly on raw multi-vectors and searches fall back to full scans. MUVERA gives each document one representative vector that HNSW can index, in three stages: SimHash clustering ([[LSH]]), Fixed Dimensional Encoding, and random-projection dimensionality reduction.

## Implementation

- **FastEmbed 0.7.2+** — `LateInteractionMultimodalEmbedding` with model `Qdrant/colmodernvbert`, and `Muvera` from `fastembed.postprocess` built via `Muvera.from_multivector_model()`; `process_document()` / `process_query()` produce the encodings and `muvera.embedding_size` gives the dimension.
- **Parameters** — `k_sim=6` (2^6 = 64 buckets), `dim_proj=32`, `r_reps=20`.
- **Collection** — two named vectors: `muvera` (cosine) and `colmodernvbert` (cosine, `MultiVectorComparator.MAX_SIM`).
- **Query** — `query_points` with a `Prefetch` on `muvera` (limit 100), then MaxSim [[Reranking]] on `colmodernvbert` to a final top 10. Candidate sets are typically 100–1000 documents.

## Cost

Storage roughly doubles, because both the MUVERA vector and the full multi-vector sequence are kept. Offloading the original vectors to disk is the suggested mitigation. The lesson describes accuracy as near-identical to full multi-vector search but gives no benchmark figures.

## Related Concepts
- [[MUVERA]] · [[Late Interaction]] · [[HNSW]] · [[Reranking]] · [[LSH]]

## Related Topics
- [[Late Interaction in Qdrant]]

## Related Articles
- [[MUVERA - Multi-Vector Retrieval via Fixed Dimensional Encodings]]
- [[Scaling Late Interaction Retrieval in OpenSearch with MUVERA]] — reuses this lesson's FDE parameter guidance and FastEmbed snippet
- [[More Efficient Multi-Vector Embeddings with MUVERA]]

## Tools
- [[FastEmbed]] · [[Qdrant Vector DB]]
