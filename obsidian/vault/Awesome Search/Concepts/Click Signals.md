---
title: "Click Signals"
aliases: ["click-through rate", "CTR", "click residual", "behavioral signals", "click data", "implicit feedback"]
tags:
  - concept
  - search-evaluation
  - behavioral
  - online-metrics
---

# Click Signals

## Definition

Click signals are behavioral data collected from user interactions with search results — clicks, dwell time, reformulations, and conversions. They provide implicit relevance feedback at scale without requiring human annotation.

## Types of Click Signals

### Click-Through Rate (CTR)
Fraction of queries where a user clicked at least one result.
```
CTR = clicks / impressions
```

Useful for: measuring engagement; comparing systems in A/B tests.
Limitation: CTR depends heavily on result presentation (position bias).

### Dwell Time
How long a user spent on a clicked result before returning.
- Long dwell (>30s): positive signal — user found what they needed
- Short dwell (<5s): negative signal — "pogo-sticking" back to SERP

### Zero Clicks
User got results but clicked nothing.
Interpretations vary:
- **Negative**: nothing was relevant
- **Positive**: query answered directly in snippet/featured snippet (no click needed)

Context matters: a zero-click rate for navigational queries is different from informational queries.

### Click Residual

A sophisticated metric: how many "expected" clicks didn't happen?

**Concept**: Given a result set of a certain relevance profile, predict how many clicks should occur. The gap between expected and actual clicks = "residual."

```
Click Residual = Expected Clicks - Actual Clicks
```

Positive residual: fewer clicks than expected → results are less relevant than they appear.  
Negative residual: more clicks than expected → results are surprisingly engaging.

### Position Bias
Users click higher-ranked results more regardless of quality. Must be corrected for when using click signals as relevance proxies:
- **Inverse propensity scoring (IPS)**: weight clicks by inverse probability of being shown at that position
- **Counterfactual evaluation**: compare clicks under different presentation orderings

## Click Data in LTR (Learning to Rank)

Click data is the primary training signal for [[Learning to Rank]] models:
1. Collect (query, result, click/no-click) data from production
2. Apply position debiasing
3. Use as implicit relevance labels for LTR training

**Key challenge**: Clicks are biased toward currently-ranked positions. A result at rank 10 gets few clicks even if it's the best answer — its click rate doesn't reflect true relevance.

## Click Signals vs. [[Judgment Lists]]

| Aspect | Click Signals | Human Judgments |
|--------|-------------|----------------|
| Scale | Millions/day | Hundreds/day |
| Cost | Free (already collected) | Expensive |
| Bias | Position bias, novelty bias | Annotation bias |
| Quality | Noisy | High (if guidelines good) |
| Freshness | Real-time | Stale quickly |

## Related Concepts

- [[Search Evaluation]] — click signals as online evaluation
- [[Session-Based Evaluation]] — clicks as session signals
- [[Judgment Lists]] — offline alternative
- [[Implicit Judgments]] — click signals aggregated into relevance labels for LTR
- [[NDCG]] — offline metric complementing click signals
- [[Diversity Metrics]] — click diversity as diversity signal

## People

- [[Daniel Tunkelang]] — measuring searcher behavior; click signals in search evaluation
- [[James Rubinstein]] — "Measuring Search" — behavioral metrics
- [[Doug Turnbull]] — click residual metric
