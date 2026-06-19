---
created: 2026-05-21
title: "Late Interaction Models: How to Scale & Optimize in Elasticsearch"
source: "https://www.elastic.co/search-labs/blog/late-interaction-model-colpali-scale"
authors:
  - "[[Peter Straßer]]"
  - "[[Benjamin Trent]]"
published: 2025-03-16
tags:
  - article
  - late-interaction
  - colpali
  - elasticsearch
  - elastic
  - vector-search
  - company-blog
---

# Late Interaction Models: How to Scale & Optimize in Elasticsearch

Part 2 of Elastic's ColPali series. Part 1 ([[ColPali & Elasticsearch - How to Search Complex Documents]]) covered building visual search with ColPali; this article focuses on making [[ColPali]]'s [[Late Interaction]] vectors production-ready at scale in [[Elasticsearch]].

Code: https://github.com/elastic/elasticsearch-labs/tree/main/supporting-blog-content/colpali

## The Scaling Problem

[[ColPali]] generates ~1000 vectors per document page, creating two bottlenecks:
1. **Disk space** — float32 vectors at ~1000/page × millions of docs
2. **Query computation** — `maxSimDotProduct()` must compare all doc vectors against all query vectors

## Optimization Techniques

### 1. Bit Vectors
Compress each document vector to 1-bit per dimension (sign quantization: `> 0 → 1`).

Elasticsearch mapping: `"element_type": "bit"` in `rank_vectors` field.

Scoring function: `maxSimInvHamming()` — inverted hamming distance (fewer bits different → higher score). Uses SIMD bitwise ops for speed.

**Asymmetric variant**: keep query vectors at full precision, quantize only document vectors. Loses bitwise speed but preserves query-side magnitude information → better accuracy at same storage cost.

### 2. Average Vectors
Compress all page vectors into a single normalized average vector. Index in a standard `dense_vector` field with HNSW for fast kNN retrieval. Combine with [[BBQ]] to reduce HNSW RAM usage.

Trade-off: accuracy drops (best match fell to rank 3 in the example). Recovered via two-stage retrieval (see below).

### 3. Token Pooling
Group similar patch vectors using clustering, replace each cluster with its mean. Pool factor 3 → 66.7% fewer vectors, 97.8% performance retained. At high pool factors (100–200) → 5–10 vectors/doc, viable for nested HNSW indexing.

See [[Token Pooling]] for details.

## Two-Stage Retrieval (Rescore Pattern)

Stage 1: fast HNSW kNN search over average vectors to get top-k candidates
Stage 2: rerank candidates with full `maxSimDotProduct()` over ColPali late interaction vectors

Uses Elasticsearch's **rescore retriever** (introduced in 8.18):
```python
"retriever": {
  "rescorer": {
    "retriever": {"knn": {...}},  # stage 1
    "rescore": {"query": {"rescore_query": {"script_score": {"maxSimDotProduct(...)"}}}  # stage 2
  }
}
```

## Late Interaction vs. Cross-Encoder vs. Bi-Encoder

| | Bi-Encoder | Late Interaction (ColPali/ColBERT) | Cross-Encoder |
|---|---|---|---|
| Vectors compared | 1 vs 1 | ~1000 vs N | Full transformer pass |
| Storage | Low | High (many vectors/doc) | None (stateless) |
| Latency | Fast | Medium | Slow |
| Quality | Lower | High | Highest |
| Indexing | Required | Required | Not needed |

**Recommendation**: Use late interaction models for reranking top-k, not first-stage retrieval (hence the field type is called `rank_vectors`).

**ColPali vs. ColBERT decision**: For image-heavy docs (PDFs, slides), ColPali's tradeoffs favor late interaction. For text-only, a cross-encoder may be simpler and better.

## Authors

- [[Peter Straßer]] — Elastic
- [[Benjamin Trent]] — Elastic

## Company / Tool

[[Elastic]] · [[Elasticsearch]]

## Related Concepts

[[Late Interaction]] · [[ColPali]] · [[Token Pooling]] · [[BBQ]] · [[HNSW]] · [[Bi-Encoder]] · [[Cross-Encoder]] · [[Reranking]] · [[Binary Quantization]]

## Related Topics

- [[Late Interaction in Elasticsearch]] — the topic this two-part series anchors
- [[Frontier of Search 2025]]
