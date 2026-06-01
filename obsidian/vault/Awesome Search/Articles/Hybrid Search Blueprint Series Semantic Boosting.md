---
title: "Hybrid Search Blueprint Series: Semantic Boosting"
aliases: ["Semantic Boosting Blueprint", "Hybrid Search Blueprint Part 3"]
type: article
source: "https://medium.com/@MongoDB/hybrid-search-blueprint-series-semantic-boosting-83b0011e080d"
author:
  - "[[Erik Hatcher]]"
company: ["[[MongoDB]]"]
published: 2026-05-14
created: 2026-05-19
tags:
  - article
  - hybrid-search
  - semantic-boosting
  - vector-search
  - mongodb
  - medium
concepts:
  - Semantic Boosting
  - Hybrid Search
  - Reciprocal Rank Fusion
  - Relative Score Fusion
  - Results Boosting
  - Dense Vector Retrieval
topics: []
---

# Hybrid Search Blueprint Series: Semantic Boosting

**[[Erik Hatcher]]** ([[MongoDB]]) presents Semantic Boosting — a two-shot hybrid retrieval technique that runs a vector search first, then injects the results as boost clauses into a final lexical search — preserving full-text features like faceting, highlighting, and pagination.

Third article in the series:
1. Survey of the hybrid search landscape
2. [[Reciprocal Rank Fusion]] (RRF) and [[Relative Score Fusion]] (RSF)
3. This article — [[Semantic Boosting]]

---

## What Is Semantic Boosting?

A two-phase approach:

1. **Vector search phase** — run `$vectorSearch` to retrieve the top-N semantically relevant documents and their similarity scores
2. **Inject + boost phase** — extract document IDs and scores; add each as an explicit `equals` boost clause (weighted by `score × multiplier`) into a final `$search` lexical query

The final result set is entirely produced by the lexical engine. This gives developers access to all standard text search features — facets, highlights, pagination — on hybrid results.

## Why Not RRF or Score Fusion?

- **RRF / RSF** merge ranked lists from two independent queries; pagination and faceting require extra wiring
- **Semantic Boosting** makes the lexical engine the single authoritative output; vector influence is injected as score signals, not a separate ranked list

The technique is a special case of *signal incorporation* — the same pattern used to boost from click/purchase signals, except the signal source is the vector query.

## Example (MongoDB Atlas Search)

```python
# 1. Vector search → get IDs + scores
vector_results = collection.aggregate([
    {"$vectorSearch": {
        "queryVector": embed_query(q),
        "index": "vector_index",
        "path": "plot_embedding_voyage_3_large",
        "numCandidates": 150,
        "limit": 10
    }},
    {"$project": {"_id": 1}},
    {"$addFields": {"score": {"$meta": "vectorSearchScore"}}}
])

# 2. Build boost clauses from vector results
vector_boost_clauses = [
    {"equals": {"path": "_id", "value": r["_id"],
                "score": {"boost": {"value": r["score"] * 10}}}}
    for r in vector_results
]

# 3. Lexical search + injected boosts
should_clauses = [
    {"text": {"query": q, "path": ["title"], "score": {"boost": {"value": 2}}}},
    {"text": {"query": q, "path": ["plot"]}}
] + vector_boost_clauses
```

The boost multiplier (`× 10`) is a tuning knob — requires calibration across a query sample.

## Embeddings

Uses [[Voyage AI]]'s `voyage-4-large` model (2048 dimensions, dot product similarity) for query embedding at query time. Documents are pre-embedded at index time.

## Key Advantages

| Feature | RRF/RSF | Semantic Boosting |
|---------|---------|-------------------|
| Faceting | Requires extra logic | Native (lexical engine handles it) |
| Highlighting | Requires extra logic | Native |
| Pagination | Requires merging | Native |
| Score tunability | Limited | Full (boost multiplier per signal) |

## Related Concepts
- [[Semantic Boosting]] — the core technique introduced
- [[Hybrid Search]] — broader family this belongs to
- [[Reciprocal Rank Fusion]] — alternative fusion strategy
- [[Relative Score Fusion]] — alternative score-based fusion
- [[Results Boosting]] — Semantic Boosting is a special case of signal boosting
- [[Dense Vector Retrieval]] — the first-phase signal source
- [[Linear Score Combination]] — another score-based combination approach

## Related Articles
- [[RRF is Not Enough]] — critiques RRF's limitations in hybrid contexts
- [[Hybrid search > sum of its parts? Berlin Buzzwords 2022]]

## People
- [[Erik Hatcher]]

## Companies
- [[MongoDB]]
- [[Voyage AI]]
