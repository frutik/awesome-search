---
type: article
tags: [article, autocomplete, autosuggest, radix-tree, fst, lucene, data-structures]
source: "https://spinscale.de/posts/2023-01-18-mirror-mirror-what-am-i-typing-next.html"
author: []
company: []
concepts: [Autocomplete]
topics: [Autocomplete and Autosuggest]
---

# Mirror, Mirror: All About Search Suggestions

A deep technical dive into autosuggest data structures and implementations, from naive list to production-grade FSTs.

## Data Structures Compared

### 1. Sorted List
Simple O(n) prefix scan. Works for tiny datasets, scales badly.

### 2. Radix Tree (Adaptive)
Prefix lookups in O(k) where k = query length. Memory-efficient — common prefixes stored once. Java: `concurrent-trees` library.

**Problem**: No weighted ordering — responses sorted alphabetically, not by relevance.

### 3. Pruning Radix Trie
Stores **maximum weight of subtree** at each internal node. Enables early exit: skip entire subtrees whose max weight is below the k-th best result found so far. Result: sorted-by-weight top-k in O(k × depth) instead of retrieving all matches first.

Created by **[[Wolf Garbe]]** (SymSpell author). Java implementation: `JPruningRadixTrie`.

### 4. Weighted FST (Lucene WFST)
`WFSTCompletionLookup` in Lucene's suggest package. Immutable but serializable; slightly faster than pruning radix trie for longer prefixes.

### 5. Elasticsearch
- **completion suggester**: pure prefix, fast, supports contexts (category filter)
- **search_as_you_type field type**: regular search with block-max WAND optimization; supports analyzers, synonyms, LTR plugin, re-scoring

## Typo Handling
- **FuzzySuggester** (Lucene): Levenshtein automata; max edit distance 2
- **Phonetic analyzer**: sounds-like matching (ColognePhonetic); good for names
- **SymSpell**: fastest known approach for spelling correction; standalone implementations

## Ranking Weights
Weight sources: search logs (successful queries), purchase data, recency signals, personalization. LTR + rescoring stage after initial retrieval is the production-grade approach.

## Key Takeaway
Two-stage pipeline: fast pruning radix trie or WFST for top-N retrieval → ML rescoring (XGBoost via Vespa or LTR plugin via Elasticsearch) for personalized/recency-aware ranking.
