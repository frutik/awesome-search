---
type: person
tags: [person, elasticsearch, retail, search-engineering]
name: Rudolf Batt
affiliation: searchHub
role: Search Engineer
articles: []
key_contributions: [elasticsearch-retail-analyzers, query-relaxation-pipeline]
---

# Rudolf Batt

Search Engineer at **searchHub**. Author of practical guidance on building Elasticsearch-based retail search.

## Key Contributions

- **Multi-analyzer strategy for retail**: Use base field (minimal analyzer) + sub-fields (standard, shingles, ngram, numeric patterns). Disable TF-IDF (`similarity: boolean`) for structured product data.
- **Query relaxation pipeline**: 3-query cascade (exact → lenient → ngram) handles the full spectrum of search patterns without a single "silver-bullet" query.

## Related Articles

- [[My Journey Building Elasticsearch for Retail]]

## Related Companies

- [[searchHub]]
