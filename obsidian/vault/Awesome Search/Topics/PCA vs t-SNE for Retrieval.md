---
type: topic
title: "PCA vs t-SNE for Retrieval"
aliases: ["t-SNE vs PCA", "why t-SNE is not suitable for retrieval", "why not t-SNE for search", "visualization vs retrieval dimensionality reduction", "PCA vs t-SNE for search"]
tags: [topic, embeddings, vector-search, dimensionality-reduction, visualization]
related_concepts: ["[[PCA]]", "[[t-SNE]]", "[[UMAP]]", "[[Dimensionality Reduction]]", "[[Approximate Nearest Neighbor Search]]", "[[Vector Similarity Metrics]]", "[[Matryoshka Embeddings]]", "[[Dense Embeddings]]"]
related_topics: ["[[Dimensionality Reduction vs Quantization]]", "[[Search Platforms]]"]
articles: []
created: 2026-07-27
---

# PCA vs t-SNE for Retrieval

Both reduce embedding dimensionality, and the two are routinely presented side by side in tutorials — which produces a recurring mistake: reaching for [[t-SNE]] because it "looks better." It does look better. It is also structurally unusable for search, while [[PCA]] is not. The two are not competing implementations of one task; they solve **different tasks that happen to share an input**.

The whole comparison reduces to one question: *is the output a picture, or a space you can measure in?*

---

## The Core Distinction

| | [[PCA]] | [[t-SNE]] |
|---|---|---|
| What it learns | A projection **matrix** | A set of **coordinates** |
| New vector at query time | Matmul — trivially cheap | **Impossible** without refitting |
| Deterministic | Yes | No — random init, different layout per run |
| Objective | Minimize squared reconstruction error | Minimize KL(P‖Q) over neighbor probabilities |
| Distances preserved | Approximately (orthogonal projection) | Local only; global distances discarded |
| Typical target dims | 128–512 | 2–3 |
| Inverse transform | Yes | No |
| Fit for retrieval | **Yes** — the default linear option | **No** |

## The Intuition

Arrange a whole school in the playground so friends stand together. It makes a good photo. But there is no *rule* by which anyone was placed — so when a new pupil arrives, the only way to position them is to rearrange everyone, and the new arrangement puts everybody somewhere different. And while "standing close" means friends, "standing far apart" means nothing at all; the gaps are just whatever space the layout needed.

Search always has a new arrival — the query — on every request, and search answers are ordered by distance. t-SNE supplies neither a placement rule nor trustworthy distances.

## Why t-SNE Fails: Two Independent Disqualifiers

Either one alone rules it out.

### 1. Non-parametric — there is no transform to apply to a query

PCA learns a matrix; projecting a new vector is `x @ W`. t-SNE learns no transform at all. Its optimization *variables are the output positions themselves*, y₁…y_N, moved by gradient descent until KL(P‖Q) bottoms out. There is no function to call on a vector that was not in the fit.

Retrieval requires embedding the query into the same space as the documents, and every query is an unseen vector. The only recourse is refitting over corpus + query, which fails twice over:

- a full O(n log n) Barnes-Hut pass over the entire corpus, **per query**;
- the objective is non-convex with random initialization, so every run yields a different layout. Already-indexed document coordinates are no longer in the same space as the new output — the corpus needs reindexing on every query.

This is not a slow retrieval system; it is not a retrieval system.

### 2. The objective optimizes for something that is not ranking

Even granting a parametric variant, the output space still cannot rank. t-SNE minimizes KL divergence between neighbor *probability* distributions — not any distance-preservation loss.

**KL's asymmetry is the crux.** KL(P‖Q) charges heavily when p_ij is large but q_ij is small — true neighbors placed far apart. It charges almost nothing when p_ij is small but q_ij is large, so **false neighbors are nearly free**. A false neighbor at rank 1 is the worst failure mode in search, and it is exactly the one this loss declines to penalize.

