---
type: article
title: "Efficient Federated Search for Retrieval-Augmented Generation using Lightweight Routing"
source: https://arxiv.org/abs/2502.19280
author:
  - Akash Dhasade
  - Rachid Guerraoui
  - Anne-Marie Kermarrec
  - Diana Petrescu
  - Rafael Pires
  - Mathis Randl
  - Martijn de Vos
published: 2025-02-26
tags:
  - article
  - paper
  - rag
  - query-routing
  - federated-search
concepts:
  - "[[Query Routing]]"
  - "[[Federated Search]]"
  - "[[RAG]]"
  - "[[Adaptive Retrieval]]"
topics:
  - "[[Federated vs Unified Search]]"
created: 2026-09-26
---

# Efficient Federated Search for RAG using Lightweight Routing (RAGRoute)

**Authors:** Akash Dhasade, Rachid Guerraoui, Anne-Marie Kermarrec, Diana Petrescu, Rafael Pires, Mathis Randl, Martijn de Vos (EPFL)
**Source:** [arXiv 2502.19280](https://arxiv.org/abs/2502.19280) — to appear at DAIS 2026; an earlier version appeared at EuroMLSys 2025

## Summary

When knowledge is spread across institutions that will not pool their data, RAG needs [[Federated Search]]: send the query to several independent sources, then merge and rerank what comes back. Most such pipelines simply query **every** source. RAGRoute adds the classic missing step — **resource selection** — with a small neural classifier that predicts, per query, which sources are worth contacting.

The motivating observation, on a medical QA benchmark with four corpora (PubMed, StatPearls, Wikipedia, textbooks): usefulness varies sharply by question set. PubMed helps everywhere; StatPearls or Wikipedia help only in particular cases; the textbooks corpus is mostly irrelevant to PubMedQA questions.

## The Router

- A **shallow neural network** of a few fully connected layers, deliberately cheap so routing costs almost nothing next to retrieval and generation — modelled on mixture-of-experts gating. It outperformed the other classifiers they tried, including random forests.
- It outputs a relevance probability per (query, source) pair, thresholded into a yes/no routing decision.
- **Training labels**, two ways: *rerank-based* — retrieve from all sources, rerank jointly, and mark a source relevant if any of its documents lands in the global top-k; or *LLM-based* — an external LLM grades retrieved documents and the grades are aggregated per source.

## Results

Evaluated on three benchmarks (MIRAGE, MMLU, FeB4RAG) against querying all sources, none, or a random subset:

- Up to **89.70% recall** in source selection, up to **80.65%** less communication volume and **52.50%** lower end-to-end latency, while matching the accuracy of querying everything.
- On MMLU: all sources 77.10%, RAGRoute 76.09%, no retrieval 73.35% — and **random source selection 71.74%, worse than no retrieval at all**. On MIRAGE: none 60.58%, random 64.98%, RAGRoute 65.64%, all 66.96%.

The random-below-none result is the argument for routing in one number: indiscriminate retrieval does not just cost more, irrelevant context actively distracts the model.

## Related Concepts

- [[Federated Search]] — resource selection, the step most RAG federations skip
- [[Query Routing]] · [[Adaptive Retrieval]] · [[RAG]]

## Related Notes

- [[Sources of Evidence for Vertical Selection]] — the same selection problem, fifteen years earlier, for web verticals
- [[LTRR - Learning To Rank Retrievers for LLMs]] — resource selection over retrievers rather than corpora
- [[Query Routing - Direct Queries to the Right Source]] — multi-route routing with a relevance threshold, as a tutorial
- [[Federated vs Unified Search]]
