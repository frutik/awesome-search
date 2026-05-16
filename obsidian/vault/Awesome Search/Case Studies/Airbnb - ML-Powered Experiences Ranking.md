---
type: use-case
company: "[[Airbnb]]"
domain: marketplace / travel
problem: rank Experiences search results to maximize bookings using ML
scale: 1M+ active users, offline pre-computation of rankings daily
concepts:
  - "[[Learning to Rank]]"
  - "[[Personalization]]"
  - "[[A-B Testing for Search]]"
  - "[[Click Signals]]"
sources:
  - "[[Machine Learning-Powered Search Ranking of Airbnb Experiences]]"
  - "[[Listing Embeddings in Search Ranking]]"
people: []
---

# Airbnb — ML-Powered Experiences Ranking

## Problem

Experiences (tours, classes, activities hosted by locals) launched with heuristic ranking. The team needed to rank results by likelihood of booking — accounting for the specific guest's preferences, trip context, and experience quality signals — not just static popularity.

## Four-Stage Progression

Each stage built on the previous and was measured separately via A/B test.

### Stage 1 — Baseline GBDT (+13% bookings)
Gradient Boosted Decision Trees, binary classification (booked/not). 50,000 labeled examples. Features: duration, price, review count, booking velocity, occupancy.

### Stage 2 — Personalization (+7.9%)
Two new dimensions:
- **Context from booked homes**: trip dates, distance from accommodation to experience
- **User click history**: Category Intensity = weighted sum of clicks with recency decay; time-of-day preferences

Offline pre-computation: rankings pre-computed for 1M+ active users daily to keep latency manageable.

### Stage 3 — Online Scoring (+5.1%)
Switched to real-time inference to include query-time features unavailable offline:
- Distance to entered location
- Guest count
- Browser language
- Origin-destination travel patterns

2M+ training examples, 90 features total.

### Stage 4 — Business Rules (+2.2%)
Up-weighted training examples to promote business goals:
- Quality: 5-star rebooking experiences weighted 1.5x
- Emerging hits: new experiences with rapid booking velocity +14% boost
- Category diversity: penalize showing all experiences in same category +2.3%

**Cumulative total: ~28% booking improvement** across all four stages.

## Key Lessons

- Incremental ML adoption works: each stage had clear scope, clear metric, and was independently validated
- Personalization requires deliberately designed features — generic click signals need domain transformation (Category Intensity, not raw clicks)
- Offline pre-computation is a practical first step for personalization; accept staleness in exchange for latency
- Business rules embedded in training data weighting are more robust than score overrides — they generalize across queries rather than requiring per-query configuration
- Diversity must be explicitly rewarded, not assumed to emerge from relevance signals

## What to Steal

- Category Intensity feature formula: weighted click sum with recency decay — applicable to any personalized ranking
- Stage gating pattern: validate each ML addition independently before adding the next layer
- Business rule via training data weighting, not post-hoc score adjustments
