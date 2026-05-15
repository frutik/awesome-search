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

### Scalar Quantization (SQ)
Maps each float32 dimension to a smaller integer type (int8, int4). Simple, fast, widely supported.
- **int8 / SQ8**: 4× memory reduction; near-lossless quality
- **int4 / SQ4**: 8× reduction; slightly more quality loss

### Binary Quantization (BQ)
Maps each dimension to a single bit (positive → 1, negative → 0).
- **32× compression** vs. float32
- Similarity via Hamming distance (XOR + popcount) — extremely fast on CPU
- Works best when vectors are centered near zero (zero-mean distribution)
- Elasticsearch's **BBQ** (Better Binary Quantization) applies centering + rescoring to recover precision loss

### Optimized Scalar Quantization (OSQ)
Elastic's approach: uniform grid → integer arithmetic → SIMD-friendly operations.
- **10–40× faster** than float32 ANN on CPU
- Uses anisotropic loss function to weight high-magnitude dimensions more heavily
- Centroid centering before quantization to reduce distortion
- See: [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]]

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
| PQ | 32–64× | moderate | moderate |
| K-Quant (Q4_K_M) | ~8× | — (LLM weights) | minimal |

## Related Concepts
- [[Dense Vector Retrieval]]
- [[Approximate Nearest Neighbor Search]]
- [[BBQ]]
- [[GGUF]]
- [[Hybrid Search]]

## Articles
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]] — [[Thomas Veasey]]; OSQ vs TurboQuant CPU benchmarks

## People
- [[Thomas Veasey]] — Elastic; BBQ and OSQ design
