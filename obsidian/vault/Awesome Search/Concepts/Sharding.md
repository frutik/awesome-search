---
type: concept
title: "Sharding"
aliases:
  - shard
  - shards
  - index partitioning
  - horizontal partitioning
  - geosharding
tags:
  - concept
  - architecture
  - scalability
  - distributed-systems
created: 2026-08-05
---

# Sharding

## Definition

Splitting an index into **shards** — disjoint partitions, each a self-contained index — so that a
corpus too large for one machine can be indexed and served by many. A query is scattered to the
shards, each returns its local top-k, and a coordinator merges the partial results into a final
ranking.

```
query ──┬──→ shard 1 ──→ local top-k ──┐
        ├──→ shard 2 ──→ local top-k ──┼──→ merge ──→ final top-k
        ├──→ shard 3 ──→ local top-k ──┤
        └──→ shard N ──→ local top-k ──┘
```

Distinct from **replication**, which copies the same shard to multiple nodes for throughput and
availability. Real deployments do both: shards divide the corpus, replicas divide the query load.

## The Costs Sharding Introduces

Sharding is not free scaling. It buys capacity by introducing four problems that a single-node index
does not have.

### 1. Fan-out makes the tail the average

Every query waits for the **slowest** shard. With enough shards, some shard is having a bad moment on
essentially every query, so p99 behaviour of individual shards becomes p50 behaviour of the system.
This is why [[Extreme Search Systems]] treats tail latency as its own scale dimension rather than a
consequence of load.

The counter-intuitive consequence: **adding shards to reduce per-shard work can make queries slower.**
[[How to Build a 256 TB Search Index]] states this shape directly — query cost is logarithmic within a
shard but **linear across shards**.

### 2. Scoring becomes approximate

[[BM25]]'s IDF term is a corpus-level statistic. Computed per shard, it differs between shards, so the
same document can score differently depending on where it landed. Systems either accept the skew
(usually fine with many documents and even distribution), or run a preliminary round to gather global
term statistics, paying a round-trip.

The same issue recurs for any global normalization — including [[Score Normalization]] in
[[Hybrid Search]] fusion, where per-shard score ranges are not comparable.

### 3. Top-k merging is only correct for decomposable rankings

Taking the top-k from each shard and merging is exact when the score of a document is independent of
other documents. It is **not** exact for anything with a global view: diversity constraints
([[MMR]], [[Search Result Diversity]]), deduplication across shards, or pagination deep into the
result set. Deep paging is the classic failure — retrieving results 10,000–10,010 requires each shard
to return 10,010 candidates.

### 4. Rebalancing

The shard key chosen for the corpus you had ages badly. Redistributing data across a live cluster
competes with query traffic for I/O and is typically throttled, making it slow precisely when it is
most needed.

## Choosing a Shard Key

| Strategy | Good for | Fails when |
|---|---|---|
| **Hash of doc ID** | Even distribution, simple | No query ever touches fewer than all shards |
| **Time-based** | Logs, news; old shards go cold and can be tiered | Recent shards are hot, load is skewed |
| **Tenant / customer** | Multi-tenant search; queries hit one shard | Tenant sizes vary by orders of magnitude |
| **Geographic** | Location-constrained retrieval | Density is uneven — cities are not uniform |
| **Semantic / cluster-based** | Skipping irrelevant shards entirely | Drift; unbalanced clusters |

The prize for a well-chosen key is **shard pruning** — proving a shard cannot contain a match and
skipping it, which converts fan-out from N shards to a handful and reverses cost 1 above.

[[Uber Eats - Scaling Search for Food Delivery]] is the vault's worked example: **H3 geosharding**,
tiling the world with hexagons (resolution 2–3) and binning them into N equal-sized shards with an
offline Spark job, with buffer zones indexing boundary documents into both neighbouring shards. It
replaced latitude-band sharding, which had grown steadily more uneven as cities grew — a shard key
aging badly, exactly as above.

## Shard Sizing

The conventional advice in shared-nothing engines like [[Elasticsearch]] is to keep shards
moderately sized — tens of GB — with the reasoning being recovery time, rebalancing cost, and
heap pressure per shard, not any intrinsic index limit.

[[Compute-Storage Disaggregation]] undermines most of that reasoning. When the authoritative copy of
the index sits in object storage and local disk is a disposable cache, node loss costs a cache refill
rather than a re-replication, and rebalancing largely dissolves. This is the argument in
[[How to Build a 256 TB Search Index]] for allowing namespaces of **256 TB**, against the roughly
**50 GB** per-shard guidance it attributes to competing systems.

## Writes Across Shards

Once a namespace spans N shards, a write must reach the right shard and the system must define what
ordering guarantees hold across them. The conventional answer is a distributed commit protocol; the
alternative is to make ordering a property of a shared log.

[[turbopuffer Search DB]] takes the latter route: **one write-ahead log per namespace, with each of
the N shards consuming 1/Nth of it** — a single sequence order for all writes, with indexing and
querying still scaled out. Two-phase commit was rejected explicitly for its coordination cost, which
object storage latency would amplify. See [[How to Build a 256 TB Search Index]].

The write-side constraint interacts with the index structure too: [[HNSW]] accepts incremental
inserts, while [[IVF]] fixes centroids at training time, so a resharding or large corpus shift means
retraining. See Axis 4 of [[Vector Search Tradeoffs]].

## Related Notes

- [[Compute-Storage Disaggregation]] — changes what a shard costs to own
- [[Extreme Search Systems]] — shard count and fan-out as scale dimensions
- [[Search Architecture]] — where partitioning sits in the whole system
- [[Uber Eats - Scaling Search for Food Delivery]] — H3 geosharding in production
- [[Vinted - Migrating Search from Elasticsearch to Vespa]] — ~1B items, 20,000 req/s at <150 ms p99
- [[Approximate Nearest Neighbor Search]] — the per-shard index the fan-out sits on top of
- [[Awesome Search/Topics/Search Observability|Search Observability]] — per-shard instrumentation is how tail latency gets diagnosed

## Sources

- [[How to Build a 256 TB Search Index]] — [[Nathan VanBenschoten]]; single-WAL multi-shard on object storage
- [[Awesome Search/Articles/Optimizing Search at Uber Eats|Optimizing Search at Uber Eats]] — H3 geosharding, index layout, parallelized subqueries
