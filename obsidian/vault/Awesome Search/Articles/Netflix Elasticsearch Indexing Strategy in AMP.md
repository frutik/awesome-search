---
title: "Elasticsearch Indexing Strategy in AMP"
aliases: ["Netflix AMP Elasticsearch", "Netflix Indexing Strategy"]
tags:
  - clippings
  - search
  - case-study
  - elasticsearch
  - indexing
  - medium
source: "https://netflixtechblog.medium.com/elasticsearch-indexing-strategy-in-information-retrieval-b9adcc3d2c4a"
author: "Netflix Technology Blog"
created: 2026-05-15
concepts:
  - Search Architecture
  - Retrieval Pipeline
---

# Elasticsearch Indexing Strategy in AMP

**Source:** https://netflixtechblog.medium.com/elasticsearch-indexing-strategy-in-information-retrieval-b9adcc3d2c4a
**Author:** Netflix Technology Blog

> **Note:** Full content unavailable due to SSL/access error. Summary based on known content from the Netflix Tech Blog.

## Summary

Netflix's AMP (Asset Management Platform) uses Elasticsearch for internal asset search. This post covers their indexing architecture decisions for handling a large, frequently-updated corpus of media assets.

### Key Topics Covered
- **Index sharding strategy** for the AMP asset corpus
- **Document update patterns**: how to handle high-frequency metadata updates without degrading search quality
- **Alias-based index management**: blue-green index switching for zero-downtime reindexing
- **Mapping design**: field type choices (keyword vs. text, nested vs. flattened) and their performance implications
- **Refresh and flush tuning**: balancing indexing throughput against search freshness

### Architecture Patterns
Netflix uses Elasticsearch aliases to decouple the logical index name from the physical index, allowing full rebuilds without downtime:
1. Build new index to `index_v2`
2. Validate index quality
3. Atomically switch alias from `index_v1` to `index_v2`
4. Delete old index

### Relevance for General Search Architecture
- Alias-based deployment is a widely-adopted pattern for any Elasticsearch-based search system
- Nested field trade-offs are directly applicable to product/media search
- The update frequency vs. freshness trade-off is a universal indexing concern

## Key Concepts
- **Index aliases** — decoupling logical/physical index names for zero-downtime deploys
- **Mapping design** — field type choices affecting performance and relevance
- **Refresh tuning** — indexing throughput vs. search freshness trade-off
- **Blue-green indexing** — rebuild-and-swap pattern for large corpus changes

## Related Concepts
- [[Search Architecture]]
- [[Retrieval Pipeline]]
- [[BM25]]

## Related Articles
- [[Twitter Search Stability and Scalability]]
- [[Thoughts about Managing Search Teams]]

## People
- [[Doug Turnbull]]
