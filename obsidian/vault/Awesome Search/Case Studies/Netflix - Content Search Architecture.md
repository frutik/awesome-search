---
type: case-study
company: "[[Netflix]]"
articles:
  - "[[How Netflix Makes a Federated Graph Searchable]]"
  - "[[Netflix Elasticsearch Indexing Strategy in AMP]]"
topics:
  - "[[E-commerce Search]]"
concepts:
  - "[[Knowledge Graph Search]]"
  - "[[Search Architecture]]"
  - "[[Dense Vector Retrieval]]"
---

# Netflix — Content Search Architecture

Netflix operates two distinct search contexts covered across their engineering blog: **AMP** (Asset Management Platform — internal tool for content operations teams) and **consumer content search** over a federated entity graph. Both surface architectural patterns applicable far beyond entertainment.

## Part 1: Making a Federated Graph Searchable

Netflix's content catalog is a federated knowledge graph: different teams own different entity types (titles, talent, studios, rights deals). Each partition is authoritative for its domain.

### The Problem

Standard search indexing assumes a single authoritative document store. Netflix's graph is distributed — querying "all movies directed by this person" requires joining data from the titles partition and the talent partition. Traditional inverted indexes don't model these relationships.

### Architecture

**Graph → Search Index**:
- Entities (movies, shows, people, studios) become indexed documents
- Relationships (actor → movie, director → studio) are materialized as pre-computed document features at index time — not resolved at query time
- Graph traversals computed offline and denormalized into search fields

**Federated Query Routing**:
- Queries decomposed into sub-queries, routed to appropriate graph partition owners
- Results merged at the search orchestration layer

**Vector Embeddings for Entities**:
- Entity embeddings derived from graph neighborhood (which other entities are nearby in the graph)
- Enable similarity search across entity types: "movies similar to X" without explicit feature engineering

### Key Principle

**Materialize graph traversals at index time, not query time.** Denormalized, enriched documents trade index size for query latency.

## Part 2: Elasticsearch Indexing in AMP

AMP is Netflix's internal asset management platform for content operations (post-production, rights, metadata). Scale: large corpus of frequently-updated media assets.

### Alias-Based Zero-Downtime Reindexing

Netflix uses Elasticsearch aliases to decouple logical from physical index:
1. Build new index to `index_v2`
2. Validate index quality against test queries
3. Atomically switch alias from `index_v1` to `index_v2`
4. Delete old index

This blue-green pattern is now industry standard for any Elasticsearch system requiring full rebuilds.

### Other Indexing Patterns
- **Mapping design**: keyword vs. text field type choices; nested vs. flattened structures — chosen based on query patterns, not data shape
- **Refresh tuning**: longer refresh intervals during bulk indexing (throughput); shorter intervals for user-facing search (freshness)
- **Update frequency vs. freshness trade-off**: batch high-frequency metadata updates vs. near-real-time indexing requires explicit SLO decisions

## What to Steal

| Pattern | Application |
|---|---|
| Denormalize relationships at index time | Any graph-structured catalog (products + brands + categories) |
| Entity embeddings from graph neighborhood | Recommendation-adjacent search features |
| Alias-based blue-green indexing | Every Elasticsearch deployment doing full rebuilds |
| Mapping design review (keyword vs. text) | Early architecture decision with large late-correction cost |
| Refresh interval tuning per workload | Bulk indexing vs. operational search have opposite optimal settings |

## Related Case Studies

- [[Canva - Search Pipeline Modernization]] — similar federated architecture challenges
- [[Zalando - Self-DoS via Facet Aggregation]] — operational risk in production search systems
- [[Uber Eats - Scaling Search for Food Delivery]] — index layout as performance lever
