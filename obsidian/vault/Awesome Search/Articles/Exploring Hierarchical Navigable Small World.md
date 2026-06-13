---
created: 2026-05-21
title: "Exploring Hierarchical Navigable Small World"
source: "https://blog.vespa.ai/exploring-hierarchical-navigable-small-world/"
authors:
  - "[[Marianne Haugvaldstad]]"
  - "[[Brage Vik]]"
published: 2025-08-22
tags:
  - article
  - hnsw
  - ann
  - vector-search
  - vespa
  - company-blog
---

# Exploring Hierarchical Navigable Small World

A hands-on deep dive into the [[HNSW]] algorithm written by two [[Vespa]] summer interns who built visualization and analysis tools during their exploration. Covers how HNSW is structured, built, and searched, along with graph quality metrics and filtering behavior.

## Key Concepts Covered

### HNSW Structure and Search
- Multi-layer proximity graph: top layers sparse (coarse navigation), bottom layer contains all nodes (fine search)
- Greedy descent from entry point; bottom layer switches to top-k beam search
- Local minima problem: search can get stuck, returning approximate (not exact) neighbors
- Recall, response time, and memory footprint as the three standard ANN quality metrics

### Graph Quality Metrics Beyond Recall
The authors developed tools to measure:
- **Disconnected components** — nodes unreachable from the main cluster are invisible to ANN search; must be reinserted or reconnected
- **Edge density distribution** — histogram of neighbor counts per node; reveals sparsity or overcrowding; helped find a Vespa bug (layer-0 neighbor cap used wrong constant: `max-links-per-node` instead of `2×max-links-per-node`)
- **Neighbor proximity** — how close a node's graph neighbors are relative to the global distance distribution (e.g., what % are in the top 15%, 2%, 0.3%)

### Distance Distribution Analysis
With ~600 visited nodes, HNSW finds ~40% of them within the closest 5% of all points in the dataset — confirming efficient navigation. [[ACORN-1]] evaluates ~14k nodes for similar recall under aggressive filtering, trading cost for connectivity.

### Filtering in HNSW
Four strategies with different trade-offs:
1. **Fallback to exact search** — used when filter selectivity drops below a threshold
2. **Post-filter** — fast but can return 0 hits when filtering is aggressive
3. **Pre-filter (standard)** — only filter-passing nodes considered; works until filtering is very selective
4. **Pre-filter + check first (ACORN-1 style)** — multi-hop neighborhoods avoid getting stuck; higher cost

### Dimensionality Reduction
PCA as an option when some embedding dimensions carry near-zero variance (< 0.01%). Offers small speed-ups with minimal data loss. Effectiveness depends on embedding model, distance metric, and data. Alternative: [[Matryoshka Embeddings]].

## Bug Found
Edge density analysis revealed a production Vespa bug: the deletion code in layer 0 capped neighbors at `max-links-per-node` instead of `2×max-links-per-node`, producing sparser graphs than intended.

## Authors

- [[Marianne Haugvaldstad]] — Developer Intern, Vespa
- [[Brage Vik]] — Developer Intern, Vespa

## Company

[[Vespa]]

## Related Concepts

[[HNSW]] · [[ACORN-1]] · [[Vector Filtering]] · [[Dense Vector Retrieval]] · [[Matryoshka Embeddings]]
