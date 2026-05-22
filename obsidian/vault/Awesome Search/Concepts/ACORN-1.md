---
title: "ACORN-1"
aliases: ["ACORN", "ACORN algorithm"]
tags:
  - concept
  - vector-search
  - ann
  - filtered-search
---

# ACORN-1

## Definition

ACORN-1 is an HNSW-based approximate nearest neighbor algorithm designed to handle **aggressive metadata filtering** better than standard HNSW. It expands graph traversal to include neighbors of neighbors (multi-hop neighborhoods), reducing the chance of getting stuck in the filtered subspace.

## Problem It Solves

Standard [[HNSW]] with pre-filtering (checking filter first, navigating only through passing nodes) can get stuck when filtering is highly selective — if few nodes pass the filter, the filtered subspace becomes poorly connected and greedy search reaches a dead end far from the true nearest neighbors.

ACORN-1 addresses this by expanding each traversal step to consider not just direct neighbors but also their neighbors, increasing the chance of finding filter-passing nodes and maintaining connectivity.

## Trade-offs

| Metric | Standard HNSW | ACORN-1 |
|--------|--------------|---------|
| Nodes visited (~600-dataset example) | ~600 | ~14,000 |
| Distance distribution | Efficiently near-query | Similar curve, but more nodes evaluated |
| Filtering recall | Degrades with aggressive filtering | Maintained under aggressive filtering |
| Cost | Low | Higher — proportional to filter selectivity |

ACORN-1 evaluates ~23× more nodes than standard HNSW in the referenced benchmark. The higher cost is justified when filter selectivity makes standard HNSW miss nearby results.

## Comparison with Standard HNSW Filtering Strategies

From the Vespa HNSW exploration study:

| Strategy | Behavior |
|----------|----------|
| Post-filter | ANN search ignores filter; applied after → can return 0 hits |
| Pre-filter (standard) | Only filter-passing nodes counted; gets stuck when selective |
| Pre-filter + check first | Skip distance computations for non-passing nodes; ACORN-1 adds multi-hop |
| Exact search fallback | Used when filtering fraction is below a threshold |

## Related Concepts

- [[HNSW]] — the base index ACORN-1 extends
- [[Vector Filtering]] — the problem space ACORN-1 addresses
- [[Dense Vector Retrieval]] — parent retrieval paradigm

## Articles

- [[Exploring Hierarchical Navigable Small World]] — comparison of HNSW vs. ACORN-1 distance distributions and node visit counts
