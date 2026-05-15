---
title: "The Missing WHERE Clause in Vector Search"
source: "https://www.pinecone.io/learn/vector-search-filtering/"
author:
  - "[[James Briggs]]"
published: 2023-06-30
created: 2026-05-15
description: "Why metadata filtering in vector search is hard, two traditional approaches (pre-filtering, post-filtering), and Pinecone's single-stage solution merging vector and metadata indexes."
tags:
  - clippings
---
# The Missing WHERE Clause in Vector Search

"Imagine Excel without data filters, SQL without a WHERE clause." Metadata filtering is essential but surprisingly complex in vector search.

## Two traditional approaches

### Pre-filtering
Apply metadata conditions first → vector search on remaining records. Accurate but brute-force on filtered subset — slow for large datasets.

### Post-filtering
Vector search first → apply conditions to top-k results. Fast but risks returning few or zero relevant results even when they exist.

## Single-stage filtering (Pinecone's approach)

Merges vector and metadata indexes into one. Achieves pre-filtering accuracy without small-dataset restrictions.

```python
# Simple filter
results = index.query(
    queries=[xq.tolist()],
    top_k=3,
    filter={'lang': {'$eq': 'en'}}
)

# Multiple conditions with ranges
results = index.query(
    queries=[xq.tolist()],
    top_k=3,
    filter={
        'lang': {'$eq': 'en'},
        'title': {'$nin': ['University_of_Kansas']},
        'date': {'$gte': 20200101, '$lte': 20201231}
    }
)
```

Search times remained ~37–38ms regardless of filter complexity.

## Performance (1.2M random vectors)

Tighter filters → faster searches:

| Filter | Latency |
|---|---|
| Unfiltered | 79.2ms |
| `tag1 > 30` | 71.3ms |
| `tag1 > 50` | 57.1ms |
| `tag1 = 50` | 51.6ms |

## Related Concepts
- [[Vector Filtering]] — the core problem and solution explained
- [[Dense Vector Retrieval]] — ANN search that needs filtering
- [[Dense Embeddings]] — the vector type being filtered
- [[Embeddings]] — parent concept
- [[Hybrid Search]] — metadata filtering often combined with hybrid retrieval

## People
- [[James Briggs]] — Pinecone; vector filtering explainer