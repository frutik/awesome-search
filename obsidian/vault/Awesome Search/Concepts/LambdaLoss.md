---
title: "LambdaLoss"
type: concept
aliases: ["LambdaLoss", "Lambda Loss"]
status: stub
tags:
  - concept
  - ranking
  - learning-to-rank
  - machine-learning
---

# LambdaLoss

> **Stub.** Created as a placeholder — expand with vault-sourced content.

A generalized **listwise [[Ranking Objectives|ranking objective]]** framework (Wang et al., Google, 2018) that frames learning-to-rank as a **mixture model** where the ranked list π is a hidden variable, with the loss defined as the negative log-likelihood of that model.

Its two key results:
1. Existing methods — [[RankNet]], LambdaRank, SoftRank, ListNet — are **special configurations** of the framework (obtained by choosing the likelihood `p(y | s, π)` and list distribution `p(π | s)`).
2. It enables **metric-driven loss functions** directly tied to the target ranking metric ([[NDCG]]), achieving state-of-the-art accuracy.

This positions LambdaLoss as the unifying generalization above the classic pointwise/pairwise/listwise split, and a principled successor to the [[LambdaMART]] family.

## Related Concepts
- [[Ranking Objectives]] · [[Learning to Rank]] · [[LambdaMART]] · [[RankNet]] · [[NDCG]]

## Related Articles
- [[Learning to Rank - A Complete Guide to Ranking using Machine Learning]] — introduces the framework
