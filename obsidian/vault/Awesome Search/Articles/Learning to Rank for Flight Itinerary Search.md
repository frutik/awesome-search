---
title: "Learning to Rank for Flight Itinerary Search"
tags:
  - clippings
  - search
  - ranking
  - case-study
source: "https://hackernoon.com/learning-to-rank-for-flight-itinerary-search-8594761eb867"
author: "Neal Lathia"
created: 2026-05-15
concepts:
  - Learning to Rank
  - Search Evaluation
---

# Learning to Rank for Flight Itinerary Search

**Source:** https://hackernoon.com/learning-to-rank-for-flight-itinerary-search-8594761eb867
**Author:** [[Neal Lathia]] (Senior Data Scientist, Skyscanner London)

## Summary

Case study of applying [[Learning to Rank]] to flight search at Skyscanner. Demonstrates the full LTR workflow from feature engineering through offline evaluation to A/B testing.

## Problem

Traditional flight search sorts by price. LTR objective: rank flights by predicted relevance to the user's actual booking intent, surfacing better matches above the standard list.

## Technical Approach

**Model**: Logistic regression (initial experiments)
**Features**: User search history, behavioral signals, flight attributes — joined, transformed, and reshaped into structured training data
**Labels**: Binary relevance = purchase completion (not just clicks)

## Evaluation

- **Offline metrics**: Mean Average Precision (MAP), [[MRR]] (Mean Reciprocal Rank)
- **Online**: A/B test comparing ML vs. rule-based vs. control

## Results

ML ranking model drove **more purchases** into the recommendation widget than the rule-based variant. No significant difference in search effort (filtering/re-sorting frequency).

## Lessons

1. Purchase completion is a better relevance signal than clicks — aligns model to business objective
2. Offline metrics (MAP/MRR) predicted online conversion improvement
3. LTR outperforms rule-based ranking even with a simple logistic regression model

## Related Concepts

- [[Learning to Rank]]
- [[MRR]]
- [[Search Evaluation]]
- [[Click Signals]]

## Related Articles

- [[How LambdaMART Works]]
- [[Machine Learning-Powered Search Ranking of Airbnb Experiences]]
