---
type: concept
title: "Unified Search Index"
aliases: ["single search index", "one index for all tables", "unified index", "search schema design"]
tags: [concept, search-architecture, schema-design, indexing]
created: 2026-06-27
---

# Unified Search Index

The design principle of indexing records of **many types into a single search index whose schema is shaped by user information needs, not by the source data model**. The canonical statement: *one field per use case of how people want to find things* — not one field per database column or one index per table.

## The Idea

When making a relational database searchable, the instinct is to mirror the database: an index per table, foreign keys preserved, relationships as nested objects. This produces fragmented, slow search. The unified-index approach instead:

1. **One index** holds every searchable record type.
2. A **`type` field** distinguishes records and drives [[Faceted Search|faceting]] and filtering.
3. The schema is a small, fixed set of **purpose fields** (names, aka, notes, address, amount, dates, permissions, url…) that every record type maps onto.
4. Relationships are [[Denormalization for Search|denormalized]] into flat multivalued fields at index time rather than joined at query time.

## Why It Works

- A single query searches across all entity types at once — a user searching a brand finds its products, the brand page, and related entities together.
- Adding a new source table is a few lines of field mapping, not a new index and query path.
- Document-level concerns (access control via a `permissions` field, soft-delete via a `deleted` date) are handled uniformly for every type.
- Avoids nested fields, which are slower and more complex than flat multivalued fields.

## Trade-offs

- Requires up-front analysis of *information needs* — what users actually search for — rather than mechanically reflecting the schema.
- Denormalization shifts cost to index time and write-side maintenance (resolved values must be re-indexed when the source changes).

## Related Concepts
- [[Denormalization for Search]] — the mechanism that makes a unified schema possible
- [[Full-Text Search]]
- [[Faceted Search]] — the `type` field is the natural primary facet
- [[Search Architecture]]

## Articles
- [[How to Really Design Search for a Database]] — [[Bonsai]] / [[Max Irwin]]; the 14-field universal schema

## Case Studies
- [[Bonsai - Designing Search for a Relational Database]]
- [[Netflix - Content Search Architecture]] — federated entities indexed into a searchable whole
