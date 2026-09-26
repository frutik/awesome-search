---
type: topic
title: "Federated vs Unified Search"
aliases: ["federated search vs unified search", "unified vs federated search", "query-time federation", "index-time consolidation"]
tags: [topic, search-architecture, enterprise-search, e-commerce-search]
related_concepts: ["[[Federated Search]]", "[[Unified Search Index]]", "[[Denormalization for Search]]", "[[Reciprocal Rank Fusion]]", "[[Hybrid Search]]", "[[Search Architecture]]", "[[Knowledge Graph Search]]", "[[Search Scopes]]"]
related_topics: ["[[Enterprise Search]]", "[[E-commerce Search]]", "[[Multilingual Search]]", "[[Search Platforms]]"]
articles: []
created: 2026-07-06
---

# Federated vs Unified Search

Two opposing answers to the same problem — one search box over many heterogeneous data sources. **Federated search** leaves the data where it lives and fans the query out to independent sources at query time; **unified search** moves the integration work to index time, consolidating everything into one centrally-owned index. The whole comparison reduces to a single question: *where does the integration happen — query time or index time?*

---

## The Core Distinction

| | [[Federated Search|Federated]] | [[Unified Search Index|Unified]] |
|---|---|---|
| Integration happens | Query time (fan-out + merge) | Index time (ingest + normalize) |
| Data lives | At each autonomous source | Copied into one central index |
| Who owns ranking | Each source scores its own results; broker merges | One engine, one scoring framework |
| Freshness | Real-time — sources answer live | As fresh as the ingestion pipeline |
| Latency | Gated by the slowest source | One pre-built index; fast and predictable |
| Adding a source | Configure a connector | Build ingestion + schema mapping |

## The Terminology Trap

"Federated search" means different things in different communities, and the difference matters:

- **Classic IR sense** — distributed information retrieval / metasearch over *independent engines* that the broker does not control. This is the [[Federated Search]] concept note: collection selection, query routing, results merging.
- **E-commerce / search-UX sense** — [[Algolia]]'s own writing (and other e-commerce vendors) uses "federated search" for a **multi-index results UI**: products, articles, FAQ, and categories shown side by side, each list ranked independently. Architecturally this is usually *one* engine with several indexes — a unified system with a federated *presentation*. Retrieval-layer federation and presentation-layer federation are different decisions; see [[Search Scopes]] for the related pre-query narrowing pattern.
- **"Federated graph"** — in the [[Netflix]] sense, federation describes how the *data* is owned (many teams' services composing one shared entity graph). To make that graph searchable, Netflix feeds it into a search index — i.e., a unified index built *from* federated sources. Data federation and search federation are independent axes; see [[Knowledge Graph Search]].

## Trade-offs

**Where federated wins:**
- Data cannot be copied — residency, compliance, or contractual constraints keep each silo authoritative (healthcare, finance, multi-vendor platforms where vendors own their databases).
- Sources are third-party — travel metasearch has no option to index the airlines' inventory; Doofinder's guide cites [[Skyscanner]] querying multiple airlines in real time as the canonical example.
- Results must be real-time — inventory or pricing that would be stale in any copied index.
- Speed to coverage — configuring connectors is far cheaper up front than building crawlers, pipelines, and a shared schema.

**Where unified wins:**
- Relevance — one index means one consistent ranking framework, comparable scores, and the corpus statistics needed for tuning. Federated ranking is structurally handicapped: per-source scores are incomparable, so merging falls back to rank-based fusion like [[Reciprocal Rank Fusion]].
- Latency — querying a pre-built index beats waiting for N live sources, where the tail is set by the slowest one.
- Personalization and ML — [[Learning to Rank]], behavioral signals, and personalization need unified features and feedback over one candidate pool.
- Uniform document-level concerns — permissions, soft-deletes, and faceting handled once for every record type (the [[Unified Search Index]] purpose-field schema, enabled by [[Denormalization for Search]]).

**Unified's price:** up-front information-needs analysis and schema design, ingestion pipelines to build and maintain, re-indexing when sources change, and governance questions raised by copying sensitive content into a central store.

## In Practice: Convergence on Unified-with-Federated-Edges

Most large deployments end up hybrid — a unified index for everything the organization owns, with federation reserved for the edges it cannot ingest. Doofinder's guide cites Expedia as the pattern: unified hotel and car inventory, federated live airline queries. [[Enterprise Search]] products follow the same shape: crawl-and-index internal content, federate out to external or un-ingestable systems.

The vault's case studies show the same gravity toward consolidation once an organization owns the data:

- [[Canva - Search Pipeline Modernization]] — four organically-grown search systems ("big ball of mud") replaced by one componentized pipeline.
- [[Reddit - Vector Database Selection]] — fragmented per-team ANN stacks (Vertex AI, Solr ANN, FAISS sidecars) consolidated into a single Milvus deployment.
- [[Netflix - Content Search Architecture]] — a federated *data* graph made searchable by indexing it into a unified Elasticsearch index.
- [[Bonsai - Designing Search for a Relational Database]] — many relational tables deliberately flattened into one index shaped by information needs.

Genuinely federated setups persist where the constraint is external: sources you don't own, data you can't copy. And the *machinery* of federation — fan-out and rank-based fusion — survives everywhere, inside [[Hybrid Search]] (federation over representation spaces), [[Multilingual Search]] (per-language index fan-out), and sharded indexes (the cooperative, degenerate case).

## Related Concepts

- [[Federated Search]] — the query-time side, in depth
- [[Unified Search Index]] — the index-time side, in depth
- [[Denormalization for Search]] · [[Reciprocal Rank Fusion]] · [[Hybrid Search]] · [[Search Architecture]] · [[Knowledge Graph Search]] · [[Search Scopes]]

- [[Vertical Selection]] · [[Query Routing]] — choosing which federated sources to query; see [[Efficient Federated Search for RAG using Lightweight Routing]] for the RAG case

## Related Topics

- [[Enterprise Search]] · [[E-commerce Search]] · [[Multilingual Search]] · [[Search Platforms]]

## Sources

- [Federated vs Unified Search: Complete Guide for eCommerce (Doofinder)](https://www.doofinder.com/en/blog/federated-vs-unified-search)
- [What is Federated Search? (Algolia)](https://www.algolia.com/blog/ux/what-is-federated-search)
- [Enterprise search vs. federated search (TechTarget)](https://www.techtarget.com/searchcontentmanagement/feature/Federated-search-vs-enterprise-search-Whats-the-difference)
