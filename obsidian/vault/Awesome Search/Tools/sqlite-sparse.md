---
type: tool
title: "sqlite-sparse"
aliases: ["sqlite-sparse", "sqlite sparse"]
website: "https://www.arbazsiddiqui.me/sparse"
repo: "https://github.com/arbazsiddiqui/sqlite-sparse"
tags:
  - tool
  - sqlite
  - sparse-retrieval
  - open-source
related_concepts:
  - "[[Learned Sparse Retrieval]]"
  - "[[Sparse Vector Retrieval]]"
  - "[[BM25]]"
created: 2026-10-14
---

# sqlite-sparse

SQLite extension for semantic search with [[Learned Sparse Retrieval]]. Documents are encoded once at INSERT by an inference-free learned sparse encoder, and the term weights are stored as posting lists inside the database file. Queries need no model and no server: the query is tokenized, its term weights are looked up in the file, and documents are scored with an exact scatter-add. MIT licensed.

- GitHub: https://github.com/arbazsiddiqui/sqlite-sparse
- PyPI: `pip install sqlite-sparse` (prebuilt extension for Linux x86-64 and macOS arm64)
- In-browser WebAssembly demo: https://www.arbazsiddiqui.me/sparse

## Performance claims

These are the project's own numbers and have not been independently replicated. 3.1 ms per query across one million [[MS MARCO]] passages in 28 MB of memory on 8 vCPUs with no GPU, against 582 ms for SQLite FTS5 [[BM25]] on the same machine. With a Q8 encoder, results land within 0.001 nDCG@10 of the model card on [[BEIR]] subsets.

## Where it fits

Embedded sparse retrieval for applications that already use SQLite, in a similar position to [[psql_bm25s]] for PostgreSQL, with learned term weights in place of BM25 statistics.

## Related

- [[Learned Sparse Retrieval]] · [[Sparse Vector Retrieval]] · [[Full-Text Search]] · [[BM25]]
- [[MS MARCO]] · [[BEIR]] · [[psql_bm25s]]
