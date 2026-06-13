---
created: 2026-05-16
type: article
tags: [article, elasticsearch, retail, analyzers, query-relaxation, e-commerce, company-blog]
source: "https://www.searchhub.io/en/my-journey-building-elasticsearch-for-retail/"
author: [Rudolf Batt]
company: [searchHub]
concepts: [BM25, Query Understanding, Synonyms]
topics: [E-commerce Search, Relevance Program Setup]
---

# My Journey Building Elasticsearch for Retail

**[[Rudolf Batt]]** (searchHub) shares lessons from building Elasticsearch-based retail search, emphasizing analyzer configuration and query relaxation.

## Analyzer Strategy

Use **multiple sub-fields with different analyzers** rather than a single field:

| Sub-field | Analyzer | Purpose |
|-----------|----------|---------|
| Base field | Minimal (lowercase + whitespace split) | Exact term matching, highest weight |
| `.standard` | Standard (stemming, stop words) | Broader matching |
| `.shingles` | Shingle (n-gram of words) | Compound words ("jackwolfskin" → "jack wolfskin") |
| `.ngram` | N-gram (character level) | Fallback partial match |
| `searchable_numeric_patterns` | Numeric-only | Unit matching ("16 GB", "15 inch") |

Key rule: **base fields have higher weight than analyzed sub-fields**. Disable TF-IDF similarity for structured product data — use `similarity: boolean`.

## Query Relaxation

No single query handles all retail search patterns. Use cascading queries:

1. **Query 1**: Most accurate, strict matching — handles majority
2. **Query 2**: More lenient, allows partial matches — for remaining ~20%
3. **Query 3**: N-gram query — last resort for partial word matching

Zero-result queries are fast even with aggregations. The overhead of 3 queries is only felt for ~20% of searches.

## Key Insight

"There is no silver-bullet query." Analyze your data, measure which queries work, and use regression testing (Quepid) to prevent regressions as you optimize.

## Related Concepts

[[BM25]] · [[Query Understanding]] · [[Synonyms]] · [[E-commerce Search]] · [[Zero Results]]
