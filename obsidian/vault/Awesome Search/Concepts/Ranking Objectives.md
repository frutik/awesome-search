---
title: "Ranking Objectives"
aliases: ["ranking objective", "ranking loss", "LTR objective", "ranking loss function"]
status: stub
tags:
  - concept
  - ranking
  - learning-to-rank
  - machine-learning
---

# Ranking Objectives

> **Stub.** Created as a placeholder — expand with vault-sourced content.

## Definition

The objective (loss) a [[Learning to Rank]] model optimizes. Three families: **pointwise** (regress/classify each doc), **pairwise** (preference between two docs), **listwise** (optimize a list metric like [[NDCG]] directly). These map onto the evaluation paradigms in [[Pointwise Relevance Evaluation]] / [[Pairwise Relevance Evaluation]] / [[Listwise Relevance Evaluation]].

## Concrete objectives by library (to verify/expand)

- **LightGBM**: `lambdarank`
- **XGBoost**: `rank:ndcg`, `rank:map`, `rank:pairwise`
- **CatBoost**: `YetiRank`, `PairLogit`, `QueryRMSE`

## TODO

- [ ] Confirm objective lists against current library docs before treating as fact.
- [ ] Cross-link each to [[LambdaMART]].

## Related

- [[Learning to Rank]] · [[LambdaMART]] · [[NDCG]] · [[Pointwise Relevance Evaluation]] · [[Pairwise Relevance Evaluation]] · [[Listwise Relevance Evaluation]]
