---
type: concept
title: "Compute-Storage Disaggregation"
aliases:
  - storage-compute separation
  - disaggregated storage
  - object storage search
  - search on S3
  - separation of storage and compute
tags:
  - concept
  - architecture
  - scalability
  - object-storage
  - cost
created: 2026-08-05
---

# Compute-Storage Disaggregation

## Definition

An architecture in which the **durable copy of the index lives in object storage** (S3, GCS, Azure
Blob) and the machines serving queries hold only a **cache** of it. Serving nodes become stateless in
the sense that matters operationally: losing one destroys no data, and replacing one costs a cache
refill rather than a data migration.

Contrast with the classical **shared-nothing** search deployment — [[Elasticsearch]], [[Solr]],
[[OpenSearch]] in their default shapes — where each node owns local disk holding a primary or replica
shard, and that ownership is the unit of durability, of failure, and of rebalancing.

```
Shared-nothing                          Disaggregated
─────────────                           ─────────────
node ── local disk (authoritative)      node ── NVMe cache ─┐
node ── local disk (authoritative)      node ── NVMe cache ─┼─→ object storage
node ── local disk (authoritative)      node ── NVMe cache ─┘   (authoritative)
   ↑ replication between peers             ↑ each node independently refills
```

## Why It Changes the Cost Model

The interesting consequences are not about storage price, though that is the headline. They are about
which distributed-systems problems you stop having.

| Problem | Shared-nothing | Disaggregated |
|---|---|---|
| Node loss | Lost replica; re-replicate from a peer | Lost cache; refill from object storage |
| Rebalancing | Move data between peers, throttled to protect queries | Largely dissolves — no authoritative local copy to move |
| Scaling reads | Add replicas, each a full copy | Add cache nodes against one shared copy |
| Durability | Replication factor × index size | Object storage's own durability |
| Idle cost | Nodes sized for the corpus, always on | Storage cost decouples from serving cost |
| Cold start | Fast (data is local) | Bounded by cache-fill bandwidth |

The last row is the real trade. Disaggregation converts a *data placement* problem into a *bandwidth
and cache hit rate* problem. It is a good trade only when refill bandwidth is high enough that a cold
node becomes useful quickly — [[How to Build a 256 TB Search Index]] cites **2–4 GB/s from S3** on
modern cloud VMs as what makes it viable, along with the ability to read sub-file ranges rather than
whole objects.

## The Latency Objection

Object storage has first-byte latency in the tens of milliseconds — hopeless for a p99-sensitive
query path if it were on the critical path per query. Disaggregated search systems answer this with a
**cache hierarchy**, typically memory → local NVMe → object storage, so object storage is touched on
cold reads and cache fills rather than per query.

This means the architecture's performance is a function of **working set** rather than corpus size.
A 200 TB index with a hot 200 GB working set behaves like a 200 GB system; one with uniformly random
access over 200 TB does not. Access-pattern skew is the load-bearing assumption, and it is why the
pattern suits large archival corpora with concentrated query traffic better than it suits uniformly
hot workloads.

## Interaction with Sharding

Disaggregation does not remove the need for [[Sharding]] — a single shard still has an index
structure with its own size limits — but it changes what a shard costs. When local state is a
disposable cache, the traditional argument for keeping shards small (rebalancing pain, recovery time,
hotspot migration) weakens considerably. [[How to Build a 256 TB Search Index]] makes exactly this
claim about ephemeral NVMe caching eliminating the rebalancing cost of large shards.

It also changes the write path. Since object storage punishes coordination round-trips more than
local disk does, distributed commit protocols become more expensive here than in a shared-nothing
cluster — which is the stated reason [[turbopuffer]] built on a single shared write-ahead log rather
than two-phase commit.

## Where It Shows Up

- **[[turbopuffer Search DB]]** — search database built object-storage-native from the start; see
  [[How to Build a 256 TB Search Index]].
- **Elasticsearch/OpenSearch searchable snapshots and tiered storage** — retrofitted onto a
  shared-nothing design, typically for warm/cold tiers rather than the hot path.
- The pattern has an older lineage in analytics databases (Snowflake, BigQuery) and streaming
  (Kafka tiered storage); search is a comparatively late adopter, because latency SLAs are tighter.

## Trade-offs Summary

**Favours disaggregation:** very large corpora, skewed access patterns, spiky or unpredictable query
load, cost-per-query as a first-class constraint, workloads where elasticity matters more than
floor latency, many idle-but-must-exist indexes (per-tenant namespaces).

**Favours shared-nothing:** small-to-medium corpora that fit comfortably in RAM, uniformly hot access,
very tight p99 targets, on-prem deployments without a good object store, workloads already well
served by an existing cluster.

## Related Notes

- [[Sharding]] — the partitioning problem this reshapes but does not remove
- [[Search Architecture]] — where the storage layer sits in the whole system
- [[Extreme Search Systems]] — the scale dimensions that make this trade worth making
- [[Multi-Tenancy in Search]] — why namespace-per-tenant became affordable
- [[Economics of Search]] — cost-per-query as a design constraint
- [[Search Platforms]] — which engines are built this way
- [[Vector Search Tradeoffs]] — the complementary lever, bytes per vector rather than location of bytes

## Sources

- [[How to Build a 256 TB Search Index]] — [[Nathan VanBenschoten]]; object-storage-native sharding at 256 TB
