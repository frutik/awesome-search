---
type: tool
title: "pg_trgm"
aliases: ["pg_trgm", "trigram similarity"]
tags:
  - tool
  - postgresql
  - full-text-search
  - open-source
created: 2026-06-12
---

# pg_trgm

Built-in [[PostgreSQL]] extension providing trigram-based similarity matching via `similarity()`, `word_similarity()`, and GIN/GiST indexes. The standard Postgres mitigation for weak typo tolerance — enables fuzzy string search without a dedicated search engine.

Often paired with `unaccent` for accent-insensitive matching.

## Related

- [[PostgreSQL]] · [[Full-Text Search]]
- [[Search using PostgreSQL]] — used as a typo-tolerance workaround
