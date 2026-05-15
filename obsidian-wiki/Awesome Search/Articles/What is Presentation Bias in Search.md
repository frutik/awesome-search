---
title: "What is Presentation Bias in Search?"
tags:
  - clippings
  - search
  - bias
  - evaluation
source: "https://softwaredoug.com/blog/2022/07/16/what-is-presentation-bias-in-search.html"
author: "Doug Turnbull"
created: 2026-05-15
concepts:
  - Position Bias
  - Click Signals
  - Search Evaluation
---

# What is Presentation Bias in Search?

**Source:** https://softwaredoug.com/blog/2022/07/16/what-is-presentation-bias-in-search.html
**Author:** [[Doug Turnbull]]

## Summary

Presentation bias is a broader form of [[Position Bias]] — the phenomenon where users can only interact with what's actually displayed to them, causing click data to reflect the system's choices rather than users' true preferences.

## Definition

> "Shoppers won't purchase what search doesn't show them!"

When search results are limited by screen space, the historical click data captured becomes contaminated by the system's prior decisions about what to show. Users can only click on what they see.

## The Self-Reinforcing Cycle

1. System shows items A, B, C (not D, E, F)
2. Users click on A, B, C (because that's all they see)
3. System trains on these clicks → "A, B, C are what users want"
4. D, E, F never get shown → never get clicks → never improve in ranking
5. System becomes more entrenched in showing A, B, C

## Highway Sign Metaphor

A highway sign shows only 6 restaurants in a town. Surveyed travelers prefer those 6. The sign itself skewed the results — this is presentation bias.

## Relationship to [[Position Bias]]

- **Position bias**: users click top results more regardless of quality
- **Presentation bias**: broader — users can only interact with what's shown; not shown = not clicked = not "preferred"

Presentation bias is the root; position bias is one specific manifestation.

## Solutions

- Result diversity (show more of the long tail)
- [[A-B Testing for Search]] with controlled experiments
- Active learning (deliberately show underexposed items)
- Non-click data sources (manual [[Judgment Lists]])

## Related Concepts

- [[Position Bias]]
- [[Click Signals]]
- [[Search Evaluation]]
- [[Diversity Metrics]]
- [[Judgment Lists]]

## People

- [[Doug Turnbull]]
