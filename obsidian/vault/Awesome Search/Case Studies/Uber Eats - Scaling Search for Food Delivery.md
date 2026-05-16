---
type: use-case
company: "[[Uber]]"
domain: food delivery / e-commerce search
problem: scale search from restaurants to grocery and retail while cutting latency
scale: ~100M users, delivery radius expanded to 50+ miles, grocery stores with 100k SKUs
concepts:
  - "[[Search Architecture]]"
  - "[[Learning to Rank]]"
  - "[[Faceted Search]]"
sources:
  - "[[Optimizing Search at Uber Eats]]"
  - "[[Food Discovery with Uber Eats - Building a Query Understanding Engine]]"
people:
  - "[[Janani Narayanan]]"
  - "[[Karthik Ramasamy]]"
---

# Uber Eats — Scaling Search for Food Delivery

## Problem

Uber Eats expanded from restaurants to grocery (100k SKUs/store) and retail, with delivery radius growing from 10–15 min to 50+ miles. Naively increasing the retrieval budget blew up latency 4x. The team needed to scale selection by nX without sacrificing query speed.

## Architecture

Four-layer stack, each layer independently cacheable:

```
Base Search (Elasticsearch/Lucene custom)
    ↓ lexical + vector retrieval
NER Query Builder
    ↓ entity recognition → implicit filters, zero-result detection
Catalog API
    ↓ fan-out, A/B test integration, redirect decisions, caching
Search API + Algorithm Gateway
    ↓ ML re-ranking, personalization, promotions bidding
```

Same infrastructure powers: Home Feed, Search, Suggestions, Ads.

## Solutions

### H3 Geosharding
Tiled the world with H3 hexagons (resolution 2–3), then used an offline Spark job to bin hexagons into N equal-sized shards. Buffer zones index boundary documents in both neighboring shards.

Previous latitude-band sharding created uneven shards over time as cities grew. H3 handles dense city centers far better.

### Document Layout Optimization
Sorted the index: `city → stores (by conversion rate) → items per store`

- Allows early termination once per-store budget is hit
- Denormalized store metadata into item documents → better delta encoding compression
- **Result: 60% latency reduction** (145ms → 60ms), index size -20%

### ETD Range Indexing
Root cause of the original 4x latency spike: the query layer couldn't distinguish close-by from far-away stores because ETD metadata was lost at ingestion. Fix: pre-compute hexagon-to-ETD range assignments offline (0–10 min, 10–20 min, etc.) and index each store in every applicable ETD bucket.

More storage and ingestion complexity → dramatically simpler, faster query execution.

### Parallelized Queries
Instead of one expanding-circle query: multiple parallel subqueries per ETD range bucket. Also parallelized: strong match + fuzzy match + OR queries.

**Result: 50% further latency reduction at constant recall, plus improved recall vs. prior algorithm.**

## Key Lessons

- **Index layout is the most overlooked piece of search engineering** — worth years of investment
- Move complexity from query time to ingestion time
- Diagnose before assuming root cause — took 3 months to identify the actual bottleneck
- Test stores mixed into production index added 3x latency overhead — environment isolation matters
- Cache layering at every tier is essential; each layer independently cacheable

## What to Steal

- H3-based geosharding for any location-sensitive search problem
- Static sort order by conversion rate + per-entity budget for structured catalogs (grocery, retail)
- ETD/SLA pre-bucketing pattern: pre-compute constraint ranges at index time instead of filtering at query time
