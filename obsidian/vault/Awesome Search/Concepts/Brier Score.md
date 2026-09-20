---
type: concept
title: "Brier Score"
aliases: ["Brier score", "quadratic scoring rule", "brier"]
tags:
  - concept
  - calibration
  - search-evaluation
  - metrics
created: 2026-09-20
---

# Brier Score

## Definition

The **Brier score** is the mean squared error of a probabilistic forecast: average
(predicted probability − outcome)² across examples, where the outcome is 0 or 1. Lower is
better; 0 is perfect. Introduced by G. W. Brier, *Verification of Forecasts Expressed in Terms
of Probability*, Monthly Weather Review 78(1): 1–3 (1950), for weather forecasting — which is
where most of the vocabulary of calibration comes from.

It is a **proper scoring rule**: it is minimized by reporting your true belief, so a model
cannot improve it by hedging toward 0.5 or by overclaiming toward the extremes.

## Why It Belongs in a Search Vault

Ranking metrics are blind to the thing Brier measures. [[NDCG]], [[MRR]] and [[MAP]] are
invariant to any monotonic transform of the scores — a system can be perfectly ordered and
wildly overconfident at the same time, and no leaderboard will say so. Once a scorer emits a
[[Calibrated Relevance Probability|probability rather than a rank]], the number acquires a
second axis of quality that needs its own metric.

That matters the moment you threshold. A cutoff on a probability is a promise about what the
number means; Brier is one way of checking the promise.

| Metric | Answers | Blind to |
|---|---|---|
| [[NDCG]] / [[MRR]] | Is the ordering good? | Whether 0.9 means anything |
| Brier | Are the probabilities close to the outcomes? | Ordering quality beyond what the probabilities imply |
| [[Expected Calibration Error\|ECE]] | Do predicted rates match observed rates per bucket? | Sharpness — a model predicting the base rate everywhere scores well |
| Log loss | Same question as Brier, but punishes confident mistakes far harder | — |

Brier and log loss disagree usefully. Because log loss is unbounded as a prediction approaches
certainty on the wrong side, a model that is *usually right but occasionally certain and wrong*
looks acceptable on Brier and terrible on log loss. Reporting both separates "a bit fuzzy" from
"catastrophically overconfident."

## In Practice

[[Adapting Jev to Your Domain with GEPA]] is the worked case in this vault, and it exercises
both roles the metric plays.

**As a diagnostic.** [[Jev]] at its default prompt scored Brier 0.156 against a TF-IDF
baseline's 0.102 on the same 300 sentences — a gap that looks modest until the log losses are
put beside it, 1.849 against 0.335. The ratio of the two gaps *is* the finding: the model was
not vaguely uncertain, it was confidently wrong on a minority of cases. Supporting counts bear
that out — confidence returned exactly 1.0 on 150 of 300 sentences, ten of them incorrect.

**As an optimization objective.** The follow-up experiment pointed [[GEPA]] at minimizing Brier
rather than maximizing accuracy, and got both: Brier fell from 0.1357 to 0.0747 on a fresh test
set (−44.9%, 95% bootstrap CI −0.0863 to −0.0372) while F1 rose from 69.1% to 79.7%. Optimizing
the probability improved the label. That is the practical argument for treating calibration as
something you tune rather than something you hope the vendor supplied.

## Cautions

- **Base rates flatter it.** On an imbalanced task, always predicting the minority rate scores
  respectably. Report it against a trivial baseline, not in isolation.
- **It is a distributional property, not a model property.** A Brier score is measured on one
  distribution and does not travel to another — the same limit that applies to
  [[Calibrated Relevance Probability|calibrated scores]] generally.
- **Bootstrap it.** A Brier delta on 300 examples needs an interval before it is a finding; the
  worked example above reports one.

## Related Concepts

- [[Expected Calibration Error]] — the bucketed companion metric
- [[Calibrated Relevance Probability]] — the property Brier measures
- [[NDCG]] · [[MRR]] · [[MAP]] — ranking metrics that cannot see calibration
- [[Precision and Recall]] — what a thresholded probability turns into
- [[Statistical Significance in Search Evaluation]] — why a Brier delta needs an interval
- [[Prompt Optimization]] — Brier as an objective rather than a report
- [[Reinforcement Learning for Calibrated Decisions]] — training directly for this property
- [[Search Evaluation]] — the wider measurement practice

## Related Articles

- [[Adapting Jev to Your Domain with GEPA]] — [[Praneeth Paikray]]; Brier as both diagnostic and objective
- [[Hev meets Jev]] — calibration measured by bucket rather than by score
