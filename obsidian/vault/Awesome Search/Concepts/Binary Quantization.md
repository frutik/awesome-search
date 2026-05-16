---
title: "Binary Quantization"
aliases: ["BQ", "1-bit quantization", "binarization", "Hamming distance search"]
tags:
  - concept
  - vector-search
  - quantization
  - performance
---

# Binary Quantization

Maps each float32 dimension of a dense vector to a single bit — the sign: positive → 1, negative → 0. The most aggressive standard form of [[Vector Quantization]]: **32× compression** vs float32, with similarity computed via Hamming distance (XOR + popcount) — natively fast on all CPU architectures.

## How It Works

```
float32 vector: [0.31, -0.72, 0.04, -0.55, ...]
binary:          [  1,    0,    1,    0,   ...]
stored:          packed bits, 1 bit per dimension
```

**Similarity**: Hamming distance = number of differing bits = `popcount(XOR(a, b))`. On modern CPUs, `POPCNT` is a single instruction; a 768-dim vector fits in 96 bytes (12× uint64), so a similarity computation is ~12 POPCNT instructions.

## Recall Characteristics

Vanilla BQ works well only on **isotropic, zero-mean** embeddings where dimensions are symmetrically distributed around zero. If vectors are not zero-mean, the sign threshold is biased and recall drops sharply.

- **Good fit**: isotropic models like OpenAI text-embedding-ada-002, Cohere v3
- **Poor fit**: embeddings with strong directional bias; domain-specific models without zero-centering

**Rescoring**: the standard fix for recall loss. Retrieve a large candidate set via BQ (fast), then rescore with full float32 vectors (accurate). Rescoring at 10× overretrieve recovers most of the recall loss.

## Variants and Improvements

### BBQ — Better Binary Quantization (Elasticsearch)
Elastic's production approach:
1. **Centroid centering** — subtract the dataset mean from all vectors before binarizing; reduces distribution bias
2. **Rescoring** — candidates reranked with full-precision dot products
Result: 32× compression with recall competitive with float32 after rescoring.
See [[BBQ]].

### Asymmetric BQ
Store vectors at 1-bit; compute query–document similarity with the query at higher precision (8-bit scalar). The asymmetry recovers recall without increasing stored memory. Qdrant uses this for TurboQuant 1-bit scoring.

### RaBitQ
[[RaBitQ]] (Gao & Long, SIGMOD 2024): rotation before binarization + per-vector length rescaling. The rotation equalizes coordinate variance; length rescaling corrects the systematic shortening caused by binarization. Bit-plane scoring for the asymmetric query path.

### TurboQuant 1-bit / 2-bit
[[TurboQuant]] at 1-bit (32×) and 2-bit (16×) compression consistently beats vanilla BQ by **9–24 pp recall** across 10 embedding datasets, via rotation + Lloyd-Max codebook + RaBitQ-style length renormalization.

## vs. Scalar Quantization

| | [[Scalar Quantization]] (SQ8) | Binary Quantization |
|---|---|---|
| Compression | 4× | 32× |
| Recall (no rescoring) | ~float32 | Significant drop |
| Recall (with rescoring) | ~float32 | Near-lossless |
| Speed | Fast integer SIMD | Fastest (POPCNT) |
| Distribution requirement | None | Isotropic / zero-mean |

## Where Used
- [[HNSW]] + BQ for memory-constrained deployments; always pair with rescoring
- [[IVF]]-Binary in FAISS
- [[BBQ]] — Elasticsearch's production BQ with centroid centering
- [[TurboQuant]] 1-bit / 2-bit — rotation-based successor; better recall at same storage

## Related Concepts
- [[Vector Quantization]] — parent concept
- [[Scalar Quantization]] — less aggressive alternative; works on all distributions
- [[BBQ]] — Elasticsearch's BQ with centering and rescoring
- [[TurboQuant]] — rotation-based; beats BQ at every compression level tested
- [[RaBitQ]] — rotation + binarization; contributes length renormalization and bit-plane scoring
- [[HNSW]] — primary index combined with BQ
- [[Dense Vector Retrieval]] — where BQ is applied
