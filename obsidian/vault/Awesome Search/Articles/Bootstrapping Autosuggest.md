---
title: "Bootstrapping Autosuggest"
tags:
  - clippings
  - search
  - autocomplete
  - ux
source: "https://medium.com/related-works-inc/bootstrapping-autosuggest-c1ca3edaf1eb"
author: "Giovanni Fernandez-Kincade"
created: 2026-05-15
concepts:
  - Autocomplete
  - Query Understanding
---

# Bootstrapping Autosuggest

**Source:** https://medium.com/related-works-inc/bootstrapping-autosuggest-c1ca3edaf1eb
**Author:** [[Giovanni Fernandez-Kincade]] (Related Works)

## Summary

First in a five-part series on building [[Autocomplete]] (autosuggest) from scratch. Establishes the goal-setting framework before implementation: distinguish between completing the query in users' minds vs. recommending new discovery paths.

## Key Distinction: Prediction vs. Recommendation

> "Our ultimate goal isn't for users to select precisely the query they had in mind, it's to help them find something useful."

This reframe shifts autosuggest from pure query completion toward guided discovery — critical for exploratory search contexts (e.g., cultural collections, discovery-oriented e-commerce).

## Metrics for Autosuggest

- **MRR** — does the right suggestion appear early?
- **Acceptance Rate** — % of searches initiated from a suggestion
- **Average Prefix Length** — how many characters before selection (lower = better)
- **Post-selection engagement** — did users find what they needed after clicking?

## Series Parts

1. **Bootstrapping** (this article) — framing and goals
2. **Building an Autosuggest Corpus, Part 1** — data sourcing
3. **Building an Autosuggest Corpus, Part 2** — NLP processing
4. **Autosuggest Retrieval Data Structures & Algorithms** — prefix trie, FST
5. **Autosuggest Ranking** — scoring and ordering suggestions

## Related Concepts

- [[Autocomplete]]
- [[Query Understanding]]
- [[MRR]]
- [[Zero Results]]

## Related Articles

- [[13 Design Patterns for Autocomplete Suggestions]]
- [[Query Understanding - Introduction]]
