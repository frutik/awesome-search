---
created: 2026-05-16
type: article
tags: [article, vespa, ann, two-tower, recommendations, e-commerce, company-blog]
source: "https://vinted.engineering/2023/10/09/adopting-vespa-for-recommendation-retrieval/"
author: ["Vinted"]
company: [Vinted]
concepts: [Dense Vector Retrieval, ANN, Embeddings, Hybrid Search]
topics: [Personalization in Search, E-commerce Search]
---

# Adopting Vespa for Recommendation Retrieval at Vinted

**Vinted** (Europe's largest second-hand fashion marketplace) migrated from FAISS to Vespa for serving personalized homepage recommendations.

## System Design

3-stage recommender:
1. **Recall** (Vespa ANN, <100ms): two-tower model encodes user history + listing metadata into embeddings; approximate nearest neighbor search retrieves candidates
2. Downstream ranking stages

## Why Not FAISS

- Read-only index required periodic rebuild/redeploy
- No prefiltering: post-processing degraded recall when user applied filters

## Vespa vs Elasticsearch Benchmark

Tested on 1M documents, 256-dim float32 embeddings, consistent HNSW parameters:

| Metric | Vespa | Elasticsearch |
|--------|-------|--------------|
| Indexing throughput | 3.8× faster | — |
| RPS before CPU saturation | 8× higher | — |
| P99 latency at saturation | 26ms | 110ms |

## ANN vs Exact Search A/B Test

HNSW recall ~60–70% vs exact, but user satisfaction did not improve enough with exact search (P99 latency jumped 40%: 50ms → 70ms) to justify the cost.

## Key Takeaway

ANN prefiltering — combining vector similarity with metadata filters (size, price, brand) at query time — is the critical capability that FAISS couldn't provide and Vespa handles natively.

## Related Concepts

[[Dense Vector Retrieval]] · [[ANN]] · [[Embeddings]] · [[Hybrid Search]] · [[Personalization in Search]] · [[E-commerce Search]]
