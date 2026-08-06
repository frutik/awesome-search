---
type: topic
title: "Multi-Tenancy in Search"
aliases: ["multitenancy", "multi-tenant search", "tenant isolation", "index per tenant", "namespace per tenant", "tenant routing"]
tags: [topic, search-architecture, scalability, saas, access-control]
related_concepts: ["[[Sharding]]", "[[Unified Search Index]]", "[[Denormalization for Search]]", "[[Compute-Storage Disaggregation]]", "[[Vector Filtering]]", "[[Search Scopes]]", "[[Search Governance]]", "[[Search Architecture]]", "[[BM25]]", "[[HNSW]]", "[[Learning to Rank]]"]
related_topics: ["[[Extreme Search Systems]]", "[[Federated vs Unified Search]]", "[[Enterprise Search]]", "[[Search Platforms]]", "[[Awesome Search/Topics/Economics of Search|Economics of Search]]", "[[Awesome Search/Topics/Search Observability|Search Observability]]", "[[Migration between Search Engines]]"]
articles: []
created: 2026-08-06
---

# Multi-Tenancy in Search

One search system serving many tenants — customers, workspaces, sellers, or individual
users — whose data must not leak into each other's results. Every design decision reduces to
one question: **at what level does one tenant's data become physically separate from
another's?** Everything else — schema, routing, scoring, cost, access control — follows from
where that line is drawn.

---

## The Isolation Ladder

| Level | Unit per tenant | Isolation | Realistic tenant count | Cost of an idle tenant |
|---|---|---|---|---|
| **Separate deployment** | Cluster | Total — separate hardware, separate blast radius | tens | A full node |
| **Separate index** | Index / collection | Strong — own schema, analyzers, settings, lifecycle | hundreds to low thousands | Per-shard base cost |
| **Named partition** | Namespace / tenant shard / partition key / group | Data physically separated, resources shared | 10⁵–10⁶ | Near zero on object storage |
| **Shared index** | A filter clause on a tenant field | Logical only — enforced by query construction | unbounded | Zero |

Isolation and tenant count trade directly against each other. The interesting recent
development is the third row: most vendors have converged on a *named partition inside a
shared resource*, which buys physical separation without per-tenant infrastructure.

## Four Questions That Decide the Level

1. **What isolation does compliance demand?** Data residency or contractual separation can
   forbid co-mingling outright, pushing you to per-region clusters or to
   [[Federated Search|federation]] over data you may not copy at all — see
   [[Federated vs Unified Search]].
2. **How many tenants, and how skewed?** Tenant size follows a power law almost everywhere.
   The whale that is 10,000× the median breaks any uniform scheme.
3. **Do queries ever cross tenants?** Admin search, cross-tenant analytics, and global
   dashboards are trivial in a shared index and a fan-out problem when each tenant owns an index.
4. **Who controls schema and relevance config?** Per-tenant synonyms, analyzers, or ranking
   rules are hard to express in one shared mapping, and often the thing that forces
   index-per-tenant.

---

## Indexing

### Schema and mapping

A shared index means one schema for everyone. If one tenant wants `field1` as text and
another as a date, someone loses — the usual resolution is first-write-wins plus a forced
rename. Left unmanaged, per-tenant custom fields produce mapping explosion.

The [[Unified Search Index]] purpose-field discipline is the way out: map every tenant's
columns onto a small fixed set of fields defined by *information need* rather than by source
schema, exactly as [[Bonsai - Designing Search for a Relational Database]] does across tables.
What it cannot absorb is per-tenant *analysis* — custom synonyms, stopwords, or language
config — which is where index-per-tenant starts to earn its cost.

### Per-tenant overhead

Index-per-tenant looks clean and fails on economics. There is a base memory cost per shard
regardless of how little data it holds, so a freemium product with a long tail of tiny tenants
ends up reserving hardware for non-paying users. Index and alias metadata also live in cluster
state, replicated to every node — thousands of per-tenant aliases become a cluster-stability
problem in their own right, on top of ordinary [[Sharding|over-sharding]].

