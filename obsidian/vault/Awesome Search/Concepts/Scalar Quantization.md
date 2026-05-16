---
title: "Scalar Quantization"
aliases: ["SQ", "SQ8", "SQ4", "int8 quantization", "Optimized Scalar Quantization", "OSQ"]
tags:
  - concept
  - vector-search
  - quantization
  - performance
---

# Scalar Quantization

Maps each float32 dimension of a dense vector to a smaller integer type — independently, coordinate by coordinate. The simplest and most widely-used form of [[Vector Quantization]]. Works on any embedding distribution; no isotropy assumption required.

## How It Works

For each coordinate independently:
1. Determine the min/max range of values across the dataset (or segment)
2. Map the float32 range linearly onto the integer range
3. Store the integer; reconstruct float at score time via the inverse mapping

```
float32 value: 0.47
range: [-1.2, 1.4]   →   int8 range: [-128, 127]
encoded:  round((0.47 + 1.2) / 2.6 × 255 - 128)  =  35
```

## Variants

| Variant | Bits/dim | Compression | Recall impact |
|---------|----------|-------------|---------------|
| **SQ8** (int8) | 8 | **4×** | < 1% on most embeddings |
| **SQ4** (int4) | 4 | **8×** | 1–3% typically |
| **SQ6** | 6 | ~5.3× | Between SQ8 and SQ4 |

SQ8 is the practical default: near-lossless at 4× compression.

## Optimized Scalar Quantization (OSQ) — Elastic's Variant

Elasticsearch's production implementation adds:
- **Uniform integer grid** → every similarity computation becomes integer arithmetic (no float division per compare)
- **Anisotropic loss function** — weights high-magnitude dimensions more heavily when choosing quantization boundaries, since they contribute more to the dot product
- **SIMD arithmetic**: `_mm_maddubs_epi16`, AVX-512 integer dot products
- Result: **10–40× faster** HNSW traversal than float32 on CPU

See [[BBQ]] (which covers OSQ as part of Elasticsearch's quantization stack).

## vs. Other Quantization Methods

| Method | Compression | Recall | Distribution assumption |
|--------|-------------|--------|------------------------|
| **SQ8** | 4× | ~float32 | None — universal |
| [[Binary Quantization]] | 16–32× | Drops without rescoring | Zero-mean, isotropic |
| [[TurboQuant]] 4-bit | 8× | Competitive with SQ8 | Handles anisotropy via calibration |
| [[TurboQuant]] 2-bit | 16× | Beats BQ 2-bit by 9–24 pp | Handles anisotropy |
| Product Quantization | 32–64× | Moderate | Learned per dataset |

SQ is the **safest default**: works well regardless of embedding model. Switch to TurboQuant 4-bit to halve memory at similar recall.

## L1 compatibility

SQ works for all distance metrics including L1. Rotation-based methods ([[TurboQuant]], [[RaBitQ]]) preserve L2 norm but not L1 — making SQ the only option for L1 similarity.

## Where Used
- [[HNSW]] + SQ is the standard production combination in Elasticsearch, Qdrant, and Weaviate
- [[IVF]]-SQ: SQ applied inside each inverted list
- FAISS `IndexIVFScalarQuantizer`

## Related Concepts
- [[Vector Quantization]] — parent concept
- [[Binary Quantization]] — more aggressive compression; needs rescoring
- [[TurboQuant]] — rotation-based alternative; 4-bit beats SQ8 at 8× compression
- [[BBQ]] — Elasticsearch's OSQ + binary quantization stack
- [[HNSW]] — primary index combined with SQ in production
- [[IVF]] — IVF-SQ variant
- [[Dense Vector Retrieval]] — where SQ is applied
