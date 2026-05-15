---
title: "Flavors of NDCG — Normalized to What!?"
source: "https://softwaredoug.com/blog/2024/05/22/flavors-of-ndcg"
author: ["Doug Turnbull"]
tags:
  - clippings
  - search-evaluation
  - ndcg
  - metrics
concepts:
  - NDCG
  - Search Evaluation
  - Judgment Lists
created: 2026-05-15
---

# Flavors of NDCG — Normalized to What!?

**Source**: https://softwaredoug.com/blog/2024/05/22/flavors-of-ndcg  
**Author**: [[Doug Turnbull]]

## Summary

[[Doug Turnbull]] clarifies a persistent source of confusion: NDCG has multiple valid mathematical formulations that produce different numbers from the same input. Not knowing which "flavor" a benchmark uses can lead to apples-to-oranges comparisons.

## The Two Main Variants

### Variant 1: Jarvelin & Kekalainen (2002) — "Grade Gain"
```
DCG@k = rel₁ + Σᵢ₌₂ᵏ rel_i / log₂(i)
```
Position 1 gets full relevance with no discount. Positions 2+ are discounted.

### Variant 2: Burges et al. (2005) — "Exponential Gain" (default in most ML frameworks)
```
DCG@k = Σᵢ₌₁ᵏ (2^rel_i - 1) / log₂(i + 1)
```
All positions discounted. The `2^rel - 1` transform amplifies high-relevance documents.

For grade 3: 2³-1 = 7. For grade 1: 2¹-1 = 1. High-relevance docs count ~7x more than marginal docs.

## Why the Difference Matters

Same judgment list, same ranking, two variants:
- Variant 1 NDCG@10: 0.72
- Variant 2 NDCG@10: 0.68

A 4-point "improvement" comparing systems on different variants is meaningless.

**Rule**: always specify which DCG formula you're using when reporting NDCG.

## Normalization: "To What"?

NDCG normalizes by IDCG (ideal DCG). The "ideal" assumes the best possible ranking given your judgment list.

**Key implication**: IDCG is bounded by your judgment pool. If you only judged documents returned by System A, System B may retrieve better documents that appear "unjudged" (treated as grade 0). This biases NDCG against systems that retrieve outside the judged pool.

## Common Implementations

| Library | Variant Used |
|---------|-------------|
| scikit-learn `ndcg_score` | Burges (exponential) |
| RankLib | Jarvelin (grade gain) |
| Quepid | Configurable |
| LightGBM LambdaRank | Burges |
| MS MARCO leaderboard | Burges |

## Practical Advice

1. Use the same variant throughout your project
2. Be explicit when comparing to published benchmarks
3. For e-commerce with 0–4 grades: Burges variant is better (amplifies highly relevant items)
4. For binary relevance (0 or 1): variants are equivalent

## Related Articles

- [[Session vs Query based Search Evals]] — same author, complementary
- [[Compute MRR using Pandas]] — same author, simpler metric
- [[Evaluating Search - Using Human Judgments]] — how judgments feed into NDCG

## Related Concepts

- [[NDCG]] — primary topic
- [[Search Evaluation]] — broader context
- [[Judgment Lists]] — input to NDCG computation
- [[MRR]] — simpler, less ambiguous alternative
