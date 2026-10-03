---
type: tool
title: "qdrant-es-gateway"
aliases: ["Qdrant Elasticsearch gateway", "qdrant es gateway"]
website: https://dstockton.github.io/qdrant-es-gateway/
repo: https://github.com/dstockton/qdrant-es-gateway
license: Apache-2.0
tags:
  - tool
  - search-engine
  - compatibility-layer
  - migration
  - lexical-search
  - open-source
related_concepts:
  - "[[BM25]]"
  - "[[Sparse Vector Retrieval]]"
  - "[[Faceted Search]]"
  - "[[Search Architecture]]"
related_topics:
  - "[[Migration between Search Engines]]"
created: 2026-10-03
---

# qdrant-es-gateway

An open-source Rust gateway that accepts a subset of the [[Elasticsearch]] REST API and serves it from a [[Qdrant Vector DB|Qdrant]] backend. An application written against Elasticsearch can point its existing client at the gateway; the gateway translates each request into Qdrant calls and shapes the responses to look like Elasticsearch's. It targets ordinary application search — catalogues, documentation, jobs, tickets, content — and explicitly not Kibana, logging, or full Elasticsearch replacement.

- Repository: https://github.com/dstockton/qdrant-es-gateway (Apache-2.0)
- Docs: https://dstockton.github.io/qdrant-es-gateway/ — [compatibility](https://dstockton.github.io/qdrant-es-gateway/compatibility/), [architecture](https://dstockton.github.io/qdrant-es-gateway/architecture/)
- Built by David Stockton; first release v0.1.1 in September 2026, v0.2.0 in October 2026

---

## What it translates

The root endpoint returns `X-Elastic-Product: Elasticsearch` and an 8.x-shaped version response, so the official Elasticsearch clients connect without modification.

| Elasticsearch feature | Gateway behaviour |
|---|---|
| Index lifecycle, mappings, CRUD, `_bulk`, `_msearch` | Supported; mapping metadata kept in SQLite |
| `match`, `match_phrase`, `multi_match` with boosts | Scored by Qdrant's server-side [[BM25]] sparse model, not Lucene — `match_phrase` is not a positional phrase match |
| `term`, `terms`, `range`, `exists`, `ids`, `bool` | Translated to Qdrant payload filters |
| `search_after`, from/size, `_source` filtering | Supported; deep pagination capped |
| `terms` aggregations | Qdrant's facet API over indexed keyword fields only |
| `regexp`, `wildcard`, `prefix` | Evaluated in the gateway by scanning candidate documents; rejected inside `should` / `must_not` |
| Aliases | Single-target only |
| Scripts, scroll, arbitrary aggregations, nested documents, analyzer settings | Rejected with a structured HTTP 400 naming the feature |

The surface is **lexical**. The documented compatibility matrix lists no kNN or dense-vector query: Qdrant is used here as a BM25 and filtering engine, not as a vector store.

The design choice worth noting is failing loudly. A request using an unsupported feature is rejected instead of being run with the offending clause silently dropped — the failure mode that makes automated query translation dangerous in a migration.

## How it maps onto Qdrant

- **One collection per index.** Each Elasticsearch index becomes a Qdrant collection. Each text field gets its own named sparse representation, populated by Qdrant's `qdrant/bm25` model; `multi_match` queries each field and merges the hits with the declared boosts in the gateway.
- **Deterministic IDs.** Elasticsearch `_id`s are hashed with the index name into UUID-shaped Qdrant point IDs, and the original ID is kept in the payload.
- **Optional document projection.** With `DOCUMENT_PROJECTION=true`, the full `_source` lives in a second, unindexed collection, and the searchable collection carries only the fields needed for filtering, sorting and facets. An async mode acknowledges the source write before the search projection catches up. The docs describe this as deliberate eventual consistency, and recommend an external worker to reconcile the two collections in a high-availability deployment.
- **Schema limits.** On the pinned Qdrant 1.15, a new text field cannot be added to an existing index, because its sparse vector cannot be added to an existing collection; it needs a new index.
- **Not yet horizontally stateless.** The SQLite metadata (mappings, field-to-vector names, aliases) must be persisted or shared between gateway replicas. The docs name moving it into Qdrant as the follow-up for replica-safe statelessness.

## The project's own measurements

All figures are the author's, on generated product data, without independent replication.

- **500,000 products.** The gateway's total storage was about **43×** the native Elasticsearch data directory (694.5 MiB against 16.1 MiB). Search p95 at 50 clients was 192 ms against 987 ms, and mixed-workload throughput 523 against 96 requests per second. Single-document updates were slower on the gateway.
- **Ranking.** The top-ranked IDs were not identical to Elasticsearch's. The docs advise judging results by relevant document IDs and product metrics, not by `_score` equality.
- **Projection trade-off.** At 50,000 documents with 20 concurrent search clients, the one-collection layout used about 18% less Qdrant storage than the two-collection layout (60.6 MiB against 73.8 MiB). The two-collection layout returned about 34% lower search p95 and 17% higher mixed throughput.

The docs' own conclusion is workload-dependent: native Elasticsearch remains the stronger choice when storage cost dominates or ranked-result equivalence is a hard requirement.

## Related Tools

- [[Qdrant Vector DB]] — the backend
- [[Elasticsearch]] — the API it emulates

## Related Concepts

- [[BM25]] — the scoring model, via Qdrant's sparse implementation
- [[Sparse Vector Retrieval]] — how text fields are represented
- [[Faceted Search]] — terms aggregations map to Qdrant facets
- [[Search Architecture]]

## Related Topics

- [[Migration between Search Engines]] — an API-compatibility option for the client-code side of a migration
