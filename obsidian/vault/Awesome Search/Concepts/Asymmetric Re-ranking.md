---
type: concept
title: "Asymmetric Re-ranking"
aliases: ["asymmetric reranking", "asymmetric closeness scoring", "asymmetric BQ re-ranking"]
tags:
  - concept
  - vector-search
  - quantization
  - reranking
  - performance
created: 2026-09-01
---

# Asymmetric Re-ranking

## Definition

Asymmetric re-ranking scores a **full-precision query embedding** directly against **binary-quantized document embeddings**, rather than requiring both sides of the comparison to be quantized (fast but lossier) or both full-precision (accurate but memory- and compute-heavy). Only one side of the comparison is quantized — hence "asymmetric."

## Why It's Needed

[[Binary Quantization]] compresses document embeddings aggressively (32× vs float32) but loses recall — the 1-bit-per-dimension representation is too coarse to rank precisely on its own. Rescoring against full-precision documents would recover that recall but defeats the point of quantizing in the first place. Asymmetric re-ranking recovers most of the lost precision cheaply: the query embedding is already available at full precision at query time, so scoring it against the existing BQ document vectors costs nothing extra in storage and very little extra in compute.

## The Vespa Implementation

[[Dainius Jocas]] describes an algebraic optimization of this scoring step in [[Vespa]], in [[Optimize Asymmetric Re-ranking with Algebra]]:

- Naive per-document form: `(q·(2·doc − 1) + 1) / 2`
- Algebraically equivalent rewrite: `q·doc + (1 − Σq)/2`

The rewrite isolates a `(1 − Σq)/2` term that depends only on the query, not the document. Vespa's constant-folding computes that term once per query (via a `query_bit_sum()` function) instead of recomputing it for every candidate document, leaving only a dot product against the unpacked document bits (`2 * unpack_bits(attribute(embeddings_bin)) - 1`) as per-document work.

Measured at 1M documents, the rewrite cut end-to-end latency 267ms → 193ms (28%), with raw re-ranking cost down to roughly 92–97 nanoseconds per document after optimization.

## Placement in the Ranking Pipeline

Recommended as a **second-phase** ranker over a first-phase BQ-based candidate set, kept to under ~1000 documents per thread to keep latency acceptable — consistent with [[Reranking]]'s general first-stage/second-stage split.

## Relation to Other Asymmetric Techniques

This is a specific instance of the broader asymmetric-scoring pattern already used elsewhere in vector quantization — e.g. Qdrant scores an 8-bit scalar-quantized query against 1-bit documents for its TurboQuant 1-bit path (see [[Binary Quantization]]). [[Vespa]]'s version goes further and keeps the query at **full float precision** rather than a lower-bit query representation.

Not to be confused with [[Asymmetric Semantic Search]], which is about query/document *length and structure* asymmetry (short query vs. long document) at the embedding-model level — a different axis from the precision asymmetry described here.

## Related Concepts

- [[Binary Quantization]] — the compression this technique recovers recall from
- [[Reranking]] — the general first-stage/second-stage architecture this fits into
- [[BBQ]] — Elasticsearch's binary quantization with centroid centering and rescoring, a related recall-recovery approach
- [[Vector Quantization]] — parent category
- [[Asymmetric Semantic Search]] — a distinct, unrelated sense of "asymmetric" in search

## Articles

- [[Optimize Asymmetric Re-ranking with Algebra]] — [[Dainius Jocas]]; the algebraic rewrite and Vespa benchmark

## People

- [[Dainius Jocas]]

## Companies

- [[Vespa]] — the engine this optimization is implemented in
