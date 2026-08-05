---
type: company
title: "turbopuffer"
aliases: ["turbopuffer.com"]
website: "https://turbopuffer.com/"
tags:
  - company
  - vector-database
  - search-infrastructure
  - object-storage
created: 2026-08-05
---

# turbopuffer

Search infrastructure company building [[turbopuffer Search DB]], a search database whose index lives
in object storage with a local cache hierarchy over it. Positioning is cost and scale at large corpus
sizes — see [[Compute-Storage Disaggregation]] for why that architecture makes a different set of
trades than [[Elasticsearch]]-style shared-nothing clusters or the local-disk vector databases
([[Qdrant]], [[Weaviate]], [[Pinecone]]).

- Website: https://turbopuffer.com/

## Notable Contributions

**Single-WAL multi-shard design (2026)** — sharding for an object-storage-native search engine that
avoids distributed commit entirely. One write-ahead log per namespace gives a single global sequence
order for writes; each of N shards consumes 1/Nth of that log, so indexing and queries scale out
without coordination between shards. Two-phase commit was rejected on the stated grounds that its
round-trip cost is amplified by object storage latency, and that "simplicity scales." Raised the
per-namespace ceiling from 1 TB (SaaS) / 4 TB (custom) to **256 TB**. See
[[How to Build a 256 TB Search Index]].

**Ephemeral-NVMe cache tiering** — the argument that rebalancing cost is a property of stateful nodes
rather than of large shards. If local state is a disposable cache refillable at 2–4 GB/s from S3,
large shards stop being operationally painful, which is what makes the 256 TB ceiling practical.

## People

- [[Nathan VanBenschoten]] — chief architect; previously principal engineer at Cockroach Labs

## Articles

- [[How to Build a 256 TB Search Index]]

## Related Notes

- [[turbopuffer Search DB]] — the product
- [[Compute-Storage Disaggregation]] — the architectural bet
- [[Search Platforms]] — where it sits among search engines
- [[Extreme Search Systems]] — the scale problems it targets
