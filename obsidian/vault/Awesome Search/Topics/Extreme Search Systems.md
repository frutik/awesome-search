---
type: topic
title: Extreme Search Systems
aliases:
  - extreme search
  - search at scale
  - large-scale search
  - scaling search systems
tags:
  - topic
  - architecture
  - scalability
  - performance
  - operations
related_concepts:
  - "[[Search Architecture]]"
  - "[[Sharding]]"
  - "[[Compute-Storage Disaggregation]]"
  - "[[Retrieval Pipeline]]"
  - "[[Faceted Search]]"
  - "[[Block-Max WAND]]"
  - "[[Approximate Nearest Neighbor Search]]"
  - "[[Vector Quantization]]"
  - "[[Reranking]]"
  - "[[Cross-Encoder]]"
  - "[[Learning to Rank]]"
  - "[[Hybrid Search]]"
  - "[[Zero Results]]"
related_topics:
  - "[[Vector Search Tradeoffs]]"
  - "[[Search Platforms]]"
  - "[[Search Observability]]"
  - "[[Economics of Search]]"
  - "[[Migration between Search Engines]]"
  - "[[E-commerce Search]]"
  - "[[Search using PostgreSQL]]"
articles:
  - "[[How to Build a 256 TB Search Index]]"
  - "[[BlockMax WAND - How Weaviate Achieved 10x Faster Keyword Search]]"
  - "[[How to Really Scale Autocomplete]]"
created: 2026-08-05
---

# Extreme Search Systems

Search systems become qualitatively harder to build once they cross certain scale thresholds. This
note catalogs the dimensions along which "extreme" systems get stressed — beyond the obvious pair of
index size and query rate — and points each one at the vault's worked example.

The useful observation across every case study below: **the thing that breaks is almost never the
thing that was scaled.** Uber Eats grew its delivery radius and the index *layout* became the
bottleneck. Zalando grew traffic and the *facet* queries took down the cluster. Reddit grew its
corpus and *ingest/query interference* decided the vendor. Scale doesn't strain a system uniformly;
it finds the one coupling nobody budgeted for.

## The Dimensions

| Dimension | Stress it creates | Vault anchor |
|---|---|---|
| Index size | Sharding, distributed merge, tiered storage | [[Vinted - Migrating Search from Elasticsearch to Vespa]] |
| Storage substrate | Where the authoritative index lives, and what a node's loss costs | [[How to Build a 256 TB Search Index]] |
| Query rate (QPS) | Sustained throughput plus sharp spikes | [[BlockMax WAND - How Weaviate Achieved 10x Faster Keyword Search]] |
| Write/update rate | Near-real-time indexing concurrent with search | [[Reddit - Vector Database Selection]] |
| Latency tail (p99/p999) | One slow shard blows the whole query's SLA | [[Uber Eats - Scaling Search for Food Delivery]] |
| Concurrency / multi-tenancy | Noisy-neighbor isolation as a hard requirement | [[Bonsai - Designing Search for a Relational Database]] |
| Cluster / shard count | Coordination, rebalancing, partial failure | [[Sharding]] |
| Facet / aggregation cardinality | Filtering over huge distinct-value fields | [[Zalando - Self-DoS via Facet Aggregation]] |
| Ranking complexity | ML reranking multiplying per-query compute | [[Retrieval Pipeline]] |
| Geo-distribution | Cross-region replication, routing, consistency | *(gap — see below)* |
| Cost efficiency | Cost-per-query as a first-class constraint | [[Economics of Search]] |
| Graceful degradation | Partial results beat an all-or-nothing outage | [[Canva - Search Pipeline Modernization]] |

## Index Size

Large enough that single-node indexing and serving are impossible: [[Sharding|sharding]], distributed
merge, and often tiered storage (hot/warm/cold).

[[Vinted]] is the vault's calibration point for what "large" means in a conventional deployment —
**~1 billion active searchable items** at migration time, having outgrown an [[Elasticsearch]]
deployment running since 2015. Corpus growth alone didn't force the move; it was corpus growth
*against* a fixed operational model. See [[Migration between Search Engines]].

The vault now holds **four distinct escapes from the index-size wall**, which is the more useful way
to hold this dimension than a single ceiling number:

| Escape | Example |
|---|---|
| Change engine | [[Vinted - Migrating Search from Elasticsearch to Vespa]] |
| Change index layout | [[Uber Eats - Scaling Search for Food Delivery]] |
| Change bytes per document | [[Vector Search Tradeoffs]] — quantization, dimensionality |
| Change where the index lives | [[How to Build a 256 TB Search Index]] |

## Storage Substrate

Usually treated as an implementation detail of index size, but it deserves its own axis, because it
determines **which distributed-systems problems you inherit**.

In a shared-nothing cluster, each node's local disk is authoritative. Node loss means
re-replication, rebalancing competes with query traffic, and shard size is kept modest largely to
keep those operations survivable. Under [[Compute-Storage Disaggregation]], the durable index lives in
object storage and local NVMe is a disposable cache: node loss costs a cache refill, and the
traditional argument for small shards weakens.

