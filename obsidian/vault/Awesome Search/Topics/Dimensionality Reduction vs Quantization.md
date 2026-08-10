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
  - "[[RaBitQ]]"
  - "[[IVF]]"
  - "[[BBQ]]"
related_topics:
  - "[[Search Platforms]]"
  - "[[Vector Search Tradeoffs]]"
created: 2026-06-01
---

# Dimensionality Reduction vs Quantization

Both techniques compress embedding vectors to reduce memory and speed up ANN search. They operate on different axes and are **complementary, not mutually exclusive**.

## Hot Take: The "vs" Is a False Taxonomy

The framing is wrong. These are not two answers to one question — they are two independent multipliers on the same quantity:

```
bytes per vector  =  dimensions  ×  bits per dimension
```

Dimensionality reduction shrinks the left factor, quantization the right. Asking "PCA or quantization?" is like asking whether to reduce a rectangle's area by narrowing it or by shortening it. They are also different *kinds* of decision: quantization changes the number of bits used to encode a coordinate, a mathematical encoding choice, while dimensionality reduction changes *which* information you keep at all, a semantic one. The production answer is almost always **both**, and the interesting question is the **order of operations**, not the choice.

### The stacked pipeline

[[Doug Turnbull]]'s stated preference (Relevance Slack, 2026-07-27) is a three-stage chain:

```
PCA  →  random rotation (TurboQuant-style)  →  scalar quantization
```

Each stage exists to fix the problem the previous one leaves behind:

1. **[[PCA]]** discards low-variance directions *in a principled way* — variance-ranked, rather than letting a quantizer spend equal bits on signal and noise alike. You drop information you can defend dropping.
2. **Random rotation** repairs what PCA creates. PCA output is maximally *anisotropic* by construction: variance is concentrated in the leading components and near-zero in the tail. That is precisely the worst input for a uniform per-coordinate quantizer, which assumes every coordinate carries comparable range. An orthogonal rotation re-spreads energy evenly without changing distances — the entire insight behind [[TurboQuant]] and [[RaBitQ]].
3. **[[Scalar Quantization]]** then operates on a well-conditioned, isotropic space where its uniform-bucket assumption actually holds.

Run stages 1 and 3 without stage 2 and the combination underperforms — which is likely why "DR vs quantization" gets read as a trade-off at all. The naive stack *is* disappointing. The rotated stack is not.

### The real decision axis: where you pay the fit cost

The genuine distinction isn't "reduce dimensions or reduce bits" — it's **how much offline training each stage demands**, a point raised by Mohammad Hasnain in the same thread:

| Technique | Offline fit required |
|---|---|
| [[Binary Quantization]], scalar bit quantization | None — sign/range rules only |
| [[PCA]] | Yes — eigendecomposition on a representative sample |
| Product Quantization, [[IVF]] | Yes — codebook / centroid training |
| Random rotation ([[TurboQuant]]) | No — the rotation is data-independent |
| [[Matryoshka Embeddings]] | Yes, but paid at *model* training time |

That table is the one worth reasoning over. [[Matryoshka Embeddings]] makes the point sharply: MRL is dimensionality reduction with the fit cost pushed all the way back into pretraining, leaving truncation free at query time. It is not an alternative to quantization — MRL-truncated vectors get quantized too.

### Where the hot take does not apply

Stacking is not free and not universal. PCA only earns its place when the spectrum is genuinely skewed; a flat eigenvalue curve ("1st eigenvalue is 15 and the 384th is 13") means an already-efficient model with no redundancy to harvest, and you have added a projection to your query path for nothing. Measure the explained-variance curve before assuming the first stage belongs in the chain.

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

*Measured data point* ([[Principal Component Analysis - an embedding shrink-ray]], MiniLM on [[MS MARCO]]): 1.9× (384→200) → 0.879 recall; 3.8× (384→100) → 0.5714; 7.7× (384→50) → 0.2029. Degradation is steeply non-linear, and the usable ceiling here sits closer to 2× than 4× — confirming that the compression budget must be measured per model and corpus rather than assumed.

**[[t-SNE]]** — non-linear, cluster-preserving projection. **Disqualified for retrieval**, on two independent grounds: it is non-parametric (there is no transform to apply to a new query), and its KL objective does not preserve distance. Visualization and exploratory analysis only.

**[[UMAP]]** — non-linear but *parametric*, so it can project new points. Plausible for retrieval, rarely worth it: the cross-entropy objective keeps a local-structure bias, cluster spacing isn't a metric to rank on, and `transform()` is a kNN-graph lookup rather than a matmul. See [[PCA vs t-SNE for Retrieval]] for why the two verdicts differ.

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

**Use PCA** when you're confident your embeddings have low-variance dimensions. Good empirical signal: explained-variance curve drops steeply after k components. The inverse is the disqualifier — a flat eigenvalue spectrum ("1st eigenvalue is 15 and the 384th is 13") means an already-efficient model with no redundancy to harvest.

