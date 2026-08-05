---
type: concept
title: "Impression Bias"
aliases: ["impression bias", "examination propensity bias", "candidate exposure bias"]
tags: [concept, bias, ranking, search-evaluation]
created: 2026-08-05
---

# Impression Bias

## Definition

Impression bias is the distortion arising because **a document's propensity to be
examined at all is determined by the rankers historically used in production**.
Users never examine the available inventory exhaustively or uniformly, so the
training data records opinions only about items past rankers chose to surface.

## How it differs from position bias

The two are routinely conflated, but they act at different stages:

| | [[Position Bias]] | Impression Bias |
|---|---|---|
| Question | Given the item was shown, did rank inflate its clicks? | Was the item ever shown at all? |
| Affects | Weighting of observed items | Which items enter the data |
| Correction | Reweight by examination probability at rank *i* | Requires exposure that never happened |

Position bias is a **measurement** problem within the candidate set. Impression
bias is a **coverage** problem about the candidate set. Debiasing clicks by rank
does nothing for an item that was never on any page a user saw — there is no
observation to reweight.

This is why impression bias is the harder of the two: position bias can be
corrected analytically from logged data, whereas impression bias generally cannot
be corrected without deliberately changing what gets shown.

## The compounding loop

An item ranked low is examined rarely → generates little engagement data → its
features look weak or stay unknown → the next trained ranker places it low again.
Past ranking decisions become self-fulfilling, and the ranker's own history
defines the boundary of what it can ever learn about.

This is the mechanism behind cold-start pathology for new inventory: a new
property, product, or document has no engagement history *because* the ranker
withheld exposure, not because users rejected it.

## Mitigations

- **[[Exploration vs Exploitation]]** — deliberately randomized or shuffled
  exposure creates observations the exploitative ranker would never produce. The
  most direct remedy, at a known cost in short-term quality.
- **Propensity estimation** — Inverse Propensity Weighting, including query-level
  variants developed for selection bias in personal search, weights observed
  actions by how likely they were to be observed.
- **Content-based / latent features** — representing items by attributes or
  embeddings rather than behavioral history lets a model generalize to items with
  no engagement data. Booking.com's use of [[Word2Vec]] over action sequences to
  place properties in a latent space partly serves this end.
- **Evaluating against the full candidate set** — at test time, score every item
  that *was available*, not just those that were displayed, so offline metrics
  reflect real inference rather than the historical ranker's choices. See
  [[Out-of-Time Validation]].

## Related Concepts

- [[Position Bias]] — the within-page counterpart
- [[Presentation Bias]] — the broader family of exposure-driven distortions
- [[Exploration vs Exploitation]] — the primary escape route
- [[Implicit Judgments]] · [[Click Signals]] — the data impression bias corrupts
- [[Isolated Feedback Loops]] — the same self-reinforcing loop inside experiments
- [[Learning to Rank]] — where the bias is baked into a model

## Articles

- [[Beyond Algorithms - Ranking at Scale at Booking.com]] — names impression bias alongside position bias and user bias
