---
type: concept
title: "Feature Store"
aliases: ["feature store", "feature stores"]
tags:
  - concept
  - ranking
  - learning-to-rank
  - infrastructure
---

# Feature Store

## Definition

A feature store is the system that persists and serves the **ranking features** an [[Learning to Rank|LTR]] model consumes — BM25 components, popularity/CTR counters, item metadata (price, category), user/profile signals — keeping training-time and serving-time feature values consistent.

## Why it matters for ranking

In a search system, ranking features are either:

- **Stored in the index** — fast at query time but requires frequent full reindexing when features change, or
- **Served from an external feature store** — decoupled from the index, updatable in real time, but adds a serving dependency and network hop.

This tradeoff is central to multi-stage / secondary re-ranking: an external re-ranker like [[Metarank]] keeps aggregated user/item feature state in **Redis**, pulled in a single batched request per re-rank (a key driver of re-ranking latency).

## Related Concepts

- [[Learning to Rank]] · [[LambdaMART]] · [[Reranking]] · [[Retrieval Pipeline]]
- [[Click Signals]] · [[Personalization]] — common feature sources

## Articles

- [[Learn-to-Rank with OpenSearch and Metarank]] — feature store vs. in-index features tradeoff
- [[Metarank - Personalized Ranking That Actually Reads Your Clicks]]
- [[Part 1 - Learning to Rank for E-Commerce Search at Otto]] — Solr feature store
