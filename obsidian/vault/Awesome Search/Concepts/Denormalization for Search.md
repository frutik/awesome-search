---
type: concept
title: "Denormalization for Search"
aliases: ["denormalization", "denormalized index", "index-time denormalization", "flattening relationships"]
tags: [concept, indexing, schema-design, search-architecture]
created: 2026-06-27
---

# Denormalization for Search

**Resolving relationships into flat, self-contained documents at index time** instead of joining normalized data at query time. The defining pattern of search-engine schema design, and the opposite of relational-database normalization.

## Definition

A normalized relational schema stores each fact once and reconstructs relationships through foreign-key joins. Search engines ([[Elasticsearch]], [[OpenSearch]], Lucene) have no efficient join: a query scans one [[Inverted Index|inverted index]] of self-contained documents. So related data is **copied into the document** that needs to be findable — foreign keys resolved to their values, parent attributes pushed down into children, multivalued fields used instead of nested objects.

## Why

- **Speed** — no query-time joins; relevance and retrieval run over one flat document.
- **Findability** — a record is matchable by attributes of its related entities (a track findable by its artist, an item findable by its store).
- **Simplicity** — flat multivalued fields avoid nested/parent-child mappings, which are slower and more complex.
- **Compression** — repeated denormalized values across documents compress well (delta encoding).

## Cost

- Writes must re-index every document affected when a shared value changes.
- Index size grows (the same value stored many times) — traded deliberately for query latency.

## Common Forms

- Foreign key → resolved entity name in a multivalued field (e.g. `aka`).
- Parent metadata pushed into child documents (store fields into item docs).
- Offline graph traversals materialized into document fields at index time.

## Related Concepts
- [[Unified Search Index]] — denormalization is what lets many tables share one schema
- [[Full-Text Search]]
- [[Inverted Index]]
- [[Search Architecture]]

## Articles
- [[How to Really Design Search for a Database]] — resolve FKs into the `aka` field; avoid nested fields
- [[Optimizing Search at Uber Eats]] — denormalize store fields into item documents
- [[Netflix Elasticsearch Indexing Strategy in AMP]] — materialize relationships at index time

## Case Studies
- [[Bonsai - Designing Search for a Relational Database]]
- [[Uber Eats - Scaling Search for Food Delivery]]
- [[Netflix - Content Search Architecture]]
