---
title: "Evaluating Good Search Part I: Measure It"
tags:
  - clippings
  - search
  - evaluation
source: "https://medium.com/@dtunkelang/evaluating-good-search-part-i-measure-it-5507b2dbf4f6"
author: "Daniel Tunkelang"
created: 2026-05-15
concepts:
  - Search Evaluation
  - NDCG
  - MRR
  - Click Signals
---

# Evaluating Good Search Part I: Measure It

**Source:** https://medium.com/@dtunkelang/evaluating-good-search-part-i-measure-it-5507b2dbf4f6
**Author:** [[Daniel Tunkelang]]
**Series:** Evaluating Search (Part 1 of 4)

## Summary

Opening of Tunkelang's four-part series on search evaluation. Anchored in Lord Kelvin's principle: "If you cannot measure it, you cannot improve it." Covers the full taxonomy of supervised and unsupervised search metrics.

## Supervised Metrics (require judgment labels)

| Metric | What it measures |
|---|---|
| **Precision** | Fraction of returned results that are relevant |
| **Recall** | Fraction of all relevant results that were returned |
| **Precision@k** | Precision for top k results only |
| **Average Precision@k** | Weighted avg giving more weight to top-ranked results |
| **[[NDCG]]** | Accounts for relevance gradations + position discounting |

## Unsupervised Metrics (from behavior)

| Metric | What it measures |
|---|---|
| **CTR** | Fraction of searches that receive clicks |
| **[[MRR]]** | Weighted click signal favoring earlier positions |
| **Conversions** | Stronger signal than clicks (purchase, signup, etc.) |

## Key Insight

Conversions are sparse but strong; clicks are plentiful but noisy. Individual components (spelling correction, autocomplete) need their own targeted metrics.

## Series
1. **Measure It** (this article)
2. [[Measuring Searcher Behavior]]
3. [[Evaluating Search - Using Human Judgments]] *(already processed)*
4. [[When There's No Conversion Rate]]

## Related Concepts

- [[Search Evaluation]]
- [[NDCG]]
- [[MRR]]
- [[Precision and Recall]]
- [[Click Signals]]
- [[Judgment Lists]]

## People

- [[Daniel Tunkelang]]
