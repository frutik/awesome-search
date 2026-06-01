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

## People
- [[Ivan Pleshkov]]
- [[Jonas Schulz]]

## Articles
- [[TurboQuant in Qdrant]]

- [[Choosing a Vector Database for ANN Search at Reddit]] — qualitative score 292 vs Milvus 281; better raw latency but lost on Go ecosystem fit and automatic rebalancing

## Tools
- [[Qdrant Vector DB]]
