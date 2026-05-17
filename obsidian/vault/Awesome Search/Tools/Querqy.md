---
title: Querqy
type: tool
tags:
  - tool
  - query-rewriting
  - search-relevance
website: https://querqy.org/
repo: https://github.com/querqy/querqy
created: 2026-05-17
---

# Querqy

Open-source query rewriting library for Elasticsearch, OpenSearch, and Solr. Provides a structured framework for applying manual query rewriting rules (synonyms, boosts, filters, redirects) at query time.

---

## Overview

Querqy separates query rewriting rules from search engine configuration, making them manageable, testable, and version-controlled. It is the foundation for the [Chorus](https://github.com/querqy/chorus) e-commerce search reference stack and the [SMUI](https://github.com/querqy/smui) rules management UI.

- Website: https://querqy.org/
- GitHub: https://github.com/querqy/querqy

## Key Capabilities

- **Synonym rules** — managed multi-word synonym expansion
- **Boost/bury rules** — per-query result promotion or demotion
- **Filter rules** — add filters to specific queries
- **Delete terms** — remove terms from queries (query relaxation)
- **Redirect rules** — send specific queries to landing pages

## Related Ecosystem

- **SMUI** (https://github.com/querqy/smui) — UI for managing Querqy rules
- **Chorus** (https://github.com/querqy/chorus) — e-commerce search reference stack built on Querqy

## Related Concepts
- [[Synonyms]] — Querqy's most common use case
- [[Query Relaxation]] — delete terms to increase recall
- [[Search Governance]] — Querqy as a governance layer for manual overrides
- [[Results Boosting]] — per-query boost rules

## Related Articles
- [[Getting Started on Search Relevance for the Understaffed Search Team]]
- [[Real Talk About Synonyms and Search]]
