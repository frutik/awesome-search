---
type: tool
title: "qdrant-relevance-feedback"
aliases: ["relevance-feedback package", "Qdrant Relevance Feedback"]
website: https://qdrant.tech/articles/relevance-feedback/
docs: https://qdrant.tech/documentation/tutorials-search-engineering/using-relevance-feedback/
tags:
  - tool
  - relevance-feedback
  - vector-search
  - hnsw
  - open-source
related_concepts:
  - "[[Relevance Feedback]]"
  - "[[HNSW]]"
  - "[[Knowledge Distillation]]"
  - "[[Cross-Encoder]]"
created: 2026-07-29
---

# qdrant-relevance-feedback

Python package that fits the three parameters (`a`, `b`, `c`) of [[Qdrant]]'s index-native [[Relevance Feedback]] query — the scoring formula that guides [[HNSW]] traversal toward what a feedback model judged relevant.

You do not train per query. Fitting happens **once per (feedback model, collection, retriever)** and the resulting weights are then passed with every relevance-feedback query. The package exists so that using the feature doesn't require an ML background — *"nobody needs a machine learning degree to use a search engine."*

## What it does

- Scores a sample of domain queries with your chosen feedback model — a [[Cross-Encoder]], a bi-encoder, a late-interaction model like [[ColBERT]], a custom [[Learning to Rank]] model, or an LLM
- Mines context pairs from the top results
- Fits `a`, `b`, `c` by pairwise ranking loss against that signal — effectively [[Knowledge Distillation]] of the feedback model into the vector index
- Emits weights for the `RelevanceFeedbackQuery` API

Reference experiments use 50–6,000 queries depending on collection size, with a 50/50 train/validation split.

## Related

- Shipped alongside the relevance feedback query in **Qdrant 1.17.0** (February 2026)
- [[Qdrant Vector DB]] — the engine holding the index
- Article: [[Relevance Feedback in Qdrant]] — the formula it fits, and the [[BEIR]] evaluation
- Tutorial: [Relevance Feedback Retrieval in Qdrant](https://qdrant.tech/documentation/tutorials-search-engineering/using-relevance-feedback/)
- Talk: [[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]] — [[Berlin Buzzwords]] 2026
- Compare: [[qdrant-sparse-finetune]] — the same "make ML approachable" framing on the sparse side
