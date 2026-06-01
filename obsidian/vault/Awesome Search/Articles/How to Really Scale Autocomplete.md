---
title: "How to Really Scale Autocomplete"
source: "https://bonsai.io/blog/how-to-really-scale-autocomplete/"
author: "bonsai.io"
published: 2025-07-18
tags: [autocomplete, elasticsearch, opensearch, scaling, aggregations, company-blog]
---

# How to Really Scale Autocomplete

**Source:** bonsai.io (Part 2 of series)

## Problem

Part 1's approach (significant_terms on shingles) collapsed at 6M Wikipedia documents: 4+ second queries, CPU at 100%, widespread timeouts. The `significant_phrases` aggregation with shingles explodes cardinality at millions of docs.

## Solution Architecture

### Schema

- `completions`: `search_as_you_type` field (max_shingle_size: 3) — fast prefix matching for page titles
- `suggest_word_all`: text field with fielddata (for `significant_terms` aggregation on words)
- `suggest_phrase`: text field with shingles analyzer + fielddata (for phrase aggregation)
- Views column as primary relevance signal (log1p boosting)

### Query Pattern

```json
{
  "query": {
    "function_score": {
      "query": {"match_phrase_prefix": {"completions": {"query": q, "boost": 0.01}}},
      "field_value_factor": {"field": "views", "modifier": "log1p"}
    }
  },
  "aggs": {
    "significant_words": {"significant_terms": {"field": "suggest_word_all", "include": "q+.*"}},
    "significant_phrases": {"terms": {"field": "suggest_phrase", "include": "q+.*"}}
  }
}
```

**Key change from Part 1**: `significant_phrases` replaced with plain `terms` aggregation (frequency-ordered). This is fast because the prefix filter narrows to thousands of docs.

## Performance Results

- **416 req/s** at p99 ≤ 45ms, warm index
- With simultaneous hybrid search on same cluster: **~96 autocomplete req/s + 96 hybrid req/s** both within SLA

## Implementation Notes

- Use a **separate index** for autocomplete — different scaling profile than main search
- **Debounce 25-50ms** before firing (saves requests, only fires on user pause)
- Watch `fielddata` memory if corpus grows very large

## Co-occurrence Sugar

After a user selects a suggestion, a follow-up query using `significant_terms` with `exclude: q` reveals semantically related terms (co-occurrence):

- "elasticsearch" → `['kibana', 'lucene', 'opensearch', 'solr']`
- "bidirectional encoder" → `['nlp', 'transformer', 'devlin', 'bert']`

Useful for guiding discovery/navigation without manual curation.

## Related Concepts

- [[Autocomplete]]
- [[Search Architecture]]
- [[Faceted Search]]
