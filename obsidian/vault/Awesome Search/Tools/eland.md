---
title: "eland"
aliases: ["eland", "Eland"]
website: "https://eland.readthedocs.io/"
repo: "https://github.com/elastic/eland"
maintainer: "[[Elastic]]"
tags:
  - tool
  - elasticsearch
  - machine-learning
  - learning-to-rank
  - python
---

# eland

Elastic's Python client for loading and managing machine-learning models in [[Elasticsearch]]. A pandas-like DataFrame API over Elasticsearch indices, plus helpers for importing trained models for in-cluster inference.

- Docs: https://eland.readthedocs.io/
- GitHub: https://github.com/elastic/eland

## Role in LTR

In [[Elasticsearch Learning to Rank|native Elasticsearch LTR]] (8.12+), the GBDT model is trained outside the cluster — typically an [[XGBoost]] `XGBRanker` ([[LambdaMART]]). eland provides the helpers that serialize that trained ranker and upload it into Elasticsearch as a deployed model, where it is then applied by the `learning_to_rank` rescorer.

## Related

- [[Elasticsearch]] · [[XGBoost]] · [[Elasticsearch Learning to Rank]] · [[LambdaMART]]

## Articles

- [[Learning To Rank (LTR) - Elasticsearch Native]] — names eland as the model-upload path