[[turbopuffer Search DB]] is the vault's instance. [[How to Build a 256 TB Search Index]] raises a
single namespace from **1 TB (SaaS) / 4 TB (custom) to 256 TB**, arguing that ephemeral NVMe caching
refillable at **2–4 GB/s from S3** eliminates the rebalancing cost normally associated with large
shards. For calibration, the article puts a public web snapshot at ~200 TB, implying a corpus of that size
would fit in a single namespace.

The trade: performance becomes a function of **working set rather than corpus size**. Skewed access
patterns make this architecture look excellent; uniformly hot access over hundreds of TB does not.

## Query Rate

Sustained throughput, usually with spikes that dwarf the average — flash sales, breaking news, viral
content. Capacity planning against the mean is how you discover your p99 during a campaign.

Three anchors at very different points on the curve:

- [[Vinted]]: **20,000 req/s at <150 ms p99** over ~1B items.
- [[Weaviate]] with [[Block-Max WAND]]: at **100M documents, 1 → 50 QPS** while holding p50 at
  100–200 ms and p99 ≤ 1000 ms. Early-termination algorithms buy throughput without buying hardware.
- [[How to Really Scale Autocomplete]]: **416 req/s at p99 ≤ 45 ms** on a warm index — a reminder that
  autocomplete runs at a multiple of search QPS, because it fires per keystroke.

## Write / Update Rate

Near-real-time indexing running *concurrently* with search — inventory changes, social feeds, log
ingestion — where staleness is a correctness bug, not a UX nit.

This is the axis that query-time benchmarks hide completely, and it decided a real vendor selection:
in [[Reddit - Vector Database Selection]], benchmarking at **340M vectors under 100–400 QPS with
filtering and ingest load**, [[Milvus Vector DB|Milvus]] won over [[Qdrant Vector DB|Qdrant]] largely
because its heterogeneous node architecture (separate query, ingest, and index nodes) **isolated
ingest from query traffic**. Qdrant had better raw latency in some single-replica tests. Recall was
not the deciding factor.

Two structural versions of the same constraint:

- **Index structure** — [[HNSW]] accepts incremental inserts; [[IVF]] fixes centroids at training time
  and needs retraining under corpus drift (Axis 4 of [[Vector Search Tradeoffs]]).
- **Write ordering across shards** — once a namespace spans N shards, something must define ordering.
  [[turbopuffer Search DB]] uses a **single write-ahead log per namespace with each shard consuming
  1/Nth of it**, explicitly rejecting two-phase commit because object storage latency amplifies
  coordination round-trips. See [[Sharding]].

## Latency Tail

Extreme systems are judged on p99/p999 under load, not on average latency. A single slow shard blows
the SLA for the entire query, because a fan-out query is only as fast as its slowest participant —
and with enough shards, *some* shard is having a bad moment on nearly every query.

[[Uber Eats - Scaling Search for Food Delivery]] is the vault's deepest treatment. Expanding the
delivery radius blew latency up 4×; the fixes were structural, not incremental:

- **Index layout** — sorting the index `city → stores (by conversion rate) → items`, plus
  denormalizing store metadata into item documents for better delta compression: **145 ms → 60 ms
  (−60% latency, −20% index size)**.
- **Parallelized subqueries** per ETD range bucket instead of one expanding-circle query: **another
  −50% at constant recall**, with better recall than the prior algorithm.
- **Pre-bucketing at ingestion** — precomputing hexagon-to-ETD range assignments offline so query
  execution gets simpler.

The through-line: move complexity from query time to ingestion time. Also worth stealing — diagnosis
took three months, and test stores mixed into the production index were adding 3× latency overhead on
their own.

## Concurrency and Multi-Tenancy

Many simultaneous users or tenants sharing infrastructure, with isolation as a hard requirement.
Two distinct problems get conflated here:

- **Resource isolation** — one tenant's expensive query must not degrade another's. This is the
  Reddit ingest-isolation problem generalized.
- **Access isolation** — results must be scoped to what the caller may see. The shared-index pattern
  from [[Bonsai - Designing Search for a Relational Database]] is a `permissions` array on the
  document plus a `terms` filter at query time, so one index serves many tenants.

[[Slack - Enterprise Message Search with LTR]] shows the ranking consequence: when every document is
user-specific and queries rarely repeat, the usual click-signal machinery has far less to work with.

[[Multi-Tenancy in Search]] takes this dimension in full — the isolation ladder from separate cluster
to shared-index filter, and how each engine implements it.

## Cluster and Shard Count

Hundreds to thousands of nodes and shards bring their own coordination, rebalancing, and
partial-failure problems — independent of how big the corpus is. [[Sharding]] holds the full cost
model: fan-out tail latency, per-shard [[BM25]] statistics skew, top-k merge correctness, deep paging,
and rebalancing.

Uber Eats' **H3 geosharding** is the concrete pattern — tile the world with H3 hexagons (resolution
2–3), bin them into N equal-sized shards with an offline Spark job, and index boundary documents into
both neighbouring shards via buffer zones. This replaced latitude-band sharding, which had grown
progressively more uneven as cities did. The general lesson: **a shard key chosen for the corpus you
had ages badly.**

