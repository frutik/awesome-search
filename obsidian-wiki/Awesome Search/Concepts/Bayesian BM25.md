---
title: "Bayesian BM25"
aliases: ["BB25", "Probabilistic BM25", "Calibrated BM25"]
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
- [[BM25]]
- [[Hybrid Search]]
- [[Reciprocal Rank Fusion]]
- [[Learning to Rank]]
- [[Dense Vector Retrieval]]

## Related Articles
- [[Bayesian BM25 is Cool]]
