---
type: article
created: 2026-10-20
title: "More efficient multi-vector embeddings with MUVERA"
source: "https://weaviate.io/blog/muvera"
author: ["[[Roberto Esposito]]", "[[Joon-Pil (JP) Hwang]]"]
published: 2025-06-05
concepts: ["[[MUVERA]]", "[[Late Interaction]]", "[[ColBERT]]", "[[ColPali]]", "[[HNSW]]", "[[LSH]]"]
topics: ["[[Vector Search Tradeoffs]]"]
tags: [multi-vector, muvera, weaviate, late-interaction, vector-search, company-blog]
---

# More Efficient Multi-Vector Embeddings with MUVERA

[[Weaviate]] blog post by [[Roberto Esposito]] and [[Joon-Pil (JP) Hwang]] announcing [[MUVERA]] support in [[Weaviate Vector DB]] 1.31. Multi-vector models ([[ColBERT]], [[ColPali]]/ColQwen) retrieve better but cost memory and indexing time; MUVERA encodes each multi-vector embedding into one fixed-size vector, so [[HNSW]] indexes one vector per object instead of many.

---

## How the Encoding Is Built

1. **Space partitioning** into `B` buckets. SimHash ([[LSH]]) is preferred over k-means because it is data-oblivious. Document buckets average their vectors, query buckets sum them; empty buckets are filled with a nearby vector.
2. **Dimensionality reduction** — a random ±1 projection to `d_proj`, following the Johnson–Lindenstrauss lemma.
3. **Repetitions** — steps 1–2 repeated `r_reps` times and concatenated.
4. **Final projection** — *not* implemented in Weaviate, since the paper's authors found its benefit limited.

Encoding length is `r_reps × 2^k_sim × d_proj`. Weaviate exposes `k_sim`, `d_proj` and `r_reps` with defaults described as sensible for most use cases.

## Benchmark

LoTTE `lotte-lifestyle` (~119k documents, [[LoTTE]]), colbertv2.0 (about 130 vectors per document), `k_sim=4, d_proj=16, r_reps=10`, on an AMD Ryzen 7 PRO 8700GE with 64 GB RAM.

- **Memory** — about 12 GB without MUVERA, under 1 GB with it. For the example parameters the stored floats drop from 1.9B to 304M; the body calls that a saving of almost 80%, while the post's quick takeaways say ~70%.
- **Import** — over 20 minutes (around 100 objects/s) without MUVERA, around 3–6 minutes with it.
- **Recall** — drops at default search settings; raising HNSW `ef` (above 512) recovers 80%+, and over 90% at 2048.
- **QPS** — higher at equal `ef`, but the authors note this is not a fair comparison because a higher `ef` is needed to recover recall.

## When to Use It

Large deployments where memory cost matters, workloads that tolerate slight recall degradation, and applications that need fast indexing. The authors recommend benchmarking recall on your own data first.

## Related Concepts
- [[MUVERA]] · [[Late Interaction]] · [[ColBERT]] · [[ColPali]] · [[HNSW]] · [[LSH]]

## Related Articles
- [[MUVERA - Multi-Vector Retrieval via Fixed Dimensional Encodings]] — the paper
- [[MUVERA in Qdrant - Multi-Vector Search Course]] — Qdrant's take
- [[Scaling Late Interaction Retrieval in OpenSearch with MUVERA]] — OpenSearch's take
- [[Muvera - Making Multi-Vector Retrieval as Fast as Single-Vector Search (HN Discussion)]] — a Weaviate commenter joins the thread

## People
- [[Roberto Esposito]] · [[Joon-Pil (JP) Hwang]]
