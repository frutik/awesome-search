---
type: article
title: "LTRR: Learning To Rank Retrievers for LLMs"
source: https://arxiv.org/abs/2506.13743
author:
  - To Eun Kim
  - "[[Fernando Diaz]]"
published: 2025-06-16
tags:
  - article
  - paper
  - rag
  - query-routing
  - learning-to-rank
  - sigir
concepts:
  - "[[Query Routing]]"
  - "[[Learning to Rank]]"
  - "[[Adaptive Retrieval]]"
  - "[[RAG]]"
  - "[[Federated Search]]"
  - "[[BM25]]"
topics:
  - "[[Query Classification]]"
created: 2026-09-26
---

# LTRR: Learning To Rank Retrievers for LLMs

**Authors:** To Eun Kim, [[Fernando Diaz]] (Carnegie Mellon University)
**Venue:** SIGIR 2026 (also a SIGIR 2025 LiveRAG spotlight) · [arXiv 2506.13743](https://arxiv.org/abs/2506.13743) · [code](https://github.com/kimdanny/Starlight-LiveRAG)

## Summary

RAG systems usually hard-wire one retriever even though no retriever wins on every query. LTRR frames the choice as **learning to rank retrievers**: for each query, rank a pool of retrievers by how much each would improve the LLM's answer, and send the query to the top one. The authors place this explicitly in the lineage of distributed IR and [[Federated Search]] — resource selection, with retrievers as the resources.

Two design choices distinguish it:

- **The target is downstream utility, not retrieval relevance.** A retriever's label is the gain in answer quality it produces over answering with *no* retrieval, min-max normalised per query.
- **"No retrieval" is a candidate route.** The router can decide the LLM is better off without context — merging *which retriever* and *whether to retrieve* into one decision (compare [[Adaptive Retrieval]]).

## Setup

- **Retriever pool:** [[BM25]] and E5-base over a sampled FineWeb corpus, each plain or followed by one of two rerankers — six retrievers, plus the no-retrieval option. The router sees retrievers only through their outputs, not the corpus.
- **Features:** pre-retrieval (query embedding reduced to 32 dimensions by [[PCA]], query length, query type) and post-retrieval per retriever — query-to-results similarity (overall, average, max, variance), a Moran coefficient of semantic autocorrelation among the results, and how similar a retriever's results are to the other retrievers'.
- **Models:** pointwise, pairwise and listwise [[Learning to Rank|LTR]] — XGBoost, SVMRank, a feedforward network, DeBERTa — plus five train-free heuristic routers.
- **Labels:** utility measured by BEM or by Answer Correctness (AC).
- **Data:** a synthetic QA set generated with DataMorgana for controlled variation in question types.

## Findings

- Routing beats the strongest single-retriever RAG baseline, with **pairwise XGBoost** the best router.
- Gains are statistically significant only for routers trained on the **Answer Correctness** objective; BEM-trained routers show no significant gain, which the authors attribute to metric reliability — the choice of utility metric matters as much as the model.
- The improvements hold in-distribution and in some of the four **unseen-query-type** splits (multi-aspect, comparison, complex, open-ended — each held out of training).

## Caveat

Post-retrieval features require **running every retriever** before routing. This router optimises answer quality, not retrieval cost — unlike cost-motivated routers such as [[Adaptive-RAG - Learning to Adapt Retrieval-Augmented LLMs through Question Complexity|Adaptive-RAG]] or [[Efficient Federated Search for RAG using Lightweight Routing|RAGRoute]], which decide before retrieving.

## Related Concepts

- [[Query Routing]] · [[Learning to Rank]] · [[Adaptive Retrieval]]
- [[Federated Search]] — resource selection, reframed for RAG
- [[RAG]] · [[BM25]] · [[PCA]]

## Related Notes

- [[RouterRetriever - Routing over a Mixture of Expert Embedding Models]] — routing over encoders, untrained router
- [[Sources of Evidence for Vertical Selection]] — Diaz's earlier work on the same selection problem for web verticals
- [[Andrei Cristea - Qdrant Vector Search and Hybrid Routing]] — a production-flavoured retriever router (sparse / dense / RRF)
