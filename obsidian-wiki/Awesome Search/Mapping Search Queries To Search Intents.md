---
title: "Mapping Search Queries To Search Intents"
source: "https://dtunkelang.medium.com/search-queries-and-search-intent-1dec79ad155f"
author:
  - "[[Daniel Tunkelang]]"
published: 2020-08-10
created: 2026-05-15
description: "Explores how to recognize when different search queries represent the same underlying intent, and how this recognition improves search through rewriting, analytics, and ML."
tags:
  - clippings
---

# Mapping Search Queries To Search Intents

## Core Insight

"Search queries are not the same as search intents." Multiple distinct queries can map to a single intent (e.g., "mens shoes" and "shoes for men").

## Recognizing Query Equivalence

**Surface Query Similarity**
Queries differing only in stemming, lemmatization, word order, or stop words often express identical intent. Includes singular/plural variations and compound word differences.

**Similar Post-Search Behavior**
Equivalent-intent queries generate matching user engagement patterns. Behavioral similarity can be represented using vector embeddings of result titles.

## Combined Approach

1. Group queries by surface similarity via canonicalization (stem tokens, alphabetize, remove stop words)
2. Split groups into behavioral clusters using vector cosine similarity

This ensures paired queries demonstrate both linguistic AND behavioral equivalence — preventing false positives like "dress shirt" vs. "shirt dress."

## Tradeoffs

| Approach | Pros | Cons |
|---|---|---|
| Surface similarity only | Minimizes false positives | Misses synonyms and reformulations |
| Behavioral only | Captures semantic equivalence | Risks conflating different intents (e.g., "pants" vs. "dress pants") |
| Combined | Best precision + recall | More complex to implement |

## Applications

- **Query Rewriting**: Convert equivalent queries to canonical representations optimizing retrieval/ranking
- **Analytics**: Aggregate fragmented behavioral signals across equivalent queries
- **Machine Learning**: Use consolidated signals for more robust model training


## Related Concepts

- [[Search Intent]]
- [[Query Understanding]]
- [[Query Types]]
- [[Session-Based Evaluation]]

## People

- [[Daniel Tunkelang]]
