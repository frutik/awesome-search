---
title: "Query Expansion"
source: "https://queryunderstanding.com/query-expansion-2d68d47cf9c8"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems add related terms to queries to improve recall by matching documents that use different vocabulary than the user — part of the Query Understanding series."
tags:
  - clippings
---

# Query Expansion

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Query expansion adds terms to the original query to increase recall — helping retrieve relevant documents that use different vocabulary than the user typed.

## Expansion Sources

**Synonym resources**
- WordNet, thesauri
- Domain-specific synonym dictionaries
- Custom synonym lists built from e-commerce catalogs

**Query logs / click data**
- Queries that lead to the same clicks are likely semantically related
- Co-click analysis: users who clicked result X also searched for Y

**Pseudo-Relevance Feedback (PRF)**
- Retrieve top-k results, extract key terms, add to query
- Risk: topic drift if initial results are poor

**Semantic embeddings**
- Word2Vec, GloVe neighborhood expansion
- Dense retrieval models for concept expansion

**Ontologies / Knowledge Graphs**
- Navigate taxonomic relationships ("shirts" → includes "dress shirts", "polo shirts")
- Hypernym/hyponym expansion

## Tradeoffs

- More expansion → higher recall, lower precision
- Expansion terms need relevance weighting (not equal weight as original terms)
- Context matters: "apple" expansion differs for food vs. tech queries

## Implementation Notes

- Apply as Elasticsearch `synonym` filter or query-time expansion
- Weight expanded terms lower than original terms
- A/B test expansion rules to measure precision/recall tradeoff

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Synonyms]]
- [[Zero Results]]
- [[Hybrid Search]]

## People

- [[Daniel Tunkelang]]
