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

Map of content for the **Search UX & Discovery** family: how users express a need, scan and refine results, recover from failure, and discover things they weren't explicitly looking for. Covers query input, results presentation, faceted navigation and filtering, search scopes, zero-results recovery, and discovery/inspiration patterns.

> [!info] Start here
> **Topic hub**: [[Search UX]] — the full narrative (interaction loop, presentation, facets, zero results, discovery, measurement). This MOC is the link-out index into the notes behind it.

## Query Input UX

- **Concept**: [[Autocomplete]] — prefix trie, neural suggestions, UX patterns
- **Topic**: [[Autocomplete and Autosuggest]] — query-input UX in full
- [[Bootstrapping Autosuggest]] — Giovanni Fernandez-Kincade: goals and metrics first
- [[13 Design Patterns for Autocomplete Suggestions]] — Baymard: 27% get it wrong; 9 UX patterns
- [[How to Really Scale Autocomplete]] — bonsai.io; search_as_you_type + significant_terms; 416 RPS at 45ms p99
- [[LLM-Powered Query Extraction for Autocomplete]] — [[Awesome Search/People/David Albrecht]]; GPT-4.1-nano solves cold-start
- [[Affordances for Conversational Search]] — [[Daniel Tunkelang]]'s affordance gap: showing users what the system can do

## Spelling Correction

- **Concept**: [[Spelling Correction]] — Norvig's algorithm, SymSpell, context-aware
- [[How to Write a Spelling Corrector]] — Norvig's classic probabilistic algorithm; 21 lines of Python
- [[1000x Faster Spelling Correction Algorithm - SymSpell]] — Wolf Garbe: O(1) via delete-only preprocessing
- [[Modeling Spelling Correction for Search at Etsy]] — industry application at scale

## Synonyms

- **Concept**: [[Synonyms]] — lexical vs. semantic synonyms; index-time vs. query-time expansion
- Real Talk About Synonyms and Search (Tunkelang)
- Boosting the Power of Elasticsearch with Synonyms

## Results Presentation

- **Concept**: [[Presentation Bias]] — what's shown shapes what's clicked; only-shown results can generate feedback
- **Concept**: [[Position Bias]] — top results get clicks regardless of quality
- [[Query Understanding - Search Results Presentation]] — layout, snippets, components matched to intent
- **Concept**: [[Results Merchandising]] — curating/pinning results to tell a product story
- **Concept**: [[Results Boosting]] — score-level promotion/demotion behind the presentation layer
- [[The Pinball Pattern - Complex Search-Results Pages Change Search Behavior]] — NN/g: nonlinear SERP scanning

## Faceted Navigation & Filtering

- **Concept**: [[Faceted Search]] — dynamic filters, constraints vs. preferences, counts, dynamic facets
- [[Facets of Faceted Search]] (Tunkelang)
- [[Facets - Constraints or Preferences]] (Tunkelang) — the key facet-UX distinction
- [[Facets, But Which Ones]] (Tunkelang) — choosing which facets to expose
- 7 Filtering Implementations That Make Macy's Best-in-Class (Baymard)

## Search Scopes

- **Concept**: [[Search Scopes]] — pre-query narrowing (department/type/“search within”); the sticky-scope failure mode
- **Concept**: [[Federated Search]] — querying multiple scopes/sources at once
- [[Query Understanding - Query Scoping]] — automatic scope detection from the query
- [[Scoped Search - Dangerous but Sometimes Useful]] — NN/g: the sticky-scope failure mode

## Zero Results & Recovery

- **Concept**: [[Zero Results]] — causes and recovery strategies; findability floor
- **Concept**: [[Query Relaxation]] — drop/loosen constraints to refill an empty page
- Search UX: 6 Essential Elements for 'No Results' Pages (Baymard)
- Strategies for Using Alternative Queries to Mitigate Zero Results

## Discovery & Inspiration

- **Topic**: [[Search Result Diversity]] — the discovery angle of result presentation
- [[Three Pillars of Search Quality - Discovery and Inspiration]] — [[Andreas Wagner]]: findability vs. discovery vs. relevance
- [[Broad and Ambiguous Search Queries]] — Tunkelang: recognizing when results need diversification
- [[Thoughts on Search Result Diversity]] — Tunkelang on diversity as a UX goal
- **Concept**: [[MMR]] — Maximal Marginal Relevance; the workhorse diversification method

## Query Types & UX

- [[Deconstructing E-Commerce Search - The 12 Query Types]] — Baymard's e-commerce query taxonomy
- [[Query Types]] — how intent type sets presentation expectations
- [[Targeting Broad Queries in Search]] — Etsy approach

## Measuring & Experimenting on UX

- **Concept**: [[A-B Testing for Search]]
- [[A-B Testing for Search is Different]] — Tunkelang: session-level analysis
- **Concept**: [[Clicks Residual]] · [[Zero Results]] — engagement and failure signals
- [[Good Abandonment on Search Results Pages]] — NN/g: no-click sessions aren't always failures
- [[Search-Log Analysis - The Most Overlooked Opportunity in UX Research]] — NN/g: query logs as UX research
- Common Pitfalls of Search Experimentation

## Related MOCs

- [[MOC - Search Quality Assurance and Query Understanding]]
- [[MOC - Ranking and Retrieval]]
