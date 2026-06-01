---
title: "Facets of Faceted Search"
tags:
  - clippings
  - search
  - faceted-search
  - ux
  - medium
source: "https://medium.com/@dtunkelang/facets-of-faceted-search-38c3e1043592"
author: "Daniel Tunkelang"
created: 2026-05-15
concepts:
  - Faceted Search
  - Search Intent
  - Query Understanding
---

# Facets of Faceted Search

**Source:** https://medium.com/@dtunkelang/facets-of-faceted-search-38c3e1043592
**Author:** [[Daniel Tunkelang]]

## Summary

Foundational overview of [[Faceted Search]] — what it is, how it works, and the design decisions that make or break a faceted navigation experience.

## What Faceted Search Is

Faceted search lets users progressively narrow a result set by selecting values from multiple independent attribute dimensions (facets). Each facet selection filters results, and facet counts update dynamically to reflect the remaining set.

## Constraints vs. Preferences

Key distinction (explored further in Tunkelang's "Facets: Constraints or Preferences?"):
- **Constraints**: hard filters — "must have free shipping"
- **Preferences**: soft signals — "prefer red, but would accept blue"

Most systems implement only hard constraints. Preference-based faceting (using soft ranking signals) better models actual user behavior.

## Dynamic vs. Static Facets

- **Static**: always show the same facets
- **Dynamic**: infer relevant facets from query context (e.g., "running shoes" → show surface/support, not color first)

Query-aware dynamic facets significantly improve the experience for non-trivial queries.

## The "Which Facets?" Problem

Not all attributes make useful facets. Good facets:
- Have meaningful variance across the result set
- Reflect how users actually think about the category
- Have manageable cardinality (not 10,000 unique values)

## Related Concepts

- [[Faceted Search]]
- [[Search Intent]]
- [[Query Understanding]]
- [[Query Types]]
- [[Zero Results]]

## People

- [[Daniel Tunkelang]]

## Related Articles

- [[Query Understanding - Introduction]]
- [[Deconstructing E-Commerce Search - The 12 Query Types]]
