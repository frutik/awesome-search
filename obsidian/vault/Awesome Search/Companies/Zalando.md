---
type: company
industry: fashion e-commerce
products:
  - Zalando (fashion marketplace)
  - Zalando Assistant (AI recommendations)
search_domain: fashion catalog search + AI-powered product recommendations
use_cases:
  - "[[Zalando - Self-DoS via Facet Aggregation]]"
---

# Zalando

## Search Context

Zalando is Europe's largest fashion platform. Their **Search & Browse team** powers:
- Catalog search (full-text + filter) for millions of daily requests
- Zalando Assistant — an AI-powered product recommendation system that queries the same search infrastructure

This coupling means search degradation has compound blast radius: not just UX failures, but AI assistant failures and dark campaigns.

## Search Challenges

- **Facet-heavy catalog**: fashion filtering (brand, size, color, price, fit) generates aggregation-heavy queries that have different load profiles from result retrieval
- **Cache stampede risk**: layered caches across all tiers create expiry coordination problems under load
- **Dual consumers**: search serves both direct user queries and AI assistant product fetches — blast radius spans both
- **Scale**: millions of daily queries with latency SLAs in the tens of milliseconds

## Tech Stack

- **Elasticsearch** as the core retrieval engine (Base Search layer)
- Four-layer architecture: Base Search → NER Query Builder → Catalog API → Search API + Algorithm Gateway
- Each layer independently cacheable; ES coordinator nodes provide additional caching
- NER for entity recognition → implicit filter injection

## People

- [[Maryna Kryvko]] — Search & Browse team
- [[Tao Ruangyam]] — Search engineering; LLM-as-judge quality framework

## Use Cases

- [[Zalando - Self-DoS via Facet Aggregation]]

## Published Articles

- [[The Day Our Own Queries DoSed Us - Zalando Search]]
- [[Search Quality Assurance with AI as a Judge]] — LLM-as-judge pipeline for pre-launch market validation (2026)
