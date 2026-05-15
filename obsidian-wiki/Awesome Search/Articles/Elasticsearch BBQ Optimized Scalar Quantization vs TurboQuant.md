---
title: "Elasticsearch BBQ: Optimized Scalar Quantization vs. TurboQuant"
source: "https://www.elastic.co/search-labs/blog/elasticsearch-bbq-osq-vs-turbo"
author: "[[Thomas Veasey]]"
published: 2026-04-09
tags: [vector-search, quantization, BBQ, OSQ, TurboQuant, CPU-search, embeddings]
---

# Elasticsearch BBQ: Optimized Scalar Quantization vs. TurboQuant

**Author:** [[Thomas Veasey]] (Elastic)

## Summary

On CPU vector search, Elasticsearch's **OSQ** (Optimized Scalar Quantization, the algorithm behind BBQ) beats TurboQuant on throughput, ranking accuracy on real embeddings, and storage efficiency. TurboQuant wins on raw MSE but that advantage doesn't translate to better CPU search.

## Key Results (Apple M2 Max)

- OSQ symmetric kernels: **10-40x faster** than TurboQuant
- OSQ 1-bit (32x compression) beats TurboQuant 4-bit on ranking accuracy on shifted (real) embeddings, at 1/5 the storage
- TurboQuant wins on MSE, but that advantage comes entirely from Hadamard rotation, not from non-uniform centroids

## Why the Speed Gap

**OSQ uses uniform-grid quantization** → integer dot products → SIMD pipelines (popcount on ARM NEON, AVX)
- 1-bit: `popcount(a AND b)` via `vcntq_u8` → **7 ns/doc**
- 4-bit mixed kernel: 4 AND+popcount passes → **14 ns/doc**

**TurboQuant uses non-uniform centroids** → each coordinate pair requires data-dependent lookup from codebook → scalar float loads before FMA → **275 ns/doc** (at 1-bit)

## OSQ Design Choices

- **Anisotropic loss** (λ=0.1): `L = 0.9×(x·e)²/‖x‖² + 0.1×‖e‖²` — deliberately sacrifices MSE to concentrate accuracy along the query direction
- **Centroid centering**: segment centroid subtracted before quantization, removing shared component → frees quantizer range for information-bearing residual
- **Block-diagonal sparse preconditioner**: equalizes coordinate variances without Hadamard's power-of-2 padding overhead
- **1-bit documents / 4-bit queries**: documents at 32x compression, queries at 4-bit (queries are free, documents are the binding constraint)

## When TurboQuant Wins

- GPU hardware: gather operations are cheap on GPU shared memory
- Calibration-free settings: e.g., KV cache compression during LLM inference — one-time quantization, no training opportunity
- Applications needing calibrated scores (not just rankings)

## Practical Takeaway

For CPU-based vector search (Elasticsearch, most operational systems):
- Uniform grid + SIMD integer arithmetic >> non-uniform centroids + lookup tables
- Centroid centering exploits real-world embedding bias (shifted distribution) → 9x lower ranking noise than TurboQuant 1-bit on shifted data
- OSQ is already in production in Elasticsearch BBQ

## Related Concepts

- [[Dense Vector Retrieval]]
- [[Hybrid Search]]
- [[Search Architecture]]
- [[Vector Quantization]]
- [[BBQ]]