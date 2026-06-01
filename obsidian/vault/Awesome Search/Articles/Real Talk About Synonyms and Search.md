---
title: "Real Talk About Synonyms and Search"
tags:
  - clippings
  - search
  - synonyms
  - query-understanding
  - medium
source: "https://medium.com/@dtunkelang/real-talk-about-synonyms-and-search-bb5cf41a8741"
author: "Daniel Tunkelang"
created: 2026-05-15
concepts:
  - Synonyms
  - Query Understanding
  - BM25
---

# Real Talk About Synonyms and Search

**Source:** https://medium.com/@dtunkelang/real-talk-about-synonyms-and-search-bb5cf41a8741
**Author:** [[Daniel Tunkelang]]

## Summary

Pragmatic discussion of synonyms in search — why they're harder than they look and how to implement them responsibly. Cuts through the appeal of "just add synonyms" as a quick fix.

## Why Synonyms Are Harder Than They Look

### Directional vs. Bidirectional
- "Sofa" → "couch" should be bidirectional
- "Laptop" → "MacBook Pro" should be **one-way** (expanding the category, not equating them)
- Getting directionality wrong causes precision loss

### Scope Sensitivity
Synonyms that work in one context break in another:
- "Bark" → "tree bark" and "bark" → "dog bark" cannot both be synonyms
- Domain and query context must gate synonym application

### Maintenance Problem
Synonym dictionaries rot. "iPhone 5" synonyms, seasonal trends, brand changes — someone must maintain them or quality degrades over time.

## Relationship to Dense Search

[[Dense Vector Retrieval]] handles many synonym problems implicitly — semantically similar terms cluster in embedding space. But:
- Rare domain terms may not appear in training data
- Abbreviations and brand names need explicit handling
- Dense vectors don't replace synonyms; they complement them

## Recommendations

1. Start with one-way synonyms from high-confidence known pairs
2. Monitor precision impact — add sparingly, not exhaustively
3. Use [[Zero Results]] rate as a leading signal that synonyms are needed
4. Audit automatically with click data: if synonym expansion leads to zero clicks, it's wrong

## Related Concepts

- [[Synonyms]]
- [[Query Understanding]]
- [[BM25]]
- [[Zero Results]]
- [[Dense Vector Retrieval]]

## People

- [[Daniel Tunkelang]]

## Related Articles

- [[Query Understanding - Introduction]]
- [[Broad and Ambiguous Search Queries]]
