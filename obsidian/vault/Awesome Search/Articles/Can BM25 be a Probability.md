---
created: 2026-05-16
title: "Can BM25 be a Probability?"
source: "https://softwaredoug.com/blog/2026/03/06/probabilistic-bm25-utopia"
author: "[[Doug Turnbull]]"
published: 2026-03-06
tags: [BM25, Bayesian-BM25, hybrid-search, probability, calibration]
---

# Can BM25 be a Probability?

**Author:** [[Doug Turnbull]]

## Summary

BM25 scores are unbounded and not interpretable as probabilities. This creates a fundamental problem for hybrid search: embedding similarities can be modeled as probabilities and combined rigorously, but BM25 cannot. This article reviews **Bayesian BM25 (BB25)** — an attempt to convert BM25 scores into calibrated probabilities enabling principled hybrid fusion.

## The Core Problem

BM25 models **odds** (a likelihood ratio), not probabilities:
```
rel_odds(t) = P(t|R=1) / P(t|R=0)
```

Other relevance factors — embedding similarity, CTR, page rank, recency — can be modeled as probabilities and combined:
- AND: `P(R | E) * P(R | L)`
- OR: prior-based combinations

BM25 doesn't fit this framework, so practitioners resort to magic number boosts and [[Reciprocal Rank Fusion]].

## Bayesian BM25 (BB25)

BB25 transforms BM25 into a probability using Bayesian reasoning:

### Prior
Default relevance assumption from TF and field length:
```
tf_prior = 0.2 + 0.7 * min(1, TERM_FREQ / 10)
norm_prior = 0.3 + 0.6 * (1 - min(bm25_norm_length, 0.5))
bb25_prior = clamp(0.7 * tf_prior + 0.3 * norm_prior, 0.1, 0.9)
```

### Likelihood
BM25 score passed through sigmoid as evidence:
```
bb25_likelihood = sigmoid(ALPHA * (bm25_score - BETA))
```
- BETA = median BM25 score (corpus-specific)
- ALPHA = steepness of transition

### Posterior (Bayes Theorem)
```
bb25_lp = bb25_prior * bb25_likelihood
bb25_marginal = bb25_lp + (1 - bb25_likelihood) * (1 - bb25_prior)
bb25_posterior = bb25_lp / bb25_marginal
```

## Calibration

The real power: **learning alpha/beta from labels** via gradient descent. Optimizes against ground truth so `P(R | L)` and `P(R | E)` are on the same scale — enabling principled hybrid search.

## Alternative Views

**Alternative 1: Make other factors look like BM25** (Craswell et al.) — scale non-BM25 signals with log/saturation functions; use Elasticsearch rank feature query. Avoids converting BM25 to probability.

**Alternative 2: Just learn the boosts** — learn weights `e` and `l` directly via random search or Bayesian optimization. Less interpretable but often wins in practice.

**Alternative 3: Scaled BM25** — Lucene's BM25 already scales TF from 0-1; IDF can also be normalized by `log(num_docs)`. Could perform gradient descent on k1/b directly.

## Related Concepts

- [[BM25]] — the underlying algorithm
- [[Bayesian BM25]] — the probabilistic extension
- [[Hybrid Search]] — the motivation: combining BM25 with embeddings
- [[Reciprocal Rank Fusion]] — current workaround for hybrid without calibration

## Related Articles

- [[Bayesian BM25 is Cool]]
- [[RRF is Not Enough]]

## People

- [[Doug Turnbull]]
