---
type: concept
title: "PCA"
aliases: ["Principal Component Analysis", "principal component analysis", "PCA", "eigenvector projection"]
tags:
  - concept
  - dimensionality-reduction
  - linear-algebra
  - embeddings
  - ml
created: 2026-06-01
---

# PCA (Principal Component Analysis)

## Definition

PCA is a linear dimensionality reduction technique that projects data onto a new coordinate system whose axes (principal components) are ordered by the amount of variance they explain. The first principal component captures the most variance; each subsequent one captures the next most, orthogonal to all previous.

## How It Works

1. **Standardize** — subtract mean, divide by std per feature
2. **Covariance matrix** — n×n matrix summarizing pairwise feature correlations
3. **Eigendecomposition** — eigenvectors = principal component directions; eigenvalues = variance explained
4. **Sort eigenvectors** by eigenvalue descending
5. **Project** — multiply original data by the top-k eigenvectors matrix → reduced representation

## Properties

| Property | Value |
|---|---|
| Type | Linear |
| Preserves | Global variance structure |
| Speed | Fast (one-pass, deterministic) |
| Parametric | Yes — reusable on new data |
| Inverse transform | Yes (lossy) |
| Suitable for ML | Yes |

## Relevance to Search

- Can reduce embedding dimensions (e.g., 768→256) before ANN indexing, cutting memory and speeding up search with modest quality loss
- Useful when embedding dimensions have near-zero variance (exploited in [[HNSW]] with PCA preprocessing)
- Alternative to [[Vector Quantization]]: DR reduces the *number* of dimensions; quantization reduces *bits per* dimension — both are often combined

## Fitting: Do You Need All the Vectors in Memory?

The worry is well founded for the naive path: ten million 1,024-dim float32 vectors is
~41 GB, and `sklearn.decomposition.PCA` does want its input array materialized.

But what PCA is *estimating* is a `d × d` object — a covariance matrix, or equivalently
the top-k right singular vectors — and that does not grow with the corpus. 1024² float64
is 8 MB whether you have ten thousand vectors or ten million. Corpus size is therefore a
property of **how you fit**, not of what PCA fundamentally needs: an implementation that
accumulates covariance over batches only has to stream the data, while sklearn's default
SVD paths decompose whatever array you hand them. The two practical routes below exploit
this from opposite ends — one shrinks the input, the other streams it.

Three ways to fit, in rough order of how often they are the right call:

### 1. Representative sample (usually enough)

Fit on a random sample and apply the resulting projection to everything. The eigenvector
directions stabilize long before the corpus is exhausted — you are estimating a `d × d`
covariance, and the measurements below found much smaller samples sufficient than
intuition suggests.

Two independent measurements bracket how small "enough" is:
[[Doug Turnbull]] fit on 100K vectors of a 9M-document corpus
([[Principal Component Analysis - an embedding shrink-ray]]), and [[Dylan Castillo]]
found a projection fit on **1,000 documents** performed almost identically to one fit on
the full corpus, and that a projection fit on a *different corpus* ([[MS MARCO]])
transferred usefully to unrelated datasets — down to 64 dims on a 1,536-dim model and 128
on a 4,096-dim one ([[Honey, I Shrunk the Embeddings - Matryoshka vs PCA]]).

Sample randomly, not by ingestion order — a prefix of a catalog is often one category.

### 2. Incremental PCA (bounded memory, exact-ish)

`sklearn.decomposition.IncrementalPCA` fits batch by batch, so peak memory tracks the
batch size rather than the corpus:

```python
from sklearn.decomposition import IncrementalPCA

pca = IncrementalPCA(n_components=256, batch_size=10_000)
for batch in batches:          # pass 1 — fit
    pca.partial_fit(batch)

for batch in batches:          # pass 2 — transform
    reduced = pca.transform(batch)
```

Two passes over the data, bounded RAM. Use it when you genuinely want the full corpus in
the fit — a heavily multi-modal catalog, or when a sample demonstrably shifts the
spectrum.

### 3. Regular PCA / randomized SVD

`PCA(svd_solver="randomized")` avoids a full decomposition and is what the default
`svd_solver="auto"` resolves to for large `d` with small `n_components`, but it still
wants the input array in memory.
Fine when the fitting set already fits — which, given option 1, it usually does.

### What you must store and re-apply

The fitted artifact is **the projection matrix and the mean vector**. PCA centers before
projecting, so the mean is part of the transform, not a detail of the fit.

The non-negotiable rule for retrieval: **the same fitted transform must be applied to
documents and to queries.** Fitting one projection on documents and another on queries
puts the two into different spaces and the similarity scores become meaningless. This
also makes the projection a versioned artifact — refitting it invalidates the entire
index, since old and new vectors no longer share a coordinate system.

