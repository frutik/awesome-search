---
type: company
aliases: ["X", "Twitter/X"]
category: end-user
industry: [social media, real-time communications]
products: [Twitter/X search, real-time tweet indexing, Earlybird]
search_domain: real-time social content search
scale: 500M+ tweets/day indexed, <15s from tweet to searchable, millions of QPS
use_cases: ["[[Twitter - Real-Time Search at Scale]]"]
tags: [company, end-user, social-media, real-time-search]
created: 2026-05-16
---

# Twitter / X

Social media platform with one of the highest-throughput real-time search systems in the world. Search must index 500M+ tweets per day with near-real-time freshness.

## Search Context

Twitter Search is extraordinary in its real-time demands: a tweet must become searchable within 15 seconds of posting. This is a fundamentally different architecture problem from batch-indexed systems.

## Key Engineering Work

### Earlybird — Real-Time Distributed Index
- Kafka write-ahead log → multiple Earlybird index shards
- In-memory inverted index segments with periodic disk merge
- Query fan-out: query all shards in parallel, merge results

### Stability Mechanisms
- **Per-shard circuit breakers** — a single overloaded shard doesn't cascade to the rest
- **Query timeout budgets** — hard latency ceiling with partial results fallback
- **Ranked shard pruning** — skip low-importance shards when under load
- **Serving latency vs completeness trade-offs** — return fewer results rather than miss SLA

## Articles

- [[Twitter Search Stability and Scalability]] — Earlybird architecture, circuit breakers, real-time indexing

## Related Concepts

- [[Search Architecture]] · [[Retrieval Pipeline]] · [[BM25]]