### Routing and co-location

The middle path is a shared index where the tenant id determines *placement*:

- Elasticsearch/OpenSearch `_routing` on tenant id, so a tenant's documents land on one shard.
- Solr composite ids (`tenant!docid`), hashing 16 bits from the shard key and 16 from the
  document id, with `_route_` at query time.
- Qdrant's `is_tenant: true` keyword index, which co-locates a tenant's vectors for
  sequential disk reads instead of random seeks.

This converts the tenant filter into **shard pruning** — the prize described in [[Sharding]] —
turning fan-out over N shards into a single-shard query.

### Tenant size skew

Routing by tenant is exactly the shard key [[Sharding]] warns ages badly: tenant sizes vary by
orders of magnitude and grow unpredictably. The durable answer is to keep **tenants and shards
independent**: pool the long tail behind routing, promote a growing tenant to its own index,
and make the mapping a config value operations can change without an application deploy. Solr
offers multi-level routing for the same problem; Vespa's streaming mode auto-shards oversized
groups across content nodes.

### Lifecycle

- **Onboarding** — creating a namespace is cheap; creating an index is an operational event.
- **Offboarding and erasure** — dropping a namespace is O(1); `delete_by_query` on a shared
  index is expensive and leaves the data in segments until merge, which matters when the
  request is a legal deletion obligation.
- **Reindexing** — per-tenant rebuilds with per-tenant alias swaps are far less risky than one
  global reindex, and only possible if the tenant owns an index or namespace.
- **Tiering** — most tenants are idle most of the time. Weaviate makes this explicit with
  tenant states (`ACTIVE` on disk and served, `INACTIVE` on disk but unavailable, `OFFLOADED`
  to cloud storage). [[Compute-Storage Disaggregation]] is what makes many
  idle-but-must-exist tenants nearly free.

---

## Retrieval and Relevance

### Corpus statistics leak across tenants

[[BM25]]'s IDF is a corpus-level statistic. In a shared index it is computed over *all*
tenants' documents, so one tenant's bulk import can change another tenant's result ordering
with no action on their part. This is the same family of problem as per-shard IDF skew in
[[Sharding]], but harder to dismiss: tenant corpora are genuinely different vocabularies, and
"rare term" usually ought to mean rare *for this tenant*. Index-per-tenant makes statistics
tenant-local by construction.

### Vector search

A single ANN graph over all tenants plus a tenant filter is precisely the filtered-ANN problem
in [[Vector Filtering]]: a highly selective filter over a global [[HNSW]] graph wrecks recall
or forces a scan. Vendors solve it structurally rather than at query time —
Qdrant's documented recipe disables the global graph (`m: 0`) and builds per-tenant subgraphs
(`payload_m: 16`), at the cost of making unfiltered global queries slow. Pinecone's argument
is cost-shaped: a query that filters one tenant out of a 100 GB namespace consumes 100 read
units where the same tenant in its own 1 GB namespace consumes 1.

### Ranking, signals, and evaluation

- **Signal sparsity is structural.** Behavioural data is per-tenant and thin, and every new
  tenant is a cold start. [[Slack - Enterprise Message Search with LTR]] is the vault's worked
  example: documents are user-specific and queries rarely repeat, so aggregate click
  machinery has little to work with — Slack substituted the work graph as a per-user signal.
- **Model strategy** — one global [[Learning to Rank]] model, per-tenant models, or a global
  model with tenant features. Per-tenant models multiply training and serving cost and are
  usually only justified for whales.
- **Per-tenant relevance config** — boosts, pins, and [[Results Merchandising]] rules are a
  per-tenant artefact even when the index is shared, so they need their own storage and
  deployment path.
