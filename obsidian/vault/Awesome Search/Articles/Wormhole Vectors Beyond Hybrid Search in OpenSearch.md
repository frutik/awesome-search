---
title: "Wormhole Vectors: Beyond Hybrid Search in OpenSearch"
source: "https://aiven.io/blog/beyond-hybrid-search-traversing-vector-spaces-with-wormhole-vectors"
author: "[[Dima Kan]]"
published: 2025-12-15
tags: [hybrid-search, wormhole-vectors, semantic-knowledge-graph, opensearch, vector-search, company-blog]
---

# Wormhole Vectors: Beyond Hybrid Search in OpenSearch

**Author:** [[Dima Kan]] (Aiven), concept by [[Trey Grainger]]

## The Problem with Standard Hybrid Search (RRF)

RRF (Reciprocal Rank Fusion) treats sparse and dense spaces as **disconnected silos**. It interleaves results but doesn't combine their intelligence. A dense vector result can't explain itself in keywords; a keyword query can't leverage semantic structure.

## Vector Spaces

- **Sparse Space**: High-dimensional (10^6+), discrete, explainable — token `postgres` exists in Doc A
- **Dense Space**: Low-dimensional (~768), continuous, abstract — float array for "database"

**Sparse → Dense**: easy — query for keywords, average embeddings of top-k results to get a centroid

**Dense → Sparse**: hard — how do you turn a float array back into keywords?

## The Semantic Knowledge Graph (SKG)

Solution: Use the search engine's own inverted index + forward index as a graph.

Algorithm:
1. **Anchor**: run dense vector query → get "Bag of Documents" (top-50 results) = **Foreground Set**
2. **Universe**: rest of index = **Background Set**
3. **Traversal**: find terms with high *P(t|Foreground) / P(t|Background)*

This finds statistically significant terms that *distinguish* the foreground from background — not just frequent terms.

### Example: Disambiguation for "Java"

- Foreground contains Hibernate, Scala, VM, Backend → `Java AND (Hibernate OR Scala)`
- Foreground contains Sumatra, Coffee, Island → `Java AND (Coffee OR Sumatra)`

## Wormhole Traversal Workflow

1. **Start in Sparse Space**: user searches for `server` → mixed results (tech + food service)
2. **Traverse to Dense**: average embeddings of top results → vector in "mushy" middle ground
3. **Refine via SKG**: aggregation reveals two clusters: `{linux, devops, rack}` and `{tip, waiter, food}`
4. **Hop to Behavioral Space**: query behavioral embeddings with `{linux, devops}` → finds "Raspberry Pi" even without the word "server"

## Implementation in OpenSearch

```python
response = client.search(
    index="products",
    body={
        "size": 50,
        "query": {"knn": {"embedding_vector": query_vector, "k": 50}},
        "aggs": {
            "wormhole_keywords": {
                "significant_terms": {
                    "field": "description_keywords",
                    "size": 10
                }
            }
        }
    }
)
```

Key OpenSearch primitives: k-NN plugin (dense layer) + `significant_terms` aggregations (SKG traversal).

## Production Benefits

1. **Zero-result bridge**: user searches "sweet dough ring" → taxonomy/keyword has no match → wormhole finds "Donut" via semantic bridge
2. **Explainability**: maps dense vectors back to sparse keywords — shows user *why* a result appeared

## Related Concepts

- [[Hybrid Search]]
- [[Wormhole Vectors]]
- [[Semantic Search]]
- [[Dense Vector Retrieval]]
- [[Reciprocal Rank Fusion]]

## Related People

- [[Trey Grainger]] (concept originator)
- [[Dima Kan]] (OpenSearch implementation)
