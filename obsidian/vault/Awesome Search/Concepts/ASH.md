---
type: concept
title: "ASH"
aliases: ["Asymmetric Scalar Hashing", "asymmetric scalar hashing"]
tags:
  - concept
  - vector-search
  - quantization
  - dimensionality-reduction
  - ann
created: 2026-08-10
---

# ASH — Asymmetric Scalar Hashing

**ASH (Asymmetric Scalar Hashing)** compresses database vectors by first projecting them
into fewer dimensions with a projection *learned from the data*, then quantizing what
remains. Queries are projected the same way but never quantized. Mariano Tepper
([[Elastic]]) and Theodore Willke (IBM WatsonX),
[arXiv:2606.07870](https://arxiv.org/abs/2606.07870), 5 June 2026.

## The Central Claim

Given a fixed number of bits you are willing to spend per vector, you are better off
keeping **fewer dimensions at more bits each** than keeping every dimension at one bit.
Both cost the same on disk. The paper measures the first option winning consistently —
better recall *and* better latency, since a shorter vector is also faster to compare.

The second claim is that the reduction must be **learned**. A random projection at the
same budget does measurably worse, and the gap widens the more dimensions you drop.

## How It Works, Conceptually

1. **Cluster and re-center.** The corpus is clustered, and each vector is expressed
   relative to its nearest cluster centre. This matters because embeddings are lopsided —
   they clump on one side of the space rather than spreading evenly — and re-centering
   makes the distribution more even before anything is compressed. Accuracy improves with
   more clusters, flattening out around 64.
2. **Project down, using a learned direction set.** This is [[PCA]] followed by a rotation
   that is tuned for the quantizer that comes next — not just "keep the highest-variance
   directions," but "keep directions that will survive being rounded to a few bits."
3. **Quantize the survivors** to a small number of bits per dimension.
4. **Decode when scoring.** Because the projection is a rotation-like operation, it
   preserves vector length exactly; the only error introduced is in direction.

The rotation is fitted by alternating between "given the current rotation, what are the
best codes" and "given those codes, what is the best rotation," repeatedly. It converges
in 20–30 rounds and needs a training sample proportional to the embedding's dimensionality
rather than to the corpus size — on a million-vector, 3,072-dimension set reduced to half
its dimensions, fitting took under 10 seconds and encoding the whole corpus under 3. (Fit
time roughly triples if you keep every dimension, which is part of the argument for
reducing: the configuration that searches better also trains faster.)

## What Is Actually Asymmetric

The name misleads slightly. **The query does go through the same learned projection as the
documents.** What it escapes is *quantization* — the query stays full precision, so no
rounding error is added on the query side. That is the same asymmetry product quantization
introduced in the 2010s.

Keeping the query side simple is also what makes it fast: the projection is applied once
per query rather than undone once per comparison, and thousands of comparisons happen per
query.

So ASH is **not** an exception to the rule that documents and queries must share one
fitted transform — it follows that rule. See [[PCA]] for why that makes the fitted
projection an index-versioning problem.

## It Generalizes Older Methods

The paper's most useful structural point: several existing methods turn out to be ASH with
pieces switched off.

| Method | Is ASH with… |
|---|---|
| [[ITQ]] | one bit per dimension |
| [[RaBitQ]] | no dimensionality reduction, one cluster, a *random* rotation instead of a learned one |

So the rotation-based binary quantizers occupy the data-agnostic, no-reduction corner of a
larger design space.

## Why "Embeddings Aren't Isotropic" Matters Here

[[TurboQuant]] and EDEN assume vectors are spread evenly over the sphere, and their
theoretical guarantees depend on that. The paper measures real embedding sets and finds
they are not — they are noticeably off-centre and occupy a narrower cone than uniform data
would. The guarantees therefore do not transfer to real embeddings, and much of the
available code space goes unused. ASH's clustering-and-re-centering step is a direct
response to this.

## Measured Results

Against [[RaBitQ]] at the higher compression setting: 2.3–7.1 points better recall, and
over 12× faster at RaBitQ's own best-recall operating point. Against product quantization
with FastScan: 6.3–22.9 points better. It also beats LOPQ, EDEN, [[TurboQuant]] and
LeanVec. In several configurations ASH matches alternatives that spend **twice** the bits.

Measured on embedding corpora at 100K and 1M scale — gecko, nv-qa-v4, ada-002,
openai-3072, cohere, mpnet — inside an [[IVF|inverted index]], single-threaded.

## Limitations

- The projection is **linear**; the authors name deeper alternatives as future work.
- Clusters and projection are learned in separate stages, not jointly.
- No out-of-distribution query handling, which LeanVec does offer.
- Being learned from data, the projection is a versioned index artifact — refitting it
  means reprojecting and reindexing the corpus. See [[PCA]].

## Related Concepts

- [[PCA]] — the first half of the learned projection, and where the refit problem is documented
- [[ITQ]] — the one-bit special case
- [[RaBitQ]] — the random-rotation, no-reduction special case
- [[TurboQuant]] — rotation-based scalar quantizer ASH measures against
- [[Scalar Quantization]] · [[Binary Quantization]] · [[Vector Quantization]] — the family
- [[Dimensionality Reduction]] — the other half of what ASH does
- [[IVF]] · [[HNSW]] — the indexes it targets
- [[Approximate Nearest Neighbor Search]]

## Related Topics

- [[Dimensionality Reduction vs Quantization]] — ASH's answer is "both, jointly, under one bit budget"
- [[Vector Search Tradeoffs]]
