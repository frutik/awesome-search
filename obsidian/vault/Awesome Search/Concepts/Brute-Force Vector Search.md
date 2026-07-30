---
title: "Brute-Force Vector Search"
type: concept
aliases:
  - Brute Force Vector Search
  - Exhaustive Search
  - Exact Nearest Neighbor Search
  - Exact Search
  - Flat Index
  - Full Scan
tags:
  - concept
  - vector-search
  - ann
created: 2026-07-30
---

# Brute-Force Vector Search

**Brute-force vector search** compares the query vector against *every* document vector and
keeps the top k. It is the exact baseline that [[Approximate Nearest Neighbor Search|ANN]]
indexes approximate: 100% recall by construction, no index to build, no parameters to tune,
no recall/latency curve to sit on. Its cost is O(n × d) per query.

## Why the Constant Factor Wins Longer Than Expected

Neither source article spells out the mechanism, but the conventional explanation is
architectural. A full scan is a dense matrix–vector product, which suits modern hardware about
as well as any operation can: sequential memory access, no pointer chasing, BLAS-level SIMD.
[[Jo Kristian Bergum]]'s version of the point is that the search *"can be parallelized,
multi-threaded, and in many cases, can use optimized HW instructions; vectors are the machine's
language."* A graph index like [[HNSW]] has better asymptotics but pays random access, cache
misses and index construction — so the crossover plausibly arrives later than the O-notation
alone would suggest.

Two reported measurements, three years apart:

| Source | Corpus | Dims | Reported |
|---|---|---|---|
| [[Three mistakes when introducing embeddings and vector search]] (2023) | 1M | 128 | ~100ms single-threaded; ~25ms on 4 threads, until memory bandwidth saturates |
| [[Just brute force your embeddings]] (2026) | 1M | 384 | 79.7 QPS and 12ms average latency single-threaded (NumPy, M4 MacBook Pro) |

These are **not directly comparable** — different hardware, dimensionality, and measurement
setup (a raw NumPy dot product versus an engine context). Read them as two independent
demonstrations that a million vectors is comfortably scannable, not as a speedup figure.

## When It's the Right Choice

Usually sufficient when *all* of these hold:

| Condition | Why it matters |
|---|---|
| Corpus around 1M vectors or fewer | Scan time stays inside a normal latency budget |
| Low query traffic | Throughput, not latency, is what a scan gives up first |
| Embeddings computed up front | No incremental index maintenance to get wrong |

It also removes whole categories of problem that ANN introduces: no recall tuning, no
[[Vector Filtering]] pathology (a metadata predicate is just a mask over the score array), no
index rebuild after writes, and nothing to operate.

## Where the Ceiling Actually Is

The limit is cost, not correctness. The scan parallelises cleanly — until memory bandwidth
saturates — and can be distributed across nodes to hold latency down, as [[Vespa]] does. What
breaks is the economics: at billions of embeddings with no way to restrict the search to a
subset, and especially with high query throughput, server rental becomes the binding
constraint.

This is why **engine-side filtering matters more than it first appears**. If the vectors live
somewhere that can efficiently narrow the candidate set with a query predicate, the effective
n is the filtered subset rather than the whole corpus, and the scan stays viable far past the
naive threshold.

## Ways to Push the Ceiling

Before reaching for an index, the scan itself has headroom:

- **Batch queries per scan** — amortise one pass over the vectors across many queries.
- **Shrink the vectors** — fewer dimensions, or fewer bits per dimension, cuts the bytes the
  scan must touch: [[Matryoshka Embeddings]], [[PCA]], [[Scalar Quantization]],
  [[Binary Quantization]].
- **Collect top-k during the scan** rather than scoring everything and sorting after.

Because the bottleneck is memory bandwidth, compression buys close to proportional speedup —
see [[Dimensionality Reduction vs Quantization]].

## Where It Shows Up Even at Scale

- **Flat indexes** — `IndexFlatL2` / `IndexFlatIP` in [[FAISS]]; the exact baseline that
  Recall@k and `overlap@k` are measured against (see [[Vector Search Evaluation]]).
- **Rescoring** — quantized ANN candidates re-ranked with exact distances over
  full-precision vectors.
- **Pre-filtered search** — when a metadata filter leaves few candidates, scanning them beats
  traversing a graph.

## Related Concepts

- [[Approximate Nearest Neighbor Search]] — what you trade recall for when the scan stops fitting
- [[HNSW]] · [[IVF]] · [[LSH]] — the index families that replace the scan
- [[Dense Vector Retrieval]] — the retrieval setting
- [[Vector Similarity Metrics]] — the per-pair function the scan evaluates
- [[Vector Filtering]] — trivial under a full scan, hard under ANN
- [[Vector Search Evaluation]] — brute force supplies the ground-truth neighbours

## Related Topics

- [[Vector Search Tradeoffs]] — where "do I need an index at all?" sits among the other axes

## Tools

- [[FAISS]] — flat indexes, plus in-memory ANN when the scan runs out
- [[ann-benchmarks]] — where the approximate alternatives are compared
- [[Sentence Transformers]] — produces the vectors being scanned

## Articles

- [[Just brute force your embeddings]] — [[Doug Turnbull]]; measured NumPy scan throughput and
  the "you don't need a vector database" argument
- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]];
  *"an exhaustive search might be all you need"*, and how to price the ANN decision

## People

- [[Doug Turnbull]] · [[Jo Kristian Bergum]]
