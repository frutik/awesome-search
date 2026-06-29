---
type: topic
title: "Late Interaction in OpenSearch"
aliases: ["ColBERT in OpenSearch", "lateInteractionScore", "Late Interaction Reranking in OpenSearch"]
tags: [topic, late-interaction, colbert, colpali, opensearch, vector-search, neural-ir, reranking]
related_concepts: [Late Interaction, ColBERT, ColPali, Token Pooling, HNSW, Dense Vector Retrieval, Bi-Encoder, Cross-Encoder, Reranking]
related_topics: [Late Interaction in Elasticsearch, Late Interaction in Qdrant, Interaction Paradigms, Search Platforms, Elasticsearch vs OpenSearch, Reasoning Reranking, Frontier of Search 2025]
related_tools: ["[[OpenSearch]]"]
companies: [AWS]
created: 2026-06-29
---

# Late Interaction in OpenSearch

How [[Late Interaction]] models — [[ColBERT]] for text, [[ColPali]] for document images — are indexed, scored, and scaled inside [[OpenSearch]]. Native support landed in **OpenSearch 3.3** (announced December 2025) via the `lateInteractionScore` scoring function, with a parallel Lucene-level path (`LateInteractionField`, Lucene 10.3+) feeding it. As in [[Elasticsearch]], late interaction is positioned as a **reranker** over a fast single-vector first stage — see the parallel topic [[Late Interaction in Elasticsearch]].

---

## The Building Blocks

### Multi-vector storage: `object` + `float`
Unlike Elastic's dedicated `rank_vectors` field, OpenSearch stores token-level multi-vectors using a composite of the `object` and `float` field types — "storage and retrieval of token-level vector embeddings used in late interaction models." Token vectors must share a consistent dimensionality, but documents may carry **varying numbers** of vectors.

### `lateInteractionScore` (painless)
Scoring is a painless script function with the same MaxSim semantics as Elastic's `maxSimDotProduct`: for each query vector, take the max similarity over all document vectors, then sum.

```
lateInteractionScore(params.query_vectors, 'my_vector', params._source, params.space_type)
```

### Lucene path (`LateInteractionField`, 10.3+)
Since Lucene 10.3, `LateInteractionField` accepts `float[][]` multi-vector embeddings, encodes them as binary, and indexes them as `BinaryDocValues`. `LateInteractionRescorer` implements the default `sum(max(vectorSimilarity))`. An open k-NN proposal ([issue #2934](https://github.com/opensearch-project/k-NN/issues/2934)) tracks deeper Lucene-based rescoring.

---

## The Pipeline

OpenSearch wires late interaction through two ML-inference processors:

| Processor | Role |
|---|---|
| **ml-inference ingest processor** | At ingest, generates both the single-vector (bi-encoder) embedding and the multi-vector late-interaction embedding |
| **ml-inference search request processor** | Rewrites the incoming query into a k-NN query plus a `lateInteractionScore` rescore |

### Two-Phase Retrieval
1. **Phase 1** — fast approximate k-NN over single-vector bi-encoder embeddings selects a small candidate set.
2. **Phase 2** — rerank those candidates with `lateInteractionScore` over the token-level multi-vectors.

---

## The Cost

Storage requirements increase **10–100×** versus single-vector retrieval — the same fundamental pressure late interaction creates everywhere. OpenSearch's mitigation story is younger than Elastic's: there is no built-in `rank_vectors`-style bit/average-vector toolkit yet; compression leans on the staged retrieve-then-rerank pattern and the underlying k-NN plugin (Faiss / nmslib / Lucene HNSW) for the cheap first stage.

---

## OpenSearch vs Elasticsearch for Late Interaction

| | [[OpenSearch]] (3.3+) | [[Elasticsearch]] (8.18+) |
|---|---|---|
| Multi-vector field | `object` + `float` composite | `rank_vectors` (dedicated) |
| MaxSim scoring | `lateInteractionScore` painless fn | `maxSimDotProduct` / `maxSimInvHamming` |
| Lucene primitive | `LateInteractionField` / `LateInteractionRescorer` | `rank_vectors` codec |
| First-stage approx | single-vector k-NN | average vectors (+ [[BBQ]]) |
| Built-in compression | (none yet) | bit vectors, average vectors, [[Token Pooling]] |
| Two-stage mechanism | ml-inference search processor | rescore retriever |
| Role | reranker | reranker |

Both converge on the same architecture; Elastic is further along on native multi-vector compression, OpenSearch has just reached parity on the core scoring primitive. See [[Elasticsearch vs OpenSearch]] for the broader engine comparison.

---

## Where Late Interaction Fits

| | [[Bi-Encoder]] | Late Interaction ([[ColBERT]]/[[ColPali]]) | [[Cross-Encoder]] |
|---|---|---|---|
| Vectors compared | 1 vs 1 | many vs many (MaxSim) | full transformer pass |
| Storage | Low | High (10–100×) | None (stateless) |
| Latency | Fast | Medium | Slow |
| Role in OpenSearch | first-stage k-NN | rerank top-k | rerank top-k |

---

## Related Concepts
- [[Late Interaction]] — the architecture (MaxSim over per-token/per-patch vectors)
- [[ColBERT]] — text-domain late interaction
- [[ColPali]] — visual late interaction (document page images)
- [[HNSW]] — k-NN plugin index for first-stage candidates
- [[Reranking]] — late interaction's role in OpenSearch
- [[Bi-Encoder]] · [[Cross-Encoder]] — the no/early-interaction endpoints

## Related Topics
- [[Late Interaction in Elasticsearch]] — the parallel Elastic implementation
- [[Late Interaction in Qdrant]] — the vector-DB take (MUVERA prefetch + ColBERT rerank)
- [[Late Interaction in Vespa]] — tensor-expression MaxSim and billion-scale ColPali
- [[Interaction Paradigms]] — the no/late/early interaction spectrum
- [[Elasticsearch vs OpenSearch]] · [[Search Platforms]] — the engine landscape
- [[Reasoning Reranking]] · [[Frontier of Search 2025]]

## Source
- [Boost search relevance with late interaction models — OpenSearch blog](https://opensearch.org/blog/boost-search-relevance-with-late-interaction-models/) (Dec 2025; Mingshi Liu, Vigya Sharma, Navneet Verma, Brian Flores)
- [k-NN issue #2934 — Lucene-based rescoring with late interaction](https://github.com/opensearch-project/k-NN/issues/2934)
