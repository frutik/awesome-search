---
title: "Search Result Snippets"
source: "https://queryunderstanding.com/search-result-snippets-e8c447950219"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search result snippets (short descriptions below titles) are generated and optimized to help users judge result relevance — part of the Query Understanding series."
tags:
  - clippings
---

# Search Result Snippets

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Search result snippets are the short text excerpts shown below result titles. They help users quickly judge whether a result is relevant before clicking, and are a key factor in click-through rates.

## Types of Snippets

**Static snippets**
- Fixed meta description from the document
- Author/publisher controlled
- Consistent but not query-specific

**Dynamic snippets**
- Generated at query time from document content
- Show the portion of document most relevant to the query
- Include highlighted query terms

**Structured snippets**
- Extracted from structured data (schema.org)
- Product snippets: price, rating, availability
- Recipe snippets: cook time, ingredients
- Event snippets: date, location

## Snippet Generation Approaches

**Sentence extraction (extractive)**
- Score sentences by query term overlap
- Max Marginal Relevance to select diverse, relevant passages
- Window-based extraction (±N words around query terms)

**Neural generation (abstractive)**
- T5, BART, GPT-based snippet generation
- Can synthesize across multiple passages
- Risk of hallucination

## Quality Criteria

- **Relevance**: Does it show why this result matches the query?
- **Informativeness**: Does it convey what the page is about?
- **Readability**: Is it grammatically complete and clear?
- **Length**: 150-300 characters is typical

## E-commerce Specifics

Snippets in e-commerce should highlight:
- Key product attributes (matching query terms)
- Unique value propositions
- Availability, shipping info

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Diversity Metrics]]

## People

- [[Daniel Tunkelang]]
