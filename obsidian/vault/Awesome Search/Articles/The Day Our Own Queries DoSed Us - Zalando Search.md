---
title: "The Day Our Own Queries DoS'ed Us: Inside Zalando Search"
source: "https://engineering.zalando.com/posts/2025/12/we-hacked-ourselves-so-you-dont-have-to.html"
author: "[[Maryna Kryvko]]"
published: 2025-12-17
tags: [search-architecture, elasticsearch, incident, faceted-search, case-study, zalando, company-blog]
---

# The Day Our Own Queries DoS'ed Us: Inside Zalando Search

**Author:** [[Maryna Kryvko]] (Zalando Search & Browse team)

## Context

Zalando's **Search & Browse team** powers catalog search and full-text search across millions of daily requests. The system feeds not just the catalog but also Zalando Assistant (AI-powered product recommendations).

When catalog search is degraded: customers can't filter, campaigns go dark, Zalando Assistant can't fetch products. It's not just a tech issue — it's a business emergency.

## System Architecture

Layered stack (bottom to top):

1. **Base Search** (Elasticsearch): lexical + vector retrieval
2. **NER Query Builder**: Named Entity Recognition → implicit filters; also probes Base Search for product counts to decide zero-result risk
3. **Catalog API**: fans out queries, handles A/B testing, caching, redirect decisions
4. **Search API**: integrates Algorithm Gateway (ML re-ranking, personalization) + Promotions bidding

Each layer has its own cache. Coordinator nodes in ES provide an additional caching layer.

**Facet queries** (brand, size, color, price buckets) are issued *separately* from result queries on every search — aggregation-heavy by design.

## The Incident

Normal Sunday. Elasticsearch cluster became sluggish and unresponsive — queries taking seconds instead of milliseconds, timeouts, empty result pages. Users saw "0 results found" on filter pages.

**Root cause**: pathological facet/aggregation queries under high load put disproportionate pressure on Elasticsearch coordinator nodes. The aggregation-heavy nature of facet queries creates a different load profile than "plain" document retrieval — the coordinator nodes became the bottleneck.

When caches miss under load, the system floods ES with expensive aggregation queries simultaneously. Cache expiry storms compound the problem.

## Key Lessons

- **Facet queries are your hidden stress test** — they're aggregation-heavy and bypass the result query cache
- Separate fanout + aggregation load visibility from result retrieval load
- Cache expiry coordination (stampede protection) is critical at Zalando's scale
- System complexity means "search is slow" can have many root causes — thorough instrumentation required to trace to the actual bottleneck
- NER system probing Base Search for product counts (to decide filter safety) adds hidden query load that amplifies during incidents

## Related Concepts

- [[Search Architecture]]
- [[Faceted Search]]
- [[Search Evaluation]]
