---
title: "Mapping Search Queries To Search Intents"
source: "https://medium.com/@dtunkelang/search-queries-and-search-intent-1dec79ad155f"
author: ["Daniel Tunkelang"]
tags:
  - clippings
  - query-understanding
  - search-intent
  - search
  - medium
concepts:
  - Search Intent
  - Query Understanding
  - Query Types
created: 2026-05-15
---

# Mapping Search Queries To Search Intents

**Source**: https://medium.com/@dtunkelang/search-queries-and-search-intent-1dec79ad155f  
**Author**: [[Daniel Tunkelang]]

## Summary

[[Daniel Tunkelang]] examines the relationship between search queries (what users type) and search intents (what users want), arguing that this mapping is the core challenge of [[Query Understanding]] and that most search failures are failures of intent mapping, not retrieval.

## The Query-Intent Gap

Users rarely express their full intent in a query. A user searching for "python" on a developer site has a completely different intent than the same query on a nature website.

**The gap**:
- Query: short, ambiguous, underspecified
- Intent: rich, contextual, often multi-faceted

Closing this gap = query understanding.

## Intent Dimensions

[[Daniel Tunkelang]] identifies multiple dimensions of intent beyond the simple navigational/informational/transactional taxonomy:

### 1. Topical Intent
What subject area? "python" → programming OR reptile

### 2. Task Intent
What task? Informational (learn about python) vs. transactional (download python) vs. navigational (go to python.org)

### 3. Specificity Intent
How specific? "shoes" (browse) vs. "Nike Air Max 90 size 10.5 white" (exact match)

### 4. Quality Intent
What quality matters? Price-sensitive, brand-loyal, novelty-seeking

### 5. Freshness Intent
How recent? "latest iphone" vs. "best iphone for older users" (historical)

## Intent Signals in Queries

Linguistic patterns that signal intent:

| Signal | Example | Intent Implied |
|--------|---------|---------------|
| Question words | "how to...", "what is..." | Informational |
| Buy/price words | "buy", "price", "cheap" | Transactional |
| Site-like queries | "amazon", "facebook login" | Navigational |
| Comparison words | "vs", "compare", "best" | Comparative |
| Vague adjectives | "cool", "nice", "interesting" | Discovery |

## The "Intent Not Inventory" Principle

Tunkelang's key insight (later developed in "Search: Intent, Not Inventory"):

> A search for "birthday cake ideas" is not a search for documents containing those words. It's a search for inspiration, recipes, images, and perhaps local bakeries.

The search system should serve the *intent* (birthday party planning help), not literally match the *query* (documents about birthday cake ideas).

## Practical Implications

1. For ambiguous queries: [[Diversity Metrics]] to cover multiple intents
2. For high-confidence intent: streamline to directly serve the intent
3. For transactional intents: structured data (price, availability) matters as much as text
4. For discovery intents: personalization and trending signals matter

## Related Articles

- [[Search - Intent Not Inventory]] — same author, extends this argument
- [[Query Understanding - Divided into Three Parts]] — three-part framework includes intent
- [[AI for Query Understanding]] — LLM approach to intent classification
- [[Food Discovery with Uber Eats]] — industrial intent mapping at scale

## Related Concepts

- [[Search Intent]] — primary concept
- [[Query Understanding]] — framework containing intent mapping
- [[Query Types]] — how types map to intents
- [[Diversity Metrics]] — for multi-intent queries

## People

- [[Daniel Tunkelang]] — author
