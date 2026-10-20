---
type: tool
title: "FastEmbed"
aliases: ["fastembed", "qdrant/fastembed"]
website: "https://qdrant.tech/documentation/fastembed/"
repo: "https://github.com/qdrant/fastembed"
maintainer: "[[Qdrant]]"
tags: [tool, embeddings, multi-vector, late-interaction, python]
created: 2026-10-20
---

# FastEmbed

[[Qdrant]]'s Python embedding library. Besides dense and sparse models it serves late-interaction multi-vector models ([[ColBERT]], ColModernVBERT) and, from version **0.7.2**, ships a [[MUVERA]] postprocessor that turns a multi-vector embedding into a fixed-dimensional single vector.

- Docs: https://qdrant.tech/documentation/fastembed/
- Repo: https://github.com/qdrant/fastembed

---

## MUVERA Postprocessing

`Muvera` lives in `fastembed.postprocess` and is built from a late-interaction model with `Muvera.from_multivector_model()` — the course example pairs it with `LateInteractionMultimodalEmbedding("Qdrant/colmodernvbert")` and `k_sim=6, dim_proj=32, r_reps=20`. `process_document()` and `process_query()` produce the asymmetric document/query encodings, and `muvera.embedding_size` gives the resulting dimension. The [[MUVERA in Qdrant - Multi-Vector Search Course|Qdrant course]] uses these encodings as the `prefetch` stage in [[Qdrant Vector DB]], with MaxSim reranking on the original multi-vectors.

FastEmbed is also how the AWS sample computes MUVERA encodings client-side for Amazon OpenSearch Service, where server-side plugins can't be installed ([[Scaling Late Interaction Retrieval in OpenSearch with MUVERA]]).

## Related Concepts
- [[MUVERA]] · [[Late Interaction]] · [[ColBERT]] · [[SPLADE]] · [[Multimodal Embeddings]]

## Related Topics
- [[Late Interaction in Qdrant]] · [[Late Interaction in OpenSearch]]

## Related Articles
- [[MUVERA in Qdrant - Multi-Vector Search Course]]
- [[Scaling Late Interaction Retrieval in OpenSearch with MUVERA]]
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 1]] — CLIP embeddings via `fastembed`
