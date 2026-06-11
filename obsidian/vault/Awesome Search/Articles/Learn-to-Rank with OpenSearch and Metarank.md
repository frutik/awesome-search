---
type: article
title: "Learn-to-Rank with OpenSearch and Metarank"
source: "https://opensearch.org/blog/ltr-with-opensearch-and-metarank/"
author: "[[Roman Grebennikov]]"
published: 2022-10-25
created: 2026-06-11
concepts:
  - "[[Learning to Rank]]"
  - "[[LambdaMART]]"
  - "[[Reranking]]"
  - "[[Retrieval Pipeline]]"
  - "[[BM25]]"
  - "[[Feature Store]]"
  - "[[Implicit Judgments]]"
  - "[[Click Signals]]"
topics:
  - "[[Search Platforms]]"
tags:
  - article
  - learning-to-rank
  - reranking
  - opensearch
  - ltr
---

# Learn-to-Rank with OpenSearch and Metarank

**Source:** https://opensearch.org/blog/ltr-with-opensearch-and-metarank/
**Author:** [[Roman Grebennikov]]
**Published:** 2022-10-25

Why and how to add a [[LambdaMART]] [[Learning to Rank|LTR]] secondary re-ranker ([[Metarank]]) on top of [[OpenSearch]].

---

## Ranking in Lucene / OpenSearch

The classic three-stage flow: **retrieval** (inverted index per shard) → per-shard **scoring** ([[BM25]]) → **collection** (merge to top-N). BM25 is a strong text-relevance baseline but only sees term frequencies and collection statistics — not behavior or item metadata.

## The `script_score` approach and its limits

OpenSearch `script_score` can fold metadata/behavior into scoring (e.g. `click_count * _score`), but: it runs per matching document (no complex computation), forces you to invent and tune your own formula, and requires features to be either in-index (frequent reindexing) or in an external **[[Feature Store]]**.

## Secondary / multi-level re-ranking

Split retrieval and re-ranking into independent stages (the multi-stage pattern Amazon uses, per Berlin Buzzwords 2019):

- **First level** — index retrieves the full matching set.
- **Second level** — fast rankers like BM25 reduce to top-N (recall-focused).
- **Third level** — a slow ranker reorders only the top-N (precision-focused).

Because final re-ranking runs **outside** the search engine on a top-N subset, you can afford complex LTR like LambdaMART. Tradeoff: it only sees the top-N — a doc under-scored at the first level can never recover (cf. [[When Reranking Becomes a System Boundary]]).

## Metarank as the external re-ranker

- Implements [[LambdaMART]] over an embedded feature-engineering pipeline (BPR, BERT4Rec on the roadmap).
- YAML DSL for ranking factors: rates, counters, sliding windows, UA/Referer/GeoIP parsers, one-hot/label encoding.
- **Agnostic to retrieval** — integrates with your app, not the engine.
- Trains on historical click-through events aggregated into **[[Implicit Judgments]]**; serves real-time inference.
- Event types: `item` (metadata), `ranking` (impression), `interaction` (click/purchase/hover).
- **Redis** state store; expect **+20–30 ms** re-ranking latency (driven by state encoding format, Redis network latency, request size, feature count).

## OpenSearch Remote Ranker Plugin RFC

OpenSearch maintainers are designing a common ranking API so an external re-ranking service can be called internally (no app-side multi-query), hot-swappable across rankers. Metarank devs are collaborating and plan to support the Remote Ranker Plugin API.

## Related Concepts

- [[Metarank]] · [[Learning to Rank]] · [[LambdaMART]] · [[Reranking]] · [[Retrieval Pipeline]] · [[Multi-Stage Ranking]] · [[BM25]] · [[Feature Store]] · [[Implicit Judgments]] · [[Click Signals]]

## Related Articles

- [[Hybrid Search and Learning-to-Rank with Metarank]]
- [[Metarank - Personalized Ranking That Actually Reads Your Clicks]]
- [[When Reranking Becomes a System Boundary]]
- [[Multi-Stage Ranking]]

## People

- [[Roman Grebennikov]] — author, Metarank co-creator