Fitting on documents and applying to queries is the standard arrangement — stated
explicitly in Turnbull's write-up, and implied by Castillo's methodology.

## Measured Cost on Real Embeddings

[[Doug Turnbull]] measured recall against brute-force ground truth after PCA-compressing
MiniLM (384-dim) embeddings of the [[MS MARCO]] passage corpus, fitting PCA on 100K vectors
([[Principal Component Analysis - an embedding shrink-ray]]):

| Dims | Compression | Eigenvalue % | Recall |
|---|---|---|---|
| 200 | 1.9× | 88.5 | 0.879 |
| 100 | 3.8× | 64.05 | 0.5714 |
| 50 | 7.7× | 42.04 | 0.2029 |

The degradation is steeply non-linear — roughly halving dimensions is survivable, but pushing
to 7.7× collapses recall. Eigenvalue % (`np.sum(eigenvalues[:k]) / np.sum(eigenvalues)`) is the
share of variance retained, and it tracks recall loosely rather than predicting it exactly.

### The Flat-Spectrum Diagnostic

PCA only pays off where there is redundancy to harvest. If an embedding model already spreads
information evenly across dimensions, the eigenvalue spectrum is flat and nothing compresses:

> "Imagine the 1st eigenvalue is 15 and the 384th is 13 you're not going to get much effective
> shrinkage with PCA."

Inspect the explained-variance curve **before** committing to PCA — a steep drop after k
components means good compressibility; a flat curve means pick a different technique.
Compressibility also depends on the corpus, not just the model.

## Measured Against MRL Truncation

[[Dylan Castillo]] compared PCA against [[Matryoshka Embeddings|MRL]] truncation across eight
[[BEIR]] subsets, scoring nDCG@10 at the reduced dimension as a fraction of nDCG@10 at
full dimensions ([[Honey, I Shrunk the Embeddings - Matryoshka vs PCA]]):

| Dims | `3-small` trunc. | `3-small` PCA | `ada-002` trunc. | `ada-002` PCA |
|---|---|---|---|---|
| 512 | 98% | 97% | 96% | 99% |
| 256 | 94% | 95% | 89% | 96% |
| 128 | 86% | 90% | 83% | 89% |
| 64 | 71% | 82% | 66% | 78% |
| 32 | 46% | 65% | 41% | 59% |

The `ada-002` column is the interesting one: that model predates MRL, and PCA still
retained 78% at 64 dims. On this evidence PCA does not depend on the model having been
trained for truncation. The two methods track each other down to 256 and diverge below.

The same study also found the projection cheaper to calibrate than usually assumed — see
the fitting section above for those numbers.

These numbers are far gentler than [[Doug Turnbull]]'s recall table above, but they are
not in contradiction — different model (1,536d/4,096d API models vs 384d MiniLM),
different corpus, and nDCG retention rather than recall against brute-force ground truth.
A higher-dimensional model has more redundancy for PCA to harvest, which is the
reconciling variable worth checking first on any new model. Both were measured with exact
search, so neither says how the projected space behaves inside an ANN index.

## Limitations

- **Linear only** — cannot capture non-linear manifolds in the data
- Information loss is unavoidable (unless eigenvalues are zero)
- Principal components are hard to interpret in original feature terms

## Related Concepts

- [[Dimensionality Reduction]] — parent concept; also covers t-SNE, UMAP, Matryoshka
- [[t-SNE]] — non-linear alternative for visualization
- [[UMAP]] — non-linear alternative with parametric option
- [[Matryoshka Embeddings]] — training-time alternative; dimension-flexible without projection
- [[Vector Quantization]] — complementary compression approach
- [[HNSW]] — ANN index that benefits from reduced dimensionality
- [[MS MARCO]] — the corpus the compression numbers above were measured on

## Related Topics

- [[Dimensionality Reduction vs Quantization]] — how PCA compares to bit-level compression
- [[PCA vs t-SNE for Retrieval]] — why PCA's orthogonality makes it retrieval-safe where t-SNE is disqualified

## Articles

- [[Principal Component Analysis - an embedding shrink-ray]] — practical walkthrough with measured recall on [[MS MARCO]]
- [[Honey, I Shrunk the Embeddings - Matryoshka vs PCA]] — head-to-head against MRL truncation on [[BEIR]]; small-sample and out-of-domain fitting
- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — comparison with all three
- [[Principal Component Analysis (PCA) In Depth]] — step-by-step with worked example
- [[Understanding Principal Component Analysis (PCA)]] — applications focus
- [[PCA vs t-SNE - Which One Should You Use for Visualization]] — MNIST comparison
- [[Exploring Hierarchical Navigable Small World]] — PCA as ANN preprocessing option