**Combine DR + Quantization** for maximum compression. PCA 768→256 (3×) followed by SQ8 (4×) = 12× total reduction with modest quality loss — better than either alone at the same storage budget. Insert a random rotation between the two stages; PCA output is anisotropic by construction, which is the worst case for a uniform quantizer (see the hot take above).

**Avoid t-SNE/UMAP for retrieval**. Use them only for visualization and debugging (understanding cluster structure, spotting data quality issues).

## A Dissenting Benchmark

The advice above — MRL first where the model supports it — is not universally held.
[[Dylan Castillo]] ran the direct comparison on eight [[BEIR]] subsets and reached the
opposite conclusion ([[Honey, I Shrunk the Embeddings - Matryoshka vs PCA]], August 2026):

> "PCA not only held its own against MRL truncation, it won on most dimensions."

nDCG@10 retained relative to full dimensions, `text-embedding-3-small` (1,536d):

| Dims | MRL truncation | PCA |
|---|---|---|
| 512 | 98% | 97% |
| 256 | 94% | 95% |
| 128 | 86% | 90% |
| 64 | 71% | 82% |
| 32 | 46% | 65% |

Two secondary findings, if they hold up, would weaken the calibration-cost argument in
the table above: a projection fit on **1,000 documents** performed almost identically to
one fit on the full corpus, and a projection fit **out of domain** on [[MS MARCO]] held
up through 64 dims on a 1,536-dim model and 128 on a 4,096-dim one. On that evidence PCA's offline fit is a much smaller operational
burden than "requires representative data" suggests.

**This is one practitioner's study and the guidance above stands unchanged.** It is
three models (two from the same vendor), exact search over raw vectors rather than a
real ANN index, and the largest BEIR datasets excluded on budget. The ANN omission
matters most: PCA output is anisotropic by construction, which is exactly the property
the rotation stage above exists to repair, and a brute-force methodology cannot see that
cost. Note too that the gap nearly vanishes on the 4,096-dim `qwen3-embedding-8b`
(84% vs 83% at 64 dims), so the headline may be as much about `3-small`'s dimensionality
budget as about the two methods.

Set against it, [[Doug Turnbull]]'s numbers on MiniLM/[[MS MARCO]] are far harsher on PCA
(recall 0.2029 at 384→50). Different model, corpus and metric, so the two do not
adjudicate each other — which is the practical takeaway: measure the compression curve
on your own model and corpus rather than importing either verdict.

## Compressibility Rules of Thumb

```
Matryoshka truncation:     quality degrades gracefully; test each tier
PCA (768 → 256):           ~5–10% recall loss on typical retrieval benchmarks
SQ8:                       ~1–3% recall loss; near-lossless
BQ without rescoring:      10–20% recall loss; unacceptable for most use cases
BQ with full rescoring:    ~3–5% recall loss; viable if latency allows
PCA + SQ8 combined:        ~6–12% recall loss; 12–16× compression
```

## Related Notes

- [[Dimensionality Reduction]] — concept note covering PCA, t-SNE, UMAP, Matryoshka
- [[Vector Quantization]] — parent concept for SQ, BQ, PQ, TurboQuant
- [[PCA]] — linear DR; the main retrieval-safe option
- [[Matryoshka Embeddings]] — training-time DR; dimension-flexible
- [[BBQ]] — Elasticsearch's binary quantization
- [[TurboQuant]] — rotation-based quantization; state of the art
- [[Vector Search Tradeoffs]] — the parent hub; this note owns the bytes-per-vector axis, which interacts with index choice, filtering, and update cost

## Sources

### Dimensionality Reduction
- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — comparison overview with code
- [[Principal Component Analysis (PCA) In Depth]] — PCA algorithm step-by-step
- [[t-SNE Explained - Math and Intuition]] — t-SNE derivation
- [[t-SNE Clearly Explained]] — t-SNE with CNN application
- [[Exploring Hierarchical Navigable Small World]] — PCA as ANN preprocessing
- [[Introduction to Matryoshka Embedding Models]] — MRL training technique
- [[Principal Component Analysis - an embedding shrink-ray]] — PCA walkthrough with a measured recall-vs-dimensions table on [[MS MARCO]]
- [[Honey, I Shrunk the Embeddings - Matryoshka vs PCA]] — [[Dylan Castillo]]; PCA vs MRL truncation head-to-head on [[BEIR]], plus small-sample and out-of-domain fitting results

### Quantization
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]] — OSQ vs TurboQuant benchmarks
- [[The Mathematics of Google's TurboQuant]] — rotation-based quantization deep dive
- [[TurboQuant in Qdrant]] — RaBitQ implementation; 9–24pp recall gain over BQ
- [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]] — binary quantization for ColBERT

### Practitioner Discussion
- Relevance Slack thread, 2026-07-27 ([[Search Communities]]) — [[Doug Turnbull]] on stacking PCA → random rotation → scalar quantization as a preferred flow; Mohammad Hasnain on the training-cost distinction between PCA, PQ/IVF, and scalar/binary quantization
