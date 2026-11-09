---
type: article
title: Why nDCG Misleads eCommerce Search
source: https://www.linkedin.com/feed/update/urn:li:activity:7524176206091735040/
author:
  - "[[Andreas Wagner]]"
published: 2026-11-05
created: 2026-11-09
concepts:
  - "[[NDCG]]"
  - "[[Position Bias]]"
  - "[[Presentation Bias]]"
  - "[[Click Models]]"
topics:
  - "[[Search Quality Assurance]]"
  - "[[E-commerce Search]]"
companies:
  - "[[searchHub]]"
tags:
  - article
  - linkedin
  - search-evaluation
  - metrics
  - e-commerce
---

# Why nDCG Misleads eCommerce Search

**Sources**: two consecutive LinkedIn posts —
[part 1](https://www.linkedin.com/feed/update/urn:li:activity:7524176206091735040/) (2026-11-05) and
[part 2](https://www.linkedin.com/feed/update/urn:li:activity:7525476642685644800/) (2026-11-09)
**Author**: [[Andreas Wagner]] ([[searchHub]])

## Summary

A two-post argument from [[Andreas Wagner]], drawing on about 20 years in eCommerce information retrieval, that [[NDCG]] should not be the default metric to optimize for product search. Its popularity in benchmarks, papers and blogs is not evidence that it fits the job. The first post raises two questions every team should answer before adopting it; the second takes one of them — the position discount — and shows why it breaks on real result layouts.

## Question 1: Does the discount match your users?

nDCG is a list-ranking metric with a steep, position-based discount. Wagner says he has rarely seen that discount match how users actually interact with results. If a team uses nDCG anyway, the discount should be derived from measured attention and interaction across positions in their own application, not taken as given — the same move [[Click Models]] make when they estimate examination probability from logs.

**The cutoff matters too.** Optimizing nDCG@5 or nDCG@10 implicitly declares everything below the cutoff irrelevant, while shoppers browse, scroll and compare far more products than that. A higher k such as @50 or @100 covers more of the ranking and lowers the risk of tuning only the first few slots — but it does not fix the discount itself.

## Question 2: Does it track the business?

How strongly does a list-based ranking metric correlate with business KPIs? For pure-text results, nDCG may map to business value fairly directly. Real product results carry images, prices, brands and promotions, so click and purchase likelihood depend on much more than a relevance label and a position. Optimizing a classic IR metric does not automatically optimize the shop. Wagner's closing line: optimize what matters, not what is easy to measure.

## Part 2: Grids, devices and viewports

The follow-up post sharpens the discount critique. nDCG applies the same logarithmic discount on desktop, tablet and phone, but shoppers do not see a ranked list — they see a visual product grid:

- On desktop the first four products may be visible at once and get nearly the same exposure.
- On mobile only one or two products may be on screen without scrolling.
- nDCG's discount drops sharply between positions 1 and 2, even where those two slots are equally visible.

Wagner illustrates this with sampled production data and argues that real examination probability falls in steps at **grid-row and viewport boundaries**, which a smooth log curve cannot represent. The recommendation: evaluate with metrics grounded in observed behaviour per device and layout rather than an assumed mathematical discount. This is [[Position Bias]] and [[Presentation Bias]] turned back on the metric itself — the layout that biases clicks also invalidates the metric's model of attention.

## Discussion

In the comments on part 1, one practitioner described an eCommerce search team that used conversion rate and no-results rate as primary metrics (later switching the A/B goal to basket-value uplift) and never made nDCG a main metric. [[Andrew Kornilov]] countered that teams reach for nDCG not because of papers but because there is no clear, implementable alternative, and a team still needs something measurable.

## Related

- [[NDCG]] · [[NDCG-f]] · [[NDCG-m]] · [[UDCG]] — the metric and its variants
- [[Flavors of NDCG]] · [[Demystifying nDCG and ERR]] · [[Choosing Your Search Relevance Evaluation Metric]]
- [[How we Compute NDCG in Daraz E-Commerce]] — an eCommerce team that does use nDCG
- [[Evaluating the Best AB Testing Metrics for Search]] — the business-KPI side of the argument
- [[Common Pitfalls of Onsite Search Experimentation]] · [[Towards Scalable Relevance Engineering]] — Wagner's other evaluation writing
