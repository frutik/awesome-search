---
type: article
tags: [article, ann, hnsw, vespa, e-commerce, image-similarity, prefiltering]
source: "https://blog.vespa.ai/image-similarity-search/"
author: [Jo Kristian Bergum]
company: [Vespa]
concepts: [Dense Vector Retrieval, ANN, Hybrid Search]
topics: [E-commerce Search, Personalization in Search]
---

# Using Approximate Nearest Neighbor Search to Find Similar Products

**[[Jo Kristian Bergum]]** (Vespa) demonstrates ANN-based "similar products" feature on Amazon Fashion dataset (~22K products) using pyvespa.

## Key Concepts Demonstrated

### ANN with Prefiltering
Combine ANN search with metadata filters in a single query:
```
nearestNeighbor(image_vector, query_vector) AND !(asin = "X") AND price > 100
```
Vespa evaluates filters at query time — not post-processing — so filtered recall is maintained.

### HNSW Configuration
- `max_links_per_node`: controls graph connectivity vs. memory tradeoff
- `neighbors_to_explore_at_insert`: controls index-time recall quality
- Toggle `approximate: true/false` at query time to switch ANN ↔ exact for A/B testing

### Real-Time Partial Updates
Attribute fields (inventory status, price, popularity) can be updated at ~40-50K updates/sec **without re-indexing the document**. Critical for keeping search index current in retail.

### Ranking Integration
ANN results can feed into a multi-signal ranking profile:
```
12.0 + 23.24 * closeness(field, image_vector) + 12.4 * (1/attribute(popularity))
```
ANN as first-stage retrieval + business signal re-ranking in one system.

## Key Takeaway

The value of Vespa's ANN isn't just speed — it's **ANN + filters + real-time updates + ML ranking** as a unified system, avoiding the need for separate ANN index + database + re-ranker.
