---
title: "Wolf Garbe"
aliases: []
tags:
  - person
  - search
created: 2026-05-15
---

# Wolf Garbe

**Known for:** Creator of SymSpell — the symmetric delete spelling correction algorithm
**GitHub:** [wolfgarbe/symspell](https://github.com/wolfgarbe/symspell)

## Areas of Expertise

- Spelling correction algorithms
- Fuzzy string matching
- Fast text preprocessing for search

## Key Innovation

SymSpell achieves **O(1) spelling correction** through pre-computed deletion dictionaries, running up to 1,000,000x faster than Norvig's algorithm for edit distance 3. The core insight: generating only deletions (not all edit operations) during preprocessing makes query-time lookup constant.

## Articles in Awesome Search

- [[1000x Faster Spelling Correction Algorithm - SymSpell]]
- SymSpell vs. BK-Tree (100x faster fuzzy string search)
- Fast Word Segmentation of Noisy Text

## Related Concepts

- [[Spelling Correction]]
- [[Query Understanding]]

## Related People

- [[Daniel Tunkelang]] — Spelling Correction queryunderstanding.com chapter
