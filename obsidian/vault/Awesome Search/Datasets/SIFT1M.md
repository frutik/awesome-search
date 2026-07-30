---
title: "SIFT1M"
type: dataset
aliases:
  - SIFT 1M
  - ANN_SIFT1M
  - Sift1M
  - SIFT
tags:
  - dataset
  - benchmark
  - vector-search
  - ann
source: "TEXMEX / IRISA evaluation corpus for approximate nearest neighbour search"
domain: "computer vision — 1M SIFT image descriptors, 128 dimensions"
created: 2026-07-30
---

# SIFT1M

**SIFT1M** is a set of **one million 128-dimensional vectors** used as the default workload for
benchmarking [[Approximate Nearest Neighbor Search|ANN]] algorithms. The vectors are SIFT
(Scale-Invariant Feature Transform) local image descriptors, distributed with query vectors and
precomputed exact nearest neighbours so that recall can be measured against ground truth.

It is a **vector-search benchmark, not a relevance benchmark** — unlike [[MS MARCO]], [[BEIR]] or
[[Amazon ESCI Dataset]], there are no queries, documents or judgments in the IR sense. Nothing
here measures whether results are *relevant*; it measures whether an index finds the same
neighbours the exact scan would. That distinction is the one drawn in [[Vector Search Evaluation]].

## Why It Recurs

- **The default x-axis of ANN comparison.** The most-cited [[ann-benchmarks]] chart is SIFT1M:
  recall@10 against QPS, single-threaded, one curve per implementation.
- **Small enough to be honest about.** At 1M × 128 dims it fits in memory on ordinary hardware,
  so results are reproducible and a [[Brute-Force Vector Search|brute-force]] baseline is cheap
  to compute — [[Jo Kristian Bergum]] reports ~100ms single-threaded for exactly this shape.
- **Ground truth is exact.** Because the true neighbours are known, `recall@k` / `overlap@k` is
  unambiguous, which is what makes the recall/speed curve meaningful in the first place.

## Limitations

- **128 dimensions is low by modern standards.** Text embeddings today run 384–1536+ dims, where
  memory bandwidth and quantization behave differently. Good SIFT1M numbers do not transfer
  automatically to a text-embedding workload.
- **Image descriptors, not learned embeddings.** SIFT features have different distributional
  structure from neural [[Dense Embeddings]] — notably no anisotropy of the kind that motivates
  the rotation step in [[TurboQuant]]-style quantization.
- **Says nothing about relevance, filtering, or updates.** Index quality on SIFT1M is silent on
  [[Vector Filtering]], CRUD support, and indexing cost.

## Related Concepts

- [[Approximate Nearest Neighbor Search]] — what SIFT1M is used to compare
- [[Brute-Force Vector Search]] — supplies the exact neighbours
- [[HNSW]] · [[IVF]] · [[LSH]] — the index families ranked on it
- [[Vector Search Evaluation]] — fidelity-to-exact versus relevance quality

## Tools

- [[ann-benchmarks]] — the suite whose headline chart uses it
- [[FAISS]] — index tutorials conventionally demonstrate on it

## Articles

- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]];
  reads the SIFT1M recall-vs-QPS curve to explain the ANN tradeoff
- [[Choosing Indexes for Similarity Search (Faiss in Python)]] — compares Flat, [[LSH]],
  [[HNSW]] and [[IVF]] on it
