---
type: topic
title: "Late Interaction in Vespa"
aliases: ["ColBERT in Vespa", "ColPali in Vespa", "Vespa tensor MaxSim", "Late Interaction Tensors in Vespa"]
tags: [topic, late-interaction, colbert, colpali, vespa, vector-search, neural-ir, reranking, multi-vector, tensors]
related_concepts: [Late Interaction, ColBERT, ColPali, Token Pooling, Binary Quantization, HNSW, Dense Vector Retrieval, Bi-Encoder, Cross-Encoder, Reranking, Hybrid Search]
related_topics: [Late Interaction in Elasticsearch, Late Interaction in OpenSearch, Late Interaction in Qdrant, Interaction Paradigms, Search Platforms, Reasoning Reranking, Frontier of Search 2025]
articles:
  - "[[Announcing the Vespa ColBERT Embedder]]"
companies: [Vespa]
people: [Jo Kristian Bergum]
created: 2026-06-29
---

# Late Interaction in Vespa

How [[Late Interaction]] models — [[ColBERT]] for text, [[ColPali]] for document images — are indexed, scored, and scaled inside [[Vespa]]. Vespa is the **origin engine for production late interaction**: it shipped a native [[ColBERT]] embedder and the binary-quantization tricks that the rest of the field later adopted (work led by [[Jo Kristian Bergum]]). Unlike [[Elasticsearch]], [[OpenSearch]], and [[Qdrant Vector DB]] — which added dedicated multi-vector fields and fixed MaxSim functions — Vespa expresses late interaction in its **general tensor ranking framework**: you write the MaxSim function yourself as a tensor expression. This is the most flexible of the four, at the cost of more to learn. See the parallel topics [[Late Interaction in Elasticsearch]], [[Late Interaction in OpenSearch]], [[Late Interaction in Qdrant]].

---

## The Building Blocks

### Multi-vector storage: mixed tensors
Late-interaction vectors are stored as **mixed tensors** — mapped dimensions (variable counts) plus a dense dimension (the compressed vector). Document tokens/patches are an unbound mapped dimension, so docs may carry different numbers of vectors.

```
# ColBERT text — one 16-byte vector per token
field colbert type tensor<int8>(token{}, v[16]) { indexing: attribute | summary }

# Long-context ColBERT — sliding context windows of tokens
field colbert type tensor<int8>(context{}, token{}, v[16])

# ColPali — one vector per page patch
field embedding type tensor<int8>(p{}, v[16])
```

### MaxSim as a ranking expression
There is no built-in `maxSim` keyword — MaxSim is a **tensor expression**: for each query vector, take the max similarity over all document vectors (`reduce(..., max, token)`), then sum over query vectors. Float version (with `unpack_bits` decompressing the stored int8 tensor back to `v[128]`):

```
sum(
  reduce(
    sum(query(qt) * unpack_bits(attribute(colbert)), v),
    max, token
  ),
  querytoken
)
```

Binary version scores directly on packed vectors with `hamming`:

```
sum(reduce(1 / (1 + sum(hamming(query, page), v)), max, p), q)
```

---

## Binary Quantization (the original 32× trick)

Vespa pioneered sign-bit binarization of late-interaction vectors: each 128-dim float token vector → 128 bits = 16 `int8` cells. From [[Announcing the Vespa ColBERT Embedder]]: ~90 KB/doc → ~2.8 KB/doc, **32× reduction with <1% quality loss**, because MaxSim's top-token alignment is robust to binarization. At query time `unpack_bits(attribute(colbert))` decompresses, or `hamming` distance scores the packed form directly (~3.5× faster than float dot products; e.g. 52.4 → 51.6 nDCG@5). This is the same idea Elastic later exposed as `maxSimInvHamming` bit vectors.

---

## Phased Ranking (Vespa's native two-stage)

Late interaction runs as Vespa's **second phase** — the engine has multi-phase ranking as a first-class concept, so no external rerank tier is needed:

1. **First phase (retrieval / shortlist)** — a cheap retriever narrows candidates: `nearestNeighbor` over single-vector embeddings (HNSW, optionally `distance-metric: hamming`) or [[BM25]]. **Query token pruning** keeps only a few query vectors here.
2. **Second phase (rerank)** — the MaxSim tensor expression scores the shortlist using the full multi-vector representation stored in-document.

