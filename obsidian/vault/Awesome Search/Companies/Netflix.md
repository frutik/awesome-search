---
type: company
category: end-user
industry: [streaming, entertainment]
products: [Netflix streaming, content catalog search, AMP (Asset Management Platform)]
search_domain: content discovery, internal asset management, federated entity search
use_cases: ["[[Netflix - Federated Graph Search]]", "[[Netflix - AMP Elasticsearch Indexing]]"]
tags: [company, end-user, streaming, knowledge-graph-search]
created: 2026-05-16
---

# Netflix

Global streaming platform with 260M+ subscribers. Search powers both external content discovery and internal asset management.

## Search Context

Netflix's content catalog is a **federated graph** — different teams own different entity types (titles, talent, studios, rights). Making this graph searchable is an unusually complex distributed systems problem.

## Key Engineering Work

### External: Federated Graph Search
- Content catalog represented as distributed graph (movies, shows, people, studios)
- Entity embeddings capture semantic relationships from graph neighborhood
- Federated query routing: sub-queries sent to appropriate partition owners; merged at orchestration layer
- Enables similarity search across entity types ("movies similar to X")

### Internal: AMP Elasticsearch Indexing
- AMP (Asset Management Platform) indexes media assets with high-frequency metadata updates
- **Alias-based blue-green indexing**: build `index_v2` → validate → atomically switch alias → delete `index_v1`
- Zero-downtime reindexing via alias decoupling
- Mapping design: field type choices (keyword vs. text, nested vs. flattened) affecting performance

## Articles

- [[How Netflix Makes a Federated Graph Searchable]] — distributed graph search architecture
- [[Netflix Elasticsearch Indexing Strategy in AMP]] — indexing patterns for high-update corpus

## Related Concepts

- [[Knowledge Graph Search]] · [[Search Architecture]] · [[Dense Vector Retrieval]] · [[Retrieval Pipeline]]
