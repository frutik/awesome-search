---
title: "Qdrant"
aliases: ["Qdrant.tech", "Qdrant vector database"]
tags:
  - company
  - vector-database
  - open-source
created: 2026-05-16
---

# Qdrant

Open-source vector database and similarity search engine. Specializes in high-performance ANN search for production ML workloads. Competes with Pinecone, Weaviate, Milvus.

## Notable Contributions

**TurboQuant (Qdrant 1.18)** — rotation-based vector quantization; extends Google Research's TurboQuant paper with anisotropy compensation (per-coordinate calibration), length renormalization from RaBitQ, full L2/dot/cosine support, and SIMD kernels. Results: 8× compression at SQ-level recall; +10–20 pp recall over BQ at 16×/32× storage.

**Scalar Quantization** — int8 per coordinate, 4× compression, near-lossless.

**Binary Quantization** — 1-bit/2-bit storage, 16×–32× compression.

**Sparse neural retrieval** — Qdrant supports [[BM25]] and [[SPLADE]] as sparse vectors over inverted indexes, making lexical and learned-sparse retrieval first-class in a vector engine. Original research includes [[miniCOIL]] (BM25 extended with a small semantic component, with BM25 fallback for out-of-vocabulary terms) and a five-part study of [[SPLADE]] domain fine-tuning, [[Fine-Tuning Sparse Embeddings for E-Commerce Search]], packaged as [[qdrant-sparse-finetune]].

## People
- [[Ivan Pleshkov]]
- [[Jonas Schulz]]
- [[Evgeniya Sukhodolskaya]] — developer advocate; [[miniCOIL]], sparse neural retrieval
- [[Thierry Damiba]] — developer relations; sparse fine-tuning research

## Articles
- [[TurboQuant in Qdrant]]

- [[Choosing a Vector Database for ANN Search at Reddit]] — qualitative score 292 vs Milvus 281; better raw latency but lost on Go ecosystem fit and automatic rebalancing
- [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] — [[Thierry Damiba]]

## Videos
- [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] — [[MICES]] 2026

## Tools
- [[Qdrant Vector DB]]
- [[qdrant-sparse-finetune]] — open-source SPLADE fine-tuning framework
