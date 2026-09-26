---
type: article
title: "Lightweight Query Routing for Adaptive RAG: A Baseline Study on RAGRouter-Bench"
source: https://arxiv.org/abs/2604.03455
author:
  - Prakhar Bansal
  - Shivangi Agarwal
published: 2026-04-03
tags:
  - article
  - paper
  - rag
  - query-routing
  - adaptive-retrieval
  - benchmark
concepts:
  - "[[Query Routing]]"
  - "[[Adaptive Retrieval]]"
  - "[[RAG]]"
  - "[[GraphRAG]]"
topics:
  - "[[Query Classification]]"
created: 2026-09-26
---

# Lightweight Query Routing for Adaptive RAG: A Baseline Study on RAGRouter-Bench

**Authors:** Prakhar Bansal, Shivangi Agarwal
**Source:** [arXiv 2604.03455](https://arxiv.org/abs/2604.03455), April 2026

## Summary

RAG strategies differ a lot in token cost: on RAGRouter-Bench, relative to an LLM-only answer, NaiveRAG costs 1.4×, [[GraphRAG]] 2.1×, HybridRAG 2.8× and IterativeRAG 3.5×. Most deployed systems still apply one strategy to every query. This short paper asks how far the *cheapest possible* routers get: classical classifiers over query text alone, predicting a query type that maps to a strategy.

**RAGRouter-Bench** (Wang et al., 2026) has 7,727 queries over four corpora — MuSiQue (Wikipedia, 3,356 queries), QuALITY (literature, 1,200), UltraDomain (legal, 1,277) and GraphRAG-Bench (medical, 1,896) — each labelled factual (52.9%), summarization (30.0%) or reasoning (17.1%). The benchmark's own finding is that **no single strategy dominates**; the best one depends on the query *and* the corpus.

## Setup

- Five classical classifiers × three feature sets — TF-IDF, MiniLM sentence embeddings, and hand-crafted structural features — for 15 combinations.
- Predicted type maps to a strategy following [[Adaptive-RAG - Learning to Adapt Retrieval-Augmented LLMs through Question Complexity|Adaptive-RAG]]: factual → NaiveRAG, reasoning → HybridRAG, summarization → IterativeRAG. The authors stress this mapping is a simplification **for cost estimation only**.

## Findings

- Best: **TF-IDF + SVM**, macro-F1 **0.928**, accuracy **93.2%**.
- **Lexical beats semantic**: TF-IDF (0.928) outperforms MiniLM embeddings (0.897) by 3.1 macro-F1 and structural features (0.788) by 14.0. Question-word type, domain terminology and patterns such as "summarize" or "compare" are enough to separate the three types; the authors' likely explanation is that dense embeddings conflate surface-similar but type-different queries from different domains, while TF-IDF keeps the vocabulary signals that differ by type.
- A simulated **28.1% token saving** versus always running the most expensive strategy.
- Medical queries are hardest to route (TF-IDF+SVM 0.803 macro-F1) — that corpus is a single long document, so every query type draws on the same text — and legal the most tractable (0.967).

## Caveats

- The savings are **simulated** from the type-to-strategy mapping, not measured answer quality under routing.
- The classifiers see **query text only**; the benchmark shows corpus properties (connectivity, density, hubness and more) also decide which strategy wins, so these results are a floor, not a ceiling.
- Predicting a query-type label is an easier task than predicting the best strategy directly.

## Related Concepts

- [[Adaptive Retrieval]] · [[Query Routing]] · [[Query Classification]]
- [[RAG]] · [[GraphRAG]]

## Related Notes

- [[Adaptive-RAG - Learning to Adapt Retrieval-Augmented LLMs through Question Complexity]] — the complexity-routing precedent this builds on
- [[Query Routing - Direct Queries to the Right Source]] — the keyword-first cascade this result supports
- [[Andrei Cristea - Qdrant Vector Search and Hybrid Routing]] — another cheap router mixing lexical and embedding features
