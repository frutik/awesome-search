---
type: company
category: end-user
industry: [travel, flight search, meta-search]
products: [Skyscanner flight search, hotel search, car hire]
search_domain: flight itinerary ranking and recommendation
people: ["[[Neal Lathia]]"]
use_cases: ["[[Skyscanner - LTR for Flight Search]]"]
tags: [company, end-user, travel, learning-to-rank]
created: 2026-05-16
---

# Skyscanner

Global travel meta-search engine. Search challenge: ranking flight itineraries by predicted relevance to booking intent, not just by price.

## Search Context

Traditional flight search sorts by price. Skyscanner applied Learning to Rank to surface flights that better match user booking intent — shifting from a commodity sort to a relevance-ranked experience.

## Key Engineering Work

- **LTR model**: logistic regression on user search history, behavioral signals, flight attributes
- **Training labels**: purchase completion (not just clicks) — aligns model to business objective
- **Offline evaluation**: MAP and MRR predicted online conversion improvement
- **Result**: ML ranking drove more purchases into the recommendation widget vs. rule-based variant

## Key Lesson

Purchase completion is a better relevance signal than clicks. An LTR model optimized for booking outperforms rule-based flight ranking even with a relatively simple logistic regression model.

## Articles

- [[Learning to Rank for Flight Itinerary Search]] — full LTR workflow, feature engineering, A/B results

## Related Concepts

- [[Learning to Rank]] · [[MRR]] · [[MAP]] · [[Search Evaluation]] · [[Click Signals]]
