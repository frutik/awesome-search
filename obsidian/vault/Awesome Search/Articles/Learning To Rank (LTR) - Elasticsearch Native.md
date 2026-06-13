---
type: article
title: "Learning To Rank (LTR) - Elasticsearch Native"
source: "https://www.elastic.co/docs/solutions/search/ranking/learning-to-rank-ltr"
author: "[[Elastic]]"
published:
created: 2026-06-13
concepts:
  - Elasticsearch Learning to Rank
  - Learning to Rank
  - LambdaMART
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

# Learning To Rank (LTR) - Elasticsearch Native

**Source:** https://www.elastic.co/docs/solutions/search/ranking/learning-to-rank-ltr
**Author:** [[Elastic]] (official docs)

Overview page for Elasticsearch's **native** LTR, introduced in **version 8.12.0** (subscription-gated). The first-party successor to the [[We're Bringing Learning to Rank to Elasticsearch|OpenSource Connections plugin]] — see [[Elasticsearch Learning to Rank]] for the two-module comparison.

---

## What it covers

LTR uses a trained ML model as a **second-stage re-ranker** over a simpler first-stage retrieval. The LTR function takes a list of documents plus a **search context** (at minimum the user's query terms; optionally user demographics/geo/age, query length, or per-document signals like the title-field score).

### Judgment list

Trained on a [[Judgment Lists|judgment list]] — query/document pairs with relevance grades (binary, or graded 0–4). Can be human- or machine-generated (often from behavioral analytics with human moderation). Quality guidance: balance examples across query types (title vs actor vs director searches) to avoid overfitting, and balance positive vs negative examples.

### Feature extraction

Three feature categories:
- **Document features** — from document properties (e.g. product price).
- **Query features** — from the query (e.g. number of words).
- **Query-document features** — document in the context of the query (e.g. BM25 score of the `title` field).

In Elasticsearch, features are extracted with **templated `query_extractor` queries** (e.g. `title_bm25` → `match` on `title` with `{{query}}`), used both when building the training set and at inference time.

### Models

The objective is to optimally rank against the judgment list under a metric like [[NDCG]] or MAP. Elasticsearch relies on **gradient-boosted decision tree (GBDT)** models for inference. **Training happens outside Elasticsearch** — [[LambdaMART]] is the recommended approach for strong ranking with low inference latency; [[XGBoost]]'s `XGBRanker` is the suggested LambdaMART implementation, and **[[eland]]** helpers integrate the trained model into Elasticsearch.

## Related Concepts

- [[Elasticsearch Learning to Rank]] · [[Learning to Rank]] · [[LambdaMART]] · [[XGBoost]] · [[eland]] · [[NDCG]] · [[Judgment Lists]] · [[Reranking]]

## Related Articles

- [[Search using LTR - Elastic Docs]] — how to apply the deployed model (rescorer / retriever)
- [[We're Bringing Learning to Rank to Elasticsearch]] — the predecessor OSC plugin
- [[Learn-to-Rank with OpenSearch and Metarank]] — external-re-ranker contrast

## Companies

- [[Elastic]]
