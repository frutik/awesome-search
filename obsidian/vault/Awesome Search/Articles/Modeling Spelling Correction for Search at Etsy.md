---
title: "Modeling Spelling Correction for Search at Etsy"
tags:
  - clippings
  - search
  - spelling-correction
  - case-study
  - company-blog
source: "https://codeascraft.com/2017/05/01/modeling-spelling-correction-for-search-at-etsy/"
author: "Etsy Engineering"
created: 2026-05-15
concepts:
  - Spelling Correction
  - Query Understanding
---

# Modeling Spelling Correction for Search at Etsy

**Source:** https://codeascraft.com/2017/05/01/modeling-spelling-correction-for-search-at-etsy/
**Author:** Etsy Engineering

## Summary

How Etsy built a production spelling correction system for search, moving beyond simple dictionary-based approaches to a context-aware ML model. Demonstrates the difference between academic spelling correction and real-world search query correction.

## The Search Context Problem

E-commerce spelling correction has unique challenges vs. general-purpose correction:
- Etsy items have non-standard names ("steampunk", "cottagecore")
- User query typos often involve category-specific terms not in standard dictionaries
- Some "misspellings" are valid Etsy-specific terms that should NOT be corrected

## Approach

Used noisy-channel model similar to [[How to Write a Spelling Corrector|Norvig's algorithm]] as the base, extended with:
- **Domain-specific language model**: trained on Etsy query logs (not generic corpus)
- **Search-specific signals**: click data to validate corrections
- **Precision guards**: avoid correcting valid uncommon terms

## Key Principle

The correction model must know what's on the platform — a query for "cottagecore" should not be corrected to "cottage core" or "core" even if it's rare in a general corpus.

## Related Concepts

- [[Spelling Correction]]
- [[Query Understanding]]
- [[BM25]]
- [[Zero Results]]

## Related Articles

- [[How to Write a Spelling Corrector]]
- [[1000x Faster Spelling Correction Algorithm - SymSpell]]
- [[Targeting Broad Queries in Search]]
