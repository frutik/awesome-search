---
type: company
tags: [company, search-optimization, ab-testing, saas, retail]
category: technology-provider
industry: search optimization SaaS
products: [searchHub SmartQuery, searchCollector, OCSS (Open Commerce Search Stack)]
search_domain: [onsite search optimization, query understanding, A/B testing]
use_cases: []
people:
  - "[[Andreas Wagner]]"
  - "[[Siegfried Schüle]]"
  - "[[Rudolf Batt]]"
---

# searchHub

German search optimization SaaS company. Helps e-commerce companies improve onsite search relevance and run statistically valid A/B experiments. Also open-sourced the **Open Commerce Search Stack (OCSS)** for Elasticsearch-based retail search.

## Notable Contributions

**A/B Testing Methodology** — identified two major pitfalls in onsite search experimentation:
1. Session-level randomization with purchase KPIs causes carry-over effect underestimation
2. Session-based basket attribution mixes search-driven and non-search purchases — measuring wrong things

**OCSS** — Elasticsearch multi-analyzer pattern for retail:
- Multiple sub-fields: minimal, standard, shingles, ngram, numeric patterns
- Boolean similarity instead of TF-IDF for product data
- Query relaxation pipeline (3 queries: exact → lenient → ngram)

**SmartQuery** — external spell-checker and query caching layer for Elasticsearch

## Key Articles

- [[Common Pitfalls of Onsite Search Experimentation]]
- [[Common Pitfalls of Onsite Search Experimentation Part 2]]
- [[My Journey Building Elasticsearch for Retail]]
