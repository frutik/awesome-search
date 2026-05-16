---
title: "The Day Our Own Queries DoS'ed Us: Inside Zalando Search"
source: "https://engineering.zalando.com/posts/2025/12/we-hacked-ourselves-so-you-dont-have-to.html"
author:
  - "[[Maryna Kryvko]]"
published: 2025-12-17
created: 2026-05-15
description: "Once upon a time, during a normal Sunday, our team ran into an unexpected challenge: an Elasticsearch cluster that suddenly became sluggish and unresponsive due to a self-inflicted Denial of Service (DoS) attack."
tags:
  - "clippings"
---
Once upon a time, during a normal Sunday, our team ran into an unexpected challenge: an Elasticsearch cluster that suddenly became sluggish and unresponsive due to a self-inflicted Denial of Service (DoS) attack (of course we didn't know it at the time). This is the story of how we identified, mitigated, and learned from this incident.

## Who We Are

We are part of Zalando's **Search & Browse team**, responsible for maintaining and optimizing the catalog and full-text search backends that power millions of user requests every single day. Our systems serve multiple catalog domains and experiences – from the core catalog to the Designer experience and our full-text search – and they also feed newer interfaces like [Zalando Assistant](https://corporate.zalando.com/en/technology/more-personal-and-smarter-zalando-assistant-enhanced-capabilities-inspire-customers), which depends on us to fetch and recommend products in real time.

When everything is healthy, the experience feels effortless. Customers can search, filter, and explore the catalog, ask Zalando Assistant for ideas and instantly see relevant products. At the same time, our brand partners' promotions, campaigns, and sponsored placements are delivered as planned, reaching the right users at the right moment.

![Catalog page with dresses](https://img01.ztat.net/engineering-blog/posts/2025/12/images/catalog-dresses.png?imwidth=1320#center)

Catalog page with dresses

But when catalog search is slow or down, the impact is immediate and far-reaching. Customers suddenly can't find what they want, filters and discovery flows break, and Zalando Assistant simply can't fetch products to show. Partner campaigns underperform or effectively go dark, meaning money, planning, and trust are burned in real time. Negative reviews, customer complaints, and internal escalations start popping up across channels as frustration grows.

In short: when catalog search is degraded, it's not "just" a tech issue. It hits customers, partners, campaigns, and Zalando's reputation all at once. **It's a big deal. A very, very big deal.**

## Anthology of the System Under High Load

From the outside, "search is slow" looks like a single symptom. In reality, it flows through several layers, each doing its own work and adding its own pressure under load.

At the bottom, we have **Base Search**, an Elasticsearch cluster that provides initial candidates using both classic lexical matching and vector search. On top of that sits our full‑text search **query builder** Named Entity Recognition (NER) system, which takes the raw user intent (query text, user filters). Based on recognized entities it promotes implicit filters. Filters could be applied to shrink or expand results. NER system builds an Elasticsearch query and attaches metadata indicating whether the result set looks sparse and might require expansion using our newer neural matching system.

NER system also queries the Base Search to acquire product counts to understand how many products match different filter combinations and to decide whether we can safely narrow the search with extra filters without risking "zero results".

Above that, the **Catalog API**, one of our presentation layers, coordinates everything that has to happen for a single "search" in the app:

- It fans out a request into several queries to Base Search.
- It is integrated with our A/B testing framework, so different users or cohorts may trigger slightly different query shapes.
- It owns the "final redirect" decisions – for example, whether a query should land on a generic search result page or on dedicated landing pages.

Each layer includes its own caching:

- The query builder and Catalog API cache popular queries and filter combinations.
- In Elasticsearch, coordinator nodes are placed on separate machines and provide another caching layer for search results and aggregations.
- The Base Search Elasticsearch cluster itself is wrapped by a lightweight Search API component - another presentation layer.

The **Search API** in turn integrates with other components:

- **Algorithm Gateway** enriches results with user actions data and re‑ranked using the rules engine and our personalization and relevance ML models.
- **Promotions bidding service**, it blends sponsored content with organic results.

For every search, the Catalog API issues a separate call to fetch the filters (facets) for that query: brand, size, color, price bucket, etc. These are aggregation‑heavy queries by design and stress Elasticsearch differently than plain result retrieval queries.

## The Incident

Normal Sunday. The Elasticsearch cluster became sluggish and unresponsive — queries taking seconds instead of milliseconds, timeouts cascading through the stack, users seeing empty result pages.

**Root cause**: pathological facet/aggregation queries under high load put disproportionate pressure on Elasticsearch coordinator nodes. The aggregation-heavy nature of facet queries creates a different load profile than plain document retrieval — the coordinator nodes became the bottleneck.

When caches miss under load, the system floods Elasticsearch with expensive aggregation queries simultaneously. Cache expiry storms compound the problem — multiple layers of caching all expiring around the same time create a thundering herd effect on the underlying cluster.

The NER system's behavior of probing Base Search for product counts (to decide filter safety) added additional hidden query load that amplified the problem during the incident.

## Key Lessons

- **Facet queries are your hidden stress test** — they're aggregation-heavy and bypass the result query cache
- Separate visibility into fanout + aggregation load from result retrieval load
- Cache expiry coordination (stampede protection) is critical at scale
- System complexity means "search is slow" can have many root causes — thorough instrumentation is required to trace to the actual bottleneck
- NER system probing Base Search for product counts adds hidden query load that amplifies during incidents
- When everything is layered with caches, a cache miss storm can cascade into a full cluster DoS

## Read More

Full article: [We Hacked Ourselves So You Don't Have To](https://engineering.zalando.com/posts/2025/12/we-hacked-ourselves-so-you-dont-have-to.html)