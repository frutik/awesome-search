---
created: 2026-05-16
title: "Optimizing Search at Uber Eats"
source: "https://www.infoq.com/presentations/optimization-search-uber/"
author: "Janani Narayanan, Karthik Ramasamy"
published: 2025-04-25
tags: [search-architecture, scaling, geosharding, lucene, case-study, uber]
---

# Optimizing Search at Uber Eats

**Authors:** [[Janani Narayanan]] (ML Engineer, Uber) and [[Karthik Ramasamy]] (Senior Staff SWE, Uber)  
QCon San Francisco 2025 talk.

## Challenge: nX Merchant Growth

Uber Eats expanded from restaurants to grocery (100k SKUs/store) and retail, with delivery radius growing from 10-15 min to 50+ miles. Goal: scale selection by nX while maintaining latency.

**Naive approach failed**: increasing early termination count by 200 restaurants → P50 latency increased 4x.

## Architecture Layers

1. **Base Search** (Elasticsearch/Lucene custom platform): lexical + vector retrieval
2. **NER Query Builder**: entity recognition → implicit filters, zero-result detection
3. **Catalog API**: fan-out queries, A/B test integration, redirect decisions; caching
4. **Search API** + **Algorithm Gateway**: personalization/ML re-ranking + promotions bidding

Discovery surfaces: Home Feed (most orders), Search, Suggestions, Ads — all served by same infra.

## Geosharding: Two Approaches

### Latitude Sharding
- World sliced into latitude bands → equal-sized shards
- Benefit: cities from different time zones co-locate (traffic follows sun) → balanced load
- Problem: bands too narrow at center (dense cities), shards become uneven over time

### Hex Sharding (H3)
- World tiled with hexagons at resolution 2-3
- Offline Spark job bins hexagons into N equal shards (bin-packing)
- Buffer zones: documents near shard boundaries indexed in both shards
- More uniform than latitude; handles dense city centers better

## Document Layout Optimization

### Eats Index Layout
Sorted: city → restaurants sorted by conversion rate → items per restaurant

- Skip directly to target city documents
- Denormalized fields (store metadata in item docs) → compression via delta encoding
- Static rank ordering → early termination once budget hit

**Result: 60% latency improvement** (145ms → 60ms for a 4K-doc query), index size -20%

### Grocery Index Layout
Sorted: city → store (by conversion rate) → items per store

- Per-store budget: skip to next store once limit reached
- Diversity: results from multiple stores, not dominated by one

## ETD (Estimated Time of Delivery) Indexing

**Root cause of 4x latency**: ingestion lost ETD distance metadata (close-by vs. far-away), so query layer couldn't differentiate.

**Solution**: Pre-compute hexagon-to-ETD range assignments offline (time ranges: 0-10 min, 10-20 min, etc.). Each store indexed multiple times across different ETD ranges.

**Trade-off**: more storage/ingestion complexity → simpler, faster query execution.

## Parallelization of ETD Ranges

Instead of one expanding-circle query:
- Multiple parallel queries, one per ETD range bucket
- Non-overlapping subqueries → safe to parallelize
- Also parallelized: strong match + fuzzy match + OR queries

**Final result**: 50% latency reduction at constant recall, *plus* improved recall vs. prior algorithm.

## Key Lessons

- Index layout is "the most overlooked piece of software" — worth years of investment
- Move complexity from query time to ingestion time
- Benchmark before assuming root cause (3 months to diagnose, 4-6 months to XP)
- Test stores in production index added 3x latency overhead — clean separation matters
- Custom search platform built on Apache Lucene with Lambda architecture (Spark batch + Kafka streaming)

## Related Concepts

- [[Search Architecture]]
- [[Learning to Rank]]
- [[Search Evaluation]]
