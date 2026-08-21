---
type: topic
title: "Two-Sided Marketplace Ranking"
aliases: ["marketplace ranking", "two-sided marketplace", "supply-side ranking"]
related_concepts: ["[[Learning to Rank]]", "[[Ranking Objectives]]", "[[Ranking Signal Selection]]", "[[Impression Bias]]", "[[Exploration vs Exploitation]]", "[[Results Boosting]]", "[[Economics of Search]]"]
related_topics: ["[[E-commerce Search]]", "[[Personalization in Search]]", "[[Search Result Diversity]]"]
tags: [topic, ranking, marketplace, e-commerce]
created: 2026-08-05
---

# Two-Sided Marketplace Ranking

Ranking where the items being ranked are supplied by **independent sellers who
have their own commercial interests**, rather than by the platform itself.
Accommodation, classifieds, freelance marketplaces, ride-hailing, and most large
e-commerce platforms are two-sided; a single-vendor product catalogue is not.

The defining property: **the ranker's output changes supplier behavior**, and
suppliers actively work to influence the ranker. This closes a loop that
single-sided search does not have.

## The competing objectives

A marketplace ranker is asked to satisfy at least three things at once:

1. **Demand side** — surface items that match what the searcher wants
2. **Supply side** — deliver a consistent, defensible level of exposure to
   suppliers, since a supplier who receives no traffic eventually leaves
3. **Supplier agency** — provide levers (promotions, boosted placement, paid
   visibility) that let suppliers influence rank according to their own strategy

These conflict. Guaranteeing exposure to weak inventory costs relevance;
selling placement costs both. Booking.com's published position is to name all
three and then optimize explicitly for the customer objective as "by far the most
important" — a scoping decision, not a claim that the others don't matter.

## Structural consequences

**Conversion as the label.** The natural target is booking or purchase rather
than click, because the marketplace is paid on conversion. That choice is sparse
and delayed — see [[Ranking Signal Selection]].

**Cold start is permanent, not initial.** New supply arrives continuously. Every
new listing has no engagement history, and [[Impression Bias]] means the ranker
withholds the exposure that would generate it. Latent/content representations and
[[Exploration vs Exploitation|exploration]] budgets are structural necessities,
not optimizations.

**Heterogeneous inventory defeats shared schemas.** Attributes that describe one
supply type may not exist for another — star ratings apply to hotels but not
apartments. Latent representations learned from behavior (e.g. [[Word2Vec]] over
user action sequences, or Airbnb's listing embeddings) sidestep the schema
mismatch.

**Suppliers optimize against the ranker.** Because rank determines revenue,
suppliers have a standing incentive to work out what the ranker rewards and
adjust accordingly. Booking.com's stated design accommodates this directly by
giving partners tools to influence their visibility according to their sales
strategy — supplier optimization is an expected behavior of the system, not an
abuse of it. The practical consequence for the platform is that ranking changes
and exposure allocation are observed and reacted to by a motivated counterparty.

**Fairness and exposure become measurable obligations.** Because exposure is the
supplier's livelihood, allocation of impressions is a first-class concern rather
than a side effect of relevance ordering. This connects to
[[Search Result Diversity]] and diversity metrics.

## In this vault

**Accommodation and travel**
- [[Beyond Algorithms - Ranking at Scale at Booking.com]] — [[Booking.com]]; the demand-side build
- [[Machine Learning-Powered Search Ranking of Airbnb Experiences]] · [[Listing Embeddings in Search Ranking]] — [[Airbnb]]
- [[Learning to Rank for Flight Itinerary Search]] — [[Skyscanner]]; meta-search, booking as label

**Marketplaces and classifieds**
- [[Etsy]] · [[Vinted]] · [[Kleinanzeigen]] · [[Carousell]] · [[Otto]]

## Related Concepts

- [[Ranking Signal Selection]] — conversion vs click as target
- [[Impression Bias]] · [[Exploration vs Exploitation]] — the supply cold-start loop
- [[Ranking Objectives]] — multi-objective formulation
- [[Results Boosting]] · [[Results Merchandising]] — the business-lever surface
- [[Economics of Search]] — why the levers exist
- [[Isolated Feedback Loops]] — experimenting inside a behavioral feedback loop

## Related Topics

- [[E-commerce Search]] · [[Personalization in Search]] · [[Search Result Diversity]] · [[Tuning BM25 for E-commerce Search]] — keyword-stuffing as a ranking-incentive problem on seller-controlled fields
