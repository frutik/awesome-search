---
title: "Building a Large-Scale Recommendation System: People You May Know"
type: article
tags:
  - clippings
  - search
  - ranking
  - recommendations
  - multi-stage-ranking
source: "https://www.linkedin.com/blog/engineering/recommendations/building-a-large-scale-recommendation-system-people-you-may-know"
author: "LinkedIn Engineering"
published: 2024-02-06
created: 2026-06-11
concepts:
  - Retrieval Pipeline
  - Learning to Rank
companies:
  - LinkedIn
---

# Building a Large-Scale Recommendation System: People You May Know

**Source:** https://www.linkedin.com/blog/engineering/recommendations/building-a-large-scale-recommendation-system-people-you-may-know
**Company:** [[LinkedIn]]

## Summary

How [[LinkedIn]] scaled its **People You May Know (PYMK)** recommender to score >1 billion candidates per member while keeping relevance high and latency low. The design is a textbook **[[Multi-Stage Ranking]]** funnel: each stage narrows the candidate set for the next, optimizing a different objective with a different speed/quality trade-off.

## The Four Stages

### L0 — Candidate Generation
Selects a few thousand candidates from billions. Goal is **recall, not order** — ensure relevant candidates survive. Metric: **Recall@k** (k ≈ 3,000–5,000). Multiple candidate-generation sources: graph-based (random walks, n-hop neighbors), embedding-based retrieval (EBR), and heuristics (e.g. new members nearby).

### L1 — Light Ranker
Takes the few thousand candidates, **calibrates** the diverse CG sources onto a common objective, and reduces to a few hundred. Lightweight model (logistic regression or [[XGBoost]]). Calibration matters because L0 mixes graph- and similarity-based candidates that aren't directly comparable. Metric: Recall@k (k ≈ 500–800).

### L2 — Rich Ranker
Heavy deep neural networks predicting probability **and value** of distinct engagement events (invitation sent, invitation accepted). Consumes the most powerful member–candidate pair features. Metrics: AUC, **Precision@k**, and ECE (expected calibration error) — scores are reused downstream, so calibration is tracked.

### Re-Ranker
Final stage of fairness re-rankers (protected attributes), diversity re-rankers, and anti-overrepresentation logic. Multiple L2 engagement-event models are **linearly combined**, with the combination weights estimated via **Bayesian optimization** — a multi-objective tuning problem.

## Why Offline ≠ Online

Each stage has offline metrics (Recall@k, AUC/Precision@k, log-likelihood/diversity), but the team trusts **A/B tests** for system-level judgment. Offline rarely matches online due to presentation/[[Position Bias|position bias]], deployment errors, and train/serve distribution skew.

## Why It Matters

A concrete production instance of the multi-stage pattern where the **ranking objective changes per stage** — recall first, then calibrated relevance, then engagement value, then fairness/diversity — illustrating that "the ranking objective" is rarely singular in real systems. See [[Ranking Objectives]] and [[Retrieval Pipeline]].

## Related Concepts
- [[Multi-Stage Ranking]]
- [[Retrieval Pipeline]]
- [[Reranking]]
- [[Learning to Rank]]
- [[Ranking Objectives]]
- [[Precision and Recall]]
- [[Position Bias]]

## Related Articles
- [[Machine Learning-Powered Search Ranking of Airbnb Experiences]] — staged ranking with personalization
- [[Optimizing Search at Uber Eats]] — multi-stage retrieval + ML re-ranking

## Companies
- [[LinkedIn]]
