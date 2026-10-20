---
type: concept
aliases: ["click residual", "click residuals", "clicks residual", "residual clicks", "CR"]
tags: [concept, metrics, behavioral, evaluation]
related: ["[[Click Signals]]", "[[Zero Results]]", "[[Search Quality Assurance]]", "[[Session-Based Evaluation]]"]
created: 2026-05-16
---

# Clicks Residual

A label-free, query-level success metric: the gap between the clicks a query is expected to get and the clicks it actually gets. A negative residual means people searched but clicked less than expected, which is a sign the query underperforms. Described by [[Walter Underwood]] in 2022, based on his work at [[Netflix]].

---

## Definition

```
expected = attempts × average CTR
residual = actual clicks − expected
```

In Underwood's version the average CTR is taken over all queries. An "attempt" can be a submitted query or a displayed results page, so the metric also works for search-as-you-type.

[[Charlie Hull]]'s toy example has a shop with 45,803 searches and 102,750 clicks (2.243 clicks per search). "vinegar" (320 searches) is expected to get 717 clicks but gets 223, a residual of −494. The misspelled "sosages" (187 searches) comes out at −317.

## Why Not Just Low CTR

Sorting queries by low CTR mostly surfaces the long tail, where fixes don't move overall results. The residual scales with traffic, so sorting by it puts the biggest customer impact first. That includes moderately common queries with very low CTR and very popular queries that underperform by a few points.

## What It Surfaces

- **Vocabulary gaps** — at Netflix, "batman" underperformed because *The Dark Knight* doesn't contain the word; an alias fixed it.
- **Missing catalogue items** — "cj7", a film not yet released in the US, led the metadata team to add an entry.
- **Typo handling and thin product range** — e-commerce examples from Hull.
- **Query clusters** — Hull groups queries to find whole underperforming families: misspellings, animal and football-team queries, and "functional" queries like "returns policy".
- **Non-search causes** — category-like searches that return irrelevant products, or distracting banner ads.

## Making It Sharper

Hull's extensions:
- **Per-category CTR** instead of one site-wide average, since click behaviour varies by intent (kitchen appliances vs. cleaning supplies).
- **Prioritisation data**: query volume, business value by subject area, average order value, and exit rate. Negative CR plus a high exit rate is a strong dissatisfaction signal.
- **Diagnosis data**: which pipeline stages fired ([[Spelling Correction|spell correction]], business rules) and relevance metrics like [[NDCG]]. Relevant results can still go unclicked because of price or stock.
- **Workflow**: issue tracker, then a business discussion (stock, UX or algorithm change), then an offline test on a sample of queries, then online monitoring with fresh click data.

## Limitations

- It shows *that* a query underperforms, not *why*.
- A single site-wide CTR baseline is crude, because query types differ in natural click rates.
- Low-volume problems may not be worth the cost of fixing.
- Low clicks can come from outside search, such as price, stock, banners or irrelevant category results.

## Related Concepts
- [[Click Signals]] — the behavioural data the metric is built from
- [[Zero Results]] — the extreme case: nothing to click at all
- [[Session-Based Evaluation]] — session-level complement to per-query metrics
- [[NDCG]] — judgement-based relevance metric to pair with residuals when diagnosing

## Related Articles
- [[Click Residual - A Query Success Metric]] — Underwood's original definition
- [[Click Residuals - A Clever Way to Find Underperforming Queries]] — Hull's e-commerce practice and extensions

## People
- [[Walter Underwood]] · [[Charlie Hull]]

## Topics
- [[Search Quality Assurance]] · [[Search Observability]]
