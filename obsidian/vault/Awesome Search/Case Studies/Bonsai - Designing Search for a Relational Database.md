---
type: case-study
company: "[[Bonsai]]"
domain: managed search / developer education
articles:
  - "[[How to Really Design Search for a Database]]"
topics:
  - "[[Search Architecture]]"
concepts:
  - "[[Unified Search Index]]"
  - "[[Denormalization for Search]]"
  - "[[Full-Text Search]]"
  - "[[Faceted Search]]"
people:
  - "[[Max Irwin]]"
created: 2026-06-27
---

# Bonsai — Designing Search for a Relational Database

How [[Bonsai]] (via [[Max Irwin]]) makes every record type in a relational database **universally findable** by collapsing many tables into a single, denormalized [[Elasticsearch]]/[[OpenSearch]] index designed around user information needs rather than database structure. Demonstrated end-to-end on the open-source **Chinook** music-store schema.

## The Problem

A relational database scatters findable data across many tables joined by foreign keys: catalog (artists, albums, tracks, genres, playlists), people (customers, employees), and transactions (invoices). The naive instincts — one search index per table, preserve foreign keys, model relationships as nested fields — produce search that is slow, fragmented, and hard to query. A user searching "AC/DC" wants matching tracks, albums, and artists together; the database shape actively fights that.

## The Core Insight

**Design the index around how people want to find things, not around the tables.** One unified index holds records of every type; a `type` keyword field distinguishes them and powers faceting. The schema has *one field per use case*, not one field per column. See [[Unified Search Index]].

## The Universal Schema (14 fields)

`id`, `type`, `permissions`, `url`, `names`, `emails`, `notes`, `aka`, `address`, `amount`, `created`, `updated`, `deleted`, `details`. Every table in the database maps onto these same fields. Adding a new table is ~10 lines of mapping.

## How Each Table Maps

| Source table group | Mapping decisions |
|---|---|
| **Catalog** (Artist, Album, Track, Genre, Playlist) | Track name → `names`; album/genre/composer → `aka` array; price → `amount`; `permissions: ["all"]` (public). Junction tables (PlaylistTrack) and enum tables skipped. |
| **People** (Customer, Employee) | First+Last concatenated → `names`; company → `aka`; address fields → `address` array. Customer `permissions`: own id + `"admin"`; Employee: `["admin"]` only. |
| **Transactions** (Invoice) | Resolved customer name → `names`; billing address → `address`; total → `amount`; `permissions`: customer id + admin. |

### Example indexed document (a track)
```json
{
  "id": "track-1",
  "type": "track",
  "permissions": ["all"],
  "names": ["For Those About To Rock (We Salute You)"],
  "aka": ["AC/DC", "Rock", "Angus Young, Malcolm Young, Brian Johnson"],
  "amount": 0.99,
  "details": {"media_type": "MPEG audio file", "duration_ms": 343719}
}
```

## Key Techniques

- **Denormalization over joins** — foreign keys resolved into flat multivalued fields (`aka`) at index time. Nested fields avoided as "slow and over-complicated." See [[Denormalization for Search]].
- **Custom analyzers per field type** — entities (light stemming, preserve proper nouns), text (full English), emails (UAX URL-email tokenizer), urls (path-hierarchy tokenizer).
- **Document-level access control in the index** — a `permissions` array filtered by a `terms` query scoped to the requesting user's role, so the same index safely serves admins and individual customers.
- **`details` stored but not indexed** (`enabled: false`) — display payload without searchability cost.
- **Query** — `multi_match cross_fields` with `names^3`, `aka^2`; plus a `match_phrase_prefix` (0.1 boost) for partial-name recall ("stair" → "Stairway to Heaven").
- **Lexical-first** — vectors explicitly discouraged unless data is paragraph-rich and lexical recall genuinely fails.

## What to Steal

| Pattern | Application |
|---|---|
| One unified index, `type` field for faceting | Any multi-entity catalog (products + people + orders) |
| Schema = one field per information need, not per column | Greenfield search-over-DB design |
| Resolve FKs into flat multivalued fields at index time | Any relational source; avoids nested-field cost |
| `permissions` array + `terms` filter | Multi-tenant / role-scoped search on a shared index |
| `match_phrase_prefix` low-boost clause | Cheap partial-name recall without an autocomplete index |
| Skip junction/enum tables | Keep the index focused on findable entities |

## Related Case Studies
- [[Netflix - Content Search Architecture]] — materialize relationships at index time; denormalize graph traversals into search fields
- [[Uber Eats - Scaling Search for Food Delivery]] — denormalize store metadata into item documents as a performance lever

## Related Concepts
- [[Unified Search Index]]
- [[Denormalization for Search]]
- [[Full-Text Search]]
- [[Faceted Search]]

## People
- [[Max Irwin]]
