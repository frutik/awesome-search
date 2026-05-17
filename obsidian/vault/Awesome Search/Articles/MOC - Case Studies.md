---
title: "MOC — Case Studies"
tags:
  - moc
  - search
  - case-study
created: 2026-05-15
---

# MOC — Case Studies

Map of content covering real-world search implementations. Each **Use Case** note synthesizes what a company built and what to steal from it. **Article** notes are the underlying source material.

## E-Commerce

### Airbnb — [[Airbnb]]
- **[[Airbnb - ML-Powered Experiences Ranking]]** — 4-stage ML progression, +28% bookings; Category Intensity; business rules via training weight
- [[Machine Learning-Powered Search Ranking of Airbnb Experiences]] *(source article)*
- [[Listing Embeddings in Search Ranking]] — 32-dim embeddings from 800M sessions, +21% CTR

### Carousell
- [[Migrating to Elasticsearch with dense vector for Carousell Spotlight 1]] — keyword → dense vector migration

### Etsy
- [[Targeting Broad Queries in Search]] — entropy/diversity for broad queries
- [[How Etsy Uses Thermodynamics for Search]] — thermodynamic entropy for result diversity
- [[Modeling Spelling Correction for Search at Etsy]]

### Uber Eats — [[Uber]]
- **[[Uber Eats - Scaling Search for Food Delivery]]** — H3 geosharding, document layout optimization (60% latency cut), ETD range indexing
- [[Optimizing Search at Uber Eats]] *(source article)*
- [[Food Discovery with Uber Eats - Building a Query Understanding Engine]] *(source article)*

### Zalando — [[Zalando]]
- **[[Zalando - Self-DoS via Facet Aggregation]]** — self-DoS via facet aggregation under load; cache stampede; layered architecture blast radius
- [[The Day Our Own Queries DoSed Us - Zalando Search]] *(source article)*

## Consumer / Social

### Slack — [[Slack]]
- **[[Slack - Enterprise Message Search with LTR]]** — work graph as LTR signal, position bias correction, +27% P@1
- [[Search at Slack]] *(source article)*

### Netflix
- [[How Netflix Makes a Federated Graph Searchable]] — federated entity graph + vector embeddings (Parts 1 & 2)
- [[Netflix Elasticsearch Indexing Strategy in AMP]]

### Spotify
- [[You Say Search I Say Recs - Spotify Agentic Query Understanding]] — agentic query understanding merging search and recommendations

### Twitter
- [[Twitter Search Stability and Scalability]]

## Travel / Marketplace

### Skyscanner
- [[Learning to Rank for Flight Itinerary Search]] — LTR for flights, purchase as relevance signal

## Enterprise / Infrastructure

### Amazon (OpenSearch + Bedrock)
- [[Innovating Search Experience with Amazon OpenSearch and Amazon Bedrock 1]]

### Canva
- [[Canva Search Pipeline Part I]] — big ball of mud problem, 20k rps, 50 entry points
- [[Canva Search Pipeline Part II]] — componentized pipeline: validation → annotation → generation → reranking

## Research / Academic

### Semantic Scholar (AI2)
- [[Building a Better Search Engine for Semantic Scholar]] — LightGBM+LambdaRank, +8% clicks, 190M papers

---

## Key Themes Across Case Studies

| Theme | Companies |
|---|---|
| Index layout as performance lever | [[Uber]] |
| Incremental ML adoption (staged rollout) | [[Airbnb]], Skyscanner |
| Work graph / interaction graph as signal | [[Slack]] |
| Position bias correction | [[Slack]], [[Airbnb]] |
| Cache stampede under load | [[Zalando]] |
| Facet aggregation as hidden load | [[Zalando]] |
| Geo-aware search sharding | [[Uber]] |
| Embedding-based personalization | [[Airbnb]], Carousell |
| Multi-stage ranking | [[Airbnb]], [[Slack]], Semantic Scholar, Skyscanner |
| Graph-based search | Netflix |
| Architecture modernization | Canva |

## Companies

[[Uber]] · [[Airbnb]] · [[Zalando]] · [[Slack]]

## Related MOCs

- [[MOC - Ranking and Retrieval]]
- [[MOC - Agentic Search and Embeddings]]
- [[MOC - Architecture and Search Team]]

## Enterprise Search

### Dropbox — [[Dropbox]]
- [[Using LLMs to Amplify Human Labeling and Improve Dash Search Relevance]] — Dropbox Dash enterprise search; LLM-as-judge calibrated on human labels; 100x label amplification; DSPy prompt optimization

## Ecommerce Governance (Elastic)

- [[Why Ecommerce Search Needs Governance and How It Improves Retrieval]] — [[Elastic]]; intent routing + governance control plane for ecommerce
- [[Ecommerce Search Governance - Move Faster Not Slower]] — [[Elastic]]; zero-deploy operating model; policies as data
- [[Elasticsearch Personalized Search in Ecommerce - Improve Relevance]] — [[Elastic]]; purchase history + cohort personalization
