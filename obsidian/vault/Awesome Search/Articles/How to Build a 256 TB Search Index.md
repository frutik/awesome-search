---
created: 2026-08-05
title: "How to Build a 256 TB Search Index"
source: "https://www.linkedin.com/pulse/how-build-256-tb-search-index-nathan-vanbenschoten-wjqic/"
author: "[[Nathan VanBenschoten]]"
company:
  - "[[turbopuffer]]"
published: 2026-08-05
type: article
concepts:
  - "[[Compute-Storage Disaggregation]]"
  - "[[Sharding]]"
  - "[[Search Architecture]]"
  - "[[Approximate Nearest Neighbor Search]]"
  - "[[Late Interaction]]"
topics:
  - "[[Extreme Search Systems]]"
  - "[[Search Platforms]]"
  - "[[Vector Search Tradeoffs]]"
tags: [article, scalability, sharding, object-storage, vector-search, architecture, turbopuffer]
---

# How to Build a 256 TB Search Index

**Author:** [[Nathan VanBenschoten]] — chief architect, [[turbopuffer]]

## Summary

An announcement-plus-design post on raising the maximum size of a single
[[turbopuffer Search DB]] namespace from **1 TB** (SaaS; 4 TB for custom deployments) to **256 TB**,
by introducing sharding to a search engine whose index already lives on object storage. The article contrasts this ceiling with the
roughly **50 GB per-shard limits** it attributes to competing systems.

The interesting content is not the number. It is the claim that **building on object storage changes
which sharding problems you have** — that several costs which normally make large shards painful
(rebalancing, data movement, coordinated commit) either shrink or disappear when the durable copy of
the index already sits in S3 or GCS and local disk is only a cache.

## The Design: Single WAL, N Shards

The central decision, in the author's words: retain

> "a single write-ahead log for sharded namespaces, but ... have each of the N shards pull 1/Nth of
> the data from the WAL when consuming it."

The stated property this buys is that it allows

> "all writes to land in a single log with a single sequence order, while enabling indexing and
> queries to scale out across the shards."

So writes stay totally ordered in one log — there is one sequence order for the whole namespace, not
one per shard — while indexing and query execution fan out. Shards are consumers of a shared log
rather than independent replicas with their own write paths.

## Why Not Two-Phase Commit

The conventional answer to "writes now span N shards" is a distributed commit protocol. The article
rejects two-phase commit (2PC) explicitly, on two grounds:

1. It "ran counter to our guiding principle that *simplicity scales*."
2. The protocol has "known performance problems at scale, problems that would be exacerbated by
   object storage."

The second point is the load-bearing one: 2PC's cost is coordination round-trips, and object storage
has latency characteristics that punish round-trips far more than local disk does. A design whose
correctness comes from *ordering in a single log* rather than *agreement across participants* avoids
paying that per-write.

Worth reading alongside the author's background — see [[Nathan VanBenschoten]] — since this is a
distributed-transactions argument imported into search infrastructure.

## Why Object Storage Changes the Shard Calculus

Claims made about the storage substrate:

- **Cache warming is fast.** Modern cloud VMs pull **2–4 GB/s from S3**, so populating a local cache
  from the durable copy is not the multi-hour ordeal it is when data must be shipped between peers.
- **Sub-file reads.** Data can be read directly out of object storage without copying whole objects.
- **Ephemeral NVMe as the lowest cache tier.** The article describes "big, fast, ephemeral NVMe
  drives (the lowest level of our cache hierarchy)" and argues this **eliminates the rebalancing
  costs traditionally associated with large shards** — if a node's local copy is disposable and
  cheaply refetched, moving or losing it is not an event.
- **Indexing parallelizes** across machines in the cluster.

A three-tier cache hierarchy is referenced but not fully specified in the post; only the NVMe tier is
described in detail.

## Query Scaling

Stated shape of the cost curve:

- **Logarithmic within a single shard** — the usual index behaviour.
- **Linear across shards** — every shard participates, so adding shards adds work per query.

This is the trade the design makes explicit: sharding buys capacity, and pays for it in fan-out. It
is the same tail-latency exposure described in [[Extreme Search Systems]] — a query's latency becomes
the slowest shard's latency.

## What 256 TB Is For

The article calibrates the ceiling against real corpora:

| Corpus | Approx. size |
|---|---|
| Wikipedia | 1 TB |
| SEC filings | 2 TB |
| U.S. case law | 5 TB |
| arXiv | 10 TB |
| Public web snapshot | 200 TB |

The implied claim: a single namespace can now hold a full public web snapshot with room left over.

## Retrieval Context

The post frames the system around **vector search**, with full-text search "to a lesser extent," and
references [[Late Interaction]] retrieval methods. [[BM25]] is not mentioned. Relevant because
multi-vector representations multiply storage per document — the corpus sizes above are the input,
not the index footprint.

## What This Vault Should Take From It

- A **fourth escape route** from the index-size wall, distinct from the ones already catalogued:
  Vinted changed engine ([[Vinted - Migrating Search from Elasticsearch to Vespa]]), Uber Eats changed
  index layout ([[Uber Eats - Scaling Search for Food Delivery]]), the quantization literature changes
  bytes per vector ([[Vector Search Tradeoffs]]) — this changes *where the index lives*.
- The observation that **storage substrate determines which distributed-systems problems you inherit.**
  Rebalancing is a cost of stateful nodes, not of large indexes.
- A concrete argument that **coordination protocols are the thing to design away**, not optimize.

## Caveats

- No query latency or write throughput figures are given. Nothing here can be compared against the
  measured numbers in [[Vinted - Migrating Search from Elasticsearch to Vespa]] (20,000 req/s at
  <150 ms p99) or [[BlockMax WAND - How Weaviate Achieved 10x Faster Keyword Search]].
- No recall or relevance results.
- Vendor-authored, announcing the vendor's own capability. The design reasoning is checkable; the
  comparative claim about competitors' 50 GB shard limits is not sourced in the post.

## Related Notes

- [[Compute-Storage Disaggregation]] — the architectural pattern this is an instance of
- [[Sharding]] — the general problem and its cost model
- [[turbopuffer Search DB]] — the system; [[turbopuffer]] — the company
- [[Extreme Search Systems]] — the dimension catalogue this feeds
- [[Search Platforms]] — where this sits among engines
