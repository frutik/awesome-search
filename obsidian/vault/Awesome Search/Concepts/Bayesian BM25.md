---
title: "Bayesian BM25"
aliases: ["BB25", "Probabilistic BM25", "Calibrated BM25"]
type: concept
tags:
  - concept
  - search
  - ranking
  - bm25
created: 2026-05-15
---

# Bayesian BM25 (BB25)

A calibrated variant of [[BM25]] that maps raw BM25 scores to probability-of-relevance estimates, enabling principled hybrid fusion with other probabilistic signals.

## The Core Problem with Raw BM25

BM25 produces a score on an arbitrary scale. Combining it with dense embedding similarity via linear interpolation requires hand-tuned weight α:

```
hybrid = α × BM25 + (1−α) × embedding_score
```

This α is brittle — it changes when either model changes, and the two scales are incommensurable.

## BB25: Calibrating BM25 to a Probability

Fit a logistic (sigmoid) transformation over BM25 scores using relevance-labeled data:

```
BB25(q, d) = σ(a × BM25(q, d) + b)
           = P(relevant | BM25 score)
```

Parameters a and b are fit by logistic regression on (query, document, relevance label) triples.

## Principled Hybrid Fusion

Once both BM25 and embedding scores are calibrated to probabilities, Bayes' theorem (under naive independence assumption) gives a principled fusion:

```
P(R | BM25, emb) ∝ P(R | BM25) × P(R | emb)
```

Equivalently, in log-odds space this is just addition — no arbitrary α needed. Additional signals (freshness, popularity) compose naturally as more likelihood terms.

## The Explicit Bayesian Formulation

[[Doug Turnbull]]'s later treatment in [[Can BM25 be a Probability]] decomposes the same idea into
actual Bayesian components rather than one fitted sigmoid.

The framing problem: BM25 models **odds** — a likelihood ratio `P(t|R=1) / P(t|R=0)` — not a
probability, which is why it won't compose with signals that *are* probabilities.

**Prior** — a default relevance assumption from term frequency and field length:

```
tf_prior    = 0.2 + 0.7 * min(1, TERM_FREQ / 10)
norm_prior  = 0.3 + 0.6 * (1 - min(bm25_norm_length, 0.5))
bb25_prior  = clamp(0.7 * tf_prior + 0.3 * norm_prior, 0.1, 0.9)
```

**Likelihood** — the BM25 score as evidence, through a sigmoid:

```
bb25_likelihood = sigmoid(ALPHA * (bm25_score - BETA))
```

`BETA` is the median BM25 score (corpus-specific); `ALPHA` sets the steepness of the transition.

**Posterior** — Bayes' theorem:

```
bb25_lp        = bb25_prior * bb25_likelihood
bb25_marginal  = bb25_lp + (1 - bb25_likelihood) * (1 - bb25_prior)
bb25_posterior = bb25_lp / bb25_marginal
```

The real leverage is **learning `ALPHA`/`BETA` from labels** by gradient descent, so that
`P(R | lexical)` and `P(R | embedding)` land on the same scale.

## Alternatives Turnbull Weighs

1. **Make the other factors look like BM25** (Craswell et al.) — scale non-BM25 signals with
   log/saturation functions instead, e.g. an Elasticsearch rank feature query. Sidesteps calibrating
   BM25 at all.
2. **Just learn the boosts** — fit the weights directly via random search or Bayesian optimization.
   Less interpretable, but he notes it often wins in practice.
3. **Scaled BM25** — Lucene already scales TF to 0–1 and IDF can be normalized by `log(num_docs)`;
   gradient descent could run on `k1`/`b` directly.

## Relationship to Learning to Rank

The full formula:

```
P(R | BM25, emb) = σ(a₁ × BM25 + a₂ × emb_score + b)
```

is logistic regression — a standard LTR baseline. BB25's contribution is framing this as Bayesian probability updating, which gives each score an interpretable meaning and makes the combination principled rather than ad-hoc.

## Key Properties
- **Interpretable scores** — outputs are true probability estimates in [0, 1]
- **Principled mixing** — no arbitrary interpolation weights
- **Composable** — additional signals add naturally as new likelihood terms
- **Calibration transfer** — when a component model changes, only its calibration params need refit

## Related Concepts
- [[BM25]] — the score being calibrated
- [[Score Normalization]] — the alternative: rescale scores to a common range rather than calibrate them to probabilities
- [[Linear Score Combination]] — the hand-tuned α that BB25 exists to eliminate
- [[Relative Score Fusion]] · [[Reciprocal Rank Fusion]] — the fusion strategies used in its absence
- [[Hybrid Search]] — the motivating use case
- [[Learning to Rank]] — the fitted form is logistic regression, a standard LTR baseline
- [[Dense Vector Retrieval]] — the signal BM25 needs to become commensurable with

## Related Articles
- [[Bayesian BM25 is Cool]] — [[Doug Turnbull]], 2021; the logistic-calibration framing
- [[Can BM25 be a Probability]] — [[Doug Turnbull]], 2026; explicit prior/likelihood/posterior, plus the alternatives
- [[RRF is Not Enough]] — why the uncalibrated workarounds disappoint
