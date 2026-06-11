---
title: "XGBoost"
aliases: ["XGBoost", "xgboost"]
status: stub
tags:
  - tool
  - ranking
  - learning-to-rank
  - machine-learning
---

# XGBoost

> **Stub.** Created as a placeholder — expand with vault-sourced content.

## What it is

Gradient-boosted decision tree library with learning-to-rank objectives (`rank:ndcg`, `rank:map`, `rank:pairwise`). Frequently deployed as a feature-based LTR reranker, including via ONNX in serving engines.

## Vault references (existing coverage)

- [[Dropbox]] — search ranking model trained with XGBoost on human + LLM-labeled data
- [[E-commerce Search and Recommendation with Vespa]] — LTR via XGBoost (ONNX)
- [[Mirror Mirror - All About Search Suggestions]] — XGBoost rescoring via Vespa / ES LTR plugin
- [[Hybrid Search and Learning-to-Rank with Metarank]] — XGBoost as a LambdaMART implementation; missing-value handling
- [[Metarank]] — ships an `xgboost` model for its LambdaMART ranker

## TODO

- [ ] Document ranking objectives → link to [[Ranking Objectives]].

## Related

- [[LambdaMART]] · [[LightGBM]] · [[CatBoost]] · [[Learning to Rank]] · [[Ranking Objectives]] · [[Metarank]]