- **Evaluation** — judgment lists are per-tenant, and an aggregate NDCG is dominated by
  whichever tenant contributes the most traffic. A/B tests need tenant-level randomization,
  or a single large tenant swamps the sample; see [[Awesome Search/Topics/A-B Testing for Search|A-B Testing for Search]].

---

## Serving and Operations

- **Noisy neighbours.** One tenant's expensive query degrades everyone's, and the failure is
  usually not volume but shape — a high-cardinality aggregation, as in
  [[Zalando - Self-DoS via Facet Aggregation]]. Per-tenant quotas and query-cost limits are
  the mitigation; [[Extreme Search Systems]] treats this isolation as its own scale dimension.
- **Caching.** In a shared index, cache warming happens over the whole corpus rather than the
  tenant's slice, so per-tenant cache hit rates are worse than the size of each tenant's data
  suggests.
- **Observability.** Aggregate metrics hide tenancy problems: one tenant with a broken p99
  disappears into a healthy average. Per-tenant dimensions on latency, error, and zero-result
  rates are the minimum — see [[Awesome Search/Topics/Search Observability|Search Observability]].
- **Cost attribution.** Cost per tenant is the number that decides pooling versus dedication,
  and it is the [[Awesome Search/Topics/Economics of Search|Economics of Search]] question in
  its most direct form.

---

## Security and Access Control

The tenant filter is a security control, so it must be enforced somewhere the tenant cannot
edit. Three patterns, in decreasing order of trust required in the caller:

1. **Server-side enforcement** — a trusted backend appends the tenant clause; the client never
   names its tenant.
2. **Signed credentials carrying the filter** — Algolia's secured API keys and Meilisearch's
   tenant tokens embed filters into a key generated on the backend, so the restriction
   survives a user editing query parameters in the browser. Algolia's guidance is explicit
   that this is what removes the need for one index per user. Note the boundary: Meilisearch
   tenant tokens restrict the search endpoint only, not indexing or settings.
3. **Document-level permissions in the index** — the
   [[Bonsai - Designing Search for a Relational Database]] pattern: a `permissions` array on
   each document filtered by a `terms` query scoped to the caller, so one index safely serves
   admins and individual customers.

Within-tenant ACLs are a second, orthogonal problem — which documents *inside* the tenant a
given user may see — and they are what makes [[Enterprise Search]] and Slack-style search hard
independently of tenancy. Where regulation forbids co-mingling at all, the answer stops being
an index-design question and becomes a deployment-topology one.

---

## How Platforms Address It

| Platform | Primary mechanism | Notes |
|---|---|---|
| [[Elasticsearch]] / [[OpenSearch]] | Index per tenant, or shared index with `_routing` on tenant id and filtered aliases | Per-shard base memory makes index-per-tenant uneconomic at high tenant counts; alias lists inflate cluster state; document-level security is a paid-tier feature |
| [[Solr]] | Collection per tenant, or composite-id routing (`tenant!docid`) with `_route_` at query time | 16 bits of the hash from the shard key, 16 from the doc id; multi-level routing exists for oversized tenants |
| [[Vespa]] | Streaming mode — the group is part of the document id (`g=userid`), selected by `streaming.groupname` | No memory index (~45 bytes/doc), storage-dominated cost; exact search, no HNSW, no stemming; large groups auto-sharded; mixing streaming and indexed modes in one cluster is discouraged |
| [[Algolia]] | Shared index with secured API keys carrying enforced filters over a filterable attribute such as `visible_by` | Index-per-user is explicitly discouraged in Algolia's own guidance; `unretrievableAttributes` hides the access-control attribute from responses |
| Meilisearch | Tenant tokens embedding search rules over a shared index | Explicitly analogous to row-level security; restricts search only |
| [[Pinecone Vector DB]] | Namespace per tenant (their recommendation) | Physical isolation, million-scale namespaces, offboarding by namespace delete, read-unit cost proportional to data scanned |
| [[Qdrant Vector DB]] | One collection, payload partitioning with a `is_tenant: true` tenant index | Co-locates tenant vectors on disk; `m: 0` + `payload_m: 16` builds per-tenant graphs; separate collections only for a small number of tenants |
| [[Weaviate Vector DB]] | Tenant = its own shard inside a collection, with ACTIVE / INACTIVE / OFFLOADED states | Cold tenants offload to cloud storage — tiering as a first-class tenancy feature |
| [[Milvus Vector DB]] | Four tiers: database (~64), collection (~65,536), manual partition (~1,024 per collection), partition key (millions) | Isolation and RBAC weaken as you descend; partition-key routing places several tenants in one physical partition |
| [[turbopuffer Search DB]] | Namespace as the unit, on object storage | Idle namespaces cost roughly their storage — see [[Compute-Storage Disaggregation]] |

