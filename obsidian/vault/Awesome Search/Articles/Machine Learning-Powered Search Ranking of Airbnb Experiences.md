---
title: "Machine Learning-Powered Search Ranking of Airbnb Experiences"
tags:
  - clippings
  - search
  - ranking
  - case-study
  - medium
source: "https://medium.com/airbnb-engineering/machine-learning-powered-search-ranking-of-airbnb-experiences-110b4b1a0789"
author: "Mihajlo Grbovic, Eric Wu, Pai Liu, Chun How Tan, Liang Wu, Bo Yu, Alex Tian"
created: 2026-05-15
concepts:
  - Learning to Rank
  - Personalization
  - Search Evaluation
---

# Machine Learning-Powered Search Ranking of Airbnb Experiences

**Source:** https://medium.com/airbnb-engineering/machine-learning-powered-search-ranking-of-airbnb-experiences-110b4b1a0789
**Authors:** [[Mihajlo Grbovic]], Eric Wu, Pai Liu, Chun How Tan, Liang Wu, Bo Yu, Alex Tian

## Summary

Case study of how Airbnb iterated through four stages of ML-powered search ranking for Experiences, achieving ~28% cumulative booking improvement.

## Four-Stage Progression

### Stage 1 — Baseline GBDT (+13% bookings)
Gradient Boosted Decision Trees with binary classification on 50,000 labeled examples. Features: duration, price, reviews, booking counts.

### Stage 2 — Personalization (+7.9%)
Added two dimensions:
- Features from booked homes (distance, trip date availability)
- User click history (category intensity/recency, time-of-day preferences)

Offline pre-computation of rankings for 1M+ active users daily.

### Stage 3 — Online Scoring (+5.1%)
Real-time inference with query features: distance to entered location, guest count, browser language, origin-destination preferences. 2M+ training examples, 90 features.

### Stage 4 — Business Rules (+2.2%)
Weighted training data to promote: quality (5-star rebooking 1.5x more), emerging hits (+14%), category diversity (+2.3%).

## Key Features

- **Experience features**: reviews, booking velocity, occupancy, duration, price, category
- **Query features**: distance, guest count, language availability, geographic preferences
- **Personalization**: Category Intensity = weighted sum of user clicks with recency decay

## Evaluation

Offline: AUC and [[NDCG]]; Online: A/B testing for booking rate.

## Related Concepts

- [[Learning to Rank]]
- [[Personalization]]
- [[NDCG]]
- [[A-B Testing for Search]]
- [[Click Signals]]

## Related Articles

- [[Listing Embeddings in Search Ranking]]
- [[How LambdaMART Works]]
