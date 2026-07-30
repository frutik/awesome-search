---
title: "ann-benchmarks"
type: tool
aliases:
  - ANN Benchmarks
  - ann_benchmarks
website: "https://ann-benchmarks.com/"
repo: "https://github.com/erikbern/ann-benchmarks"
tags:
  - tool
  - benchmark
  - vector-search
  - ann
created: 2026-07-30
---

# ann-benchmarks

**ann-benchmarks** is the standard open comparison of [[Approximate Nearest Neighbor Search|ANN]]
algorithms and their implementations, run over a set of standard vector datasets on a common
runtime. Its output is the plot most ANN discussions are implicitly citing: **recall@10 against
queries per second**, one curve per implementation.

- **Repo**: https://github.com/erikbern/ann-benchmarks

It is the reference [[Jo Kristian Bergum]] points at in
[[Three mistakes when introducing embeddings and vector search]] as the way to build intuition
for the recall/speed tradeoff before choosing an index.

## Reading the Plot

Taking the [[SIFT1M]] chart (1M × 128-dim) as the worked example:

- The benchmark is **single-threaded**, which makes QPS directly invertible into latency: 10²
  QPS means 10ms, 10³ QPS means 1ms.
- **Up and to the right is better** — more recall at more throughput. The lower-left quadrant is
  the bad tradeoff.
- Multiple cores multiply QPS roughly linearly (2 cores ≈ 2× QPS) absent contention or locking
  problems, so single-threaded numbers are a floor rather than a limit.
- Spread between implementations is large: some algorithms **struggle to get past 50% recall**
  at any speed.

## What the Plot Does Not Show

Three blind spots worth holding in mind, all noted in the article above:

| Missing | Why it matters |
|---|---|
| **Indexing cost** | The curve is query-time only; building the index may dominate total cost |
| **Update / CRUD support** | Some algorithms are batch-oriented and need a large vector sample before an index can be built at all; others build incrementally |
| **Proprietary systems** | Only open-source algorithms reproducible on the same runtime can be included, so *"some commercial and proprietary vector search vendors have unknown recall versus performance tradeoffs"* |

That third point is the sharpest one for buyers: a vendor's absence from ann-benchmarks is not
evidence of anything, but it does mean their tradeoff curve is unpublished.

Also absent: memory and disk footprint, which for large corpora often decides the choice before
recall does.

## Related Concepts

- [[Approximate Nearest Neighbor Search]] — what is being benchmarked
- [[Brute-Force Vector Search]] — the exact baseline recall is measured against
- [[HNSW]] · [[IVF]] · [[LSH]] — index families appearing on the charts
- [[Vector Search Evaluation]] — how approximation fidelity relates to relevance quality
- [[Vector Quantization]] — a compression axis the plots don't separate out

## Datasets

- [[SIFT1M]] — the most-cited chart in the suite

## Tools

- [[FAISS]] — repeatedly among the compared implementations

## Articles

- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]];
  how to read these curves, and their documented blind spots

## People

- [[Jo Kristian Bergum]]
