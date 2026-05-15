---
title: "How to Succeed with Explicit Relevance Evaluation using PPS Sampling"
source: "https://opensourceconnections.com/blog/2022/10/13/how-to-succeed-with-explicit-relevance-evaluation-using-probability-proportional-to-size-sampling/"
author: ["OpenSource Connections"]
tags:
  - clippings
  - search-evaluation
  - sampling
  - judgment-lists
concepts:
  - Judgment Lists
  - Search Evaluation
  - Query Types
created: 2026-05-15
---

# How to Succeed with Explicit Relevance Evaluation using PPS Sampling

**Source**: https://opensourceconnections.com/blog/2022/10/13/how-to-succeed-with-explicit-relevance-evaluation-using-probability-proportional-to-size-sampling/  
**Publisher**: OpenSource Connections

## Summary

Explains Probability-Proportional-to-Size (PPS) sampling as a strategy for building representative [[Judgment Lists]] — sampling queries in proportion to their traffic volume to ensure evaluation reflects the real impact of system changes.

## Why Sampling Strategy Matters

When building judgment lists, you must choose which queries to judge. The choice dramatically affects what your evaluation measures.

### The Head Query Trap
If you sample uniformly from all unique queries:
- 80% of queries appear once ("tail" queries)
- 1% of queries account for 50%+ of traffic ("head" queries)
- Your evaluation overweights rare queries that affect few users

A metric improvement on tail queries may mean nothing for business outcomes.

## Three Sampling Strategies

### Random Sampling
Every unique query has equal probability of selection.
- **Pro**: Simple, fair to all queries
- **Con**: Overrepresents tail queries; underrepresents head queries
- **Use when**: You care about all queries equally (e.g., edge case coverage)

### Stratified Sampling
Sample a fixed number from each stratum (query frequency bucket):
- Stratum 1: High-frequency (>1000 searches/month)
- Stratum 2: Medium-frequency (100–1000)
- Stratum 3: Low-frequency (<100)

- **Pro**: Guaranteed coverage of each tier
- **Con**: Arbitrary stratum boundaries; requires knowing bucket sizes
- **Use when**: You want explicit control over head/torso/tail representation

### PPS (Probability-Proportional-to-Size) Sampling
Each query's probability of selection = its traffic share.

```python
import numpy as np

# query_counts: dict of {query: count}
total_queries = sum(query_counts.values())
queries = list(query_counts.keys())
probabilities = [count / total_queries for count in query_counts.values()]

sampled_queries = np.random.choice(
    queries, 
    size=1000, 
    replace=False, 
    p=probabilities
)
```

- **Pro**: Selection probability reflects business impact
- **Con**: May under-represent important edge cases
- **Use when**: You want evaluation to predict business metric impact

## PPS for Evaluation Validity

PPS sampling produces evaluation sets where:
- A system improvement of X% on the evaluation = X% improvement on real traffic
- High-traffic queries receive proportional weight
- Statistical tests reflect actual user impact

Without PPS: a system might optimize rare queries while degrading common ones — metric says "improved", business impact says "worsened".

## Recommended Hybrid Approach

Combine PPS with stratified for comprehensive evaluation:

1. **Core set** (PPS): 500 queries proportional to traffic — business impact measurement
2. **Stress set** (adversarial/tail): 100 queries from known failure modes — regression detection
3. **New feature set**: 50 queries specifically targeting the new functionality being shipped

## Related Articles

- [[What Is a Judgment List]] — judgment list creation
- [[Measuring Search Effectiveness]] — how sampled judgments feed into evaluation

## Related Concepts

- [[Judgment Lists]] — what sampling feeds into
- [[Search Evaluation]] — context
- [[Query Types]] — stratum definition based on query type
- [[NDCG]] — metric computed over sampled queries
