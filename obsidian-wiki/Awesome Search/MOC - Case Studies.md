---
title: "MOC — Case Studies"
tags:
  - moc
  - search
  - case-study
created: 2026-05-15
---

# MOC — Case Studies

Map of content covering real-world search implementations across e-commerce, consumer, enterprise, and research contexts.

## E-Commerce

### Airbnb
- [[Machine Learning-Powered Search Ranking of Airbnb Experiences]] — 4-stage ML progression, +28% bookings
- [[Listing Embeddings in Search Ranking]] — 32-dim embeddings from 800M sessions, +21% CTR

### Carousell
- [[Migrating to Elasticsearch with Dense Vector for Carousell Spotlight]] — keyword → dense vector migration

### Etsy
- [[Targeting Broad Queries in Search]] — entropy/diversity for broad queries
- [[How Etsy Uses Thermodynamics for Search]] — thermodynamic entropy for result diversity

### Uber Eats
- [[Optimizing Search at Uber Eats]] — geosharding (H3), document layout optimization (60% latency cut), ETD range indexing; [[Janani Narayanan]] & [[Karthik Ramasamy]] at QCon

### Zalando
- [[The Day Our Own Queries DoSed Us - Zalando Search]] — [[Maryna Kryvko]]; self-DoS via facet aggregation; layered architecture (Base Search → NER → Catalog API → Search API)

## Consumer / Social

### Slack
- [[Search at Slack]] — LTR with SVM on work graph, +27% P@1; position bias handling

### Netflix
- [[How Netflix Makes a Federated Graph Searchable]] — federated entity graph + vector embeddings (Parts 1 & 2)

## Travel / Marketplace

### Skyscanner
- [[Learning to Rank for Flight Itinerary Search]] — LTR for flights, purchase as relevance signal

## Enterprise / Infrastructure

### Amazon (OpenSearch + Bedrock)
- [[Innovating Search Experience with Amazon OpenSearch and Amazon Bedrock]]

### Canva
- [[Canva Search Pipeline Part I]] — big ball of mud problem, 20k rps, 50 entry points
- [[Canva Search Pipeline Part II]] — componentized pipeline: validation → annotation → generation → reranking

## Research / Academic

### Semantic Scholar (AI2)
- [[Building a Better Search Engine for Semantic Scholar]] — LightGBM+LambdaRank, +8% clicks, 190M papers

## Key Themes Across Case Studies

| Theme | Companies |
|---|---|
| Embedding-based personalization | Airbnb, Carousell |
| Multi-stage ranking | Airbnb, Slack, Semantic Scholar, Skyscanner |
| Graph-based search | Netflix |
| Architecture modernization | Canva |
| Position bias handling | Slack |

## Related MOCs

- [[MOC - Ranking and Retrieval]]
- [[MOC - Agentic Search and Embeddings]]
- [[MOC - Architecture]]
