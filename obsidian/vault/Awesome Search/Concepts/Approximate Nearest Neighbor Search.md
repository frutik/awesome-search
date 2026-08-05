---
title: "Approximate Nearest Neighbor Search"
type: concept
aliases:
  - ANN
  - Approximate Nearest Neighbor
  - ANN Search
  - Nearest Neighbor Search
tags:
  - concept
  - vector-search
  - ann
created: 2026-07-05
---

# Approximate Nearest Neighbor Search (ANN)

**Approximate Nearest Neighbor (ANN) search** finds vectors close to a query vector
*without* comparing against every vector in the dataset. Exact nearest-neighbor search
is O(n × d) — an exhaustive scan that becomes infeasible at millions or billions of
vectors and real-time query rates. ANN methods trade a small, tunable loss of **recall**
for orders-of-magnitude gains in **speed** and (often) **memory**.

## The Core Trade-off

Every ANN index sits on a curve of **search quality vs. speed**, with **index size /
memory** as a third axis. Exact (Flat) search is 100% recall but slowest; each
approximate index gives up a little recall to prune the search space. The practical
skill is tuning each index's knobs to land where the application needs on that curve.

## Index Families

| Family | Approach | Note |
|--------|----------|------|
| [[Brute-Force Vector Search\|Flat]] | Exhaustive brute force | Exact baseline, not an approximation |
| [[LSH]] | Hash similar vectors into shared buckets | Best at low dimensionality |
| [[HNSW]] | Multi-layer proximity graph traversal | Dominant for high-recall, low-latency |
| [[IVF]] | Cluster into Voronoi cells, probe nearest | Scales to very large corpora |
| [[Vector Quantization]] | Compress vectors (PQ/SQ/BQ) | Combined with IVF or HNSW |

## Evaluation

ANN quality is measured by **Recall@k** — the fraction of the true top-k neighbors an
approximate search returns — reported alongside query latency and index size. See
[[Vector Search Evaluation]].

The same quantity is often called **`overlap@k`**: run the exact search, run the approximate
search, and compute the overlap between the two result sets. The vocabularies are
interchangeable, and both are measured against a [[Brute-Force Vector Search|brute-force]]
baseline, which is why an exact scan remains useful even in systems that never serve one.

## How Much Recall Loss Is Acceptable

Tolerance is a property of the use case, not of the index. [[Jo Kristian Bergum]] frames the
extremes: a billion-photo image search does not need perfect recall — *"there are many equally
great cat photos"* — while a retina scan deciding building access needs excellent `overlap@1`.
Academic ANN work separates these as **high-recall** and **low-recall** settings.

The three axes to price before adopting ANN at all are the latency SLA, the anticipated peak
throughput, and the accuracy loss the application can absorb — which together decide how many
servers are needed, or whether servers are needed. See
[[Three mistakes when introducing embeddings and vector search]].

## Related Concepts

- [[HNSW]] · [[IVF]] · [[LSH]] — the main ANN index structures
- [[Brute-Force Vector Search]] — the exact baseline ANN approximates, and often the right answer below ~1M vectors
- [[Dense Vector Retrieval]] — the retrieval setting where ANN is applied
- [[Vector Quantization]] · [[Scalar Quantization]] · [[Binary Quantization]] — compression combined with ANN indexes
- [[Vector Similarity Metrics]] — the distance functions ANN indexes optimize over
- [[Vector Filtering]] — applying metadata predicates during ANN search

## Related Topics

- [[Vector Search Tradeoffs]] — the umbrella hub: the axes this index choice sits on, and how they interact

## Tools

- [[FAISS]] — reference library implementing all major ANN index families
- [[ann-benchmarks]] — the standard recall-vs-QPS comparison across implementations

## Datasets

- [[SIFT1M]] — the conventional benchmark workload for these comparisons

## Articles

- [[Choosing Indexes for Similarity Search (Faiss in Python)]] — video comparing the four index families
- [[Nearest Neighbor Indexes for Similarity Search]] — Pinecone companion write-up
- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]]; how to price the exact-vs-approximate decision, and how to read the ann-benchmarks curves
- [[Just brute force your embeddings]] — [[Doug Turnbull]]; the case for not reaching for an index at ~1m documents
