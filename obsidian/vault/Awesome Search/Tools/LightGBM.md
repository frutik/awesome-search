---
title: "LightGBM"
aliases: ["LightGBM", "LGBMRanker"]
status: stub
tags:
  - tool
  - ranking
  - learning-to-rank
  - machine-learning
---

# LightGBM

> **Stub.** Created as a placeholder — expand with vault-sourced content.

## What it is

Microsoft's gradient-boosted decision tree library. Its `lambdarank` objective implements [[LambdaMART]], making it a common choice for feature-based LTR rerankers. Exposes `ndcg_eval_at` and uses the Burges (exponential-gain) [[NDCG]] variant by default.

## Vault references (existing coverage)

- [[Learning to Rank]] — `LGBMRanker(objective="lambdarank", ...)` code snippet
- [[Building a Better Search Engine for Semantic Scholar]] — LightGBM + LambdaRank reranker, 22 engineered features
- [[NDCG]] / [[Flavors of NDCG]] — LightGBM uses the Burges NDCG variant
- [[Hybrid Search and Learning-to-Rank with Metarank]] — LightGBM as a LambdaMART implementation; missing-value handling

## TODO

- [ ] Document ranking objectives and how they map to [[Ranking Objectives]].

## Related

- [[LambdaMART]] · [[XGBoost]] · [[CatBoost]] · [[Learning to Rank]] · [[Ranking Objectives]] · [[Metarank]]
