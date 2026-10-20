---
type: article
created: 2026-10-20
title: "Scaling Late Interaction Retrieval in OpenSearch with MUVERA (aws-samples)"
source: "https://github.com/aws-samples/AI-search-with-amazon-opensearch-service/tree/muvera-late-interaction/muvera-late-interaction"
author: "[[Amazon Web Services]]"
concepts: ["[[MUVERA]]", "[[Late Interaction]]", "[[ColBERT]]", "[[ColPali]]", "[[Reranking]]", "[[Scalar Quantization]]", "[[Token Pooling]]", "[[HNSW]]"]
topics: ["[[Late Interaction in OpenSearch]]"]
tags: [multi-vector, muvera, opensearch, late-interaction, benchmark, code-sample]
---

# Scaling Late Interaction Retrieval in OpenSearch with MUVERA

A sample in the [[Amazon Web Services]] `aws-samples/AI-search-with-amazon-opensearch-service` repo (branch `muvera-late-interaction`) showing how to scale [[Late Interaction]] — [[ColBERT]] and [[ColPali]] multi-vectors — on [[OpenSearch]] with [[MUVERA]]. Its benchmark write-up reproduces the numbers from the OpenSearchCon talk "Scaling Late Interaction Retrieval in OpenSearch".

---

## The Pattern

1. **Retrieve** — each document's multi-vectors are encoded into one FDE, indexed as a `knn_vector` and searched with ordinary ANN.
2. **Rerank** — the top candidates are rescored with exact MaxSim over their stored multi-vectors via k-NN's `lateInteractionScore` script function ([[Reranking]]).

## Two Deployment Paths

- **Self-managed OpenSearch** — [[opensearch-muvera-plugin]] (Java, Apache-2.0) adds server-side `muvera` ingest and `muvera_query` search processors. The prebuilt zip targets OpenSearch 3.8.0 only; other versions need a source build with JDK 21.
- **Amazon OpenSearch Service (managed)** — custom plugins can't be installed, so the FDE is computed client-side with [[FastEmbed]] 0.7.2+; the `knn_vector` + `lateInteractionScore` steps are unchanged.

FDE dimension is `r_reps × 2^k_sim × dim_proj`, capped at 16,000, and documents and queries must share `dim`, `k_sim`, `dim_proj`, `r_reps` and `seed`. `k_sim=5, dim_proj=16, r_reps=20` gives 10,240 dims; Qdrant's `k_sim=6, dim_proj=32, r_reps=20` (40,960) exceeds the cap. The FDE parameter guidance and FastEmbed snippet are credited to Qdrant ([[MUVERA in Qdrant - Multi-Vector Search Course]]).

## Benchmarks

Single node EC2 g4dn.4xlarge, OpenSearch 3.8.0, Lucene [[HNSW]] (innerproduct, m=16, ef_construction=512). ColBERTv2 on NFCorpus and SciFact ([[BEIR]] text sets, ~180 and ~233 vectors/doc), ColModernVBERT on IRPAPERS (PDF pages, ~1,011 vectors/doc). Quality numbers came from a faiss run and latency from a lucene run, with an expected ~1–2 point offset.

| Approach | SciFact nDCG@10 | NFCorpus nDCG@10 | IRPAPERS recall@10 |
|---|---|---|---|
| Exact MaxSim (ceiling) | 0.692 | 0.344 | 0.839 |
| MUVERA + rerank | 0.671 | 0.311 | 0.733 |
| FDE-only | 0.528 | 0.249 | 0.083 |
| Mean-pool + rerank | 0.363 | 0.144 | 0.233 |

MUVERA + rerank keeps 97% / 90% / 87% of exact; mean-pooling loses 48% / 58% / 72%.

**Rerank dominates latency.** FDE-only runs in ~10 ms on text (17 ms on IRPAPERS); with a 4× oversampled rerank it is ~340 ms, and on SciFact ~97% of the time is the rerank. On IRPAPERS it grows from ~1.5 s at depth 40 to 7.5 s at depth 256.

**A better FDE buys a shallower rerank.** On SciFact, cutting depth from 40 to 20 gives −43% latency for −2.5% nDCG. Raising `r_reps` from 20 to 30 at depth 20 matches the depth-40 baseline (0.6549 vs 0.6593 SciFact, 0.3020 vs 0.3036 NFCorpus) at about 40% less latency, for ~50% more FDE memory (~8% more total shard).

**FDE-only is conditional.** It reaches 72% (NFCorpus) and 76% (SciFact) of exact at ~35× the speed, but only 10% on IRPAPERS — dense visual pages collapse, and raising `k_sim` does not close the gap under the 16,000-dim cap.

**Quantization and pruning.** int8 ([[Scalar Quantization]]) multi-vectors keep nDCG nearly flat (0.6667 vs 0.6682) at 4× smaller storage but give no latency gain in the `_source` path. Adding norm-based token pruning ([[Token Pooling|token reduction]]) gives 8–16× smaller and 1.6–3.3× faster at 93–96% quality kept. A Lucene 10.5 microbenchmark of native `LateInteractionField` scoring ran 13.1 ms vs 440.9 ms for `_source` deserialization — about 34× — which the authors see as the bigger latency win (k-NN RFC #3439).

## Related Concepts
- [[MUVERA]] · [[Late Interaction]] · [[ColBERT]] · [[ColPali]] · [[Reranking]] · [[Scalar Quantization]] · [[Token Pooling]] · [[HNSW]]

## Related Topics
- [[Late Interaction in OpenSearch]]

## Related Articles
- [[MUVERA - Multi-Vector Retrieval via Fixed Dimensional Encodings]]
- [[MUVERA in Qdrant - Multi-Vector Search Course]]

## Tools
- [[OpenSearch]] · [[opensearch-muvera-plugin]] · [[FastEmbed]]
