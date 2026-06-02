---
type: company
industry: search infrastructure / observability
products:
  - Elasticsearch
  - Kibana
  - Elastic Search Labs
category: technology-provider
search_domain: open-source + managed search and observability platform
---

# Elastic

## What They Build

Elastic makes **Elasticsearch** — the dominant open-source distributed search engine built on Apache Lucene. It is the default backend for a large share of production search systems globally (e-commerce, log analytics, enterprise search). Elastic also runs a cloud offering (Elastic Cloud) and a Search Labs blog that publishes practical search engineering content.

## Search Contributions

### Retrieval Models
- **[[ELSER]]** (Elastic Learned Sparse Encoder) — production-grade sparse retrieval model based on [[SPLADE]]. Achieves +17% NDCG@10 over BM25 on BEIR benchmarks with zero-shot performance
- **[[BBQ]]** (Better Binary Quantization) — scalar + binary quantization approach for Elasticsearch dense vector fields; competitive with TurboQuant at fraction of the cost

- **[[Block-Max WAND]]** — introduced in Lucene 8.0 / Elasticsearch 7.0 (2019) by [[Adrien Grand]]; 3x–15x speedup for top-k retrieval; required API change (`hits.total` now object with `value`+`relation`, controlled by `track_total_hits`)

### Search Features
- `function_score` query — the primary [[Results Boosting]] mechanism in Elasticsearch
- `kNN` + pre-filter pipeline — [[Vector Filtering]] support in dense vector search
- Native [[Hybrid Search]] with BM25 + dense vector combination

### Applied Examples Published
- Multilingual hybrid search + reranking on Elasticsearch
- E-commerce personalization via purchase history in Elasticsearch
- Margin and popularity boosting patterns (governed control plane)

## Tech Stack Significance

Elasticsearch is used as the underlying engine in many case studies in this vault:
- [[Zalando]] — Base Search layer
- [[Uber]] — custom Lucene platform
- Semantic Scholar — Elasticsearch with ML reranker on top

## People

- [[Thomas Veasey]] — Principal Engineer, Elastic
- [[Leonie Monigatti]] — Developer Advocate / ML Engineer; writes on agentic search and context engineering

- [[Adrien Grand]] — Principal Engineer, Elastic; core Lucene committer; implemented [[Block-Max WAND]]

## Articles

- [[Elastic Learned Sparse Encoder ELSER Retrieval Performance]]
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]]
- [[Multilingual Embedding Model Hybrid Search Reranking]]
- [[Ecommerce search optimization with margin & popularity boosting]]
- [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]]
- [[Agentic Search for Context Engineering]] — [[Leonie Monigatti]]; three search tool patterns for context engineering

- [[Faster Retrieval of Top Hits in Elasticsearch with Block-Max WAND]]

## Concepts
[[ELSER]] · [[BBQ]] · [[BM25]] · [[Block-Max WAND]] · [[WAND]] · [[Results Boosting]] · [[Hybrid Search]]


### Governed Ecommerce Search Series (2026)

A 7-part series on building governed search control planes for ecommerce:
- [[Why Ecommerce Search Needs Governance and How It Improves Retrieval]] — intent classification + routing
- [[Ecommerce Search Governance - Move Faster Not Slower]] — zero-deploy operating model
- [[Elasticsearch Personalized Search in Ecommerce - Improve Relevance]] — purchase history + cohort personalization

## Additional People

- [[Alexander Marquardt]] — Elastic Services Engineering
- [[Honza Král]] — Elastic
- [[Taylor Roy]] — Elastic
- [[Peter Straßer]] — Elastic; late interaction / ColPali scaling
- [[Benjamin Trent]] — Elastic; late interaction / ColPali scaling

## Additional Concepts

[[Search Governance]] · [[Personalization]]

## Tools
- [[Elasticsearch]]
