---
type: company
tags: [company, e-commerce, fashion, recommendations, vespa, ann]
category: end-user
industry: second-hand fashion marketplace
products: [Vinted marketplace]
search_domain: [product recommendations, personalized homepage retrieval]
use_cases: []
people: []
---

# Vinted

Europe's largest online second-hand fashion marketplace. Serves users across multiple European markets with personalized item recommendations on the homepage.

## Search & Recommendations Architecture

**3-stage recommender system**:
1. **Recall** (Vespa + ANN): Two-tower model — user embedding (from interaction sequence) vs. listing embedding (brand, price, size, photos). ANN retrieves candidates in <100ms. Key requirement: prefiltering by user-set filters (size, category) at query time.
2. Downstream ranking stages

**Why Vespa over FAISS**: FAISS is a read-only index requiring periodic rebuild; no prefiltering. Vespa supports real-time updates and metadata-filtered ANN natively.

**Benchmark results** (1M docs, 256-dim):
- Vespa indexing: 3.8× faster than Elasticsearch
- Vespa query throughput: 8× higher RPS before CPU saturation
- Vespa P99 latency: 26ms vs. 110ms for Elasticsearch

**ANN accuracy**: ~60–70% recall vs. exact search, but user satisfaction did not improve with exact search (latency cost not worth it).

## Key Articles

- [[Adopting Vespa for Recommendation Retrieval at Vinted]]
