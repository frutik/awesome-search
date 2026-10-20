---
type: concept
title: "MUVERA"
aliases: ["Multi-Vector Retrieval via Fixed Dimensional Encodings", "Fixed Dimensional Encoding", "FDE", "Muvera"]
tags:
  - concept
  - search
  - neural-ir
  - multi-vector
  - late-interaction
created: 2026-06-29
---

# MUVERA

## Definition

**MUVERA** (Multi-Vector Retrieval via Fixed Dimensional Encodings) collapses a [[Late Interaction]] multi-vector representation (e.g. [[ColBERT]]'s per-token matrix) into a **single fixed-dimensional vector** — a *Fixed Dimensional Encoding* (FDE) — whose inner product approximates the MaxSim score (called *Chamfer similarity* in the paper). This lets a multi-vector document be retrieved with standard single-vector ANN ([[HNSW]], DiskANN, any [[Maximum Inner Product Search|MIPS]] index) in the first stage, sidestepping the cost of full MaxSim during candidate generation. It comes from [[Google]] Research and Google DeepMind — [[Laxman Dhulipala]], [[Majid Hadian]], [[Rajesh Jayaram]], [[Jason Lee]], [[Vahab Mirrokni]] ([[MUVERA - Multi-Vector Retrieval via Fixed Dimensional Encodings|the paper]]).

## Why It Matters

The central problem of late interaction is that MaxSim compares every query vector against every document vector — too expensive for first-stage retrieval over a large corpus, and, as the Qdrant course puts it, "inherently asymmetric and non-metric", so graph indexes navigate it poorly. MUVERA provides a cheap, ANN-indexable proxy:

1. **Stage 1** — encode query and documents as FDEs, retrieve top-k candidates with fast single-vector ANN.
2. **Stage 2** — rerank those candidates with the full multi-vector MaxSim ([[ColBERT]]).

## How an FDE Is Built

1. **Partition** — SimHash ([[LSH]]) with `k_sim` random Gaussian hyperplanes gives `B = 2^k_sim` buckets. Being random rather than fitted (k-means was tested and gave no Pareto gain), the encoding is *data-oblivious* — no training, robust to distribution shift, usable for streaming.
2. **Aggregate** — query buckets *sum* their vectors; document buckets *average* them.
3. **Fill empty buckets** — documents only, from the vector closest in Hamming distance to the bucket's bit-string.
4. **Project** — a random ±1 projection shrinks each bucket to `d_proj`.
5. **Repeat** — `r_reps` independent runs concatenated: `d_FDE = r_reps × 2^k_sim × d_proj`.
6. **Final projection** — optional; the paper reports a 1–2% recall boost, and [[Weaviate Vector DB]] skips it.

As with any random-hyperplane scheme, documents and queries must share the same parameters *and seed* — the AWS sample calls this out explicitly. The paper proves the FDE dot product is an ε-additive, one-sided (never overestimating) approximation of normalized Chamfer similarity.

## What the Numbers Say

- **vs [[PLAID]]** (paper, six [[BEIR]] datasets) — 10% higher Recall@k and 90% lower latency on average. To match the recall of PLAID's deduplicated single-vector heuristic, FDEs retrieve 1.75–3.75× fewer candidates at 4096 dims and 2.6–5× fewer at 10240 dims. No win on [[MS MARCO]], possibly because PLAID was carefully tuned for it. PQ-256-8 ([[Vector Quantization]]) compresses FDEs 32×.
- **Memory and indexing** ([[Weaviate Vector DB]], [[LoTTE]] lifestyle) — ~12 GB → under 1 GB, import from 20+ minutes to 3–6 minutes; recall recovers to 80%+ only with a higher HNSW `ef`.
- **Quality after rerank** ([[OpenSearch]] sample) — MUVERA + rerank keeps 97% / 90% of exact MaxSim nDCG@10 on SciFact / NFCorpus and 87% of recall@10 on IRPAPERS visual pages. FDE-only keeps 72–76% on text but collapses to 10% on dense visual pages. Rerank is ~97% of query latency, and raising `r_reps` 20 → 30 allows halving rerank depth at equal quality for ~40% less latency.

## Trade-offs

- **Recall loss** before reranking — must be bought back with ANN breadth (`ef`) or rerank depth.
- **Storage** — the FDE is stored *alongside* the multi-vectors needed for reranking, so storage roughly doubles versus single-vector search (Qdrant course).
- **Hyper-parameter sensitivity** — a [[Muvera - Making Multi-Vector Retrieval as Fast as Single-Vector Search (HN Discussion)|Hacker News]] commenter found results "very hyper-parameter dependent"; the paper's grid search lists (r_reps, k_sim, d_proj) = (20, 3–5, 8) and (20, 5, 16) among Pareto-optimal settings.
- **Dimension caps** — OpenSearch's 16,000-dim `knn_vector` cap rules out Qdrant's `k_sim=6, dim_proj=32, r_reps=20` (40,960 dims).

## MUVERA vs Average Vectors

The simplest single-vector stand-in for a multi-vector document is the mean of its vectors. [[Elastic]] takes that route: its [[Late Interaction Models - How to Scale and Optimize in Elasticsearch|scaling guide]] for ColPali averages each document's vectors for a first-stage kNN query and reranks with the full vectors. No Elastic documentation, blog post or GitHub issue on MUVERA turned up as of October 2026. The AWS OpenSearch benchmark compares the two directly under the same rerank: mean-pool + rerank loses 48–72% of exact quality where MUVERA + rerank loses 3–13% — roughly 3× better. See [[Late Interaction in Elasticsearch]].

## In Practice

| Engine | How MUVERA is exposed |
|---|---|
| [[Weaviate Vector DB]] (1.31+) | built-in encoding, parameters `k_sim`, `d_proj`, `r_reps`; HNSW over one vector per object |
| [[Qdrant Vector DB]] | [[FastEmbed]] 0.7.2+ `Muvera` postprocessor; `prefetch` on the MUVERA vector, MaxSim rerank on the multivector — see [[Late Interaction in Qdrant]] |
| [[OpenSearch]] | [[opensearch-muvera-plugin]] (self-managed 3.8.0) or client-side FastEmbed (Amazon OpenSearch Service); rerank with `lateInteractionScore` — see [[Late Interaction in OpenSearch]] |
| [[Elasticsearch]] | no MUVERA; average vectors as the first stage |

## Related Concepts

- [[Late Interaction]] — the architecture MUVERA accelerates
- [[ColBERT]] · [[ColPali]] — the multi-vector models MUVERA approximates
- [[PLAID]] — the multi-vector engine MUVERA is benchmarked against
- [[LSH]] — SimHash is the partitioning step
- [[Maximum Inner Product Search]] — the single-vector problem MUVERA reduces to
- [[HNSW]] — single-vector ANN index MUVERA makes usable for late interaction
- [[Token Pooling]] — alternative multi-vector compression (clusters vectors rather than collapsing to one)
- [[Bi-Encoder]] — the single-vector baseline MUVERA imitates for stage 1

## Related Topics

- [[Late Interaction in Qdrant]] — where MUVERA is used as the prefetch stage
- [[Late Interaction in OpenSearch]] — plugin and client-side FDE paths
- [[Late Interaction in Elasticsearch]] — "average vectors" play the analogous role there
- [[Vector Search Tradeoffs]] — the one-vector-or-many axis, and why the multi-vector cost is moved to stage two

## Related Articles

- [[MUVERA - Multi-Vector Retrieval via Fixed Dimensional Encodings]] — the paper
- [[MUVERA - Transforming Multi-Vector Information Retrieval Through Fixed Dimensional Encodings]] — paper walkthrough
- [[More Efficient Multi-Vector Embeddings with MUVERA]] — Weaviate
- [[MUVERA in Qdrant - Multi-Vector Search Course]] — Qdrant
- [[Scaling Late Interaction Retrieval in OpenSearch with MUVERA]] — OpenSearch benchmarks
- [[Muvera - Making Multi-Vector Retrieval as Fast as Single-Vector Search (HN Discussion)]]
- [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]] — the average-vector alternative

## People

- [[Laxman Dhulipala]] · [[Majid Hadian]] · [[Rajesh Jayaram]] · [[Jason Lee]] · [[Vahab Mirrokni]] — paper authors
- [[Roberto Esposito]] · [[Joon-Pil (JP) Hwang]] — Weaviate implementation
- [[Keyur Ramoliya]] — walkthrough
