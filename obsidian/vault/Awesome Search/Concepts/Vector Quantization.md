---
title: "Vector Quantization"
aliases: ["Quantization", "ANN Quantization", "Embedding Quantization"]
tags:
  - concept
  - vector-search
  - performance
  - embeddings
---

# Vector Quantization

Compressing dense embedding vectors to reduce memory footprint and speed up similarity search, at the cost of some precision. Essential for scaling ANN indexes to billions of vectors.

## Why Quantize?

A full-precision (float32) 768-dim vector takes 3,072 bytes. At 100M documents that's ~300 GB — too large for RAM. Quantization trades a small recall loss for orders-of-magnitude reductions in memory and index size.

## Quantization Types

### [[Scalar Quantization]] (SQ)
Maps each float32 dimension to a smaller integer type (int8, int4). Simple, fast, widely supported.
- **int8 / SQ8**: 4× memory reduction; near-lossless quality
- **int4 / SQ4**: 8× reduction; slightly more quality loss

### [[Binary Quantization]] (BQ)
Maps each dimension to a single bit (positive → 1, negative → 0).
- **32× compression** vs. float32
- Similarity via Hamming distance (XOR + popcount) — extremely fast on CPU
- Works best when vectors are centered near zero (zero-mean distribution)
- Elasticsearch's **[[BBQ]]** (Better Binary Quantization) applies centering + rescoring to recover precision loss

### Optimized Scalar Quantization (OSQ)
Elastic's approach: uniform grid → integer arithmetic → SIMD-friendly operations.
- **10–40× faster** than float32 ANN on CPU
- Uses anisotropic loss function to weight high-magnitude dimensions more heavily
- Centroid centering before quantization to reduce distortion
- See: [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]]

### TurboQuant / RaBitQ (Rotation-Based)
New family of rotation-based quantization algorithms (2024–2026). Apply a random orthogonal rotation before quantization to equalize per-coordinate variance.
- **[[TurboQuant]]** (Google Research, Zandieh et al. 2026): Lloyd-Max codebook; universal (no per-dataset training); 4/2/1.5/1-bit operating points. Ships in [[Qdrant]] 1.18 with anisotropy compensation and SIMD kernels.
- **[[RaBitQ]]** (Gao & Long, SIGMOD 2024): binarization + per-vector length rescaling + bit-plane scoring. Qdrant borrows its length renormalization for TurboQuant.
- Key advantage: TurboQuant 4-bit (8×) is competitive with SQ (4×) at half the storage; TurboQuant 2-bit beats binary quantization by 9–24 pp recall

### Product Quantization (PQ)
Splits vectors into sub-vectors; each sub-vector quantized against a separate codebook.
- Very high compression (32–64×) with moderate quality
- Used in FAISS IVF-PQ indexes
- Higher encoder complexity than scalar methods

### K-Quants / I-Quants (GGUF)
Block-level quantization used in the [[GGUF]] format for LLM weights.
- **K-Quants** (Q4_K_M, Q5_K_S, etc.): mixed-precision per block; scale + min values stored separately
- **I-Quants** (IQ2_XS, IQ3_S, etc.): importance-matrix-guided; non-uniform quantization levels
- See: [[GGUF Quantization - A Technical Deep Dive]]

## Precision Recovery: Rescoring

Quantized indexes are fast for candidate retrieval but imprecise. Standard practice:
1. ANN search with quantized index → top-K candidates (e.g. 100)
2. Rescore candidates with full-precision vectors → final top-k (e.g. 10)

## Key Tradeoffs

| Method | Compression | Speed Gain | Recall Impact |
|--------|-------------|-----------|---------------|
| SQ8 | 4× | ~3–5× | <1% |
| Binary / BBQ | 32× | ~10–40× | 3–10% (with rescoring: <1%) |
| TurboQuant 4-bit | 8× | ~5–10× | ~1–2% vs SQ |
| TurboQuant 2-bit | 16× | high | 9–24 pp better than BQ |
| PQ | 32–64× | moderate | moderate |
| K-Quant (Q4_K_M) | ~8× | — (LLM weights) | minimal |

## Related Concepts
- [[Dense Vector Retrieval]]
- [[Approximate Nearest Neighbor Search]]
- [[HNSW]] — primary index combined with quantization
- [[IVF]] — IVF-SQ and IVF-PQ variants
- [[Scalar Quantization]] — int8/int4 per coordinate
- [[Binary Quantization]] — 1-bit per coordinate; Hamming distance
- [[BBQ]]
- [[TurboQuant]]
- [[RaBitQ]]
- [[GGUF]]
- [[Hybrid Search]]

## Articles
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]] — [[Thomas Veasey]]; OSQ vs TurboQuant CPU benchmarks
- [[TurboQuant in Qdrant]] — [[Ivan Pleshkov]] & [[Jonas Schulz]]; Qdrant 1.18 full implementation with RaBitQ extensions

## People
- [[Thomas Veasey]] — Elastic; BBQ and OSQ design
- [[Ivan Pleshkov]] — Qdrant; TurboQuant + RaBitQ hybrid implementation
