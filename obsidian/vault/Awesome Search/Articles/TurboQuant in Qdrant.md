---
title: "TurboQuant in Qdrant"
aliases: ["TurboQuant Qdrant", "Qdrant TurboQuant 1.18"]
source: "https://qdrant.tech/articles/turboquant-quantization/"
author:
  - "[[Ivan Pleshkov]]"
  - "[[Jonas Schulz]]"
published: 2026-05-13
created: 2026-05-16
company: [Qdrant]
tags:
  - article
  - vector-quantization
  - qdrant
  - turboquant
  - rabitq
  - simd
  - performance
  - company-blog
concepts:
  - Vector Quantization
  - TurboQuant
  - RaBitQ
  - Dense Vector Retrieval
  - ANN
topics: []
---

# TurboQuant in Qdrant

**[[Ivan Pleshkov]] and [[Jonas Schulz]]** ([[Qdrant]]) describe TurboQuant — a rotation-based vector quantization algorithm from Google Research — shipping in Qdrant 1.18, with production-grade extensions on top of the original paper.

## The Compression Ladder

Before TurboQuant, Qdrant's quantization options:

| Method | Compression | Notes |
|--------|-------------|-------|
| Scalar Quantization (SQ) | 4× | int8 per coordinate; near-lossless |
| Binary Quantization (BQ) | 16× or 32× | Works well on isotropic models only |

TurboQuant adds a new path:

| TQ Variant | Compression | Key comparison |
|------------|-------------|----------------|
| TQ 4-bit | 8× | Competitive with SQ at half the storage |
| TQ 2-bit | 16× | Beats BQ 2-bit by 9–24 pp recall |
| TQ 1.5-bit | ~21× | Between 2-bit and 1-bit |
| TQ 1-bit | 32× | Beats BQ 1-bit by 9–21 pp recall |

## What TurboQuant Is

[[TurboQuant]] (Zandieh et al., 2026, arXiv:2504.19874) is a rotation-based quantization in the Product Quantization family:

1. **Apply a random orthogonal rotation** — redistributes per-coordinate variance evenly so coordinates approximate N(0,1)
2. **Quantize each coordinate** using a fixed Lloyd-Max codebook for the standard normal distribution — universal; no per-dataset training, no calibration set, no stored codebooks
3. **Score** via codebook lookup; the orthogonal rotation preserves dot products and L2 distances

Two paper variants: **MSE** (symmetric scoring, bit-efficient) and **PROD** (adds QJL projection to cancel length bias, splits the bit budget). Qdrant ships MSE — symmetric scoring is required for HNSW graph construction, and the length bias is fixed more cheaply via RaBitQ renormalization.

## What Qdrant Adds

Qdrant builds a hybrid of TurboQuant and [[RaBitQ]] (Gao & Long, SIGMOD 2024, arXiv:2405.12497), the other major rotation-based algorithm:

### Length Renormalization (from RaBitQ)
Vanilla MSE has a persistent length bias — quantized vectors are systematically shorter. Fix: store one per-vector scalar (ratio of original to reconstructed length), multiply back at score time. Cost: 4 bytes/vector, one multiply. Far cheaper than PROD's full QJL projection.

### Per-Coordinate Calibration (Anisotropy Compensation)
The N(0,1) rotation assumption breaks on anisotropic embeddings (real production data concentrates variance in a few directions). Fix: per-segment single pre-pass estimates a `(shift, scale)` pair per coordinate using the **P-Square algorithm** (streaming, constant memory) over a **reservoir sample** (Vitter's Algorithm R). Applied as `x → (x + shift) · scale` to align per-coordinate distribution with the Lloyd-Max grid. **Free at search time** — the correction folds into a per-query precomputation; the inner scoring loop is unchanged.

Isotropic data collapses to `(shift=0, scale=1)` — bit-identical to vanilla TurboQuant.

### L2 and Unnormalized Dot Support
Vanilla TurboQuant assumes unit-sphere inputs (cosine only). Qdrant stores the original L2 norm and reconstructs L2 via `‖q − v‖² = ‖q‖² + ‖v‖² − 2⟨q, v⟩`. **Cosine, dot, and L2 are first-class.** L1 is not supported — random orthogonal rotation preserves L2 norm, not L1.

### SIMD Acceleration
- **4-bit / 2-bit**: Codebook fits in one SIMD register; lookup via `pshufb`. Query scalar-quantized to `i8` halves for `_mm_maddubs_epi16`. On VNNI CPUs: `VPDPBUSD`; on ARMv8.2-A: `SDOT`
- **1-bit**: RaBitQ bit-plane scoring — data packed at 128 dims/16 bytes; query transposed into B bit-planes; inner product = `AND + popcount` per plane, weighted by `2^b`

## Benchmark Results (10 Datasets, HNSW m=16 ef_construct=128)

| Variant (compression) | arxiv-384 | arxiv-iXL | dbp-oai | cohere | h&m | laion |
|---|---|---|---|---|---|---|
| f32 (1×) | 0.9855 | 0.9419 | 0.9625 | 0.9446 | 0.9967 | 0.9897 |
| SQ (4×) | 0.9674 | 0.9285 | 0.8839 | 0.9014 | 0.9789 | 0.9276 |
| **TQ 4-bit (8×)** | **0.9442** | **0.9193** | **0.9299** | **0.9271** | **0.9739** | **0.9438** |
| TQ 2-bit (16×) | 0.8477 | 0.8227 | 0.8480 | 0.8303 | 0.9195 | 0.8349 |
| BQ 2-bit (16×) | 0.6948 | 0.6756 | 0.7332 | 0.6880 | 0.7018 | 0.5953 |
| TQ 1-bit (32×) | 0.7127 | 0.6763 | 0.7356 | 0.6300 | 0.8540 | 0.6807 |
| BQ asymmetric (32×) | 0.7070 | 0.5919 | 0.7072 | 0.6287 | 0.7802 | 0.5800 |
| BQ 1-bit (32×) | 0.6028 | 0.4683 | 0.6098 | 0.5409 | 0.6989 | 0.4762 |

Key patterns across all 10 datasets:
- TQ 4-bit beats SQ on 3/10 datasets (up to +4.6 pp on dbp-oai); within 2 pp on 9/10
- TQ 2-bit beats BQ 2-bit by **9–24 pp** on every dataset
- TQ 1-bit beats BQ 1-bit by **9–21 pp** on every dataset; still beats asymmetric BQ (8-bit query)

## Practical Decision Guide

| Current setup | Recommendation |
|---|---|
| SQ | Try TQ 4-bit — comparable recall, half the memory |
| BQ (any bit depth) | Try TQ at same storage budget — typically +10–20 pp recall |
| L1 similarity | Stay on SQ |

Migration: config change + re-index only. One-time per-segment calibration pre-pass runs in seconds.

## Related Concepts

[[Vector Quantization]] · [[TurboQuant]] · [[RaBitQ]] · [[BBQ]] · [[Dense Vector Retrieval]] · [[ANN]] · [[Embeddings]]

## People

- [[Ivan Pleshkov]] — Qdrant engineer; led implementation and authored companion deep-dive
- [[Jonas Schulz]] — Qdrant co-author

## Related Articles

- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]] — Elastic's benchmark of OSQ vs TurboQuant from the Elasticsearch side
