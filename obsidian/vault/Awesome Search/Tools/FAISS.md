---
title: "FAISS"
type: tool
aliases:
  - Faiss
  - Facebook AI Similarity Search
website: "https://faiss.ai/"
repo: "https://github.com/facebookresearch/faiss"
tags:
  - tool
  - vector-search
  - ann
  - library
---

# FAISS

**FAISS** (Facebook AI Similarity Search) is [[Meta]]'s open-source C++/Python library
for efficient similarity search and clustering of dense vectors. It is the reference
implementation for [[Approximate Nearest Neighbor Search|ANN]] indexes and underpins or
inspires many production vector stores.

- **Repo**: https://github.com/facebookresearch/faiss
- **Docs**: https://faiss.ai/
- **Index-choice guide**: https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index

## Index Families

| Index | Class | Character |
|-------|-------|-----------|
| [[Brute-Force Vector Search\|Flat]] | `IndexFlatL2` / `IndexFlatIP` | Exact, exhaustive; 100% recall baseline |
| [[LSH]] | `IndexLSH` | Hash-bucket ANN; low-dimensionality only |
| [[HNSW]] | `IndexHNSWFlat` | Graph ANN; fast, high recall, memory-heavy |
| [[IVF]] | `IndexIVFFlat` | Cluster/Voronoi ANN; needs training |
| IVF-PQ | `IndexIVFPQ` | IVF + [[Vector Quantization|Product Quantization]] for billion-scale |

Supports L2 and inner-product [[Vector Similarity Metrics|metrics]], GPU acceleration,
and composite indexes.

## Role in the Ecosystem

- **Library, not a service** — no filtering, persistence, or dynamic updates on its own;
  it is a read-only index that must be periodically rebuilt.
- **The step past brute force.** For corpora a plain scan still handles, an in-process
  [[Brute-Force Vector Search|exact scan]] needs no library at all; FAISS is what you reach for
  when the scan stops fitting but a hosted vector database is still more machinery than the
  problem deserves — "just load them all in memory in FAISS or something and call it done."
- Built on or wrapped by [[Milvus Vector DB|Milvus]], [[OpenSearch]] (k-NN plugin),
  and used directly in many custom pipelines.
- Teams needing live updates or metadata filtering often migrate to
  [[Weaviate Vector DB|Weaviate]], [[Qdrant Vector DB|Qdrant]], Vespa, or
  [[Pinecone Vector DB|Pinecone]].

## Related Concepts

- [[Approximate Nearest Neighbor Search]] · [[Dense Vector Retrieval]]
- [[Brute-Force Vector Search]] — what `IndexFlat*` implements, and the baseline recall is measured against
- [[HNSW]] · [[IVF]] · [[LSH]] · [[Vector Quantization]] · [[Vector Similarity Metrics]]

## Datasets

- [[SIFT1M]] — the workload index-choice tutorials conventionally use

## Articles

- [[Choosing Indexes for Similarity Search (Faiss in Python)]] — James Briggs video on picking an index
- [[Nearest Neighbor Indexes for Similarity Search]] — Pinecone/James Briggs companion article
- [[Just brute force your embeddings]] — [[Doug Turnbull]]; FAISS as the in-memory step once a raw scan runs out
- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]]; pricing the exact-vs-approximate decision FAISS index choice embodies

## People

- [[James Briggs]]

## Company

- [[Meta]] — creator and maintainer
