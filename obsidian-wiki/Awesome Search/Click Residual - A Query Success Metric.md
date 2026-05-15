---
title: "Click Residual: A Query Success Metric"
source: "https://observer.wunderwood.org/2022/08/08/click-residual-a-query-success-metric/"
author:
  - "[[Walter Underwood]]"
published: 2022-08-08
created: 2026-05-15
description: "Click residual identifies underperforming queries by comparing actual clicks against expected (baseline CTR × attempts) — more actionable than low-CTR analysis alone."
tags:
  - clippings
---
# Click Residual: A Query Success Metric

Low CTR analysis surfaces long-tail queries with minimal traffic impact. Click residual combines traffic volume with performance degradation to find queries worth fixing.

## Calculation

```
exp = attempts × system_avg_CTR    # expected clicks
res = actual_clicks − exp           # residual
```

Sort by residual ascending → queries with the biggest negative gap (expected more clicks than received).

## Real-world examples (Netflix)

- **"Batman"** had poor performance because *The Dark Knight* lacked that keyword → added an alias
- **"CJ7"** showed demand for unreleased content → engaged metadata team

## Note

For character-by-character search, "attempts" includes sequential refinements like "b", "ba", "bat", "batm" — treat these as a session, not separate queries.


## Related Concepts

- [[Click Signals]]
- [[Search Evaluation]]
- [[Session-Based Evaluation]]

## People

- [[Walter Underwood]]
