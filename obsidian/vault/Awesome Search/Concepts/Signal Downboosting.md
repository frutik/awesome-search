---
title: Signal Downboosting
aliases:
  - signal downboosting
  - downboosting
  - result downboosting
type: concept
tags:
  - concept
  - ranking
  - search-relevance
  - click-signals
created: 2026-05-17
---

# Signal Downboosting

A ranking technique that identifies search results with high impression counts but statistically poor click/conversion performance per query, then moves those results toward the bottom of the ranking.

---

## Definition

Signal downboosting is the inverse of [[Results Boosting|signal boosting]]. Instead of amplifying what already converts well (which reinforces [[Position Bias]]), downboosting targets confirmed underperformers — items shown frequently for a query that consistently underperform their peers with statistical confidence — and demotes them.

## Why Downboosting, Not Boosting?

[[Results Boosting|Signal boosting]] (placing high-click results first) creates a feedback loop: highly-ranked results get more clicks not because they're relevant, but because they're prominent. This amplifies presentation bias and traps ranking in a local optimum.

Downboosting avoids this by:
1. **Improving precision** — removing known-bad results from the top-N
2. **Increasing diversity** — freeing up slots for untested results
3. **Overcoming presentation bias** — giving other results a chance to be evaluated

## Implementation Approach

1. For each query, track impression count and performance (CTR, conversion) per result
2. Identify results with high impressions but significantly below-average performance (use statistical significance thresholds)
3. Apply a scoring penalty or rank demotion to these confirmed underperformers

## Relationship to Signal Boosting

| Approach | Mechanism | Risk |
|----------|-----------|------|
| Signal boosting | Promote high-performers | Amplifies position bias; local optimum |
| Signal downboosting | Demote confirmed underperformers | More conservative; improves diversity |

Introduced (or named) in Doug Turnbull's understaffed search team guide as a preferred alternative to signal boosting.

## Related Concepts
- [[Position Bias]] — the bias that signal boosting amplifies
- [[Results Boosting]] — the complementary boosting technique
- [[Click Signals]] — the raw data used to identify underperformers
- [[A/B Testing for Search]] — used to validate downboosting impact
- [[Search Evaluation]] — how to measure improvement from downboosting

## Related Articles
- [[Getting Started on Search Relevance for the Understaffed Search Team]]
- [[What is Presentation Bias in Search]]
