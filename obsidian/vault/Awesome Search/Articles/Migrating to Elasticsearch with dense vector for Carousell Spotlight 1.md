---
title: "Migrating to Elasticsearch with dense vector for Carousell Spotlight search engine"
source: "https://medium.com/carousell-insider/migrating-to-elasticsearch-with-dense-vector-for-carousell-spotlight-search-engine-e328b16155fc"
author:
  - "[[Eric Feng Chao]]"
published: 2021-09-22
created: 2026-05-15
description: "How Carousell migrated from a custom Lucene-based vector search engine (Carolene) to Elasticsearch with dense vector support — architecture, pitfalls, and production results."
tags:
  - clippings
  - medium
---
# Migrating to Elasticsearch with dense vector for Carousell Spotlight

## Background

Carousell's Spotlight boosts listing visibility. Their custom vector search engine **Carolene** (Carousell + Lucene) was built in 2018 because Elasticsearch lacked dot product support at the time. After growing to 10K+ documents, Carolene had critical issues: OOM errors, index corruption, and replication failures.

## Why Elasticsearch (from v7.6)

Elasticsearch 7.6 added stable dense vector support (DotProduct + CosineSimilarity), plus mature cluster orchestration, HA, index sharding, and replication.

**Important caveat**: dense vector operations are still O(M×N) — Elasticsearch offers better operations, not better algorithms.

## Performance results

| Setup | P50 | P90 | P99 |
|---|---|---|---|
| Carolene (stronger hardware, 13K docs, 400 QPS) | ~4ms | ~30ms | ~100ms |
| Elasticsearch POC (13K docs, 400 QPS) | ~43ms | ~77ms | ~121ms |
| Elasticsearch production (actual) | **~8ms** | **~24ms** | **~77ms** |

Production outperformed POC expectations significantly.

## Practical tips

1. **No silver bullets** — benchmark your specific configuration
2. **Separate indexes early** — split by frequently filtered predicates
3. **Filter aggressively first** — reduce N in O(M×N) before vector calculations
4. **Match tool to scale** — dense vector for small-to-medium indexes needing high precision; ANN (FAISS, Annoy) for massive datasets prioritizing recall

## Related Concepts
- [[Dense Embeddings]] — the vector type used for Spotlight search
- [[Dense Vector Retrieval]] — dot product and cosine similarity in Elasticsearch
- [[Embeddings]] — parent concept
- [[Search Architecture]] — migration case study; Carolene → Elasticsearch architecture
- [[Vector Filtering]] — filtering before vector calculations to reduce O(M×N) cost

## People
- [[Eric Feng Chao]] — Carousell; migration author