---
title: "BBQ"
aliases: ["Better Binary Quantization", "Binary Quantization", "OSQ", "Optimized Scalar Quantization"]
tags:
  - concept
  - vector-search
  - performance
  - elasticsearch
---

# BBQ — Better Binary Quantization

Elasticsearch's production approach to aggressive vector compression, combining binary quantization with techniques that recover precision. Part of Elasticsearch's broader [[Vector Quantization]] story.

## The Core Idea

Naive binary quantization (sign of each dimension → 1 bit) is fast but lossy. BBQ adds:
1. **Centroid centering** — subtract the mean vector from all stored vectors before quantizing; reduces distortion from asymmetric distributions
2. **Rescoring** — BBQ candidates are reranked with full-precision dot products, recovering most of the lost recall

Net result: 32× memory reduction with recall competitive with float32.

## OSQ — Optimized Scalar Quantization

Elastic's companion technique: maps float32 dimensions to a uniform integer grid, enabling integer SIMD arithmetic.

- **10–40× faster** than float32 HNSW traversal on CPU hardware
- Uniform grid = every comparison becomes integer arithmetic (no float division)
- Uses **anisotropic loss** — weights high-magnitude dimensions more heavily when choosing quantization boundaries, since they contribute more to dot product
- CPU-friendly: leverages AVX2/AVX-512 SIMD without GPU requirement

## OSQ vs TurboQuant

[[TurboQuant]] (Google Research, Zandieh et al. 2026) uses a rotation + Lloyd-Max codebook approach. OSQ uses a uniform integer grid — simpler, SIMD-native.

- **Elastic's benchmark** (Thomas Veasey): OSQ competitive with TurboQuant at practical recall targets; OSQ wins on CPU throughput
- **Qdrant's benchmark** (10 datasets): TurboQuant 4-bit (8×) beats SQ on 3/10 datasets by up to 4.6 pp; TurboQuant 2-bit beats BQ by 9–24 pp across all datasets

## Elasticsearch BBQ in Practice

```
- Index type: dense_vector with element_type: byte or bit
- bbq_hnsw: Elasticsearch's binary quantized HNSW index
- bbq_flat: flat scan with binary quantization
- Rescoring: num_candidates >> k, then exact rescore
```

## Related Concepts
- [[Vector Quantization]] — parent concept; BBQ is one strategy
- [[Binary Quantization]] — the underlying 1-bit quantization BBQ extends
- [[Scalar Quantization]] — OSQ is Elastic's int8 companion technique
- [[Dense Vector Retrieval]] — where BBQ is applied
- [[HNSW]] — the index BBQ accelerates
- [[Approximate Nearest Neighbor Search]]
- [[GGUF]] — quantization for LLM weights (different domain)

## Articles
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]] — [[Thomas Veasey]]; Elastic's CPU benchmarks comparing OSQ and TurboQuant
- [[TurboQuant in Qdrant]] — [[Ivan Pleshkov]] & [[Jonas Schulz]]; Qdrant 1.18 implementation with anisotropy compensation and RaBitQ extensions

## People
- [[Thomas Veasey]] — Elastic principal engineer; BBQ and OSQ designer