---

## Scaling to Billions

Vespa's scaling story (ColPali at billion-page scale): keep the MaxSim computation **on the content nodes next to the data** — "transfer vector data at the speed of memory and not the network." Combined with binarization, `hamming` first-phase retrieval, patch/token pooling, and real-time CRUD, this makes billion-scale late-interaction retrieval practical in one engine. Vespa also supports **long-context ColBERT** via the `context{}` dimension — splitting a long document into sliding windows and reducing MaxSim within or across windows.

---

## Vespa vs the Other Engines

| | [[Vespa]] | [[Elasticsearch]] (8.18+) | [[OpenSearch]] (3.3+) | [[Qdrant Vector DB]] |
|---|---|---|---|---|
| Multi-vector field | mixed `tensor<int8>` | `rank_vectors` | `object`+`float` | native `multivector_config` |
| MaxSim scoring | **you write the tensor expression** | `maxSimDotProduct` / `maxSimInvHamming` | `lateInteractionScore` painless fn | `MultiVectorComparator.MAX_SIM` |
| Binary / hamming | `hamming` + `unpack_bits` (32×) — **pioneered here** | `maxSimInvHamming` bit vectors | (none built-in yet) | [[Binary Quantization]] |
| Two-stage | native multi-phase ranking | rescore retriever | ml-inference search processor | `prefetch` + `query` (one call) |
| First-stage approx | `nearestNeighbor` / BM25 + query-token pruning | average vectors | single-vector k-NN | MUVERA / dense / sparse |
| ColPali / billion-scale | yes (compute on content nodes) | yes (rescore) | emerging | yes (rerank) |
| Role | reranker (2nd phase) | reranker | reranker | reranker |

All four converge on the same retrieve-then-rerank architecture. Vespa's distinction: it never needed a dedicated field type because its tensor engine already expressed MaxSim — and it set the binary-quantization precedent the others followed.

---

## Where Late Interaction Fits

| | [[Bi-Encoder]] | Late Interaction ([[ColBERT]]/[[ColPali]]) | [[Cross-Encoder]] |
|---|---|---|---|
| Vectors compared | 1 vs 1 | many vs many (MaxSim) | full transformer pass |
| Storage | Low | High (mitigated 32× by binarization) | None (stateless) |
| Latency | Fast | Medium | Slow |
| Role in Vespa | first-phase `nearestNeighbor` | second-phase rerank | external rerank |

---

## Related Concepts
- [[Late Interaction]] — the architecture (MaxSim over per-token/per-patch vectors)
- [[ColBERT]] — text-domain late interaction; Vespa's native embedder
- [[ColPali]] — visual late interaction; scaled to billions in Vespa
- [[Binary Quantization]] — the sign-bit 32× compression Vespa pioneered for late interaction
- [[HNSW]] — `nearestNeighbor` first-phase index
- [[Hybrid Search]] — BM25/dense first stage feeding the MaxSim rerank
- [[Reranking]] — late interaction's role (Vespa second phase)

## Related Topics
- [[Late Interaction in Elasticsearch]] · [[Late Interaction in OpenSearch]] · [[Late Interaction in Qdrant]] — the parallel engine implementations
- [[Interaction Paradigms]] — the no/late/early interaction spectrum
- [[Search Platforms]] · [[Reasoning Reranking]] · [[Frontier of Search 2025]]

## Related Articles
- [[Announcing the Vespa ColBERT Embedder]] — the native ColBERT embedder and 32× binary quantization

## People
- [[Jo Kristian Bergum]] — [[Vespa]] (now [[Hornet]]); author of the ColBERT embedder, binarization, and ColPali-scaling work

## Source
- [Announcing the Vespa ColBERT Embedder](https://blog.vespa.ai/announcing-colbert-embedder-in-vespa/)
- [Announcing Vespa Long-Context ColBERT](https://blog.vespa.ai/announcing-long-context-colbert-in-vespa/)
- [Scaling ColPali to billions of PDFs with Vespa](https://blog.vespa.ai/scaling-colpali-to-billions/)
- [Transforming the Future of Information Retrieval with ColPali](https://blog.vespa.ai/Transforming-the-Future-of-Information-Retrieval-with-ColPali/)
