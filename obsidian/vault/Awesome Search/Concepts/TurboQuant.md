---
title: "TurboQuant"
aliases: ["TurboQuant quantization", "rotation-based quantization", "Zandieh quantization"]
tags:
  - concept
  - vector-search
  - quantization
  - performance
created: 2026-05-16
---

# TurboQuant

Rotation-based vector quantization algorithm from Google Research. **Zandieh et al., 2026** (arXiv:2504.19874). Now ships in [[Qdrant]] 1.18 with production extensions. Part of the [[Vector Quantization]] family; in the same design space as [[RaBitQ]].

## Core Algorithm

1. **Random orthogonal rotation** — every vector is rotated; redistributes per-coordinate variance evenly so coordinates approximate N(0, 1) post-rotation
2. **Coordinate-wise quantization** — fixed Lloyd-Max codebook for the standard normal distribution; **universal** — no per-dataset training, no calibration set, no stored codebooks; one lookup table works across all embeddings and dimensionalities
3. **Scoring** — reconstruct dot product directly from codebook indices; orthogonal rotation preserves dot products and L2 distances

## Two Paper Variants

| Variant | Description | Trade-off |
|---------|-------------|-----------|
| **MSE** | Literal recipe; codebook lookup only | Symmetric: any pair of stored vectors can be scored from indices alone |
| **PROD** | Adds QJL random projection to cancel per-vector length bias | Better bias correction; splits bit budget between codebook and projection |

Qdrant ships MSE: symmetric scoring is required for HNSW graph construction; the length bias is fixed more cheaply via RaBitQ renormalization.

## Compression Operating Points

| Variant | Bits/dim | Compression |
|---------|----------|-------------|
| 4-bit | 4 | 8× vs float32 |
| 2-bit | 2 | 16× |
| 1.5-bit | 1.5 | ~21× |
| 1-bit | 1 | 32× |

## Performance vs. Alternatives (Qdrant benchmarks, 10 datasets)

- **TQ 4-bit vs SQ (4×)**: competitive — within 2 pp on 9/10 datasets; beats SQ on 3/10 (up to +4.6 pp); half the storage
- **TQ 2-bit vs BQ 2-bit**: +9–24 pp recall on every dataset
- **TQ 1-bit vs BQ 1-bit**: +9–21 pp recall on every dataset; still beats asymmetric BQ

## Qdrant's Production Extensions

Beyond the paper: [[Qdrant]] adds length renormalization from [[RaBitQ]] (per-vector scalar, 4 bytes), per-coordinate anisotropy compensation (P-Square quantile calibration per segment, free at query time), full L2/dot/cosine support (stores original L2 norm), and SIMD kernels (AVX-VNNI/AVX-512/NEON).

## vs. Related Algorithms

| Algorithm | Quantization approach | Key difference |
|-----------|-----------------------|---------------|
| [[RaBitQ]] | Rotation + binarization | Length rescaling + bit-plane scoring; complements TurboQuant |
| [[BBQ]] / OSQ | Binary + centering | Elasticsearch; uniform integer grid; SIMD-optimized |
| Product Quantization | Sub-vector codebooks | Per-dataset trained; high compression, higher build cost |

## Articles
- [[TurboQuant in Qdrant]] — Qdrant 1.18 implementation, production extensions, full benchmarks
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]] — Elastic's OSQ vs TurboQuant benchmarks

## People
- [[Ivan Pleshkov]] — Qdrant; TurboQuant implementation
- [[Thomas Veasey]] — Elastic; OSQ/BBQ comparison benchmarks

## Related Concepts
- [[Vector Quantization]] — parent concept
- [[Scalar Quantization]] — baseline at 4× compression; TurboQuant 4-bit achieves 8× at comparable recall
- [[Binary Quantization]] — baseline at 16–32×; TurboQuant beats BQ by 9–24 pp at same storage
- [[RaBitQ]] — companion rotation-based algorithm; contributes length renormalization and 1-bit scoring
- [[BBQ]] — Elasticsearch's approach
- [[HNSW]] — TurboQuant's MSE variant chosen for HNSW compatibility (symmetric scoring)
- [[Dense Vector Retrieval]]
- [[ANN]]
