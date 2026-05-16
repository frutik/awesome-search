---
type: use-case
company: "[[Zalando]]"
domain: fashion e-commerce
problem: production incident — self-induced DoS from facet aggregation queries under load
scale: millions of daily requests; search also feeds Zalando Assistant (AI product recommendations)
concepts:
  - "[[Search Architecture]]"
  - "[[Faceted Search]]"
  - "[[Search Evaluation]]"
sources:
  - "[[The Day Our Own Queries DoSed Us - Zalando Search]]"
people:
  - "[[Maryna Kryvko]]"
---

# Zalando — Self-DoS via Facet Aggregation

## Problem

On a normal Sunday, Zalando's Elasticsearch cluster became sluggish and unresponsive. Queries took seconds instead of milliseconds. Users saw "0 results found" on filter pages. The system that feeds both catalog search and the AI assistant (Zalando Assistant) was down. Not just a technical failure — campaigns went dark, and the AI assistant couldn't fetch products.

## Architecture

```
Base Search (Elasticsearch)
    ↓ lexical + vector retrieval
NER Query Builder
    ↓ entity recognition → implicit filters; probes Base Search for product counts
Catalog API
    ↓ fan-out, A/B tests, caching, redirect decisions
Search API
    ↓ Algorithm Gateway (ML re-ranking) + Promotions bidding
```

Each layer has its own cache. ES coordinator nodes provide an additional caching layer.

**Facet queries** (brand, size, color, price buckets) are issued *separately* from result queries on every search — aggregation-heavy by design.

## Root Cause

Pathological interaction between load and facet queries:

1. Facet aggregation queries are structurally different from document retrieval — they put disproportionate pressure on ES coordinator nodes
2. Under high load, caches missed simultaneously across the tier
3. Cache expiry storms: when cache TTLs aligned and cache missed at scale, the system flooded ES with expensive aggregation queries simultaneously
4. NER system's habit of probing Base Search for product counts (to decide filter safety) added hidden query load that amplified the cascade

The coordinator nodes became the bottleneck — not the data nodes, not the network.

## Key Lessons

- **Facet queries are a hidden stress test** — they're aggregation-heavy and bypass the result cache
- Separate fanout + aggregation load visibility from result retrieval load in monitoring
- Cache stampede protection (jitter on TTL, distributed lock on expensive recomputes) is critical at scale
- A layered architecture means "search is slow" can have many root causes — thorough per-layer instrumentation is required to trace the actual bottleneck
- The AI assistant dependency on search made the blast radius much larger than a pure UX failure

## What to Steal

- Treat facet/aggregation queries as a distinct load class in capacity planning
- Add cache stampede protection (probabilistic early expiry or lock-based recompute) wherever aggregation queries share a cache tier
- Monitor coordinator node saturation separately from data node saturation in Elasticsearch
- Instrument NER and other query-expansion systems for the hidden query load they generate
