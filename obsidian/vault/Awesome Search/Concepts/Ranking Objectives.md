---
title: "Ranking Objectives"
type: concept
aliases: ["ranking objective", "ranking loss", "LTR objective", "ranking loss function", "objective function"]
tags:
  - concept
  - ranking
  - learning-to-rank
  - machine-learning
---

# Ranking Objectives

The **objective (loss) function** a [[Learning to Rank]] model optimizes. The objective — not the model architecture — is where the product's definition of relevance is encoded: it states *what "well-ordered results" means* for your application, and the optimizer then chases that target. As [[Doug Turnbull]] puts it, the objective function "holds your power to make or break your search application, far more than the chosen model."

## The Three Families

Ranking objectives are classified by **how many documents the loss function considers at once** (the framing popularized by [[Nikhil Dandekar]] in [[Pointwise vs Pairwise vs Listwise Learning to Rank]]):

| Family | Unit of loss | Idea | Example algorithms |
|---|---|---|---|
| **Pointwise** | one document | Regress/classify each doc's relevance independently, then sort by score | Linear/logistic regression, GBDT regression |
| **Pairwise** | a pair of documents | Learn the correct *relative order* of each pair; minimize **inversions** | [[RankNet]], LambdaRank, [[LambdaMART]] |
| **Listwise** | the whole list | Optimize the ordering of the entire result list directly | SoftRank, AdaRank, ListNet, ListMLE |

### Pointwise
Each document gets a score independent of the others in the result list; the ranking is just a sort over those scores. Any standard regression/classification algorithm works directly. Simple, but the training signal (absolute label accuracy) only loosely matches ranking quality.

### Pairwise
Looks at two documents and learns which should rank higher, penalizing pairs placed in the wrong order. Predicting *relative* order is closer to the nature of ranking than predicting an absolute label, so pairwise generally outperforms pointwise in practice. The dominant production lineage is pairwise: **RankNet → LambdaRank → LambdaMART**.

### Listwise
Operates on the full ranked list. Two sub-techniques:
1. **Direct optimization of an IR measure** such as [[NDCG]] (the metric is non-smooth, so it needs approximation) — e.g. SoftRank, AdaRank.
2. **Custom listwise loss** built from properties of the target ranking — e.g. ListNet, ListMLE.

Listwise methods are the most faithful to ranking metrics but also the most complex. [[LambdaLoss]] generalizes the whole landscape: a mixture-model framework in which RankNet, LambdaRank, SoftRank and ListNet are all special cases.

## The Objective Encodes Business Goals

The objective function is where domain-specific product decisions live. You choose:
1. **The relevance labels/grades** (from human judgments or behavioral signals like clicks/reads).
2. **The ranking metric to optimize** — [[NDCG]], DCG, MAP, MRR, Precision@k, or a metric you invent for your use case.

Different goals → different metrics:
- **Research / recall-heavy** (e.g. legal search): many relevant docs in the top N → a DCG/Precision@k style metric.
- **Known-item search** (exactly one right answer): only the top position matters → **MRR** or **Precision@1**.

## How Pairwise Approximates a Listwise Metric (LambdaMART)

[[LambdaMART]] is the canonical bridge between pairwise training and a listwise objective. Per query it converts the listwise metric into per-document **lambda** gradients by swapping every document pair and accumulating each swap's impact on the metric (e.g. ΔDCG):

```
1. Sort docs by grade descending → ideal ordering
2. Compute ideal_dcg
3. For each pair (doc_i, doc_j), j > i:
     swap them, compute new_dcg
     dcg_diff = ideal_dcg - new_dcg
     lambdas[doc_i] += dcg_diff
     lambdas[doc_j] -= dcg_diff
```

A regression model is then trained to predict those lambdas — turning a listwise problem into a pointwise-looking one. Because the swaps are weighted by the chosen metric, the same trick optimizes **any** metric: swap DCG for Precision@10 and the lambdas change shape (DCG weights the top positions heavily; Precision@10 treats positions 1–10 equally). See [[How LambdaMART Works]].

## Concrete Objectives by Library

How the families surface as configurable objectives in common gradient-boosting LTR libraries:

| Library | Pairwise | Listwise | Pointwise |
|---|---|---|---|
| **[[LightGBM]]** | — | `lambdarank`, `rank_xendcg` | — |
| **[[XGBoost]]** | `rank:pairwise` | `rank:ndcg`, `rank:map` | — |
| **[[CatBoost]]** | `PairLogit`, `PairLogitPairwise` | `YetiRank`, `YetiRankPairwise`, `QuerySoftMax` | `QueryRMSE` |

> Objective names track library versions — confirm against current docs before relying on exact strings.

## Related Concepts
- [[Learning to Rank]]
- [[LambdaMART]] · [[RankNet]]
- [[NDCG]]
- [[Pointwise Relevance Evaluation]] · [[Pairwise Relevance Evaluation]] · [[Listwise Relevance Evaluation]]

## Related Tools
- [[LightGBM]] · [[XGBoost]] · [[CatBoost]] · [[Metarank]]

## Related Articles
- [[Pointwise vs Pairwise vs Listwise Learning to Rank]] — the family taxonomy
- [[Learning to Rank - A Complete Guide to Ranking using Machine Learning]] — full objective landscape through [[LambdaLoss]]
- [[LambdaMART Explained - The Workhorse of Learning-to-Rank]] — RankNet → LambdaRank → LambdaMART lineage
- [[How LambdaMART Works]] — objective-as-business-goal, the lambda trick

## People
- [[Nikhil Dandekar]] · [[Doug Turnbull]]