**Between-cluster distance is deliberately discarded.** The Student-t heavy tail in low-D — t-SNE's fix for the crowding problem — maps every sufficiently distant pair to roughly the same tiny q_ij. Past a certain separation the gradient stops caring *how* far apart things are. Ranking is nothing but a claim about relative distances ([[Vector Similarity Metrics]]), so the quantity you would sort on is precisely the one t-SNE refuses to model.

**Perplexity is a horizon.** It fixes an effective neighborhood size (typically 5–50); structure beyond that radius is essentially unmodeled, making anything past a shallow top-k noise.

### And the target dimension is wrong anyway

t-SNE aims at 2–3 dimensions because crowding worsens as the target dimension rises — it is built for a screen. Retrieval compression wants 768→256, not 768→2. In the range that matters for [[Approximate Nearest Neighbor Search]], t-SNE offers no advantage while retaining every drawback.

## Why PCA Works

PCA is an **orthogonal linear projection**, and orthogonality is the whole reason it survives contact with retrieval: it approximately preserves inner products and Euclidean distances. Cosine ranking comes through degraded but structurally intact, so a query projected by the same matrix lands in a space where nearness still means what it meant at 768 dimensions.

It is also cheap and boring in the ways a query path needs — one matmul, deterministic, invertible (so original vectors can be reconstructed for rescoring), and fittable once offline on a representative sample.

The cost is real but bounded: PCA only earns its place when the eigenvalue spectrum is genuinely skewed, and degradation is steeply non-linear — on MiniLM / [[MS MARCO]], 1.9× compression holds 0.879 recall while 3.8× collapses to 0.5714 ([[Principal Component Analysis - an embedding shrink-ray]]). See [[Dimensionality Reduction vs Quantization]] for where PCA sits in a full compression chain.

## Where UMAP Sits

[[UMAP]] is the case that shows the two disqualifiers are genuinely independent. It **is** parametric — a real `transform()` exists — so disqualifier 1 disappears. But its cross-entropy objective carries the same local-structure bias; cluster spacing is more meaningful than t-SNE's without being a metric worth ranking on; and the transform is a fitted kNN-graph lookup, far heavier on the query path than a matmul.

Hence the vault's three-way verdict: **PCA is the default, UMAP is plausible but rarely worth it, t-SNE is disqualified.**

## The General Principle

This is not a quality gap between two dimensionality-reduction methods. It is a category difference:

- **Visualization DR** optimizes for *human perception of cluster structure*. Success is a legible picture. Distorting global distances is a feature — it buys separation on a screen.
- **Retrieval DR** optimizes for *metric fidelity*. Success is that ranking by distance in the small space matches ranking in the large one.

t-SNE's objective is not a weaker version of PCA's; it is a different one, and its distortions are deliberate. The heuristic generalizes: before adopting any dimensionality-reduction method for search, ask what its loss function actually rewards. If it does not reward distance preservation, it will not rank.

## Related Concepts

- [[PCA]] · [[t-SNE]] · [[UMAP]] — the three methods compared
- [[Dimensionality Reduction]] — parent concept
- [[Vector Similarity Metrics]] — what ranking actually measures
- [[Approximate Nearest Neighbor Search]] — the consumer of the reduced space
- [[Matryoshka Embeddings]] — DR moved into model training; free at query time

## Related Topics

- [[Dimensionality Reduction vs Quantization]] — the sibling comparison; where PCA fits in a stacked compression pipeline

## Sources

- [[PCA vs t-SNE vs UMAP - Visualizing the Invisible]] — three-way comparison with code
- [[PCA vs t-SNE - Which One Should You Use for Visualization]] — MNIST comparison
- [[t-SNE Explained - Math and Intuition]] — the KL objective and Student-t derivation
- [[t-SNE Clearly Explained]] — crowding problem and optimization tricks
- [[Principal Component Analysis - an embedding shrink-ray]] — measured recall-vs-dimensions on [[MS MARCO]]
- [[Principal Component Analysis (PCA) In Depth]] — PCA algorithm step-by-step
