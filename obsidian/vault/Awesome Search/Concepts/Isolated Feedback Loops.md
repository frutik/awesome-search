---
type: concept
title: "Isolated Feedback Loops"
aliases: ["isolated feedback loop", "feedback loop isolation", "experiment data isolation"]
tags: [concept, experimentation, ranking, evaluation, a-b-testing]
created: 2026-08-05
---

# Isolated Feedback Loops

## Definition

Isolated Feedback Loops means keeping the **data logging of each experiment group
separate**, so that the ranker serving control and the ranker serving treatment
each learn only from the traffic they themselves produced. It is the structural
fix for data leakage in online ranking experiments.

## The problem it solves

Ranking is a **self-learning system**: the model that sorts the items also
influences the data it will later be trained on. That property, harmless in
production, quietly breaks randomized controlled trials. Two distinct leaks:

**Re-training leakage** — if rankers are retrained during the trial on logs
pooled across all groups regardless of origin, customer preferences leak between
control and treatment. The two rankers converge toward recommending similar items
in similar order, and the measured difference shrinks toward zero. The experiment
understates the true effect.

**Feature leakage** — even with *no* retraining, any **time-dynamic feature**
carries the leak. If a ranker consumes "reservations in the last day" or a
rolling CTR, then treatment's behavior alters a feature value that control also
reads. The two arms are coupled through shared feature state.

Both compromise the trial if unaddressed.

## The two remedies

| Approach | How | Cost |
|---|---|---|
| **Freezing** data sources | Restrict features to pre-experimental data points only | Minimal logging infrastructure, but assumes a **stationary world** — unacceptable when the ranker depends on very recent performance |
| **Isolated Feedback Loops** | Separate logging and feature computation per RCT group | Clean separation, but adds complexity in how the collected data is later reused |

Freezing is the cheap option and fails precisely where recency matters most.
Isolation is correct but means each group's feature pipeline, and potentially
each group's training set, must be maintained independently.

## Why it generalizes

Any ranking or recommendation system with a behavioral feedback loop has this
problem, not just travel marketplaces. If your features include popularity, CTR,
purchase rate, or recent engagement — the standard behavioral features in
[[LTR Feature Engineering]] — then your A/B tests are coupled through them by
default, and the coupling is invisible in the experiment readout.

The failure mode is **not** a false positive. It is systematic **attenuation**:
real improvements look smaller than they are, so genuinely good rankers get
rejected.

## Related Concepts

- [[A-B Testing for Search]] — the experiment design this protects
- [[Interleaving]] — sidesteps the problem differently, by randomizing on position
- [[Exploration vs Exploitation]] — the same self-reinforcing loop, seen from training
- [[Impression Bias]] · [[Position Bias]] — biases the feedback loop compounds
- [[LTR Feature Engineering]] — time-dynamic features are the leak vector
- [[Feature Store]] — where per-group feature isolation would be implemented
- [[Statistical Significance in Search Evaluation]] — attenuation directly costs power

## Articles

- [[Beyond Algorithms - Ranking at Scale at Booking.com]] — origin of the term in this vault; both leak types and both remedies
