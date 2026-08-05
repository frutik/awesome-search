---
type: concept
title: "Hashing Trick"
aliases: ["hashing trick", "feature hashing", "hash kernel"]
tags: [concept, ranking, features, scale, serving]
created: 2026-08-05
---

# Hashing Trick

## Definition

The hashing trick maps feature names directly to indices in a fixed-size vector
by applying a hash function, instead of maintaining an explicit
feature-name→index dictionary. The hash space size is chosen up front, which
bounds memory regardless of how many distinct features appear.

## Why ranking systems use it

Ranking feature spaces are large and open-ended — every categorical crossing
(destination × month, brand × query token, neighborhood identifiers) multiplies
the vocabulary, and new values appear continuously in production. Two distinct
benefits, at two different stages:

**In training** — variable-size feature vectors become possible without a
vocabulary pass over the data, and the memory footprint stays bounded. This pairs
naturally with online / out-of-core incremental learning over datasets too large
to fit in memory: no dictionary must be held or kept in sync.

**In serving** — the naive approach stores a key-value map from feature to weight,
whose memory footprint becomes problematic at a large feature space. Hashing
removes the map. Lookup cost is on the scale of **nanoseconds**, a negligible
addition to request latency, and memory is capped by the chosen hash length.

## The tradeoff

Distinct features can collide into the same index and share a weight. The
reported practical position is that impact on model performance is **negligible
if the hash space size is chosen correctly** — collisions are spread randomly, so
a colliding pair is unlikely to be two features that both matter strongly for the
same prediction. Size the space too small and this stops being true.

The cost that remains regardless is **interpretability**: an index no longer
names a feature, so inspecting or debugging individual weights requires keeping a
separate mapping that the trick was introduced to avoid.

## Related Concepts

- [[LTR Feature Engineering]] — the feature space this bounds
- [[Learning to Rank]] · [[Feature Store]] — where features are served from
- [[Search Architecture]] — latency and memory budgets at serving time
- [[LSH]] — different goal (similarity preservation), same hashing intuition

## Articles

- [[Beyond Algorithms - Ranking at Scale at Booking.com]] — hashing used in both training and production serving
