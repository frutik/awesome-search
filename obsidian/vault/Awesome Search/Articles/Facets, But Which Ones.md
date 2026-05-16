---
title: "Facets, But Which Ones?"
aliases: ["Which Facets", "Tunkelang Facets Selection"]
tags:
  - clippings
  - search
  - faceted-search
source: "https://queryunderstanding.com/facets-but-which-ones-4a25c9cf3a1f"
author: "Daniel Tunkelang"
created: 2026-05-15
concepts:
  - Faceted Search
  - Query Understanding
  - Personalization
---

# Facets, But Which Ones?

**Source:** https://queryunderstanding.com/facets-but-which-ones-4a25c9cf3a1f
**Author:** [[Daniel Tunkelang]]

## Summary

Not every attribute should become a facet. This article covers strategies for selecting which facets to surface, when to surface them, and how to avoid the **presentation bias** problem.

### Three Strategies for Facet Selection

**1. Supply-Based**
Surface facets that cover the most items in the result set:
- Always shows "full" facets — no misleadingly sparse options
- Problem: may surface attributes users don't care about (e.g., "item weight")

**2. Demand-Based**
Surface facets that users click most often across historical sessions:
- Aligns with user intent and real filtering behavior
- Problem: cold-start for new attribute types; perpetuates existing patterns

**3. Curation / Editorial**
Human editors define the canonical facet set per category:
- High quality for core categories
- Doesn't scale to long-tail categories
- Can be combined with supply/demand signals

### The Presentation Bias Problem
If you always show the same facets, you can't measure demand for facets you didn't show. Classic exploration-exploitation problem:
- Occasionally surface less-common facets to measure latent demand
- A/B test facet sets

### Dynamic Facets
Query-adaptive facets: different queries in the same category may warrant different facets.
- "Red dress" → color facet less useful (already specified); surface occasion/style instead
- "Dress" → color, size, occasion all relevant

### Facet Value Ordering
Within a facet, ordering values matters:
- By count (most items first) — shows what's available
- By predicted relevance — shows what the user probably wants
- Alphabetical — predictable, scannable

## Key Concepts
- **Supply-based facets** — coverage-driven facet selection
- **Demand-based facets** — click-driven facet selection
- **Presentation bias** — can't observe demand for unexposed facets
- **Dynamic facets** — query-adaptive facet sets
- **Facet value ordering** — ranking values within a facet

## Related Concepts
- [[Faceted Search]]
- [[Query Understanding]]
- [[Personalization]]
- [[A-B Testing for Search]]

## Related Articles
- [[Facets - Constraints or Preferences]]
- [[Searching for Goldilocks]]

## People
- [[Daniel Tunkelang]]
