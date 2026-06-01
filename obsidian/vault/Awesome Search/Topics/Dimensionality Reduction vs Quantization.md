---
type: topic
title: Dimensionality Reduction vs Quantization
aliases:
  - DR vs quantization
  - vector compression techniques
tags:
  - topic
  - embeddings
  - vector-search
  - dimensionality-reduction
  - quantization
  - performance
related_concepts:
  - "[[Dimensionality Reduction]]"
  - "[[Vector Quantization]]"
  - "[[PCA]]"
  - "[[t-SNE]]"
  - "[[UMAP]]"
  - "[[Matryoshka Embeddings]]"
  - "[[Scalar Quantization]]"
  - "[[Binary Quantization]]"
  - "[[TurboQuant]]"
  - "[[BBQ]]"
related_topics:
  - "[[Search Platforms]]"
created: 2026-06-01
---

# Dimensionality Reduction vs Quantization

Both techniques compress embedding vectors to reduce memory and speed up ANN search. They operate on different axes and are **complementary, not mutually exclusive**.

## The Core Distinction

| | Dimensionality Reduction | Quantization |
|---|---|---|
| What changes | Number of dimensions | Bits per dimension |
| E.g. | 768-dim → 256-dim | float32 → int8 (or 1-bit) |
| Storage savings | Proportional to ratio | 4–32× (float32 baseline) |
| ANN speed gain | High (fewer multiply-adds) | High (SIMD integer ops) |
| Quality loss | Moderate (depends on data) | Low to moderate |
| Requires new model | Sometimes (Matryoshka) | No |
| Calibration data needed | Yes (PCA/UMAP) / No (Matryoshka) | Often (SQ, TurboQuant) / No (BQ) |

## Techniques Side by Side

### Dimensionality Reduction Methods

**[[PCA]]** — linear projection onto eigenvectors of maximum variance. One-time calibration on representative data; fast projection for new vectors. 2–4× compression is common; 6× starts introducing meaningful quality loss. Best when embedding dimensions have low-variance "dead zones."

**[[UMAP]] / [[t-SNE]]** — non-linear, cluster-preserving projections. Useful for *visualization* and exploratory analysis, but **not for search retrieval**: t-SNE is non-parametric (can't project new queries); UMAP can project new points but output isn't a meaningful distance space for ANN.

**[[Matryoshka Embeddings]]** — training-time technique; model is trained so the first N dimensions already form a good representation. No projection needed — just truncate. **Dimension-flexible at inference time**: choose 64, 128, 256, 512 without re-encoding. Requires a model trained with MRL; cannot be retrofitted to arbitrary embeddings.

### Quantization Methods

**[[Scalar Quantization]] (SQ8/SQ4)** — maps each float32 coordinate to int8 or int4 using a per-vector or per-dataset scale. 4× (SQ8) or 8× (SQ4) compression. Near-lossless at SQ8. Universal — works on any embedding model.

**[[Binary Quantization]] (BQ / [[BBQ]])** — maps each coordinate to 1 bit (sign: `>0 → 1`). 32× compression. Requires rescoring with original vectors for top results. Works best on *isotropic* embedding models (coordinates roughly zero-mean, equal variance). Elasticsearch's BBQ + OSQ achieves 10–40× query speedup.

**Product Quantization (PQ)** — splits vectors into subvectors; quantizes each subvector against a codebook. Cluster-based; higher compression than SQ but more information loss. Billion-scale systems (IVF-PQ).

**Rotation-based ([[TurboQuant]] / [[RaBitQ]])** — applies a random orthogonal rotation before quantizing; redistributes energy evenly across dimensions, compensating for anisotropy. Beats plain BQ by 9–24 pp recall at same compression. Qdrant 1.18 ships RaBitQ under the TurboQuant name.

## When to Use Each

**Use Matryoshka** if your embedding model supports MRL. It's the cleanest option: no calibration data, no projection math, dimension-flexible at query time. Choose dimension by latency/quality budget.

**Use SQ8 as the default** when you can't change the model. It's near-lossless, universally applicable, and gives a free 4× memory reduction.

**Use BQ/BBQ** when you need aggressive compression and can absorb rescoring cost. Benchmark recall degradation first — isotropic models (e.g., text-embedding-3) work well; others may not.

**Use PCA** when you're confident your embeddings have low-variance dimensions. Good empirical signal: explained-variance curve drops steeply after k components.

**Combine DR + Quantization** for maximum compression. PCA 768→256 (3×) followed by SQ8 (4×) = 12× total reduction with modest quality loss — better than either alone at the same storage budget.

**Avoid t-SNE/UMAP for retrieval**. Use them only for visualization and debugging (understanding cluster structure, spotting data quality issues).

## Compressibility Rules of Thumb

```
Matryoshka truncation:     quality degrades gracefully; test each tier
PCA (768 → 256):           ~5–10% recall loss on typical retrieval benchmarks
SQ8:                       ~1–3% recall loss; near-lossless
BQ without rescoring:      10–20% recall loss; unacceptable for most use cases
BQ with full rescoring:    ~3–5% recall loss; viable if latency allows
PCA + SQ8 combined:        ~6–12% recall loss; 12–16× compression
```

## The Structural Difference

Quantization changes the *number of bits* needed to represent a coordinate, which is a mathematical encoding choice. Dimensionality reduction changes *which* information you keep, which is a semantic choice. This is why they combine well: you're solving independent aspects of the memory problem.

## Related Notes

- [[Dimensionality Reduction]] — concept note covering PCA, t-SNE, UMAP, Matryoshka
- [[Vector Quantization]] — parent concept for SQ, BQ, PQ, TurboQuant
- [[PCA]] — linear DR; the main retrieval-safe option
- [[Matryoshka Embeddings]] — training-time DR; dimension-flexible
- [[BBQ]] — Elasticsearch's binary quantization
- [[TurboQuant]] — rotation-based quantization; state of the art

## Sources

### Dimensionality Reduction
- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — comparison overview with code
- [[Principal Component Analysis (PCA) In Depth]] — PCA algorithm step-by-step
- [[t-SNE Explained - Math and Intuition]] — t-SNE derivation
- [[t-SNE Clearly Explained]] — t-SNE with CNN application
- [[Exploring Hierarchical Navigable Small World]] — PCA as ANN preprocessing
- [[Introduction to Matryoshka Embedding Models]] — MRL training technique

### Quantization
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]] — OSQ vs TurboQuant benchmarks
- [[The Mathematics of Google's TurboQuant]] — rotation-based quantization deep dive
- [[TurboQuant in Qdrant]] — RaBitQ implementation; 9–24pp recall gain over BQ
- [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]] — binary quantization for ColBERT
