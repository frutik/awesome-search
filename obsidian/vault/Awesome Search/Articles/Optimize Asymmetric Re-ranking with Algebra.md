---
type: article
title: "Optimize Asymmetric Re-ranking with Algebra"
aliases: ["Asymmetric Ranking Optimization"]
source: "https://www.jocas.lt/notes/vespa/asymmetric-ranking-optimization-1/"
author:
  - "[[Dainius Jocas]]"
published: 2026-09-01
created: 2026-09-01
company: [Vespa]
tags:
  - article
  - vespa
  - binary-quantization
  - reranking
  - performance
concepts:
  - Asymmetric Re-ranking
  - Binary Quantization
  - Reranking
topics: []
---

# Optimize Asymmetric Re-ranking with Algebra

**[[Dainius Jocas]]** shows how to make [[Asymmetric Re-ranking]] — rescoring [[Binary Quantization|binary-quantized]] document embeddings against a full-precision query embedding — faster in [[Vespa]] by rewriting the scoring expression algebraically instead of changing the underlying math.

## The Setup

After a first-phase retrieval over binary-quantized (BQ) document embeddings, some of the recall BQ loses needs to be recovered. Rather than rescoring against full-precision documents (expensive), the full-precision query embedding — already available at no extra cost — is scored directly against the BQ document vectors. This is "the cheapest reranking to do" for clawing back recall lost to quantization.

## The Optimization

The naive per-document expression `(q·(2·doc − 1) + 1) / 2` is algebraically rewritten as `q·doc + (1 − Σq)/2`. The rewritten form separates out a `(1 − Σq)/2` term that depends only on the query, not the document, so Vespa's constant-folding computes it once per query (via a dedicated `query_bit_sum()` function) instead of once per document — the per-document work collapses to a single dot product against the unpacked bits (`2 * unpack_bits(attribute(embeddings_bin)) - 1`).

## Results

Benchmarked at 1M documents:
- End-to-end latency: 267ms → 193ms (28% improvement) after the rewrite
- Profiled totals: naive 562.884ms → rewritten 365.990ms → bare scoring 346.356ms
- Raw re-ranking cost after optimization: roughly 92–97 nanoseconds per document (~92ms per million documents)

The author recommends placing asymmetric re-ranking as a **second-phase** ranker, kept under ~1000 documents per thread to keep latency acceptable, and flags two further opportunities not yet implemented: accelerating the bit-unpacking step itself, and fusing bit-unpacking with the dot product via a specialized kernel.

## Related Concepts

[[Asymmetric Re-ranking]] · [[Binary Quantization]] · [[Reranking]] · [[Vector Quantization]]

## People

- [[Dainius Jocas]] — Vinted search engineer; author

## Companies

- [[Vespa]]
