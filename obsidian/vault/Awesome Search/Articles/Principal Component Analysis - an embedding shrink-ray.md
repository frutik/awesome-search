---
created: 2026-07-27
title: "Principal Component Analysis: an embedding shrink-ray"
source: "https://softwaredoug.com/blog/2026/07/24/pca-shrink-ray"
author: "[[Doug Turnbull]]"
published: 2026-07-24
type: article
tags: [article, PCA, dimensionality-reduction, embeddings, vector-search, eigendecomposition, recall]
concepts: ["[[PCA]]", "[[Dimensionality Reduction]]", "[[Embeddings]]", "[[Dense Vector Retrieval]]", "[[Precision and Recall]]"]
topics: ["[[Dimensionality Reduction vs Quantization]]"]
---

# Principal Component Analysis: an embedding shrink-ray

**Author:** [[Doug Turnbull]]

A walkthrough of using [[PCA]] to reduce embedding dimensionality, with a recall
experiment on [[MS MARCO]] quantifying what each level of compression costs.

## The Memory Problem

Embedding the MSMarco passage corpus with the 384-dimension MiniLM model:

```
9,000,000 records
x 384 dimensions
x 4 bytes per float 32
-------
~ 14GB
```

> "It doesn't take much for millions of PDFs turn into billions of chunks, and petabytes
> of floats. An overwhelmed, expensive vector index can be no bueno."

## Finding Redundancy Through Covariance

The question: *what makes a dimension wasteful and redundant, and can redundant dimensions
be collapsed?* Covariance matrices are how you find out.

Sample 10–100K vectors from the corpus to get a manageable `10K x 384` matrix:

```python
# Compute the mean of each dimension
mean = vectors.mean(axis=0)

# Center around the mean
centered = vectors - mean

# Compute a covariance matrix
covar = np.cov(centered, rowvar=False)
```

This yields a 384×384 matrix where `covar[i, j]` holds the covariance between dimensions
i and j. Covariance measures how values vary together — if dimension *i* sits far from its
mean at the same time as dimension *j*, the two may be redundant.

### The Food Analogy

Imagine food embeddings where dimension 0 is sweet-ness, 1 is fruit-ness, and 2 is
vegetable-ness. Dimensions 0 and 1 vary together; dimension 2 does not.

You could score "fruit-sweetness-ness" by weighting just those dimensions — a vector like
`[9, 5, 0, ...]`:

```
fruit_sweetness_score = 9*v[0] + 5*v[1] + 0 * v[2] + ...
```

That collapses two correlated dimensions into one number. But one number isn't the whole
story — "M&Ms, dark chocolate, apples, gum, and licorice differ quite a bit," and there are
foods outside the sweet/fruit set entirely. So you need more such factors.

## Eigendecomposition as Ranked Scoring Functions

If the fruit-sweetness weights are `c1` and other hidden factors are `c2`, the matrix
rewrites as a sum of components:

```
M = c1*c1T + c2*vcT + ... + c384*c384T
```

Each `c` is an **eigenvector** — one component of the vector space, hence *principal
component analysis*. Factoring out weights `λ1..λ384` (the eigenvalues), with normalized
`cN` making `λN` the magnitude:

```
covar = λ1*c1*c1T + λ2*c2*c2T + ... + λ384*c384*c384T
```

Sorted highest-eigenvalue-first, λ1 might be 5000 (a corpus with a *lot* of sweet/fruit
food described), trailing off to "table scraps" like λ383 ≈ 0.05 — "(Vegemite?)".

The reframing that matters for search practitioners:

> "For a search person, what we've really done is decompose the matrix into a series of
> 'scoring functions' of decreasing importance. Each element of the vector weighs the
> input embeddings differently."

## Actually Reducing Dimensions

Because the components are ordered by importance, you truncate — keep the top 200
eigenvectors, discard the other 184, and accept a lossy compression that "selectively
lost the lowest priority information."

Each incoming embedding `u` is scored against all 200 retained eigenvectors, producing a
200-dimension vector that approximates the original 384.

```python
# Compute eigenvalue decomposition
eigenvalues, eigenvectors = np.linalg.eigh(covar)
pca_eigens = eigenvectors[:, :200]

# Shrunk PCA embedding per 
pcad_vectors = np.empty((rows, 200), dtype=np.float64)
for idx, vector in enumerate(vectors):
    transformed = vector @ pca_eigens
    pcad_vectors[idx] = transformed
```

Queries must go through the *same* transformation to land in the same space:

```python
# Force query into 200 dimensional space
query_transformed = query_vector @ pca_eigens
```

## The Experiment

PCA'd scoring compared against brute-force ground truth. MSMarco corpus, MiniLM
embeddings, PCA fit on 100K embeddings.

| Dims | Eigenvalue % | Recall |
|---|---|---|
| 50 | 42.04 | 0.2029 |
| 100 | 64.05 | 0.5714 |
| 200 | 88.5 | 0.879 |

Eigenvalue % is `np.sum(eigenvalues[:50]) / np.sum(eigenvalues)` — "a hint how much
explanatory power is in this many dimensions."

The curve is steeply non-linear: 384→200 holds 0.879 recall, but 384→50 collapses to
0.2029. Compression quality does not degrade proportionally.

## Three Caveats

**Model and corpus dependent.** "PCA will depend heavily on the embedding model you choose
and your corpus." A health-food grocery store might carry little candy but lots of fruit —
changing how dimensions vary against each other.

**Efficient models resist compression.** A model already distributing information evenly
across dimensions won't shrink. Flat eigenvalues are the diagnostic:

> "Imagine the 1st eigenvalue is 15 and the 384th is 13 you're not going to get much
> effective shrinkage with PCA."

**Recall is one metric — "like a microbenchmark."** 0.879 may be fine depending on how
embeddings feed the final ranker. Cases where the embedding is load-bearing may demand
higher accuracy.

## Takeaway

PCA is the cheap, deterministic first thing to try on an oversized vector index: one
calibration pass over a 10–100K sample, a matrix multiply per vector, and an
explained-variance curve that signals in advance where quality will fall off. Inspect the
eigenvalue spectrum first — a flat spectrum means there is nothing to shrink.

## Related Concepts

- [[PCA]] — the technique in full
- [[Dimensionality Reduction]] — parent concept
- [[Vector Quantization]] — complementary axis: fewer bits rather than fewer dimensions
- [[Matryoshka Embeddings]] — training-time alternative needing no projection matrix
- [[Precision and Recall]] — the metric used here
- [[Dense Vector Retrieval]] — what the compressed vectors serve
- [[Approximate Nearest Neighbor Search]] — the index PCA is shrinking

## Related Topics

- [[Dimensionality Reduction vs Quantization]] — where PCA sits among compression options

## Sources

- Article: https://softwaredoug.com/blog/2026/07/24/pca-shrink-ray
- Experiment code: https://github.com/softwaredoug/vector-bench/blob/main/docs/PCA.md
- Corpus: https://ir-datasets.com/msmarco-passage.html
- Model: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- Course: https://maven.com/softwaredoug/vectordb — *Build your own vector database*
