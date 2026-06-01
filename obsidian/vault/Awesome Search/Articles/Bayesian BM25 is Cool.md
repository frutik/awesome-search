---
title: "Bayesian BM25 is Cool"
aliases: ["BB25", "Bayesian BM25", "Turnbull BB25"]
tags:
  - clippings
  - search
  - ranking
  - bm25
  - company-blog
source: "https://opensourceconnections.com/blog/2021/09/02/bayesian-bm25-is-cool/"
author: "Doug Turnbull"
created: 2026-05-15
concepts:
  - BM25
  - Hybrid Search
  - Learning to Rank
---

# Bayesian BM25 is Cool

**Source:** https://opensourceconnections.com/blog/2021/09/02/bayesian-bm25-is-cool/
**Author:** [[Doug Turnbull]]

## Summary

**Bayesian BM25 (BB25)** recasts the BM25 score as a probability estimate P(relevant | BM25 score), enabling principled hybrid fusion with other probability-calibrated signals (e.g., dense embedding scores).

### The Problem with Raw BM25
BM25 produces a score that is not interpretable as a probability. Combining BM25 with a dense embedding score (also uncalibrated) via linear interpolation requires hand-tuning a mixing weight α:

```
hybrid = α × BM25 + (1-α) × embedding_score
```

This is fragile: α changes when either model changes, and the scales are incompatible.

### Bayesian Calibration Approach
If we calibrate BM25 to a probability, we can use Bayes' theorem to combine signals:

```
P(R | BM25, emb) ∝ P(BM25 | R) × P(emb | R) × P(R)
```

Under a naive-Bayes independence assumption:

```
P(R | BM25, emb) ∝ P(R | BM25) × P(R | emb)
```

This gives a **principled fusion formula** where each signal contributes a likelihood ratio update.

### BB25 Formula
```
BB25(q, d) = P(R | BM25(q,d)) = σ(a × BM25(q,d) + b)
```
Where σ is the logistic (sigmoid) function, and a, b are calibration parameters fit on relevance data. The output is a probability in [0,1].

### Combining with Embedding Score
```
P(R | BM25, emb) = σ(a₁ × BM25 + a₂ × emb_score + b)
```
This is just logistic regression — which is a known-good LTR baseline. BB25's contribution is framing this as Bayesian updating and giving interpretability to the intermediate scores.

### Practical Benefits
1. **Interpretability**: scores mean something (probability of relevance)
2. **Principled mixing**: no arbitrary α tuning
3. **Composability**: additional signals add naturally as new likelihood terms
4. **Calibration data reuse**: calibration parameters update cleanly when models change

## Key Concepts
- **BB25** — Bayesian-calibrated BM25 producing probability outputs
- **Calibration** — mapping raw scores to probabilities via logistic regression
- **Principled hybrid fusion** — Bayesian product of independent probability estimates
- **Likelihood ratio** — each signal's contribution as a probability update

## Related Concepts
- [[BM25]]
- [[Hybrid Search]]
- [[Learning to Rank]]
- [[Reciprocal Rank Fusion]]
- [[Dense Vector Retrieval]]

## Related Articles
- [[Practical BM25 - The Effect of k1 and b]]
- [[Elasticsearch and BM25]]
- [[Hybrid Search Explained]]

## People
- [[Doug Turnbull]]
