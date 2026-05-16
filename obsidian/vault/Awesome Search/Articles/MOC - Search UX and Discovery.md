---
title: "MOC — Search UX and Discovery"
tags:
  - moc
  - search
  - ux
  - discovery
created: 2026-05-15
---

# MOC — Search UX and Discovery

Map of content covering autocomplete, spelling correction, synonyms, faceted search, zero results, and search UX patterns.

## Autocomplete / Suggestions

- **Concept**: [[Autocomplete]] — prefix trie, neural suggestions, UX patterns
- [[Bootstrapping Autosuggest]] — Giovanni Fernandez-Kincade: goals and metrics first
- [[13 Design Patterns for Autocomplete Suggestions]] — Baymard: 27% get it wrong; 9 UX patterns
- **Series** (Giovanni Fernandez-Kincade):
  - Building an Autosuggest Corpus (Parts 1 & 2)
  - Autosuggest Retrieval Data Structures & Algorithms
  - Autosuggest Ranking

- [[How to Really Scale Autocomplete]] — bonsai.io; search_as_you_type + significant_terms agg; views as relevance signal; 416 RPS at 45ms p99 on 6M docs
- [[LLM-Powered Query Extraction for Autocomplete]] — [[Awesome Search/People/David Albrecht]]; GPT-4.1-nano on WANDS; LLM-generated queries solve cold-start for under $5

## Spelling Correction

- **Concept**: [[Spelling Correction]] — Norvig's algorithm, SymSpell, context-aware
- [[How to Write a Spelling Corrector]] — Norvig's classic probabilistic algorithm; 21 lines of Python
- [[1000x Faster Spelling Correction Algorithm - SymSpell]] — Wolf Garbe: O(1) via delete-only preprocessing
- [[Modeling Spelling Correction for Search at Etsy]] — industry application at scale

## Synonyms

- **Concept**: [[Synonyms]] — lexical vs. semantic synonyms; index-time vs. query-time expansion
- Real Talk About Synonyms and Search (Tunkelang)
- Boosting the Power of Elasticsearch with Synonyms

## Faceted Search

- **Concept**: [[Faceted Search]] — dynamic filters, constraints vs. preferences, taxonomy
- [[Facets of Faceted Search]] (Tunkelang)
- Facets: Constraints or Preferences? (Tunkelang)
- 7 Filtering Implementations That Make Macy's Best-in-Class (Baymard)

## Zero Results

- **Concept**: [[Zero Results]] — causes and recovery strategies; findability pillar
- Search UX: 6 Essential Elements for 'No Results' Pages (Baymard)
- Strategies for Using Alternative Queries to Mitigate Zero Results

## Query Types and UX

- [[Deconstructing E-Commerce Search - The 12 Query Types]] — Baymard's e-commerce query taxonomy
- [[Broad and Ambiguous Search Queries]] — Tunkelang on broad query challenges
- [[Targeting Broad Queries in Search]] — Etsy approach

## A/B Testing and Experimentation

- **Concept**: [[A-B Testing for Search]]
- [[A-B Testing for Search is Different]] — Tunkelang: session-level analysis
- Common Pitfalls of Search Experimentation

## Related MOCs

- [[MOC - Search Quality Assurance and Query Understanding]]
- [[MOC - Ranking and Retrieval]]
- [[MOC - Case Studies]]
