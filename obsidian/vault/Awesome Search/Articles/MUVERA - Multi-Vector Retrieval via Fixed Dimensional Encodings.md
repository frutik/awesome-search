---
type: article
created: 2026-10-20
title: "MUVERA: Multi-Vector Retrieval via Fixed Dimensional Encodings"
source: "https://arxiv.org/html/2405.19504v2"
author: ["[[Laxman Dhulipala]]", "[[Majid Hadian]]", "[[Rajesh Jayaram]]", "[[Jason Lee]]", "[[Vahab Mirrokni]]"]
published: 2024-05
concepts: ["[[MUVERA]]", "[[Late Interaction]]", "[[ColBERT]]", "[[PLAID]]", "[[Maximum Inner Product Search]]", "[[LSH]]", "[[Vector Quantization]]", "[[Reranking]]"]
topics: ["[[Vector Search Tradeoffs]]"]
tags: [paper, multi-vector, late-interaction, muvera, vector-search, google]
---

# MUVERA: Multi-Vector Retrieval via Fixed Dimensional Encodings

The original [[MUVERA]] paper (arXiv 2405.19504) from [[Google]] Research and Google DeepMind — [[Laxman Dhulipala]] (Google Research and UMD), [[Majid Hadian]] (Google DeepMind), [[Rajesh Jayaram]] (corresponding author), [[Jason Lee]] and [[Vahab Mirrokni]] (Google Research). It reduces multi-vector similarity search to single-vector [[Maximum Inner Product Search|MIPS]], so off-the-shelf MIPS solvers can serve [[Late Interaction]] models such as [[ColBERT]].

---

## The Problem

Multi-vector models score with **Chamfer similarity** — for each query vector, the max inner product over the document's vectors, summed. This is the MaxSim score of ColBERT-style late interaction. Single-vector ANN indexes cannot search it directly, and the prior state of the art ([[PLAID]] and the single-vector "SV heuristic" underneath ColBERTv2) retrieves candidates token-by-token and then deduplicates.

## Fixed Dimensional Encodings (FDEs)

MUVERA builds asymmetric query and document FDEs whose inner product approximates Chamfer similarity:

1. **Space partition** — SimHash with `k_sim` random Gaussian hyperplanes ([[LSH]]) splits space into `B = 2^k_sim` clusters. k-means was tested too and gave no Pareto gain while losing the data-oblivious property.
2. **Aggregation** — query blocks *sum* the query vectors in each cluster; document blocks take the *centroid* of the document vectors in each cluster.
3. **Fill empty clusters** (documents only) — an empty cluster takes the document vector closest in Hamming distance to that cluster's bit-string. Not applied to queries, so no query vector contributes twice.
4. **Inner projection** — a random ±1 projection shrinks each block from `d` to `d_proj`.
5. **Repetitions** — `R_reps` independent partitions/projections are concatenated: `d_FDE = B · d_proj · R_reps`.
6. **Final projection** (optional) — down to `d_final`; worth "small but non-trivial 1-2% recall boosts" at fixed dimension.

Retrieval runs MIPS over document FDEs, then re-ranks candidates with exact Chamfer similarity. Because FDEs do not depend on the data, the authors argue they are robust to distribution shift and usable in streaming settings.

## Guarantees

- **Theorem 2.1** — the normalized FDE dot product is within ε additive error of normalized Chamfer similarity with probability ≥ 1−δ.
- **Lemma A.3** — the estimate is one-sided: it never overestimates normalized Chamfer when `d = d_proj`.
- **Theorem 2.2** — the retrieved document is within ε of the best normalized Chamfer score with high probability; the authors call this the first algorithm with provable guarantees for Chamfer search that is strictly faster than brute force.

## Experiments

Six [[BEIR]] datasets — [[MS MARCO]], HotpotQA, NQ, Quora, SciDocs, ArguAna (8K to 8.8M documents, 18–165 average tokens) — with ColBERTv2 embeddings (`d = 128`, 32 query embeddings). Single-vector search used DiskANN (max degree 200, build beam-width 600); product quantization PQ-256-8 gives 32× compression, so a 10,240-dim FDE takes 1,280 bytes ([[Vector Quantization]]).

**FDE vs SV heuristic (MS MARCO, offline)**
- 4096-dim FDEs match the deduplicated SV heuristic's recall with 1.75–3.75× fewer candidates (10.5–15× fewer than non-deduplicated).
- 10240-dim FDEs: 2.6–5× and 20–22.5× fewer.
- At 80% recall: 60 candidates (10,240-dim) and 80 (4,096-dim), versus 300 (dedup) or 1,200 (non-dedup) for SV.
- `d_FDE = 5120` reaches 95% recall with 75 candidates.

**End-to-end vs PLAID**
- Within 0.4% of PLAID's Recall@k on MS MARCO; up to 1.56× higher recall elsewhere (e.g. HotpotQA).
- Averaged over datasets and k ∈ {100, 1000}: 10% higher Recall@k (up to 56%) and 90% lower latency (up to 5.7×).

**Optimizations**
- *Ball carving* of query embeddings (τ = 0.7): 5.9 clusters per query on average, a 5.4× reduction; ~25% QPS gain for sequential and 20% for parallel re-ranking.
- *PQ-256-8*: 32× space reduction and up to 20× higher QPS at the same beam-width with minimal recall loss.

## Limitations

MUVERA did not beat PLAID on MS MARCO, possibly because PLAID was carefully tuned for that dataset. The paper also does not study how the average number of embeddings per document affects FDE quality.

## Related Concepts
- [[MUVERA]] · [[Late Interaction]] · [[ColBERT]] · [[PLAID]]
- [[Maximum Inner Product Search]] · [[LSH]] · [[Vector Quantization]] · [[Reranking]]

## Related Articles
- [[MUVERA - Transforming Multi-Vector Information Retrieval Through Fixed Dimensional Encodings]] — long-form walkthrough of this paper
- [[More Efficient Multi-Vector Embeddings with MUVERA]] — Weaviate's implementation
- [[MUVERA in Qdrant - Multi-Vector Search Course]] — Qdrant/FastEmbed implementation
- [[Scaling Late Interaction Retrieval in OpenSearch with MUVERA]] — OpenSearch implementation and benchmarks
- [[Muvera - Making Multi-Vector Retrieval as Fast as Single-Vector Search (HN Discussion)]]

## People
- [[Laxman Dhulipala]] · [[Majid Hadian]] · [[Rajesh Jayaram]] · [[Jason Lee]] · [[Vahab Mirrokni]]
