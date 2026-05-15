---
title: "BBQ"
aliases: ["Better Binary Quantization", "Binary Quantization", "OSQ", "Optimized Scalar Quantization", "TurboQuant"]
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

TurboQuant (from the research community) uses non-uniform quantization levels optimized per-dataset. OSQ uses a uniform grid — simpler, more predictable, SIMD-native.

Elastic's benchmark: OSQ wins on CPU at practical recall levels (>0.9 recall@10); TurboQuant advantages appear at very high compression ratios or GPU hardware.

## Elasticsearch BBQ in Practice

```
- Index type: dense_vector with element_type: byte or bit
- bbq_hnsw: Elasticsearch's binary quantized HNSW index
- bbq_flat: flat scan with binary quantization
- Rescoring: num_candidates >> k, then exact rescore
```

## Related Concepts
- [[Vector Quantization]] — parent concept; BBQ is one strategy
- [[Dense Vector Retrieval]] — where BBQ is applied
- [[Approximate Nearest Neighbor Search]]
- [[GGUF]] — quantization for LLM weights (different domain)

## Articles
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]] — [[Thomas Veasey]]; detailed CPU benchmarks comparing OSQ and TurboQuant at various recall targets

## People
- [[Thomas Veasey]] — Elastic principal engineer; BBQ and OSQ designer
