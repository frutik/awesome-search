---
title: "Synonyms"
aliases: ["synonym expansion", "query expansion", "lexical synonyms", "semantic synonyms"]
tags:
  - concept
  - search
  - query-understanding
created: 2026-05-15
---

# Synonyms

Vocabulary bridging technique that maps alternative phrasings, abbreviations, and related terms to shared canonical tokens, improving recall for queries that don't lexically match indexed content.

## Types

### Lexical Synonyms
Direct word-level equivalences: "sofa" → "couch", "tv" → "television"

### Semantic Synonyms
Contextually equivalent terms in a domain: "heart attack" → "myocardial infarction"

### Product/Domain Synonyms
E-commerce specific: "shirt" → "top", "blouse", "tee"

### Abbreviations
"ml" → "machine learning", "ir" → "information retrieval"

## Application Points

Synonyms can be applied at:
1. **Index time** — expand document terms during ingestion
2. **Query time** — expand the query before retrieval
3. **Both** — risk of explosion in index size

## Trade-offs

| Expansion Point | Pros | Cons |
|---|---|---|
| Index time | Fast query execution | Index bloat, static |
| Query time | Flexible, updatable | Slower, affects all queries |

## Automated Synonym Discovery

- Word2Vec / fastText neighborhood mining
- Co-click analysis (users click same doc for different queries)
- LLM-generated synonym sets
- Query log clustering

## Relationship to Dense Search

[[Dense Vector Retrieval]] handles some synonym problems implicitly — semantically similar terms map to nearby vectors. However, rare domain terms and abbreviations still benefit from explicit synonym lists.

## Related Concepts

- [[Query Understanding]]
- [[BM25]]
- [[Spelling Correction]]
- [[Zero Results]]
- [[Hybrid Search]]
