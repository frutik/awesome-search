---
type: tool
title: "VectorChord"
aliases: ["VectorChord", "vchord"]
repo: "https://github.com/tensorchord/VectorChord"
tags:
  - tool
  - postgresql
  - vector-search
  - ann
  - open-source
created: 2026-06-12
---

# VectorChord

[[PostgreSQL]] extension for high-performance vector search by TensorChord. Uses RaBitQ quantization for compressed ANN indexes. Also ships **vchord_bm25**, a companion [[BM25]] extension (dual-licensed AGPLv3/ELv2), used as a benchmark baseline against [[ParadeDB]] and [[psql_bm25s]].

- GitHub: https://github.com/tensorchord/VectorChord

## Related

- [[pgvector]] — the standard alternative it benchmarks against
- [[Search using PostgreSQL]] — architectural context
- [[Dense Vector Retrieval]] · [[Binary Quantization]] · [[BM25]]
