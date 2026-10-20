---
type: article
title: "Click Residual: A Query Success Metric"
aliases: ["Click Residual", "Underwood Click Residual"]
tags:
  - search
  - evaluation
  - metrics
  - blog
source: "https://observer.wunderwood.org/2022/08/08/click-residual-a-query-success-metric/"
author:
  - "[[Walter Underwood]]"
published: 2022-08-08
created: 2026-05-15
description: "Walter Underwood's definition of click residual — actual clicks minus expected clicks (query attempts × site-wide CTR) — a metric he developed at Netflix for ranking queries by how much their underperformance hurts customers."
concepts:
  - Clicks Residual
  - Click Signals
  - Search Evaluation
topics:
  - Search Observability
  - Search Quality Assurance
---

# Click Residual: A Query Success Metric

[[Walter Underwood]] defines **[[Clicks Residual|click residual]]** on his blog *Most Casual Observer*: the difference between the number of clicks a query should get and the number it actually gets. He developed the metric at [[Netflix]].

---

## Definition

```
exp = att × ctr
res = clk − exp
```

- `att` — query attempts. An attempt can be a submitted query or a displayed results page, so the metric also works for character-by-character (search-as-you-type) search.
- `ctr` — the average click-through rate across all queries
- `clk` — actual clicks for the query

A negative residual marks a query where people searched but didn't click much. The post first printed the second formula with the sign reversed; Underwood fixed it after a reader pointed it out.

## Why Not Just Low CTR

Ranking queries by low CTR mostly surfaces long-tail queries, where fixes barely move overall results. Sorting by residual puts the biggest customer impact first. That covers both moderately common queries with very low CTR and very popular queries that underperform by only a few points.

## Netflix Examples

- **"batman"** was the top underperformer one week. *The Dark Knight* doesn't contain the word "batman"; adding an alias fixed the query after the next indexing run.
- **"cj7"** came from fans looking for a Stephen Chow film not yet released in the US. The movie metadata team added an entry so subscribers could follow its availability.

---

## Related Concepts
- [[Clicks Residual]]
- [[Click Signals]]
- [[Search Evaluation]]

## Related Articles
- [[Click Residuals - A Clever Way to Find Underperforming Queries]] — [[Charlie Hull]]'s practitioner extension: per-category CTR, exit rate, business prioritisation

## People
- [[Walter Underwood]] — author
