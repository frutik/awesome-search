---
title: "Beyond Hybrid Search: Traversing Vector Spaces with Wormhole Vectors"
source: "https://aiven.io/blog/beyond-hybrid-search-traversing-vector-spaces-with-wormhole-vectors"
author: ["Dima Kan"]
tags:
  - clippings
  - hybrid-search
  - wormhole-vectors
  - vector-search
  - search
concepts:
  - Wormhole Vectors
  - Hybrid Search
  - Dense Vector Retrieval
  - Sparse Vector Retrieval
created: 2026-05-15
---

# Beyond Hybrid Search: Traversing Vector Spaces with Wormhole Vectors

**Source**: https://aiven.io/blog/beyond-hybrid-search-traversing-vector-spaces-with-wormhole-vectors  
**Author**: [[Dima Kan]] (Aiven, Product Director of Search)

## Summary

[[Dima Kan]] implements [[Trey Grainger]]'s [[Wormhole Vectors]] concept at Aiven, demonstrating how documents that bridge multiple retrieval spaces (sparse + dense + behavioral) can be used as traversal hubs for better retrieval than standard hybrid fusion.

## The Problem with Standard Hybrid Search

Standard [[Hybrid Search]] (RRF fusion):
```
query → [sparse retrieval] → top-k₁
query → [dense retrieval]  → top-k₂
merge(top-k₁, top-k₂, via RRF) → final ranking
```

**Limitation**: The merge is a *late* operation. Each retrieval system still operates independently, potentially missing connections that only become visible when spaces are traversed jointly.

**Example failure case**: A relevant document might score 80th in sparse retrieval and 80th in dense retrieval — never making either top-k — but would be recognized as highly relevant if we could traverse between the spaces.

## Wormhole Vectors in Practice

Kan's implementation identifies "wormhole" documents:
- Documents that rank in the **top percentile of both** sparse AND dense retrieval for a given query cluster
- These documents act as hubs: their neighborhood in each space reveals different relevant documents

```
Query → [sparse top-100] ∩ [dense top-100] → wormhole candidates
       ↓
For each wormhole doc:
    expand its sparse neighbors
    expand its dense neighbors
    merge expanded neighborhoods
       ↓
Much richer candidate set than standard hybrid
```

## Implementation at Aiven

Using PostgreSQL + pgvector + full-text search:

```sql
-- Find wormhole documents (high score in both sparse and dense)
WITH sparse_scores AS (
  SELECT id, ts_rank(search_vector, plainto_tsquery(query)) as sparse_score
  FROM documents
  ORDER BY sparse_score DESC LIMIT 100
),
dense_scores AS (
  SELECT id, 1 - (embedding <=> query_embedding) as dense_score
  FROM documents  
  ORDER BY dense_score DESC LIMIT 100
)
SELECT s.id, s.sparse_score, d.dense_score
FROM sparse_scores s JOIN dense_scores d ON s.id = d.id
-- These are wormhole documents
```

## Results

Kan reports measurable improvements over standard RRF hybrid:
- Better recall for long-tail queries
- More diverse result sets
- Fewer "zero result" failures on edge cases

The improvement is most pronounced for queries where the relevant documents use different vocabulary than the query (vocabulary mismatch + semantic gap simultaneously).

## Conceptual Framework

Wormhole vectors reveal that the retrieval space is not flat:
- Some documents are "attractors" in multiple spaces
- These attractors act as semantic transit hubs
- Traversing through attractors extends retrieval reach beyond direct similarity

## Relation to Knowledge Graphs

The traversal metaphor connects to [[Graphs/Taxonomies/Knowledge Graph]] approaches:
- In KG search: traverse entity-relation-entity paths
- In wormhole search: traverse document-similarity-document paths across spaces

## Related Articles

- [[Hybrid Search SPLADE Sparse Encoder]] — standard hybrid this extends
- [[SPLADE for Sparse Vector Search Explained]] — sparse component
- [[Nearest Neighbor Indexes for Similarity Search]] — dense component infrastructure

## Related Concepts

- [[Wormhole Vectors]] — primary concept
- [[Hybrid Search]] — what this extends
- [[Dense Vector Retrieval]] — one space being traversed
- [[Sparse Vector Retrieval]] — another space
- [[Bag-of-Documents Model]] — related probabilistic framing

## People

- [[Dima Kan]] — author, Aiven implementation
- [[Trey Grainger]] — Wormhole Vectors concept originator
