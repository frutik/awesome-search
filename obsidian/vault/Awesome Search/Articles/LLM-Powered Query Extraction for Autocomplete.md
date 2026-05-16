---
title: "LLM-Powered Query Extraction for Auto-Complete and Auto-Suggest"
source: "https://dpalbrecht.github.io/LLM-Autocomplete-Autosuggest.html"
author: "[[David Albrecht]]"
published: 2025
tags: [autocomplete, autosuggest, LLM, query-generation, cold-start]
---

# LLM-Powered Query Extraction for Auto-Complete and Auto-Suggest

**Author:** [[David Albrecht]]  
**Dataset:** WANDS (43k Wayfair product descriptions), processed with GPT-4.1-nano for <$5

## Problem

Three autocomplete/autosuggest challenges:
1. **Cold-start**: no search activity to draw from
2. **Query-document mismatch**: users search for what they want, not what matches document text
3. **Short phrases**: traditional NLP (SpaCy) produces short, underwhelming phrases

## LLM as Query Extractor

Use an LLM to generate 10 search queries per product description. The LLM uses the document creatively — not just extracting existing words.

Example input:
```
Product Name: trestle coffee table
Description: it is an elegant french design...
```

Example output:
```python
['French design coffee table', 'Elegant rectangular coffee table',
 'Designer living room table', 'Nautical map bar furniture']
```

These are novel, user-like phrases impossible to extract with traditional NLP.

**Cost**: parallel batch with GPT-4.1-nano, several hours for 43k products.

## Auto-Complete

Prefix index built from extracted phrases. At query time, return all phrases starting with prefix (sorted shortest-first).

```python
autocomplete('bed')
# ['bed riser blocks', 'bed security pad', 'bedroom decor rug', ...]
```

Re-ranking by semantic similarity is a suggested improvement.

## Auto-Suggest

Embedding similarity over all extracted phrases. Acts as a semantic fallback when auto-complete has no matches.

```python
autosuggest('nautical furniture')
# [('furniture with nautical elements', 0.963), ('nautical coastal furniture for living room', 0.887), ...]
```

Implemented with `sentence-transformers/all-MiniLM-L6-v2`, normalized cosine similarity.

## Key Insight

Rather than waiting for user behavior to build suggestion corpora, **use the document collection itself** to simulate diverse, realistic queries. Solves cold-start while producing richer phrases than statistical NLP methods.

## Practical Notes

- Online learner (contextual bandit) suggested for managing which completions/suggestions perform over time
- Click data / conversion filtering can clean up low-quality LLM phrases
- For production: use search engine's native prefix capabilities, not this toy prefix index

## Related Concepts

- [[Autocomplete]]
- [[Query Understanding]]

## Related Articles

- [[Autosuggest Retrieval Data Structures and Algorithms]]
- [[Autosuggest Ranking]]
- [[Bootstrapping Autosuggest]]