## Facet and Aggregation Cardinality

Filtering and faceting over huge distinct-value fields (user IDs, SKUs, geo-tiles) without falling
back to full scans.

[[Zalando - Self-DoS via Facet Aggregation]] is the vault's cautionary tale, and the case study this
note most wants you to read. Facet queries are issued *separately* from result queries on every
search, are aggregation-heavy by design, and bypass the result cache. Under load, aligned cache TTLs
produced a stampede that flooded Elasticsearch with expensive aggregations and saturated the
**coordinator nodes** — not the data nodes, not the network. Users saw "0 results found" on filter
pages; the AI assistant depending on search widened the blast radius well past a UX failure.

What to take: treat aggregation as a **distinct load class** in capacity planning, monitor coordinator
saturation separately from data node saturation, and put stampede protection (TTL jitter, lock-based
recompute) on any shared aggregation cache. See [[Faceted Search]].

## Ranking Complexity

Multi-stage retrieval with ML reranking ([[Learning to Rank]], [[Cross-Encoder]]s) layered on a fast
first-stage retriever multiplies compute per query. The [[Retrieval Pipeline]] cascade exists
precisely because a cross-encoder is O(n) in corpus size and cannot be pointed at millions of
documents.

At extreme scale the latency budget, not the accuracy curve, sets the depth of the candidate set —
which makes first-stage recall the binding constraint. A document that never entered the candidate set
cannot be recovered by any reranker downstream;
[[Hybrid Fusion Failure - BM25 Displacing Reference Documents]] is the vault's worked failure of
exactly that.

## Geo-Distribution

Cross-region replication and query routing for latency and disaster recovery, with consistency
tradeoffs to manage.

**Vault gap.** Uber Eats' H3 work is geo-*partitioning* of a corpus, which is a different problem from
multi-region replication of a service. Object storage backends don't answer it either — a bucket has
its own regional story. Nothing currently in the vault covers cross-region replication topology,
read-local/write-global consistency, or regional failover for search. Worth filling with a public
write-up.

## Cost Efficiency

At this scale, cost-per-query becomes a design constraint on par with capability: compression, tiered
storage, and hardware utilization matter as much as recall.

[[Economics of Search]] holds the business framing. Three mechanical levers, in rough order of
effort:

1. **Bytes per vector** — usually the best return per unit of effort, since
   [[Vector Quantization|quantization]] costs precision per coordinate rather than recall structure:
   SQ8 for a near-lossless 4×, [[Binary Quantization]]/[[BBQ]] for 32× with rescoring. See Axis 2 of
   [[Vector Search Tradeoffs]].
2. **Index layout** — Uber Eats' −20% index size came free alongside its latency win, from
   denormalizing for better delta encoding.
3. **Storage substrate** — [[Compute-Storage Disaggregation]] decouples storage cost from serving
   cost entirely, which is the structural version of this lever rather than the incremental one.

## Graceful Degradation

Partial results under partial failure — dropped shards, timeouts — rather than an all-or-nothing
outage.

[[Canva - Search Pipeline Modernization]] implements the pattern directly: a **50 ms deadline** on
candidate generation, producing as many candidates as possible and hard-stopping at the deadline,
explicitly choosing degradation over errors. Zalando is the counter-example — the failure surfaced to
users as [[Zero Results|"0 results found"]], indistinguishable from a legitimate empty result set and
therefore the worst possible degradation signal.

Designing this well means deciding, in advance, what a degraded result is allowed to look like and how
the user and your monitoring can tell it apart from a healthy one. See [[Search Observability]].

## Case Studies in This Vault

| Case study | Dimensions it stresses |
|---|---|
| [[Vinted - Migrating Search from Elasticsearch to Vespa]] | Index size, QPS, latency tail |
| [[Uber Eats - Scaling Search for Food Delivery]] | Latency tail, shard count, index layout |
| [[Zalando - Self-DoS via Facet Aggregation]] | Aggregation cardinality, degradation, caching |
| [[Reddit - Vector Database Selection]] | Write rate, concurrency, vendor selection at scale |
| [[Canva - Search Pipeline Modernization]] | Graceful degradation under a latency deadline |
| [[Kleinanzeigen - Vespa Migration for Homepage Feed]] | Platform limits driving migration |
| [[Slack - Enterprise Message Search with LTR]] | Multi-tenancy, per-user document visibility |
| [[Netflix - Content Search Architecture]] | Federated graph search, indexing strategy |

## Related Notes

- [[Search Architecture]] — the canonical pipeline these dimensions stress
- [[Sharding]] · [[Compute-Storage Disaggregation]] — the two structural axes in full
- [[Vector Search Tradeoffs]] — the same axes viewed from the vector index side
- [[Search Platforms]] — which engine survives which dimension
- [[Search Observability]] — you cannot manage any of this without per-layer instrumentation
- [[Migration between Search Engines]] — what happens when a platform runs out of a dimension
- [[Hybrid Search]] — lexical + vector, and the fusion costs it adds per query
- [[Search Evaluation]] — the quality side; scale changes what you can afford to measure
- [[Search using PostgreSQL]] — the other end of the spectrum, and where it stops being viable
