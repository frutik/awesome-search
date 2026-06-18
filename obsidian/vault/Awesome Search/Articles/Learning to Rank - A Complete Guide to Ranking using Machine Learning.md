---
title: "Learning to Rank: A Complete Guide to Ranking using Machine Learning"
type: article
tags:
  - clippings
  - search
  - ranking
  - learning-to-rank
source: "https://towardsdatascience.com/learning-to-rank-a-complete-guide-to-ranking-using-machine-learning-4c9688d370d4/"
author: "Francesco Casalegno"
published: 2022-02-28
created: 2026-06-16
concepts:
  - Learning to Rank
  - Ranking Objectives
  - NDCG
  - MAP
---

# Learning to Rank: A Complete Guide to Ranking using Machine Learning

**Source:** https://towardsdatascience.com/learning-to-rank-a-complete-guide-to-ranking-using-machine-learning-4c9688d370d4/
**Author:** [[Francesco Casalegno]]

## Summary

A comprehensive reference on [[Learning to Rank]]: where ranking arises (search, recommenders, travel), the scoring-function framing `s = f(q, d)`, the evaluation metrics, and a thorough tour of the three [[Ranking Objectives|objective families]] up to the **LambdaLoss** generalization.

## Scoring Function

A ranking model predicts a relevance score `s = f(x)` for each input `x = (q, d)` (query, document), then sorts by score. Scoring can be a vector-space model (TF-IDF / [[BERT]] cosine similarity) or a learned LTR model trained by minimizing a ranking loss.

## Evaluation Metrics
- **[[MAP]] (Mean Average Precision)** — for binary relevance; area under the precision–recall curve, averaged over queries.
- **DCG / [[NDCG]]** — for graded relevance; gain `2^y − 1` discounted by `1/log(k+1)`, normalized by the ideal ordering (IDCG).

Both reward putting highly relevant documents near the top, and both are non-differentiable — the central difficulty of LTR.

## The Three Objective Families
- **Pointwise** — sum of per-document losses; regress predicted score to ground truth (e.g. Subset Ranking, MSE loss).
- **Pairwise** — loss over document pairs; binary classification of `y_i > y_j` (e.g. [[RankNet]], BCE loss). Works with relative preference, useful when only partial signals (clicks) are available.
- **Listwise** — loss over the whole list, directly incorporating ranking metrics.

## The Listwise Landscape
- **LambdaRank / [[LambdaMART]]** — define gradients of an *implicit* loss, re-weighting pairs by metric impact; sit *between* pairwise and listwise.
- **SoftRank** — smooth the metric by predicting a probabilistic score `s ~ N(f(x), σ²)`, then optimize expected NDCG (SoftNDCG).
- **ListNet** — define a probability over permutations via the Plackett–Luce model; loss is cross-entropy between true and predicted permutation distributions.
- **[[LambdaLoss]]** — a generalized mixture-model framework where the ranked list π is a hidden variable. Proves that RankNet, LambdaRank, SoftRank, ListNet are *special cases*, and enables metric-driven losses with state-of-the-art accuracy.

## Why It Matters

The most complete single-article map of how ranking losses relate, ending at LambdaLoss as the unifying framework. Directly expands [[Ranking Objectives]] beyond the basic three families.

## Related Concepts
- [[Learning to Rank]]
- [[Ranking Objectives]]
- [[RankNet]] · [[LambdaMART]] · [[LambdaLoss]]
- [[NDCG]] · [[MAP]]
- [[Pointwise Relevance Evaluation]] · [[Pairwise Relevance Evaluation]] · [[Listwise Relevance Evaluation]]

## Related Articles
- [[Pointwise vs Pairwise vs Listwise Learning to Rank]] — the family taxonomy
- [[LambdaMART Explained - The Workhorse of Learning-to-Rank]] — the GBDT workhorse
- [[How LambdaMART Works]] — hands-on lambda computation

## People
- [[Francesco Casalegno]] — author
