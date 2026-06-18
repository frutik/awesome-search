---
title: "Pointwise vs. Pairwise vs. Listwise Learning to Rank"
type: article
tags:
  - clippings
  - search
  - ranking
  - learning-to-rank
source: "https://medium.com/@nikhilbd/pointwise-vs-pairwise-vs-listwise-learning-to-rank-80a8fe8fadfd"
author: "Nikhil Dandekar"
published: 2016-09-29
created: 2026-06-16
concepts:
  - Ranking Objectives
  - Learning to Rank
topics:
  - Ranking
---

# Pointwise vs. Pairwise vs. Listwise Learning to Rank

**Source:** https://medium.com/@nikhilbd/pointwise-vs-pairwise-vs-listwise-learning-to-rank-80a8fe8fadfd
**Author:** [[Nikhil Dandekar]]

## Summary

A concise taxonomy of the three families of [[Learning to Rank]] approaches, distinguished by **how many documents the loss function considers at once**. This is the canonical framing for [[Ranking Objectives]].

## The Three Families

### Pointwise
Looks at a **single document** at a time. Trains a standard regressor/classifier to predict a relevance score per document; the final ranking is produced by sorting on those scores. Each document's score is independent of the others in the result list. Any standard regression/classification algorithm applies directly.

### Pairwise
Looks at a **pair of documents** at a time. The model learns the optimal ordering for each pair and is penalized for **inversions** (pairs ordered wrongly relative to ground truth). Pairwise works better in practice than pointwise because predicting *relative order* is closer to the nature of ranking than predicting an absolute label. [[RankNet]], LambdaRank and [[LambdaMART]] are pairwise approaches.

### Listwise
Looks at the **entire list** and optimizes its ordering directly. Two sub-techniques:
1. **Direct optimization of IR measures** such as [[NDCG]] — e.g. SoftRank, AdaRank.
2. **Custom listwise loss** capturing properties of the target ranking — e.g. ListNet, ListMLE.

Listwise approaches can get considerably more complex than pointwise or pairwise.

## Why It Matters

The choice of family is the choice of **ranking objective** — what the model is actually told to optimize. Predicting relative order (pairwise) or list quality (listwise) aligns the training signal with how ranking quality is measured, which is why the pairwise/listwise lineage (RankNet → LambdaRank → LambdaMART) dominates production LTR.

## Related Concepts
- [[Ranking Objectives]]
- [[Learning to Rank]]
- [[RankNet]]
- [[LambdaMART]]
- [[NDCG]]
- [[Pointwise Relevance Evaluation]]
- [[Pairwise Relevance Evaluation]]
- [[Listwise Relevance Evaluation]]

## Related Articles
- [[How LambdaMART Works]] — the pairwise-swap trick that approximates a listwise metric

## Primary Sources (from the article's footnotes)
- [From RankNet to LambdaRank to LambdaMART: An Overview](https://www.microsoft.com/en-us/research/publication/from-ranknet-to-lambdarank-to-lambdamart-an-overview/) — Burges, Microsoft Research (the definitive lineage overview)
- [SoftRank: Optimising Non-Smooth Rank Metrics](https://www.microsoft.com/en-us/research/publication/softrank-optimising-non-smooth-rank-metrics/) — listwise, metric smoothing
- [AdaRank on LETOR](http://research.microsoft.com/en-us/um/beijing/projects/letor/Baselines/AdaRank.html) — boosting for IR measures
- [Learning to Rank: From Pairwise Approach to Listwise Approach (ListNet)](https://www.microsoft.com/en-us/research/publication/learning-to-rank-from-pairwise-approach-to-listwise-approach/)
- [Position-Aware ListMLE: A Sequential Learning Process for Ranking](http://auai.org/uai2014/proceedings/individuals/164.pdf)
- Tutorials: [Learning to Rank for IR (WWW2009)](http://www2009.org/pdf/T7A-LEARNING%20TO%20RANK%20TUTORIAL.pdf) · [A Short Introduction to Learning to Rank](http://times.cs.uiuc.edu/course/598f14/l2r.pdf)

## People
- [[Nikhil Dandekar]] — author
