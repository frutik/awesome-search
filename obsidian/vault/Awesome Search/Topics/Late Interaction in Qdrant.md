---
type: topic
title: "Late Interaction in Qdrant"
aliases: ["ColBERT in Qdrant", "Multivectors in Qdrant", "MultiVectorComparator.MAX_SIM"]
tags: [topic, late-interaction, colbert, colpali, qdrant, vector-search, neural-ir, reranking, multi-vector]
related_concepts: [Late Interaction, ColBERT, ColPali, MUVERA, Token Pooling, HNSW, Dense Vector Retrieval, Bi-Encoder, Cross-Encoder, Reranking, Hybrid Search]
related_topics: [Late Interaction in Elasticsearch, Late Interaction in OpenSearch, Interaction Paradigms, Search Platforms, Reasoning Reranking, Frontier of Search 2025]
related_tools: ["[[Qdrant Vector DB]]"]
companies: [Qdrant]
created: 2026-06-29
---

# Late Interaction in Qdrant

How [[Late Interaction]] models — [[ColBERT]] for text, [[ColPali]] for document images — are stored, scored, and reranked inside [[Qdrant Vector DB]]. Unlike [[Elasticsearch]] and [[OpenSearch]], which bolted multi-vector support onto search-engine cores in 2025, Qdrant has treated multivectors as a **first-class collection type** for longer: a native `multivector_config` with a MaxSim comparator, plus a single-call retrieve-then-rerank flow via the Query API. As everywhere, late interaction is used for **reranking a small candidate set**, not first-stage retrieval — see the parallel topics [[Late Interaction in Elasticsearch]] and [[Late Interaction in OpenSearch]].

---

## The Building Blocks

### Native multivector collection
A late-interaction field is declared directly on the collection. Each document is a matrix — one vector per token (ColBERT example shape `(48, 128)`):

```python
vectors_config = models.VectorParams(
    size=128,                          # ColBERT token dim
    distance=models.Distance.COSINE,
    multivector_config=models.MultiVectorConfig(
        comparator=models.MultiVectorComparator.MAX_SIM,
    ),
)
```

`MultiVectorComparator.MAX_SIM` is Qdrant's MaxSim: for each vector in matrix A, find the most similar vector in matrix B; their similarity is the contribution to the matrix-level score.

### Disable ANN for rerank-only vectors
Because the multivector is used for rescoring rather than first-stage ANN, the conventional setup disables HNSW on it — `hnsw_config` with `m=0` — so vectors are stored but not graph-indexed. The cheap first stage runs over a separate dense, sparse, or [[MUVERA]] representation.

---

## Single-Call Two-Stage Retrieval (`prefetch` + `query`)

Qdrant's Query API (`query_points()`) does retrieve-then-rerank in **one request**. `prefetch` pulls candidates with a cheap representation; the main `query` rescores them with the ColBERT multivector. The `using` parameter selects which named vector applies at each stage:

```python
client.query_points(
    collection_name=...,
    prefetch=models.Prefetch(
        query=query_muvera,     # cheap single-vector stage 1
        using="muvera",
        limit=20,               # candidates to rerank
    ),
    query=query_multivec,       # ColBERT multivector
    using="colbert",            # MaxSim rerank
    limit=3,                    # final results
)
```

Qdrant computes the MaxSim for the multivector stage automatically — no manual reranking code — while keeping accuracy close to a full-collection multivector search. First stage can be dense, sparse, or [[MUVERA]] (a fixed-dimensional approximation of the multivector). Recommended candidate depth: ~100–500 before the ColBERT rerank.

---

## The Cost

ColBERT-style storage is the same multi-vector pressure seen elsewhere — many vectors per document. Qdrant's mitigations: `m=0` avoids spending HNSW memory on the rerank field, [[MUVERA]] gives a single-vector first stage, and Qdrant's quantization family ([[Scalar Quantization]], [[Binary Quantization]], [[TurboQuant]]) can compress the stored vectors.

---

## Qdrant vs the Search Engines

| | [[Qdrant Vector DB]] | [[Elasticsearch]] (8.18+) | [[OpenSearch]] (3.3+) |
|---|---|---|---|
| Multi-vector field | native `multivector_config` | `rank_vectors` | `object`+`float` composite |
| MaxSim scoring | `MultiVectorComparator.MAX_SIM` | `maxSimDotProduct` | `lateInteractionScore` painless fn |
| First-stage approx | [[MUVERA]] / dense / sparse | average vectors | single-vector k-NN |
| Two-stage mechanism | `prefetch` + `query` (one call) | rescore retriever | ml-inference search processor |
| Disable ANN on rerank field | `hnsw_config m=0` | (rank_vectors not HNSW-indexed) | (rescore-only) |
| Role | reranker | reranker | reranker |

All three land on the same retrieve-then-rerank shape; the difference is packaging — Qdrant exposes it as one Query API call with the cleanest first-class multivector ergonomics.

---

## Where Late Interaction Fits

| | [[Bi-Encoder]] | Late Interaction ([[ColBERT]]/[[ColPali]]) | [[Cross-Encoder]] |
|---|---|---|---|
| Vectors compared | 1 vs 1 | many vs many (MaxSim) | full transformer pass |
| Storage | Low | High | None (stateless) |
| Latency | Fast | Medium | Slow |
| Role in Qdrant | first-stage ANN / `prefetch` | rerank candidates (`m=0` field) | external rerank |

---

## Related Concepts
- [[Late Interaction]] — the architecture (MaxSim over per-token/per-patch vectors)
- [[ColBERT]] — text-domain late interaction; the primary subject here
- [[ColPali]] — visual late interaction (document page images)
- [[MUVERA]] — fixed-dimensional approximation used as the Qdrant first stage
- [[HNSW]] — ANN index (disabled with `m=0` on the rerank field)
- [[Hybrid Search]] — sparse/dense first stage feeding the rerank
- [[Reranking]] — late interaction's role in Qdrant

## Related Topics
- [[Late Interaction in Elasticsearch]] — the parallel Elastic implementation
- [[Late Interaction in OpenSearch]] — the parallel OpenSearch implementation
- [[Late Interaction in Vespa]] — tensor-expression MaxSim and billion-scale ColPali
- [[Interaction Paradigms]] — the no/late/early interaction spectrum
- [[Search Platforms]] · [[Reasoning Reranking]] · [[Frontier of Search 2025]]

## Source
- [Multivectors and Late Interaction — Qdrant docs](https://qdrant.tech/documentation/advanced-tutorials/using-multivector-representations/)
- [Working with ColBERT — Qdrant docs](https://qdrant.tech/documentation/fastembed/fastembed-colbert/)
- [Multi-Vector Postprocessing — Qdrant docs](https://qdrant.tech/documentation/fastembed/fastembed-postprocessing/)
