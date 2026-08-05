---
type: company
website: https://www.booking.com
tech_blog: https://booking.ai/
industry: travel / online travel agency / two-sided marketplace
products: [Booking.com accommodation search, flights, car rental, attractions]
search_domain: accommodation search ranking at scale
people: ["[[Themis Mavridis]]", "[[Soraya Hausl]]", "[[Andrew Mende]]", "[[Roberto Pagano]]"]
tags: [company, end-user, travel, marketplace, learning-to-rank]
created: 2026-08-05
---

# Booking.com

One of the world's largest online travel companies, headquartered in Amsterdam.
Millions of accommodations of varied types — chain hotels, private apartments,
guest houses — are listed for customers worldwide. In popular destinations
thousands of properties are available for a single search, which customers cannot
review exhaustively; filtering is used by only a minority. Ranking therefore
carries most of the discovery burden.

## Search context

A [[Two-Sided Marketplace Ranking|two-sided marketplace]] ranking problem with
several simultaneous objectives: matching customer preferences, delivering
consistent exposure to accommodation providers, and giving partners tools to
influence their visibility. Published work scopes to the customer objective as
the most important of the three.

## Engineering positions worth knowing

- **Reservations as the primary positive label**, with clicks and dwell-gated
  clicks as secondary positives; skip-above impressions as negatives. See
  [[Ranking Signal Selection]].
- **Latent property representations** via [[Word2Vec]] over sequences of user
  actions, because explicit attributes describe heterogeneous inventory poorly —
  star ratings exist for hotels but not apartments.
- **Three named biases**: [[Impression Bias]], [[Position Bias]], and user bias
  (heavy users dominating training data).
- **[[Isolated Feedback Loops]]** for experiment integrity, addressing re-training
  and feature leakage between RCT arms.
- **Team-draft [[Interleaving]]** for ranker preselection, reported as offering
  10–100x experimentation speedup, with the stated limitation that it cannot
  estimate effect size.
- **[[Out-of-Time Validation]]** (walk-forward), with testing over all *available*
  properties rather than only displayed ones.
- **Sharded serving** — destination-to-property reverse index per shard, partial
  top-N merged by a coordinator; enables precomputed availability at the cost of
  no global availability visibility.
- **[[Hashing Trick]]** in both training and production serving.
- **Architectural arc**: years of incrementally added ML components eventually
  plateaued; consolidating them into a single full-scale Machine Learned ranker
  produced the largest reported step change.

## Experimentation culture

Randomized controlled trials are long-established in product development at
Booking.com, with published work on democratizing online controlled experiments
(Kaufman, Pitchforth & Vermeer, 2017) and on mediation analysis for disentangling
direct and indirect effects (Öztan et al., 2018). The widely-cited *150 Successful
Machine Learning Models: 6 Lessons Learned at Booking.com* (Bernardi, Mavridis &
Estevez, KDD 2019) comes from the same organisation.

## Articles

- [[Beyond Algorithms - Ranking at Scale at Booking.com]] — modelling, experimentation, and serving
- [[Paper Review - Ranking at Scale at Booking.com]] — third-party review (paywalled)

## People

- [[Themis Mavridis]] · [[Soraya Hausl]] · [[Andrew Mende]] · [[Roberto Pagano]]

## Related

- [[Airbnb]] — the closest comparable accommodation-marketplace ranking published work
- [[Skyscanner]] — travel meta-search with booking-completion labels
- [[Two-Sided Marketplace Ranking]] · [[E-commerce Search]]
