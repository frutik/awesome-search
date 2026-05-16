---
title: "Autosuggest Retrieval Data Structures & Algorithms"
aliases: ["Autosuggest Retrieval", "Giovanni Autosuggest Retrieval"]
tags:
  - clippings
  - search
  - autocomplete
  - data-structures
source: "https://medium.com/@dtunkelang/autosuggest-retrieval-data-structures-algorithms"
author: "Giovanni Fernandez-Kincade"
created: 2026-05-15
concepts:
  - Autocomplete
  - Search Architecture
---

# Autosuggest Retrieval Data Structures & Algorithms

**Source:** https://medium.com/@dtunkelang/autosuggest-retrieval-data-structures-algorithms
**Author:** [[Giovanni Fernandez-Kincade]]

## Summary

A deep dive into the data structures and algorithms used to retrieve autocomplete candidates given a prefix (or fuzzy match). Part 1 of a two-part series; Part 2 covers ranking.

### The Core Problem
Given a user typing "sho", return the top candidate completions (e.g., "shoes", "shorts", "shopping bags") in under 50ms. The challenge is both algorithmic (fast prefix lookup) and scale (billions of query candidates).

### Data Structure 1: Trie
The classic prefix tree:
- Each node is a character; paths spell out strings
- Prefix lookup: O(|prefix|) to find all completions
- **Problem**: memory-intensive for large vocabularies; doesn't support fuzzy matching

### Data Structure 2: FST (Finite State Transducer)
Compressed trie that maps strings to values:
- Much more memory-efficient than naive trie
- Supports exact prefix lookup and constrained fuzzy matching
- Used in Lucene/Elasticsearch for suggest implementations
- **Trade-off**: complex to build incrementally; batch construction is standard

### Data Structure 3: DFA (Deterministic Finite Automaton)
Used for fuzzy matching (edit-distance-bounded prefix lookup):
- Levenshtein DFA accepts all strings within edit distance k of the prefix
- Intersect Levenshtein DFA with the suggestion trie to get fuzzy completions
- Enables "sho" to match "shoe" (deletion) or "shos" to match "shoes" (substitution)

### Data Structure 4: N-gram Index
Index all character n-grams from suggestion strings:
- "shoes" → {"sho", "hoe", "oes", "shoe", "hoes", "shoes", ...}
- Lookup by prefix n-gram, union results
- Fast for small n; degrades for large vocabularies
- Good for infix matching ("oes" finds "shoes")

### Data Structure 5: Edge N-grams
Elasticsearch's built-in approach:
- Index prefixes at each edge: "shoes" → ["s", "sh", "sho", "shoe", "shoes"]
- Standard inverted index lookup for the current prefix
- Simple and fast; no fuzzy support; larger index size

### Memory vs. Computation Trade-offs

| Structure | Memory | Speed | Fuzzy | Build Complexity |
|-----------|--------|-------|-------|-----------------|
| Trie | High | Fast | No | Low |
| FST | Low | Fast | Limited | High |
| Levenshtein DFA | Medium | Medium | Yes | Medium |
| N-gram index | High | Fast | Yes | Low |
| Edge N-grams | Medium | Fast | No | Low |

## Key Concepts
- **Trie** — character-level prefix tree for exact prefix lookup
- **FST** — compressed trie with efficient memory use
- **Levenshtein DFA** — fuzzy prefix matching via edit-distance automaton
- **N-gram index** — character n-gram indexing for flexible matching
- **Edge N-grams** — simple prefix indexing in inverted index

## Related Concepts
- [[Autocomplete]]
- [[Search Architecture]]
- [[Spelling Correction]]

## Related Articles
- [[Autosuggest Ranking]]
- [[Spelling Correction in Search]]

## People
- [[Giovanni Fernandez-Kincade]]
