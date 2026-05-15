---
title: "Vector Filtering"
aliases: ["filtered vector search", "metadata filtering", "pre-filter", "post-filter", "single-stage vector search"]
tags:
  - concept
  - search
  - vector-search
  - infrastructure
---

# Vector Filtering

## Definition

Vector filtering refers to combining ANN (approximate nearest neighbor) similarity search with metadata filters — e.g., finding the most similar vectors *that also match* `category="shoes" AND price<100`.

This is harder than it sounds: standard ANN indexes are built for pure similarity search and don't natively handle arbitrary metadata predicates.

## The Filter Problem

Three naive approaches, each with serious flaws:

### Pre-filtering
1. Filter to matching docs first
2. Run ANN on the filtered subset

**Problem**: If the filter is selective (1% of corpus matches), the filtered subset may be too small for ANN to work well, or the subset doesn't have a usable ANN index.

### Post-filtering
1. Run ANN to get top-K candidates
2. Filter candidates by metadata

**Problem**: If 90% of top-K candidates are filtered out, effective recall collapses. Need to over-retrieve K by 10–100x, killing latency.

### Re-indexing per filter
Pre-build separate ANN indexes for each filter combination.

**Problem**: Combinatorial explosion. `n_categories × n_price_buckets × ...` indexes is infeasible.

## Single-Stage Solution (Pinecone's Approach)

[[James Briggs]] of Pinecone explains their single-stage approach:
- Metadata is stored alongside vectors at index time
- During search: metadata filter and ANN search happen **simultaneously**
- The index is structured so metadata predicates can prune the search space during graph traversal (HNSW)
- No separate filter step, no over-retrieval

This avoids the pre-filter/post-filter tradeoff by making filtering a native operation.

## HNSW with Filters

In HNSW (Hierarchical Navigable Small World) graphs:
- Traditional traversal: follow edges to nearest neighbors
- Filtered traversal: follow edges only to nodes matching the predicate
- Challenge: if predicate is highly selective, graph becomes poorly connected in filtered subspace

Solutions:
- Build separate graph layers per filter value (for high-cardinality fields)
- Hybrid: coarse filter first, then graph search in filtered subspace

## Elasticsearch Dense Vector Filtering

```python
GET /products/_knn_search
{
  "knn": {
    "field": "embedding",
    "query_vector": [...],
    "k": 10,
    "num_candidates": 100,
    "filter": {
      "term": {"category": "shoes"}
    }
  }
}
```
Elasticsearch's kNN search applies the filter during candidate selection.

## Selective Filtering Impact

| Filter Selectivity | Pre-filter Risk | Post-filter Risk |
|-------------------|----------------|-----------------|
| 50% of corpus | Low | Low |
| 10% of corpus | Medium | Medium |
| 1% of corpus | High (ANN degrades) | High (recall collapse) |
| 0.1% of corpus | Critical | Critical |

## Related Concepts

- [[Dense Vector Retrieval]] — base ANN search infrastructure
- [[Hybrid Search]] — combines metadata filters with both sparse and dense
- [[RAG]] — often needs filtered retrieval (e.g., retrieve only from specific docs)
- [[Sparse Vector Retrieval]] — sparse indexes handle filters more naturally

## People

- [[James Briggs]] — "The Missing WHERE Clause in Vector Search" (Pinecone)
