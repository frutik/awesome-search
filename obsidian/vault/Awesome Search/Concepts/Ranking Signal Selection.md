---
type: concept
title: "Ranking Signal Selection"
aliases: ["signal definition", "target variable definition", "label selection for ranking", "positive and negative signals"]
tags: [concept, ranking, learning-to-rank, training-data, evaluation]
created: 2026-08-05
---

# Ranking Signal Selection

## Definition

Ranking Signal Selection is the choice of **which observed user actions become
positive and negative training labels** for a ranker. It precedes model choice
and usually matters more: a strong algorithm trained toward the wrong target
optimizes the wrong thing efficiently.

## The four-axis tradeoff

No single user action is a good label. Every candidate is evaluated on four axes,
and they conflict — the actions most tightly bound to satisfaction are the
rarest and slowest to observe:

1. **Relation to user satisfaction** — does the action actually mean the user was served well?
2. **Amount of data points** — is there enough volume to train on?
3. **Delay to observe** — how long until the label is known?
4. **Bias of the action** — what systematic distortion does it carry?

### Worked example: accommodation search

| Positive signal | Satisfaction | Volume | Delay | Bias |
|---|---|---|---|---|
| Click | Weak | Large | Small | Clicking ≠ satisfaction |
| Click with dwell > threshold | Medium | Large/Medium | Small | Browsing time ≠ satisfaction |
| Reservation | Strong | Small | Medium (days) | No knowledge of later cancellation |
| Stay | Strong | Small | Large (months) | No knowledge of stay experience |
| Stay with good review | Strong | Very small | Large | Who chooses to review is biased |

The axes move in opposition as you descend the funnel. Clicks are plentiful,
immediate, and nearly meaningless; a positively-reviewed completed stay is
almost ground truth and far too sparse and delayed to train on. **The practical
answer is rarely one signal.**

## The layered pattern

A workable resolution is a primary conversion label plus secondary weaker ones:

- **Primary positive** — the deepest action with acceptable volume and delay
  (a reservation, a purchase, a booking).
- **Secondary positives** — clicks, optionally dwell-gated. These teach the model
  that *several* items could have satisfied the user even though only one was
  converted. Without them, the ranker learns an artificially peaked notion of
  relevance in which exactly one item per session was ever acceptable.

## Negative signals

Harder than positives, because a non-click is ambiguous — unseen or rejected?

- **Skip-above** — if a user clicked position 5, positions 1–4 were plausibly
  examined and deliberately passed over. Large volume, fast, and much stronger
  than a bare impression. Its assumption (that users examine everything above the
  click) is a known simplification.
- **Bare impressions with no click anywhere in the session** — weak individually,
  but valuable for a different reason: including no-click sessions stops the
  ranker over-fitting to the subpopulation that clicks and books. Dropping them
  is a silent selection bias toward engaged users.
- **Short-dwell clicks** — a click followed by a fast bounce, as a
  dissatisfaction proxy.
- **Poorly reviewed stays** — strongest and least available.

## Why practitioners underrate it

The target variable is often treated as a given — "we have clicks, we'll train on
clicks" — rather than as a design decision with a tradeoff surface. It determines
the ceiling on everything downstream: no amount of feature engineering,
architecture, or reranking recovers from optimizing a target that does not
correspond to user success. Choosing the label is the point where the business
definition of a good outcome enters the model, and it should be made explicitly.

## Related Concepts

- [[Implicit Judgments]] — behavioral actions as relevance labels
- [[Click Signals]] — the most common and weakest choice
- [[Ranking Objectives]] — what the model optimizes once labels are fixed
- [[Learning to Rank]] · [[LTR Feature Engineering]]
- [[Position Bias]] · [[Impression Bias]] — biases the fourth axis refers to
- [[Judgment Lists]] — the explicit human-labeled alternative
- [[Session-Based Evaluation]] — session context determines skip-above validity

## Articles

- [[Beyond Algorithms - Ranking at Scale at Booking.com]] — the four-axis framing and both signal tables
- [[Paper Review - Ranking at Scale at Booking.com]] — singles out target-variable definition as the foundational difficulty
- [[Learning to Rank for Flight Itinerary Search]] — purchase completion chosen over clicks
- [[Search at Slack]] — click labels with position-bias correction
