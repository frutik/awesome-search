---
title: "Targeting Broad Queries in Search"
tags:
  - clippings
  - search
  - query-understanding
  - case-study
source: "https://codeascraft.com/2015/07/29/targeting-broad-queries-in-search/"
author: "Etsy Engineering"
created: 2026-05-15
concepts:
  - Query Understanding
  - Query Types
  - Diversity Metrics
---

# Targeting Broad Queries in Search

**Source:** https://codeascraft.com/2015/07/29/targeting-broad-queries-in-search/
**Author:** Etsy Engineering

## Summary

Etsy's approach to handling "broad" or "head" queries — high-volume, ambiguous queries like "necklace" or "bag" that have many valid interpretations. These queries require diversity and exploration rather than precision.

## The Problem

Broad queries cover a huge semantic space. A user searching "necklace" might want:
- Gold vs. silver
- Minimalist vs. statement
- Budget vs. luxury
- Handmade vs. manufactured

Standard relevance scoring fails here — there's no single "best" document.

## Approach: Diversity Over Precision

For broad queries, Etsy shifted objective from "find the best matching item" to "show a diverse, representative sample of the space." Techniques:
- **Query classification**: identify whether a query is broad/head vs. navigational/specific
- **Diversity injection**: ensure results span multiple interpretations
- **Thermodynamic analogy**: use entropy-based metrics to measure and optimize for result diversity (see [[How Etsy Uses Thermodynamics for Search]])

## Related Concepts

- [[Query Types]]
- [[Query Understanding]]
- [[Diversity Metrics]]
- [[Search Intent]]
- [[Faceted Search]]

## Related Articles

- [[How Etsy Uses Thermodynamics for Search]]
- [[Broad and Ambiguous Search Queries]]
- [[Deconstructing E-Commerce Search - The 12 Query Types]]
