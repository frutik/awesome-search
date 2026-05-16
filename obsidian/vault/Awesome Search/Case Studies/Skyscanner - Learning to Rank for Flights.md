---
type: case-study
company: "[[Skyscanner]]"
articles:
  - "[[Learning to Rank for Flight Itinerary Search]]"
topics:
  - "[[Query Understanding in Practice]]"
  - "[[Relevance Program Setup]]"
concepts:
  - "[[Learning to Rank]]"
  - "[[Search Evaluation]]"
people:
  - "[[Neal Lathia]]"
---

# Skyscanner — Learning to Rank for Flights

Skyscanner is a flight and travel search engine. Traditional flight search sorts results by price. Their LTR project aimed to rank results by predicted booking intent — surfacing the flights users actually buy, not just the cheapest option.

## Key Insight

**Price sort ≠ user intent.** Users who sort by price often scroll past the cheapest flight and book something slightly pricier that better fits their schedule. Purchase completion is a cleaner relevance signal than clicks.

## Technical Approach

**Model**: Logistic regression as initial experiments (deliberately simple — proves the concept before increasing complexity)

**Features**:
- User search history
- Behavioral signals (dwell, clicks, reformulations)
- Flight attributes (price, stops, duration, airline, departure/arrival times)
- Historical booking patterns for route + time segment

**Labels**: Binary relevance = purchase completion. Clicks alone were noisy; completed bookings directly encode user satisfaction.

## Evaluation

**Offline**: Mean Average Precision (MAP) and MRR — computed against held-out booking data.

**Online**: A/B test with three arms:
1. ML ranking model
2. Rule-based ranking (hand-tuned heuristics)
3. Control (price sort)

ML model drove more purchases into the recommendation widget than the rule-based variant. No significant difference in search effort metrics (filtering/re-sorting frequency).

## Lessons

1. **Purchase > click as relevance label** — aligns training objective with the business metric that matters.
2. **Offline MAP predicted online conversion** — in this case, offline metrics were a reliable proxy. (Not always true in search; worth validating.)
3. **Even simple LTR beats rule-based ranking** — logistic regression on good features outperforms hand-tuned rules.
4. **Hold back search effort metrics** — absence of increased filtering/re-sorting confirmed users were satisfied with ML ordering.

## What to Steal

| Pattern | Application |
|---|---|
| Use purchase as relevance label | Any transactional search where clicks are noisy |
| Start with logistic regression | Prove LTR value before tuning model complexity |
| Three-arm A/B (ML vs. rules vs. control) | Isolates ML uplift from feature-engineering uplift |
| Validate offline → online correlation | Calibrate how much to trust offline metrics before shipping |

## Related Case Studies

- [[Airbnb - ML-Powered Experiences Ranking]] — multi-stage ML progression with similar trajectory
- [[Slack - Enterprise Message Search with LTR]] — LTR in a non-e-commerce context
