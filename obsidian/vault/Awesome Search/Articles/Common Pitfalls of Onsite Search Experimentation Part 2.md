---
created: 2026-05-16
type: article
tags: [article, ab-testing, experimentation, basket-attribution, kpi, company-blog]
source: "https://www.searchhub.io/en/common-pitfalls-of-onsite-search-experimentation-part-2/"
author: [Siegfried Schüle]
company: [searchHub]
concepts: [A-B Testing, Session-Based Evaluation]
topics: [A-B Testing for Search]
---

# Common Pitfalls of Onsite Search Experimentation Part 2

**[[Siegfried Schüle]]** (searchHub) exposes the basket attribution trap in search A/B testing.

## The Problem: Testing the Wrong Thing

**Intended test**: How does the new ranking algorithm affect search result page performance?  
**Actual test** (with standard analytics tools): All carts and orders of users who performed *any* search during their visit.

The mismatch: a user browses a newsletter link → adds first item → then uses search for additional items. Standard analytics attributes the entire basket to "sessions with site search," even though the first item had nothing to do with search.

## Why This Fails Statistically

- Searches are many; orders are few. A 10% search improvement → ~10% order improvement, but the signal is diluted in the large "sessions with site search" denominator.
- With small uplift signals and low order-to-visit ratios, standard A/B test tools report **no significant difference** even when the improvement is real.
- Amazon/Google have enough volume to detect these signals. Smaller e-commerce sites must dig deeper.

## Solution

1. Track the customer journey from search bar to basket at the **item level** — identify which basket positions were driven by search vs. other sources
2. Measure only on the search-attributable portion: "average add-to-basket value from search-initiated journeys"
3. **Don't rely on summarized session-level numbers** that include non-search basket decisions

## Key Rule

*"First: Make sure you're precisely measuring the stuff you want to measure."*

## Related Concepts

[[A-B Testing]] · [[Session-Based Evaluation]] · [[A-B Testing for Search]]
