---
title: "LambdaMART"
aliases: ["LambdaMART", "Lambda MART"]
status: stub
tags:
  - concept
  - ranking
  - learning-to-rank
  - machine-learning
---

# LambdaMART

> **Stub.** Created as a placeholder — expand with vault-sourced content.

## Definition

LambdaMART (Burges, 2010) is the dominant production [[Learning to Rank]] algorithm. It combines **MART** (Multiple Additive Regression Trees = gradient-boosted decision trees) with **LambdaRank** gradients, where the gradient of each pairwise swap is weighted by its impact on a ranking metric (typically [[NDCG]]).

## Vault references (existing coverage)

- [[Learning to Rank]] — has a full LambdaMART section + `LGBMRanker` code
- [[How LambdaMART Works]] — Doug Turnbull explainer (lambda gradients + MART)
- [[Part 1 - Learning to Rank for E-Commerce Search at Otto]] — production use
- [[Building a Better Search Engine for Semantic Scholar]] — LightGBM + LambdaRank reranker
- [[Learn-to-Rank with OpenSearch and Metarank]] — Metarank implements LambdaMART as an external re-ranker
- [[Hybrid Search and Learning-to-Rank with Metarank]] — LambdaMART for multi-retriever fusion
- [[Metarank - Personalized Ranking That Actually Reads Your Clicks]] — LambdaMART via YAML config
- [[LambdaMART Explained - The Workhorse of Learning-to-Rank]] — Tullie Murrell / Shaped; lineage, boosting loop, advantages/limits
- [[Learning to Rank - A Complete Guide to Ranking using Machine Learning]] — Casalegno; LambdaMART positioned between pairwise and listwise, up to [[LambdaLoss]]

## TODO

- [ ] Decide whether this stays a standalone note or stays folded into [[Learning to Rank]] (currently an alias there).
- [ ] Link to implementations: [[LightGBM]], [[XGBoost]], [[CatBoost]], [[RankLib]].

## Implementations & Serving

- Libraries: [[LightGBM]], [[XGBoost]], [[CatBoost]] (all handle missing feature values natively), [[RankLib]]
- Serving: [[Metarank]] — open-source service that trains and serves LambdaMART as a secondary re-ranker

## Related

- [[Learning to Rank]] · [[Ranking Objectives]] · [[NDCG]] · [[RankNet]] · [[Metarank]]
