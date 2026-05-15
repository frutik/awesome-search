---
title: "Facets: Constraints or Preferences?"
aliases: ["Facets Constraints Preferences", "Tunkelang Facets Constraints"]
tags:
  - clippings
  - search
  - faceted-search
  - ux
source: "https://queryunderstanding.com/facets-constraints-or-preferences-7c25d3a0f4b"
author: "Daniel Tunkelang"
created: 2026-05-15
concepts:
  - Faceted Search
  - Query Understanding
  - Search Intent
---

# Facets: Constraints or Preferences?

**Source:** https://queryunderstanding.com/facets-constraints-or-preferences-7c25d3a0f4b
**Author:** [[Daniel Tunkelang]]

## Summary

Should a facet selection be treated as a **hard filter** (constraint — zero results outside) or a **soft preference** (boost results matching the facet, but don't eliminate others)?

### Hard Constraints
- Boolean filter: only show items matching the selected facet value
- Problem: can create **zero-result pages** when the intersection is empty
- User expectation: "I want ONLY brand X, size Y"

### Soft Preferences
- Boost items matching facet selection in ranking, but don't hard-filter
- Allows graceful degradation: show best matches first, then near-misses
- Problem: may confuse users who expect strict filtering

### The UX Trust Problem
If users believe facets are hard constraints (as most e-commerce facets behave), and the system softens them silently, it erodes trust. Users will see items that don't match and assume the search is broken.

### ML Approach: Inferring Flexibility
Train a model to predict whether a given user + query + facet combination signals a hard constraint vs. soft preference:
- **Features**: query type, facet dimension, user history, result set size
- **Signal**: do users click non-matching items after selecting the facet?

### Design Implications
- For **navigational queries**: hard constraints are appropriate
- For **exploratory queries**: soft preferences improve discovery
- Hybrid: hard-filter but show "did you mean to include X?" suggestions

## Key Concepts
- **Hard constraint** — boolean filter eliminating non-matching items
- **Soft preference** — ranking boost for matching items
- **UX trust** — user mental model of facet behavior
- **Flexibility inference** — ML model to predict constraint vs. preference intent

## Related Concepts
- [[Faceted Search]]
- [[Query Understanding]]
- [[Search Intent]]
- [[Zero Results]]
- [[Query Types]]

## Related Articles
- [[Facets, But Which Ones]]
- [[Searching for Goldilocks]]
- [[Thoughts on Search Result Diversity]]

## People
- [[Daniel Tunkelang]]
