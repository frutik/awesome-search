---
type: concept
title: "Expected Calibration Error"
aliases: ["ECE", "expected calibration error", "calibration error", "reliability diagram"]
tags:
  - concept
  - calibration
  - search-evaluation
  - metrics
created: 2026-09-20
---

# Expected Calibration Error

## Definition

**Expected Calibration Error (ECE)** summarises a reliability diagram into one number. Bucket
predictions by their probability, and in each bucket compare the **average predicted
probability** against the **observed fraction of positives**. ECE is the weighted mean of those
gaps, weighted by bucket size. Zero means every bucket delivers what it promised.

The bucket count is a parameter and belongs in the report — "10-bin ECE" is a measurement, "ECE"
alone is not. The underlying reliability diagram is the more honest artifact: it shows *where*
the model is wrong, which a scalar cannot.

Popularised in machine learning by Guo, Pleiss, Sun and Weinberger, *On Calibration of Modern
Neural Networks*, Proceedings of ICML (PMLR 70): 1321–1330 (2017) — the paper that showed modern
networks are systematically overconfident.

## What It Adds Over Brier

[[Brier Score|Brier]] blends two things: how well-calibrated the probabilities are and how
*sharp* they are (how far they dare to move from the base rate). ECE isolates the first.

That isolation cuts both ways. A model that predicts the base rate for every single example is
perfectly calibrated and completely useless — ECE near zero, no discrimination whatsoever. ECE
is therefore a metric to read **alongside** a discrimination metric, never instead of one.

| | Measures | Fooled by |
|---|---|---|
| ECE | Do the buckets deliver their promised rates? | A model that never leaves the base rate |
| Brier | Squared distance from the outcome | Class imbalance |
| Log loss | Same, with unbounded penalty for confident errors | A single catastrophic prediction |

## In Practice

The bucket-and-compare procedure is exactly what [[Hev meets Jev]] does informally: on SciFact,
documents [[Jev]] scored above 0.9 were judged relevant 76% of the time and those below 0.1,
half a percent. That is two buckets of a reliability diagram, reported without the summary
statistic — and it is the measurement that made the case for
[[Calibrated Relevance Probability]] as [[Jev]]'s real differentiator.

[[Adapting Jev to Your Domain with GEPA]] supplies the scalar, on a classification task rather
than a retrieval one. 10-bin ECE for [[Jev]] at its default prompt was **0.173**, against 0.052
for a TF-IDF baseline on the same 300 sentences — the model's probabilities were off by about 17
percentage points per bucket on average. A [[GEPA]]-optimized prompt cut it to 0.069 on a fresh
split, from 0.142 for the original prompt on that same split. Calibration turned out to be a
property of the instruction at least as much as of the model.

Read together, the two measurements say something more useful than either alone: usable
calibration in one bucket range on one corpus ([[Hev meets Jev]]) does not imply calibration
across the range on another task, and neither reading transfers without re-measuring.

## Cautions

- **Binning choices move the number.** Equal-width and equal-mass bins give different answers;
  so do 10 bins and 20. Fix the scheme and state it.
- **It hides direction.** Over- and under-confidence in different buckets partially cancel in
  the weighted mean. Look at the diagram.
- **It is measured on a distribution.** Like every calibration statistic, it is a claim about the
  data it was computed on, and the model gives no signal when it has left that distribution —
  see [[Calibrated Relevance Probability]] and [[Out-of-Time Validation]].

## Related Concepts

- [[Brier Score]] — the companion metric ECE decomposes part of
- [[Calibrated Relevance Probability]] — the property being measured
- [[Reinforcement Learning for Calibrated Decisions]] — a training objective aimed at it
- [[NDCG]] · [[MRR]] — ranking metrics invariant to calibration entirely
- [[Staged Judging]] — the pattern that depends on the buckets meaning what they say
- [[Out-of-Time Validation]] — re-measuring when the distribution moves
- [[Search Evaluation]] — the wider practice

## Related Articles

- [[Adapting Jev to Your Domain with GEPA]] — [[Praneeth Paikray]]; 10-bin ECE before and after prompt optimization
- [[Hev meets Jev]] — [[Hev]]; the same check done as buckets on BEIR
- [[Introducing System One Models & Jev]] — the calibration claim these measurements test
