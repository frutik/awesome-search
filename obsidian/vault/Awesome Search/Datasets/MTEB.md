---
title: "MTEB"
aliases: ["MTEB benchmark", "Massive Text Embedding Benchmark", "MMTEB", "MTEB leaderboard"]
tags:
  - dataset
  - benchmark
  - embeddings
  - leaderboard
  - search-evaluation
type: dataset
source: Muennighoff et al. (2022), maintained by the embeddings-benchmark community
domain: heterogeneous — 8 task types across many languages
website: https://github.com/embeddings-benchmark/mteb
created: 2026-08-05
---

# MTEB

## Overview

**MTEB** (Massive Text Embedding Benchmark) is the aggregate benchmark and public leaderboard that the embedding model field competes on. Unlike [[BEIR]], which is retrieval-only, MTEB spans **eight task types** — retrieval, reranking, classification, clustering, pair classification, semantic textual similarity, summarization, and bitext mining.

That breadth is the single most important thing to understand about it: **a model can top the MTEB overall average while being unremarkable at search.** The overall score rewards general-purpose embedding quality, not retrieval quality. Anyone selecting a model for a search system should read the *retrieval* sub-board, not the headline.

MTEB absorbed [[BEIR]] as its retrieval component, so BEIR scores are reported inside MTEB rather than alongside it.

## Boards and Versions

There is no single "MTEB leaderboard," and this causes constant confusion in vendor marketing:

- **MTEB English v2** — the English board
- **MMTEB / multilingual** — the massively multilingual extension, usually with a different leader
- **[[RTEB]]** — the retrieval-focused board with private data, run by the same maintainers
- Domain and language-specific boards (code, law, and various national-language variants)

**MTEB v1 and v2 scores are not comparable.** Task composition and aggregation changed. A number quoted without its board and version is not interpretable.

## Why the Scores Inflate

MTEB's datasets are public — corpus, queries, and labels. That is good for reproducibility and bad for honesty: public test sets leak into training corpora, deliberately or not, and the leaderboard rewards the leakage. The result is a **generalization gap**, where reported scores exceed real-world retrieval accuracy on unseen data.

This is precisely the problem [[RTEB]] was created to address, and it is why teams routinely find that a mid-ranked model beats the board leader on their own data. See [[Retrieval Benchmarks and Leaderboards]] for the full set of failure modes.

## How to Use It

Use MTEB to build a shortlist of 3–5 candidates, then decide between them on your own [[Judgment Lists|judgments]]. Never select on the leaderboard alone. See [[Model Selection and Fine-Tuning Evaluation]].

The `mteb` Python library runs any [[Sentence Transformers]]-compatible model across the suite and is the standard way to reproduce or contribute a number.

## Related

- [[Retrieval Benchmarks and Leaderboards]] — the wider landscape
- [[BEIR]] — the retrieval component, absorbed into MTEB
- [[RTEB]] — the private-data answer to MTEB's overfitting problem
- [[BRIGHT]] — the reasoning stress test MTEB leaders fail badly
- [[Embedding Models Compared]] — the models this ranks
- [[Model Selection and Fine-Tuning Evaluation]] · [[Search Evaluation]] · [[NDCG]]
