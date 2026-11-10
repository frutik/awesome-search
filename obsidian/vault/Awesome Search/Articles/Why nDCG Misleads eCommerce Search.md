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
  - "[[Learning to Rank]]"
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

**Sources**: three consecutive LinkedIn posts —
[part 1](https://www.linkedin.com/feed/update/urn:li:activity:7524176206091735040/) (2026-11-05),
[part 2](https://www.linkedin.com/feed/update/urn:li:activity:7525476642685644800/) (2026-11-09) and
[part 3](https://www.linkedin.com/feed/update/urn:li:activity:7525863175238615042/) (2026-11-10)
**Author**: [[Andreas Wagner]] ([[searchHub]])

## Summary

A three-post argument from [[Andreas Wagner]], drawing on about 20 years in eCommerce information retrieval, that [[NDCG]] should not be the default metric to optimize for product search. Its popularity in benchmarks, papers and blogs is not evidence that it fits the job. The first post raises two questions every team should answer before adopting it; the second takes one of them — the position discount — and shows why it breaks on real result layouts; the third questions the deeper assumption that a product's value is its own, independent of the products around it.

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

## Part 3: Products are not valued in isolation

The third post, from a series titled *How to NOT Fail in eCommerce Search*, opens with the line **stop assuming that products only contribute value when they get purchased**. While working on [[Learning to Rank]] from implicit customer feedback versus relevance-engineer feedback in 2019, Wagner noticed products with lots of clicks and almost no sales — high CTR, low CVR, little direct commercial value, which traditional ranking approaches might classify as poor performers. Yet products displayed next to these highly clicked items appeared more likely to be purchased.

His example is the latest iPhone: almost everyone wants one but not everyone can afford it, so shoppers click it without buying, and the more affordable smartphones beside it start to look more appealing. Marketing and behavioural economics describe related phenomena as attention spillovers, halo effects and decoy effects.

This exposes a limitation of conventional learning-to-rank. Most ranking objectives treat relevance as an individual property: each product gets a score, and its position decides how much that score contributes to the metric. In eCommerce a product's value may depend on its neighbours — some products convert, some attract attention, inspire exploration or make neighbouring products more appealing, and some do both. The post's illustration shows two "women shoes" grids with the same expert rating (5) that differ in a single slot, one of them marked −8% GMV.

Wagner is explicit that correlation is not causation — higher conversion near these products does not prove a spillover, and confirming it needs controlled experiments. But if the effect is real, optimizing each product's individual conversion probability could produce a worse overall ranking. His conclusion: the best ranking may not be the one containing the individually best products, but the one where the products work best together.

## Discussion

In the comments on part 1, one practitioner described an eCommerce search team that used conversion rate and no-results rate as primary metrics (later switching the A/B goal to basket-value uplift) and never made nDCG a main metric. [[Andrew Kornilov]] countered that teams reach for nDCG not because of papers but because there is no clear, implementable alternative, and a team still needs something measurable.

## Related

- [[NDCG]] · [[NDCG-f]] · [[NDCG-m]] · [[UDCG]] — the metric and its variants
- [[Flavors of NDCG]] · [[Demystifying nDCG and ERR]] · [[Choosing Your Search Relevance Evaluation Metric]]
- [[How we Compute NDCG in Daraz E-Commerce]] — an eCommerce team that does use nDCG
- [[Evaluating the Best AB Testing Metrics for Search]] — the business-KPI side of the argument
- [[Learning to Rank]] — the per-item objective part 3 questions; contrast its Findify story, where a click-heavy, never-bought product is demoted
- [[Common Pitfalls of Onsite Search Experimentation]] · [[Towards Scalable Relevance Engineering]] — Wagner's other evaluation writing

- [[Psychological and Behavioural Effects and Biases in Search]] — spillover, halo and decoy effects alongside other user and data biases
