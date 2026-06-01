---
title: "Broad and Ambiguous Search Queries"
tags:
  - clippings
  - search
  - query-understanding
  - medium
source: "https://medium.com/@dtunkelang/broad-and-ambiguous-search-queries-1bbbe417dcc"
author: "Daniel Tunkelang"
created: 2026-05-15
concepts:
  - Query Types
  - Query Understanding
  - Diversity Metrics
  - Search Intent
---

# Broad and Ambiguous Search Queries

**Source:** https://medium.com/@dtunkelang/broad-and-ambiguous-search-queries-1bbbe417dcc
**Author:** [[Daniel Tunkelang]]

## Summary

Exploration of the challenge that broad and ambiguous queries pose for search systems. These queries have multiple valid interpretations and require diversity/disambiguation strategies rather than precision optimization.

## Types of Broad/Ambiguous Queries

- **Broad**: "shoes" — clear topic but enormous scope
- **Ambiguous**: "apple" — genuinely unclear intent (fruit vs. company vs. color)
- **Vague**: "good stuff" — undefined quality criterion

## Why Standard Ranking Fails

Relevance algorithms optimize for the "best" single interpretation. For broad queries:
- The "best" interpretation may serve only a fraction of users
- Result homogeneity leaves many users unserved
- Users who don't see their intent represented will reformulate or leave

## Strategies

1. **Diversify results** — represent multiple interpretations in the result set
2. **Clarification queries** — prompt user to narrow intent (risky: adds friction)
3. **Personalization** — infer likely intent from user context
4. **[[Faceted Search]]** — let users self-select their interpretation dimension

## Related Concepts

- [[Query Types]]
- [[Query Understanding]]
- [[Search Intent]]
- [[Diversity Metrics]]
- [[Faceted Search]]
- [[Zero Results]]

## People

- [[Daniel Tunkelang]]

## Related Articles

- [[Targeting Broad Queries in Search]]
- [[How Etsy Uses Thermodynamics for Search]]
- [[Query Understanding - Introduction]]
