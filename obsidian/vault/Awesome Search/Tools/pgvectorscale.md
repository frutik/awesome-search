---
type: tool
title: "pgvectorscale"
aliases: ["pgvectorscale"]
repo: "https://github.com/timescale/pgvectorscale"
tags:
  - tool
  - postgresql
  - vector-search
  - ann
  - open-source
created: 2026-06-12
---

# pgvectorscale

[[PostgreSQL]] extension by [[Tiger Data]] (formerly Timescale) that complements [[pgvector]] with a faster DiskANN-style index (StreamingDiskANN) designed for high-throughput vector search on larger corpora. Uses the same SQL interface as pgvector (`<=>` operator, `ORDER BY … LIMIT`).

- GitHub: https://github.com/timescale/pgvectorscale

## Related

- [[pgvector]] — the base vector extension it augments
- [[Search using PostgreSQL]] — architectural context
- [[HNSW]] · [[IVF]] · [[Dense Vector Retrieval]]
- [[Tiger Data]] — maintainer