Two things stand out across the table. First, the vendors that started serverless jumped
straight to namespace-per-tenant, because their cost model makes an idle tenant nearly free —
the constraint that made index-per-tenant fail on shared-nothing clusters simply isn't there.
Second, the vector engines all had to solve tenancy *and* the filtered-ANN problem at once,
which is why their answers are index-structure decisions rather than query-time filters.

---

## The Usual Endpoint: Tiered Tenancy

Mature systems rarely pick one row of the ladder. They pool the long tail behind routing or
namespaces, promote whales to dedicated indexes or clusters, and isolate regulated tenants
entirely — with the tenant-to-placement mapping held in configuration so a tenant can be
moved without a code change. Consolidating previously single-tenant clusters onto a shared
platform forces exactly this design, and is a recurring source of surprise in
[[Migration between Search Engines]].

## Related Notes

- [[Sharding]] — routing, shard keys, and the fan-out costs tenancy inherits
- [[Unified Search Index]] · [[Denormalization for Search]] — one schema for heterogeneous records
- [[Federated vs Unified Search]] — when data cannot be co-located at all
- [[Extreme Search Systems]] — multi-tenancy as a scale dimension
- [[Compute-Storage Disaggregation]] — why idle tenants stopped being expensive
- [[Vector Filtering]] — the filtered-ANN problem tenancy runs into
- [[Search Scopes]] — the user-facing cousin of partitioning
- [[Search Governance]] · [[Enterprise Search]] · [[Awesome Search/Topics/Economics of Search|Economics of Search]]
- [[Bonsai - Designing Search for a Relational Database]] · [[Slack - Enterprise Message Search with LTR]] · [[Zalando - Self-DoS via Facet Aggregation]]

## Sources

- [Discovering the Need for an Indexing Strategy in Multi-Tenant Applications (Elastic)](https://www.elastic.co/blog/found-multi-tenancy)
- [Multi-Tenancy with Elasticsearch and OpenSearch (BigData Boutique)](https://bigdataboutique.com/blog/multi-tenancy-with-elasticsearch-and-opensearch-c1047b)
- [Solr Cloud Document Routing (Lucidworks)](https://lucidworks.com/blog/solr-cloud-document-routing)
- [Streaming Search (Vespa docs)](https://docs.vespa.ai/en/streaming-search.html)
- [Multitenancy (Qdrant docs)](https://qdrant.tech/documentation/guides/multiple-partitions/)
- [Multi-tenancy (Weaviate docs)](https://docs.weaviate.io/weaviate/manage-data/multi-tenancy)
- [Multi-tenancy strategies (Milvus docs)](https://milvus.io/docs/multi_tenancy.md)
- [Implement multitenancy (Pinecone docs)](https://docs.pinecone.io/guides/index-data/implement-multitenancy)
- [Multitenancy and tenant tokens (Meilisearch docs)](https://www.meilisearch.com/docs/learn/security/multitenancy_tenant_tokens)
- [Restrict access to data per user (Algolia docs)](https://www.algolia.com/doc/guides/security/api-keys/how-to/user-restricted-access-to-data/)
