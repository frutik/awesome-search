---
type: article
title: "How to Really Design Search for a Database"
source: "https://bonsai.io/blog/how-to-design-search-for-a-database/"
author: "[[Max Irwin]]"
company: "[[Bonsai]]"
tags: [article, company-blog, search-schema, denormalization, elasticsearch, opensearch, relational-database]
concepts: ["[[Unified Search Index]]", "[[Denormalization for Search]]", "[[Full-Text Search]]", "[[Faceted Search]]"]
topics: ["[[Search Architecture]]"]
created: 2026-06-27
---

# How to Really Design Search for a Database

A prescriptive [[Bonsai]] tutorial by [[Max Irwin]] on building search over a relational database. Its core argument: **don't mirror your database structure in your search index**. The common failure modes — one index per table, foreign keys preserved, nested fields — produce slow, over-complicated search. Instead, design a single unified index around *how people actually want to find things*, and make every type of record universally findable through one schema.

---

## Thesis

> "One field per use case of how people want to find things."

Database full-text features are not enough; use a dedicated engine ([[Elasticsearch]] / [[OpenSearch]]). But the engine choice is secondary to the **schema** — the index should be designed around user information needs, not around tables. See [[Unified Search Index]].

## The Universal 14-Field Schema

A single mapping applicable to any relational database. Records of every type (catalog, people, transactions) coexist in one index, distinguished by a `type` field:

| Field | Type | Purpose |
|---|---|---|
| `id` | keyword | Unique record identifier |
| `type` | keyword | Source table name — drives faceting/filtering |
| `permissions` | keyword | Access-control list (multivalued) |
| `url` | url | Link to record page |
| `names` | entity | Primary searchable names |
| `emails` | email | Email addresses |
| `notes` | text | Long-form free text |
| `aka` | entity | Alternate names / resolved related entities |
| `address` | entity | Location data |
| `amount` | numeric | Primary numeric value |
| `created` / `updated` / `deleted` | date | Lifecycle timestamps (soft delete) |
| `details` | object | Stored-but-not-indexed display data (`enabled: false`) |

## Denormalization Over Foreign Keys

Relationships are **resolved at index time into flat, multivalued fields** rather than preserved as foreign keys or nested objects. In the Chinook example, an album's `ArtistId` becomes the artist's name in the `aka` array; a track's genre/composer collapse into a single `aka` array. This makes related records discoverable through one query. The author notes nested fields "are slow and make things over-complicated." See [[Denormalization for Search]].

## Custom Analyzers

- `analyze_entities` — light stemming (English possessive only) to preserve proper nouns
- `analyze_text` — full English analysis (stop words + stemming)
- `analyze_emails` — UAX URL-email tokenizer
- `analyze_urls` — path-hierarchy tokenizer with protocol stripping

## Query Design

- **Base query**: `multi_match` `cross_fields` with boosts — `names^3`, `aka^2`, then `emails`/`notes`/`address`/`url`.
- **Permissions filtering**: a `terms` filter on the `permissions` array scoped to the user's role (admin passes `["all","admin"]`; a customer passes `["all","customer-1"]`). Document-level access control baked into the index.
- **Partial-name recall**: an added `match_phrase_prefix` clause (0.1 boost) lets "stair" match "Stairway to Heaven".

## When *Not* to Use Vectors

The article explicitly recommends **against** vector search for typical SaaS/database search unless data has rich free-text paragraphs *and* lexical techniques (prefix, fuzzy, n-grams) prove insufficient on a real recall problem. For entity-focused queries, vectors add noise.

## Worked Example — Chinook Database

The 11-table Chinook music store is mapped into the unified schema (catalog, people, transaction tables); junction tables and enum tables are skipped. Adding a new table costs ~10 lines of mapping. Reference implementation uses a Rails `Searchable` concern. See [[Bonsai - Designing Search for a Relational Database]].

## Related Concepts
- [[Unified Search Index]]
- [[Denormalization for Search]]
- [[Full-Text Search]]
- [[Faceted Search]]
- [[Search Architecture]]

## Related Articles
- [[Optimizing Search at Uber Eats]] — denormalizing store fields into item documents for speed
- [[Netflix Elasticsearch Indexing Strategy in AMP]] — materializing relationships at index time
- [[Agentic Search Models with OpenSearch and Elasticsearch]] — also from [[Bonsai]]

## People
- [[Max Irwin]]

## Source References
- Article: https://bonsai.io/blog/how-to-design-search-for-a-database/
- Example code: https://github.com/omc/bonsai-training-examples
- Chinook database: https://github.com/lerocha/chinook-database (MIT)
