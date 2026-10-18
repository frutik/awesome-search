---
type: tool
title: "sqlite-sparse"
aliases: ["sqlite-sparse", "sqlite sparse", "sparse0"]
website: "https://www.arbazsiddiqui.me/sparse/"
repo: "https://github.com/arbazsiddiqui/sqlite-sparse"
tags:
  - tool
  - sqlite
  - learned-sparse-retrieval
  - inverted-index
  - open-source
related_concepts:
  - "[[Learned Sparse Retrieval]]"
  - "[[SPLADE]]"
  - "[[Sparse Vector Retrieval]]"
  - "[[Sparse Embeddings]]"
created: 2026-10-18
---

# sqlite-sparse

SQLite extension (`sparse0` virtual table) that runs [[Learned Sparse Retrieval]] inside a single SQLite file. The encoder runs only at INSERT; a query needs no model, only the tokenizer and a static per-token weight table stored in the file, and is scored by an exact inverted-index scatter-add — no ANN index, no candidate stage. Written in C by Arbaz Siddiqui; MIT. First published to PyPI on 2026-09-05; v1.1.0 released 2026-09-07.

- GitHub: https://github.com/arbazsiddiqui/sqlite-sparse
- PyPI / npm: `pip install sqlite-sparse`, `npm install sqlite-sparse` (prebuilt binaries for Linux x86-64 and macOS arm64)
- In-browser demo (query-only WebAssembly build): https://www.arbazsiddiqui.me/sparse/

---

## How it works

It uses the **inference-free** variant of [[SPLADE]]-style encoding popularised by [[OpenSearch]]'s neural sparse models: documents go through the transformer, queries do not — each query token takes one learned weight from a lookup table, and retrieval is an exact dot product.

- **The MLM head is the trick.** A SPLADE encoder is a BERT model whose masked-language-model head scores every vocabulary word per token; max-pooling across tokens with `log(1 + ReLU)` yields the sparse vector, so a passage about heart attacks earns weight on `cardiac` without containing it. llama.cpp's converter drops that head and runs BERT models for embeddings only. sqlite-sparse keeps it: the converter writes the head's weights plus the query weight table into a `.sprs` sidecar next to the GGUF encoder, llama.cpp runs the encoder at insert, and the extension runs the head (dense layer, GELU, LayerNorm, vocabulary scores) itself in C on ggml.
- **INSERT.** Each resulting term is appended to that word's posting list — stored as rows in the database, with the weight quantised to one byte.
- **MATCH.** The query is tokenized, each token's weight read from the table in the file, and each posting list walked, adding query weight × stored weight into every listed document's total. Neither the GGUF nor the sidecar is read at query time, so a `.db` built on one machine can be searched on another with no model downloaded.
- **Rows, not a black box.** Results come back as SQL rows with a `score`, so a `k` candidate count can be combined with ordinary `JOIN` and `WHERE` filters.

The intended workload is small, read-heavy systems: build a large corpus once (on a GPU machine, via `sqlite-sparse build`) and ship the file to where reads happen. Positioned by its author as doing for learned sparse in SQLite what sqlite-vec did for embeddings, where learned sparse had previously lived inside engines such as [[OpenSearch]], [[Elasticsearch]] and [[Vespa]].

## Models

Default `mini` is OpenSearch's `opensearch-neural-sparse-encoding-doc-v2-mini` (23M parameters); `base` is `doc-v3-distill` (67M); `multilingual` is `multilingual-v1` (168M). Weights are the unmodified Apache-2.0 OpenSearch checkpoints, converted to GGUF. Any inference-free OpenSearch-style sparse encoder can be converted, provided it is a BERT-family encoder with an MLM head and a static query weight table, on an architecture llama.cpp supports.

## Performance claims

The project's own benchmarks on a GCE `c3-standard-8`, against SQLite FTS5 [[BM25]] (OR of query tokens) and brute-force dense search with sqlite-vec int8; not independently replicated.

| [[MS MARCO]], 1M docs | FTS5 BM25 | dense brute-force | sqlite-sparse |
|---|---|---|---|
| query p50, warm | 582 ms | 735 ms | 3.1 ms |
| peak RAM, query path | 37 MB | 527 MB | 28 MB |
| index bytes / document | 540 | 807 | 1,092 |
| indexing docs/s (CPU) | ~43,000 | 167 | 20.5 |

The costs are explicit in the same table: indexing on CPU is roughly 2,000× slower than FTS5 and the index is about twice FTS5's size per document. On four [[BEIR]] subsets (SciFact, NFCorpus, SCIDOCS, FiQA) the project reports nDCG@10 matching the OpenSearch model card to within about 0.001 — i.e. the quality is the model's, and the extension's claim is only that Q8 encoding and one-byte storage do not lose it.

## Where it fits

Embedded, serverless [[Sparse Vector Retrieval]] for applications already on SQLite — a parallel to [[psql_bm25s]] and [[ParadeDB]] bringing [[BM25]] into [[PostgreSQL]], but with learned term weights and vocabulary expansion instead of term statistics, and to [[pgvector]] on the dense side. See [[Search Platforms]] for database-embedded search generally.

## Related Concepts

- [[Learned Sparse Retrieval]] · [[SPLADE]] · [[Sparse Embeddings]] · [[Sparse Vector Retrieval]]
- [[BM25]] · [[Full-Text Search]] · [[Dense Vector Retrieval]]
- [[MS MARCO]] · [[BEIR]]
- [[psql_bm25s]] · [[pgvector]] · [[Search using PostgreSQL]] · [[OpenSearch]]
