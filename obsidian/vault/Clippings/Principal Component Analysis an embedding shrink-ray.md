---
title: "Principal Component Analysis: an embedding shrink-ray"
source: "https://softwaredoug.com/blog/2026/07/24/pca-shrink-ray"
author:
  - "[[Doug Turnbull]]"
published:
created: 2026-07-27
description: "Let's walk through basics of using PCA to reduce dimensionality of embeddings"
tags:
  - "clippings"
---
Embeddings take up a lot of space.

When I embed the [MSMarco passage corpus](https://ir-datasets.com/msmarco-passage.html) with the [384 dimension MiniLM model](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), I quickly get to ~14GB in memory embeddings:

```
9,000,000 records
x 384 dimensions
x 4 bytes per float 32
-------
~ 14GB
```

It doesn’t take much for millions of PDFs turn into billions of chunks, and petabytes of floats. An overwhelmed, expensive vector index can be no bueno.

Not where we want to spend time in a universe that has puppies and cool movies (about puppies).

Let’s shrink embeddings today with a common dimensionality reduction technique [Principal Component Analysis](https://en.wikipedia.org/wiki/Principal_component_analysis).

## How to find important components

One question we want to answer: what makes a dimension wasteful and redundant? Can we collapse those redundant dimensions into fewer dimensions?

Covariance matrices help find redundancy.

If we sample random (10-100K) or so of our billions of vectors, we now have a `10K x 384` matrix. We can compute the covariance matrix with a bit of NumPy code:

```
# Compute the mean of each dimension
mean = vectors.mean(axis=0)

# Center around the mean
centered = vectors - mean

# Compute a covariance matrix
covar = np.cov(centered, rowvar=False)
```

Now we have a 384 x 384 matrix where `covar[i, j]` stores the covariance between dimensions i and j.

Covariance measures how values vary together. If the i’th dimension is far from its mean at the same time the j’th dimension, then those dimensions might be redundant. Can we remove that redundancy?

![](https://softwaredoug.com/assets/media/2026/dim-reduction/image1.png)

Since I’m hungry, let’s use food as an example. Imagine hypothetical food embeddings where the 0th dimension is sweet-ness, 1st value is fruit-ness, and the 2nd is vegetable-ness. Dimensions 0 and 1 obviously vary together. The 2nd dimension does not vary with 0 and 1.

We might identify the fruit-sweetness-ness of a piece of food. By just looking at the fruit+sweet dimensions (0th and 1st) and ignoring others.

A way to score JUST that would be with vector: `[9, 5, 0, ...]` (weigh sweet dimension high, fruit second high, ignore vegetableness, etc).

Then we can score embedding `v` for this sweet-fruitness by multiplying through:

```
fruit_sweetness_score = 9*v[0] + 5*v[1] + 0 * v[2] + ...
```

We’ve now got a single number. If it’s close for two pieces of food they’re possibly similar. It’s possible, though, we have other factors to consider before making that determination. M&Ms, dark chocolate, apples, gum, and licorice differ quite a bit. Not to mention items OUTSIDE the set of sweet/fruit.

If ‘fruit-sweetness-ness’ weights correspond to c1, and some other hidden factors correspond to c2, then we can rewrite the matrix as a sum of components:

```
M = c1*c1T + c2*vcT + ... + c384*c384T
```

Each vector, c, here, known as an eigenvector, is one ‘component’ of the vector space. Hence, the name ‘principal component analysis’.

Some components here explain a lot of the original matrix. Others explain just the remaining table scraps. In reality, we factor out a weights, `λ1..λ384` aka eigenvalues. When we normalize `cN`, then `λN` just becomes the magnitude.

```
covar = λ1*c1*c1T + λ2*c2*c2T + ... + λ384*c384*c384T
```

Usually we sort these so that the highest eigenvalue comes first. Perhaps λ1 is 5000. Indicating we have a LOT of sweet/fruit foods described. Then we get towards the table scraps at the end λ383 which is maybe 0.05 (Vegemite?).

All this is a lame way of describing [eigendecomposition of a matrix](https://en.wikipedia.org/wiki/Eigendecomposition_of_a_matrix).

For a search person, what we’ve really done is decompose the matrix into a series of ‘scoring functions’ of decreasing importance. Each element of the vector weighs the input embeddings differently.

## Actually reducing dimensions

And since they’re of decreasing importance, we can truncate them. Then we have a lossy compressed version of the embeddings.

What we really want to do is take the 200 most important components, and ignore 184 of the remaining. We can do that. We remember 200 eigenvectors:

```
M = λ1*c1*c1T + λ2*c2*c2T + ... + λ200*c200*c200T
```

With 200 component vectors, how do we shrink the index?

An embedding `u` comes in, first we multiply `u` by c1, giving component 1s score:

```
c1_score: 0.54
```

We repeat for all 200 eigenvectors until we have a 200 dimension embedding that approximates the original 384 dimensions. But smaller. We’ve selectively lost the lowest priority information

```
c1_score: 0.54
...
c200_score: -0.12
```

In Python, shrinking the embeddings looks like:

```
# Compute eigenvalue decomposition
eigenvalues, eigenvectors = np.linalg.eigh(covar)
pca_eigens = eigenvectors[:, :200]

# Shrunk PCA embedding per 
pcad_vectors = np.empty((rows, 200), dtype=np.float64)
for idx, vector in enumerate(vectors):
    transformed = vector @ pca_eigens
    pcad_vectors[idx] = transformed
```

When a query comes in, we perform the same transformation:

```
# Force query into 200 dimensional space
query_transformed = query_vector @ pca_eigens
```

Then dot it into the:

```
scores = pcad_vectors @ transformed
```

## Running an experiment

When we compare PCA’d scoring to brute-force, ground-truth how does it stack up?

In this experiment ([code here](https://github.com/softwaredoug/vector-bench/blob/main/docs/PCA.md)), I take MSMarco, compute MiniLM embeddings, and perform PCA on 100K embeddings to get principal components.

We can see below the recall at PCA of 50, 100, and 200 out of 384. I also print out the eigenvalue %. Basically `np.sum(eigenvalues[:50]) / np.sum(eigenvalues)` which gives us a hint how much explanatory power is in this many dimensions.

| Dims | Eigenvalue % | Recall |
| --- | --- | --- |
| 50 | 42.04 | 0.2029 |
| 100 | 64.05 | 0.5714 |
| 200 | 88.5 | 0.879 |

PCA will depend heavily on the embedding model you choose and your corpus. A health-food grocery store might not have many “sweet” candy, but maybe a lot of fruit, for example. That might change how dimensions vary against each other.

Second, the efficiency of the embedding model itself matters a great deal. An embedding model already very efficiently distributed across dimensions won’t easily be shrunk. Given relatively flat eigenvalues, there’s little to compress. Imagine the 1st eigenvalue is 15 and the 384th is 13 you’re not going to get much effective shrinkage with PCA.

Finally, recall is only one metric here. It’s like a microbenchmark. Your domain might do fine with a recall of 0.879. Depending how you use embeddings in your final ranker, it may or may not matter. Other situations where the embedding becomes load-bearing ([nyuk nyuk](https://x.com/hosseeb/status/2035057152386375894)) may demand higher accuracy.

---

### Upcoming course: Build your own vector database

[![Build your own vector database](https://softwaredoug.com/assets/media/2026/vectordb-social.png)](https://maven.com/softwaredoug/vectordb)

Want to understand what makes embedding retrieval fast, relevant, and useful in real AI systems? Join [Build your own vector database](https://maven.com/softwaredoug/vectordb) and build the core pieces yourself, from embeddings and indexing to search and retrieval.

---