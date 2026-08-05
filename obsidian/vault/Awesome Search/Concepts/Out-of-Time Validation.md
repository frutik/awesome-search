---
type: concept
title: "Out-of-Time Validation"
aliases: ["walk-forward validation", "out-of-time validation", "temporal validation", "time-based split"]
tags: [concept, evaluation, ranking, training, methodology]
created: 2026-08-05
---

# Out-of-Time Validation

## Definition

Out-of-time validation evaluates a model on data from a **time period after** the
one it was trained on, rather than on a random sample of the same period.
**Walk-forward validation** is the repeated form: train on a window, test on the
next window, roll forward, and evaluate across successive periods.

## Why random splits lie

A ranker is trained on historical observations in order to produce good rankings
*in the future*. A random train/test split does not test that. It tests
interpolation within a period the model has already partly seen, and it leaks
future information into training in several ways:

- **Seasonality** — a random split puts December sessions in both train and test,
  so the model is scored on a season it memorized rather than one it must
  anticipate.
- **Popularity drift** — item popularity, inventory, and user behavior all shift;
  a random split hides the decay by construction.
- **Rolling features** — behavioral features like "reservations in the last 6
  months" computed over the whole dataset embed future information in past rows.

The result is an optimistic offline number that does not survive deployment. This
is the same failure that makes offline metrics a *health check* rather than a
predictor of business value.

## The companion rule: train on displayed, test on available

A subtler discipline that belongs with temporal validation. During **training**
you necessarily use the items that were displayed to users — that is all you have
labels for. During **testing** you must score **every item available at that
moment**, not only the displayed ones.

Testing only on displayed items evaluates the model on a candidate set the
previous ranker already curated, which flatters the new model and hides
[[Impression Bias]]. Scoring the full available inventory simulates what actually
happens at inference time, and only then are precision, recall, [[MRR]], and
[[NDCG]] a meaningful health check.

## Multi-scenario evaluation

A global metric averaged over all traffic conceals subgroup failure. Where a
model leans on behavioral and personalization features, it can perform very well
for users with interaction history and inadequately for users who just arrived —
and the aggregate looks fine because returning users dominate the volume. Segment
offline evaluation by user tenure, session depth, query type, or destination.

## Related Concepts

- [[Search Evaluation]] — the broader evaluation frame
- [[Vector Search Evaluation]] · [[Session-Based Evaluation]]
- [[Impression Bias]] — what testing on displayed-only items hides
- [[A-B Testing for Search]] — online evaluation that offline validation gates
- [[Statistical Significance in Search Evaluation]]
- [[Learning to Rank]] · [[LTR Feature Engineering]] — rolling features are the leak vector
- [[NDCG]] · [[MRR]] · [[MAP]] · [[Precision and Recall]] — metrics this governs

## Articles

- [[Beyond Algorithms - Ranking at Scale at Booking.com]] — walk-forward validation and the train-on-displayed/test-on-available rule
