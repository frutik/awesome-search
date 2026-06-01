---
title: "Migrating to Elasticsearch with Dense Vector for Carousell Spotlight Search"
source: "https://medium.com/carousell-insider/migrating-to-elasticsearch-with-dense-vector-for-carousell-spotlight-search-engine-e328b16155fc"
author: ["Carousell Engineering"]
tags:
  - clippings
  - elasticsearch
  - dense-vectors
  - case-study
  - e-commerce-search
  - medium
concepts:
  - Dense Vector Retrieval
  - Semantic Search
  - Hybrid Search
created: 2026-05-15
---

# Migrating to Elasticsearch with Dense Vector for Carousell Spotlight Search

**Source**: https://medium.com/carousell-insider/migrating-to-elasticsearch-with-dense-vector-for-carousell-spotlight-search-engine-e328b16155fc  
**Author**: Carousell Engineering

## Summary

A case study from Carousell (Southeast Asian C2C marketplace) describing their migration from a pure keyword-based search engine to Elasticsearch with dense vector support for their "Spotlight" ad ranking product.

## Business Context

Carousell Spotlight is a paid placement product: sellers pay to have their listings appear prominently in search. The challenge:
- Match sponsored listings to user queries semantically, not just lexically
- "selling my old iphone 12" listing should appear for query "used apple phone"
- Pure BM25 fails this semantic matching

## Architecture Before Migration

```
User query → BM25 (Elasticsearch) → keyword match → ranked results
```

Problems:
- Zero results for semantic queries with vocabulary mismatch
- Can't match synonyms or related terms without manual synonym dictionaries
- Sponsored listings not shown when they should be

## Migration Strategy

### Phase 1: Add Dense Vectors

Encode all listing titles + descriptions with a multilingual sentence transformer (important: Carousell operates in multiple Asian languages).

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

listing_embedding = model.encode(
    f"{listing.title} {listing.description}"
)
```

### Phase 2: Elasticsearch kNN Indexing

```json
PUT /spotlight_listings
{
  "mappings": {
    "properties": {
      "embedding": {
        "type": "dense_vector",
        "dims": 384,
        "index": true,
        "similarity": "cosine"
      },
      "title": {"type": "text"},
      "price": {"type": "float"},
      "category": {"type": "keyword"}
    }
  }
}
```

### Phase 3: Hybrid Retrieval

```json
GET /spotlight_listings/_search
{
  "query": {
    "bool": {
      "should": [
        {"match": {"title": "used apple phone"}},
        {"knn": {
          "field": "embedding", 
          "query_vector": [0.1, 0.2, ...],
          "k": 100
        }}
      ]
    }
  }
}
```

## Results

Post-migration metrics:
- **+23% CTR** on Spotlight listings (more relevant ads shown for semantic queries)
- **-18% zero-result queries** — listings found where previously none existed
- **Seller satisfaction** improved: more impressions for semantically relevant listings

## Key Learnings

1. **Multilingual matters**: Carousell users mix English with local languages (Filipino, Bahasa, Mandarin) — multilingual model was essential
2. **Hybrid over pure dense**: BM25 still wins for exact model/SKU searches; dense wins for categorical/semantic
3. **Embedding freshness**: new listings need embeddings computed before indexing — adds latency to seller listing creation flow
4. **Dimensionality tradeoff**: 384-dim MiniLM chosen over 768-dim for storage/speed reasons at their scale

## Related Articles

- [[Innovating Search Experience with Amazon OpenSearch and Amazon Bedrock]] — similar AWS-stack case study
- [[Nearest Neighbor Indexes for Similarity Search]] — ANN infrastructure used
- [[How to Choose the Best Model for Semantic Search]] — model selection framework

## Related Concepts

- [[Dense Vector Retrieval]] — primary migration target
- [[Semantic Search]] — capability enabled
- [[Hybrid Search]] — final deployment pattern
- [[Bi-Encoder]] — architecture used for embeddings
- [[Asymmetric Semantic Search]] — short query → long listing description
