---
type: article
title: "Search using LTR - Elastic Docs"
source: "https://www.elastic.co/docs/solutions/search/ranking/learning-to-rank-search-usage"
author: "[[Elastic]]"
published:
created: 2026-06-13
concepts:
  - Elasticsearch Learning to Rank
  - Learning to Rank
topics:
  - Ranking and Retrieval
tags:
  - article
  - documentation
  - ranking
  - learning-to-rank
  - elasticsearch
  - ltr
---

# Search using LTR - Elastic Docs

**Source:** https://www.elastic.co/docs/solutions/search/ranking/learning-to-rank-search-usage
**Author:** [[Elastic]] (official docs)

How to apply a deployed [[Elasticsearch Learning to Rank|native Elasticsearch LTR]] model at search time (8.12.0+, subscription-gated). Two ways to use it.

---

## As a rescorer

Add a `learning_to_rank` block under `rescore`, referencing the `model_id` and passing named `params` (e.g. `query_text`) into the feature query templates. A first-pass query supplies the candidates to rescore.

```json
"rescore": {
  "learning_to_rank": {
    "model_id": "ltr-model",
    "params": { "query_text": "the quick brown fox" }
  },
  "window_size": 100
}
```

## As a retriever (Stack 9.1+)

LTR can also sit in the retriever pipeline via a **`rescorer` retriever** that wraps an inner retriever (e.g. a `standard` retriever) and applies the same `learning_to_rank` rescore over its results.

## Known limitation: `window_size`

LTR scores are generally **not comparable** to first-pass query scores and can be lower, so a non-rescored doc could otherwise outrank a rescored one. Therefore `window_size` is **mandatory** for LTR rescorers and must be `>= from + size`. When paginating, keep `window_size` constant across pages (only `from` changes) — otherwise top hits shift confusingly as the user steps through pages.

## Related Concepts

- [[Elasticsearch Learning to Rank]] · [[Learning to Rank]] · [[Reranking]] · [[Retrieval Pipeline]]

## Related Articles

- [[Learning To Rank (LTR) - Elasticsearch Native]] — the overview / training side
- [[We're Bringing Learning to Rank to Elasticsearch]] — the predecessor OSC plugin

## Companies

- [[Elastic]]
