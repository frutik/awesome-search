---
title: turbopuffer Search DB
type: tool
tags:
  - tool
  - vector-database
  - search-engine
  - object-storage
  - scalability
website: https://turbopuffer.com/
maintainer: "[[turbopuffer]]"
created: 2026-08-05
---

# turbopuffer Search DB

Search database built **object-storage-native**: the authoritative copy of the index lives in S3 or
GCS, and serving nodes hold a cache hierarchy over it. Maintained by [[turbopuffer]] (the company).

- Website: https://turbopuffer.com/

---

## What It Does

Vector search first, with full-text search as a secondary capability, over indexes whose durable
storage is object storage rather than local disk. The design goal is cost-per-query and elasticity at
large corpus sizes rather than minimum achievable latency.

Key characteristics, as described in [[How to Build a 256 TB Search Index]]:

- **[[Compute-Storage Disaggregation]]** — object storage is authoritative; local NVMe is the lowest
  level of a cache hierarchy, and is **ephemeral**. Losing a node costs a cache refill, not a
  re-replication.
- **Namespaces** — the unit of an index. As of the sharding release, a single namespace can reach
  **256 TB**, up from 1 TB on the SaaS product and 4 TB for custom deployments.
- **[[Sharding]] with a single WAL** — one write-ahead log per sharded namespace, each of N shards
  consuming 1/Nth of it. All writes land in one log with one sequence order; indexing and queries
  scale out across shards. Two-phase commit was explicitly rejected.
- **Query cost** — logarithmic within a shard, linear across shards.
- **Cache warming** — 2–4 GB/s from S3 on modern cloud VMs, with sub-file reads rather than whole-object
  copies.
- **Parallel indexing** across machines in the cluster.
- Supports filtering, and references [[Late Interaction]] retrieval methods.

## Scale Calibration

The corpora the 256 TB ceiling is pitched against, from the same article:

| Corpus | Approx. size |
|---|---|
| Wikipedia | 1 TB |
| SEC filings | 2 TB |
| U.S. case law | 5 TB |
| arXiv | 10 TB |
| Public web snapshot | 200 TB |

## Where It Sits Among Engines

| | turbopuffer | [[Elasticsearch]] / [[OpenSearch]] | [[Qdrant Vector DB]] / [[Milvus Vector DB]] |
|---|---|---|---|
| Durable index | Object storage | Local disk (searchable snapshots for cold tiers) | Local disk |
| Node loss | Cache refill | Re-replicate shard | Re-replicate shard |
| Strength | Cost at large corpora, elasticity | Mature full-text, ecosystem | ANN features, filtered search |
| Floor latency | Bounded by cache hit rate | Local disk | Local disk / memory |

See [[Search Platforms]] for the broader comparison and [[Compute-Storage Disaggregation]] for when
this trade is the right one.

## Caveats for Evaluation

- **No published latency or throughput numbers** in the source article — nothing here is comparable
  to the measured figures in [[Vinted - Migrating Search from Elasticsearch to Vespa]] or
  [[BlockMax WAND - How Weaviate Achieved 10x Faster Keyword Search]].
- Performance depends on **working set**, not corpus size. A large index with concentrated query
  traffic behaves very differently from one with uniformly random access.
- The comparative claim about competitors' ~50 GB shard limits is the vendor's, unsourced in the post.

## Related Notes

- [[Compute-Storage Disaggregation]] — the architecture pattern
- [[Sharding]] — the partitioning problem and its costs
- [[Extreme Search Systems]] — the scale dimensions this addresses
- [[Search Platforms]] — engine comparison
- [[Vector Search Tradeoffs]] — the index-level trades underneath

## Sources

- [[How to Build a 256 TB Search Index]] — [[Nathan VanBenschoten]], 2026-08-05
