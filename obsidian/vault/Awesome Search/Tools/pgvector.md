---
type: tool
title: "pgvector"
aliases: ["pgvector", "pg_vector"]
website: "https://github.com/pgvector/pgvector"
repo: "https://github.com/pgvector/pgvector"
tags:
  - tool
  - vector-search
  - postgresql
  - ann
  - open-source
---

# pgvector

Open-source [[PostgreSQL]] extension adding a `vector` column type and approximate-nearest-neighbor indexing for [[Dense Vector Retrieval|vector search]] inside Postgres.

- GitHub: https://github.com/pgvector/pgvector

## Capabilities

- **Index types**:
  - [[HNSW]] — recommended default; high recall, low latency. Built incrementally on insert, so no upfront clustering step (works on an empty table).
  - [[IVF|IVFFlat]] — smaller index, faster build, lower recall. Needs a one-time **k-means clustering pass at `CREATE INDEX`** to compute its `lists` cell centroids from the rows already present — **load data first**, and `REINDEX` if the distribution shifts. ("Training" here = unsupervised clustering, not model training.)
- **Distance ops**: cosine (`<=>`), L2 (`<->`), inner product (`<#>`).
- **Types**: `vector`, `halfvec` (half-precision), `sparsevec` (sparse), binary vector indexing (see [[Binary Quantization]]).

```sql
ALTER TABLE products ADD COLUMN embedding vector(1536);
CREATE INDEX ON products USING hnsw (embedding vector_cosine_ops);
SELECT * FROM products ORDER BY embedding <=> :q LIMIT 20;
```

## Role

The semantic-retrieval leg of a PostgreSQL [[Hybrid Search]] stack; combined with native FTS or [[ParadeDB]] BM25 and fused via [[Reciprocal Rank Fusion|RRF]].

## Related

- [[Search using PostgreSQL]] · [[PostgreSQL]] · [[ParadeDB]]
- [[HNSW]] · [[IVF]] · [[Dense Vector Retrieval]] · [[Binary Quantization]]
- Compare: [[Qdrant Vector DB]] · [[Weaviate Vector DB]] · [[Milvus Vector DB]] · [[Pinecone Vector DB]]
