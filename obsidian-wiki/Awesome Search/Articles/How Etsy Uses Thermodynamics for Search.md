---
title: "How Etsy Uses Thermodynamics to Help You Search for 'Geeky'"
tags:
  - clippings
  - search
  - ranking
  - diversity
  - case-study
source: "https://codeascraft.com/2015/08/31/how-etsy-uses-thermodynamics-to-help-you-search-for-geeky/"
author: "Etsy Engineering"
created: 2026-05-15
concepts:
  - Diversity Metrics
  - Query Types
  - BM25
---

# How Etsy Uses Thermodynamics to Help You Search for "Geeky"

**Source:** https://codeascraft.com/2015/08/31/how-etsy-uses-thermodynamics-to-help-you-search-for-geeky/
**Author:** Etsy Engineering

## Summary

Etsy applies concepts from statistical thermodynamics — specifically entropy — to measure and optimize result diversity for broad, ambiguous queries. Companion piece to [[Targeting Broad Queries in Search]].

## The Thermodynamics Analogy

In thermodynamics, **entropy** measures disorder/spread of a system. Applied to search results:
- **Low entropy** = results all look similar (converged, narrow)
- **High entropy** = results span many categories and styles (diverse, exploratory)

For a query like "geeky", optimal results have high entropy — they should show geeky necklaces, t-shirts, mugs, art prints, etc., not five variations of the same item.

## Key Technical Idea

1. **Measure result entropy** using Shannon entropy over category/attribute distributions
2. **Set entropy targets** per query based on query type (broad = high target, specific = low)
3. **Re-rank or inject** results to meet entropy target while maintaining base relevance

## Why This Matters

Pure relevance ranking on broad queries produces "winner takes all" results — the most popular category dominates. Entropy-based diversification corrects this by ensuring the result set represents the full intent space.

## Related Concepts

- [[Diversity Metrics]]
- [[Query Types]]
- [[Query Understanding]]
- [[BM25]]

## Related Articles

- [[Targeting Broad Queries in Search]]
- [[Broad and Ambiguous Search Queries]]
