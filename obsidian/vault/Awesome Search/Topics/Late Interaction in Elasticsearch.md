---
type: topic
title: "Late Interaction in Elasticsearch"
aliases: ["ColPali in Elasticsearch", "rank_vectors", "Late Interaction Vectors in Elasticsearch"]
tags: [topic, late-interaction, colpali, elasticsearch, vector-search, neural-ir, reranking]
related_concepts: [Late Interaction, ColPali, ColBERT, Token Pooling, BBQ, HNSW, Dense Vector Retrieval, Bi-Encoder, Cross-Encoder, Reranking]
related_topics: [Frontier of Search 2025, Search Platforms, Elasticsearch vs OpenSearch, Reasoning Reranking]
articles:
  - "[[ColPali & Elasticsearch - How to Search Complex Documents]]"
  - "[[Late Interaction Models - How to Scale and Optimize in Elasticsearch]]"
companies: [Elastic]
people: [Peter Straßer, Benjamin Trent]
created: 2026-06-19
---

# Late Interaction in Elasticsearch

How [[Late Interaction]] models — [[ColBERT]] for text, [[ColPali]] for document images — are indexed, scored, and scaled inside [[Elasticsearch]]. From version **8.18** (tech preview), Elasticsearch supports multi-vector late-interaction retrieval natively via the `rank_vectors` field type and `maxSim` scoring functions. This topic tracks the mechanics and the production-scaling techniques, drawn from [[Elastic]]'s two-part ColPali series by [[Peter Straßer]] (and [[Benjamin Trent]]).

The central tension: late interaction stores **~1000 vectors per document page** and scores by comparing every query vector against every document vector — far more expensive than single-vector [[Bi-Encoder|bi-encoders]]. Making it production-viable is an exercise in compression and staged retrieval.

---

## The Building Blocks

### `rank_vectors` field + `maxSimDotProduct`
The new `rank_vectors` field stores the multi-vector representation. Scoring uses `maxSimDotProduct(query_vector, 'field')` inside a `script_score` query — for each query vector, take the max dot product over all document vectors, then sum. (See [[ColPali & Elasticsearch - How to Search Complex Documents]].)

### Why scale is hard
1. **Disk** — storing ~1000 float32 vectors per page is expensive at scale.
2. **Compute** — `maxSimDotProduct` compares all doc vectors against all query vectors per document.

---

## Scaling & Optimization Techniques

From [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]] (Part 2):

| Technique | Mechanism | Trade-off |
|---|---|---|
| **Bit vectors** | Sign-quantize each dimension (`>0 → 1`); `element_type: "bit"`; score with `maxSimInvHamming` (SIMD bitwise) | ~32× storage cut; slight accuracy loss. *Asymmetric* variant keeps the query full-precision for better quality at same storage |
| **Average vectors** | Mean of all page vectors → one normalized `dense_vector`, indexed in [[HNSW]] | Enables fast kNN over millions of docs; loses per-token granularity (best match can drop in rank) — pair with [[BBQ]] to cut RAM |
| **[[Token Pooling]]** | Cluster similar patch vectors, replace each cluster with its mean | Pool factor 3 → 66.7% fewer vectors, 97.8% performance retained; high pool factors (100–200) → 5–10 vectors/doc, nestable in HNSW |

### Two-Stage Retrieval (rescore pattern)
The production pattern combines them: **Stage 1** retrieves top-k candidates with fast HNSW kNN over average vectors; **Stage 2** reranks those candidates with full `maxSimDotProduct` over the late-interaction vectors. Implemented with the **rescore retriever** introduced in 8.18.

---

## Where Late Interaction Fits

Elastic's recommendation: use late-interaction models **for reranking the top-k, not first-stage retrieval** — which is why the field is called `rank_vectors`.

| | [[Bi-Encoder]] | Late Interaction ([[ColPali]]/[[ColBERT]]) | [[Cross-Encoder]] |
|---|---|---|---|
| Vectors compared | 1 vs 1 | ~1000 vs N | full transformer pass |
| Storage | Low | High | None (stateless) |
| Latency | Fast | Medium | Slow |
| Quality | Lower | High | Highest |

**Model choice**: for image-heavy docs (PDFs, slides) ColPali's tradeoffs win — evaluating visual content at query time would be too slow. For text-only, a cross-encoder (e.g. `elastic-rerank-v1`) may be simpler and just as good.

---

## Related Concepts
- [[Late Interaction]] — the architecture (MaxSim over per-token/per-patch vectors)
- [[ColPali]] — visual late interaction; the primary subject here
- [[ColBERT]] — text-domain late interaction
- [[Token Pooling]] — multi-vector compression
- [[BBQ]] — quantization to shrink the HNSW graph for average vectors
- [[HNSW]] — first-stage candidate retrieval
- [[Reranking]] — late interaction's primary role

## Related Topics
- [[Frontier of Search 2025]] — late interaction as a 2025 frontier theme
- [[Search Platforms]] · [[Elasticsearch vs OpenSearch]] — the engine landscape
- [[Reasoning Reranking]] — the broader rerank-as-its-own-problem shift

## Related Articles
- [[ColPali & Elasticsearch - How to Search Complex Documents]] — Part 1 (what ColPali is, `rank_vectors`, `maxSimDotProduct`)
- [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]] — Part 2 (bit/average vectors, token pooling, rescore)

## People
- [[Peter Straßer]] — [[Elastic]]; author of both ColPali articles
- [[Benjamin Trent]] — [[Elastic]]; co-author on scaling
