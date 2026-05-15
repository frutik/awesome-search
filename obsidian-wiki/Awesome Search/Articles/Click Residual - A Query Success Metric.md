---
title: "Click Residual: A Query Success Metric"
aliases: ["Click Residual", "Underwood Click Residual"]
tags:
  - clippings
  - search
  - evaluation
  - metrics
source: "https://medium.com/towards-data-science/click-residual-a-query-success-metric"
author: "Ted Underwood"
created: 2026-05-15
concepts:
  - Search Evaluation
  - Click Signals
  - Position Bias
---

# Click Residual: A Query Success Metric

**Source:** https://medium.com/towards-data-science/click-residual-a-query-success-metric
**Author:** Ted Underwood

## Summary

**Click Residual** is a metric that surfaces queries where actual clicks deviate significantly from expected clicks — revealing both underperforming high-traffic queries and overperforming long-tail queries.

### The Core Problem with Raw CTR
Raw click-through rate conflates two things:
- The quality of the result set (relevance)
- The attractiveness of the query type (navigational queries always get high CTR; exploratory queries always get low CTR)

You can't compare CTR across query types to judge relevance quality.

### Click Residual Formula
```
residual(q) = actual_clicks(q) - expected_clicks(q)
expected_clicks(q) = attention(q) × avg_ctr_at_position
```

Where `attention` is the estimated number of impressions × position discount factor. More precisely:

```
residual(q) = clk(q) - (att(q) × avg_ctr)
```

- **Positive residual**: query gets more clicks than expected → performing well
- **Negative residual**: query gets fewer clicks than expected → underperforming

### Why This Is Useful
Click residual controls for position bias and query frequency, revealing:
1. **High-traffic underperformers**: popular queries getting low clicks relative to expected → high-priority fix targets
2. **Low-traffic overperformers**: niche queries with surprisingly high engagement → understand why and replicate
3. **Neutral**: queries performing as expected → no action needed

### Practical Example
Suppose "running shoes" gets 100K impressions and 5K clicks (5% CTR), but similar navigational queries average 12% CTR. Click residual = 5000 - (100000 × 0.12) = -7000. This query is severely underperforming despite high traffic.

### Comparison to Other Metrics
- **CTR**: ignores position and query type → misleading for cross-query comparison
- **NDCG**: requires relevance labels → expensive to compute at scale
- **Click Residual**: label-free, scalable, controls for confounders

### Limitations
- Assumes avg_ctr is a good expected-click proxy (may need stratification by query type)
- Position bias correction depends on accurate position discount model
- Doesn't tell you *why* a query underperforms

## Key Concepts
- **Click Residual** — actual minus expected clicks, controlling for position and traffic
- **Expected clicks** — attention × average CTR baseline
- **Positive/negative residual** — over/underperformance signals
- **Position bias correction** — expected clicks account for rank-based attention

## Related Concepts
- [[Search Evaluation]]
- [[Click Signals]]
- [[Position Bias]]
- [[A-B Testing for Search]]
- [[NDCG]]

## Related Articles
- [[Measuring Searcher Behavior]]
- [[Evaluating Good Search - Measure It]]
- [[When There's No Conversion Rate]]

## People
- [[Daniel Tunkelang]]
