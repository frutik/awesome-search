---
type: case-study
company: "[[Vinted]]"
tags: [case-study, vespa, elasticsearch, platform-migration, e-commerce, scalability, faceted-search]
source: "https://vinted.engineering/2024/09/05/goodbye-elasticsearch-hello-vespa/"
published: 2024-09-05
people:
  - "[[Ernestas Poškus]]"
---

# Vinted — Migrating Search from Elasticsearch to Vespa

> Field report from "Search Scaling Chapter 8: Goodbye Elasticsearch, Hello Vespa Search Engine" ([[Ernestas Poškus]], Vinted Engineering, 2024-09-05).

## Context

[[Vinted]] is Europe's largest C2C marketplace for second-hand fashion. It had run on [[Elasticsearch]] since **May 2015**, but the platform hit scalability limits as the catalog and traffic grew. At migration time the system served:

- **~1 billion** active searchable items
- **20,000 req/s** at **<150 ms p99**
- indexing at **10,300 RPS** (updates/removals); a single item update visible at **4.64 s p99**
- on **6 Elasticsearch clusters × 20 data nodes** (each 128 cores, 512 GB RAM, 0.5 TB SSD RAID1)

## Problem

The pain was operational, not relevance:

- **Shard/replica management** was "time-consuming and error-prone," especially **reindexing on schema changes**.
- Constant fine-tuning of shard/replica ratios — maintenance was "a constant burden."
- **Hot nodes** and uneven load; scaling forced **complex data reshuffling**.

They wanted a long-term, scalable engine that removed this toil while handling growing data and query complexity.

## Solution: Consolidate onto Vespa

A dedicated **Search Platform team of 4** drove the migration, organized around five pillars: architecture, infrastructure, indexing, querying, and metrics/performance testing.

### Infrastructure
- **One** [[Vespa]] cluster: **60 content nodes, 3 config nodes, 12 container nodes** (content nodes: 128 cores, 512 GB RAM, **3 TB NVMe RAID1**).
- HAProxy balances traffic across **stateless container nodes** (no hot nodes); Istio/Envoy planned.

### Indexing
- Plugged Vespa into the existing **Apache Flink** Search Indexing Pipeline, adopting Vespa's document schema.
- **Open-sourced a Vespa Kafka Connect sink connector**, sustaining up to **50k RPS** updates/removals per deployment.

### Querying
- Integrated **Lucene text-analysis components into Vespa** so they could **keep their existing language analysers** and port Elasticsearch text-analysis config directly — a key de-risking move.
- Built custom searchers behind a standardized **"search contract"** in a **Go middleware service**, exposing **12 distinct query patterns** to product apps.

### Ranking
- Increased **ranking depth >3×, to 200,000 candidate items** — a significant relevance/business win.
- Took **~4 A/B-test iterations** before search quality matched the old system.

## Migration Timeline

| Date | Milestone |
|---|---|
| **May 2023** | Project start |
| **Nov 2023** | Item-search traffic fully on Vespa |
| **April 2024** | Faceted search migrated |

## Results

- **Search latency: 2.5× faster**
- **Indexing latency: 3× faster**
- **Change visibility: 300 s → 5 s** (Elasticsearch refresh interval → near-real-time)
- **Servers halved, to 60**
- **No more hot nodes** — load evenly distributed; no data reshuffling when scaling
- Eliminated the recurring shard/replica management tax
- **3× ranking depth (200k candidates)** improved relevance with measurable business impact

As of the post, Vinted ran **21 distinct Vespa deployments** (item search, image retrieval, search suggestions, …), with only a handful of features still on Elasticsearch and full consolidation planned by end of 2024. The team called it "a roaring success."

## Postscript: Reaching Billion-Scale (Chapter 9, Jan 2025)

A follow-up ([[Dainius Jocas]], 2025-01-10) reports the payoff: the index passed **1 billion searchable documents by Nov 2024** — ~10× the ~100M of 2019 — on the same Vespa platform. Mean latency stayed **<20 ms at the data layer** with low, controlled CPU, internal benchmarks showed **~2× headroom**, and the billion-scale transition was "surprisingly uneventful." Next on their roadmap: vector semantic search (delivered in [[Dense Retrieval at Vinted]]) and reverse image search.

## Why It Matters

A rare, concrete account of a **billion-item, 20k-RPS production search platform** moving off Elasticsearch — and the lesson that the decisive win was **operational** (shard toil, hot nodes, near-real-time visibility, halved fleet) as much as raw latency. The Lucene-analyzers-in-Vespa trick is the migration-enabling detail. Compare with [[Kleinanzeigen - Vespa Migration for Homepage Feed]] (the same ES→Vespa move, for a personalized feed).

## Concepts

[[Vespa]] · [[Elasticsearch]] · [[Search Architecture]] · [[Faceted Search]] · [[Retrieval Pipeline]] · [[Search Platforms]]

## Related Notes

- [[Kleinanzeigen - Vespa Migration for Homepage Feed]] — the parallel ES→Vespa migration
- [[Adopting Vespa for Recommendation Retrieval at Vinted]] — Vinted's other Vespa use (recommendation retrieval / ANN)
- [[Elasticsearch vs OpenSearch]] · [[Search Platforms]] — engine-selection context
- [[Late Interaction in Vespa]] · [[Vespa Learning to Rank]] — what Vespa's ranking framework enables next
- [[Migration between Search Engines]] — the broader platform-migration topic this case study anchors
