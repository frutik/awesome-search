---
title: "Faceted Search"
aliases: ["facets", "faceted navigation", "guided navigation", "filters", "drill-down navigation"]
tags:
  - concept
  - search-ux
  - e-commerce-search
  - search
---

# Faceted Search

## Definition

Faceted search allows users to iteratively filter and narrow search results along multiple dimensions (facets) simultaneously — for example, filtering by brand, price range, color, and size at the same time. It combines search retrieval with structured navigation.

## Facets vs. Filters

**Filters**: Binary — include/exclude based on a condition.  
**Facets**: Dynamic filters that update based on the current result set, showing available options and their counts.

The key distinction: facets are *result-set-aware* — if you filter to "Nike shoes", only colors that exist in Nike shoes are shown.

## Facet Types

| Type | Example | Notes |
|------|---------|-------|
| Category | Brand, Category, Department | Hierarchical possible |
| Range | Price ($0-50, $50-100), Rating (4+) | Numeric values |
| Boolean | In stock, Free shipping | Yes/No |
| Multi-select | Color (can select multiple) | OR logic between values |
| Single-select | Size (only one applies) | Exclusive values |
| Hierarchical | Category > Subcategory | Tree navigation |

## Constraints vs. Preferences (Tunkelang)

[[Daniel Tunkelang]]'s important distinction:
- **Constraints**: must-have filters (size must fit, brand must be Nike)
- **Preferences**: nice-to-have (prefer blue, prefer under $100 but not required)

Systems that treat preferences as constraints over-filter and create zero-result pages. A good faceted search distinguishes between the two.

## How Many Facets?

The Accidental Taxonomist research: users typically engage with 3–5 facets per session. More facets → analysis paralysis. Best practice:
- Show 5–8 most useful facets by default
- Collapse others behind "More filters"
- Prioritize facets that most reduce result set size

## Faceted Search and Retrieval

Facets interact with the retrieval system:
- **Pre-filter approach**: apply facet filters before ANN search → may destroy index efficiency ([[Vector Filtering]])
- **Post-filter approach**: retrieve results, then filter → results count is inaccurate
- **Native filtered search**: Pinecone, Elasticsearch kNN support inline filtering ([[Vector Filtering]])

## Dynamic Facets

Advanced: dynamically generate facets based on query content rather than showing all facets always:
- Query "shoes" → show size, color, brand facets
- Query "laptop" → show RAM, storage, processor facets
- Requires ML to predict relevant facets per query type

## Facet Counting Problem

Showing accurate counts per facet value is technically challenging:
- Must count matching documents per facet value without actually filtering
- For sparse facets (most docs have the value), count = full result set size minus non-matching
- For dense attribute fields: term aggregations in Elasticsearch handle this efficiently

## Related Concepts

- [[Search Intent]] — facets help disambiguate broad queries
- [[Query Types]] — navigational queries often don't need facets; exploratory queries do
- [[Vector Filtering]] — technical implementation of facet + vector search
- [[Diversity Metrics]] — facets are a user-driven diversity mechanism
- [[Zero Results]] — misconfigured facets cause empty result sets

- [[Compositional Queries]] — AND/OR/NOT facet combinations; the query type faceting produces
- [[Box Embedding]] — region/Venn-diagram embeddings that answer compositional facet queries (see [[Answering Compositional Queries with Set-Theoretic Embeddings]])

## People

- [[Daniel Tunkelang]] — "Facets of Faceted Search", "Facets: Constraints or Preferences?", queryunderstanding.com faceted search

- [[Facets - Constraints or Preferences]]
- [[Facets, But Which Ones]]
- [[Searching for Goldilocks]]
- [[Thoughts on Search Result Diversity]]
