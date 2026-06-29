---
type: company
tags: [company, e-commerce, fashion, recommendations, vespa, ann]
category: end-user
industry: second-hand fashion marketplace
products: [Vinted marketplace]
search_domain: [item search, product recommendations, personalized homepage retrieval]
use_cases: [Elasticsearch-to-Vespa search migration]
people: ["[[Ernestas Poškus]]"]
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

## Search Platform Migration

Vinted ran on [[Elasticsearch]] from 2015 until migrating its **billion-item, 20k-RPS** search platform to [[Vespa]] (item search Nov 2023, facets April 2024) — halving the server fleet and cutting change-visibility from 300s to 5s. See [[Vinted - Migrating Search from Elasticsearch to Vespa]].

## Key Articles & Case Studies

- [[Vinted - Migrating Search from Elasticsearch to Vespa]] — the ES→Vespa search-platform migration
- [[Adopting Vespa for Recommendation Retrieval at Vinted]] — ANN recommendation retrieval on Vespa ([[Dainius Jocas]], [[Aleksas Kateiva]])
- [[Optimizing Vespa Latency with Match-Features at Vinted]] — `match-features` for in-engine feature serving + P99 9ms→3ms ([[Dainius Jocas]])
- [[Dense Retrieval at Vinted]] — multilingual-CLIP two-tower hybrid semantic retrieval on Vespa ([[Laurynas Jasiukėnas]], [[Dainius Jocas]])
