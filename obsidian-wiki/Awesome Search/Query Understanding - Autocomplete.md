---
title: "Autocomplete"
source: "https://queryunderstanding.com/autocomplete-69ed81bba245"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems provide query completion suggestions as users type to speed up query formulation and guide users toward successful queries — part of the Query Understanding series."
tags:
  - clippings
---

# Autocomplete

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Autocomplete (also: search suggestions, search-as-you-type, typeahead) predicts the full query a user is typing and presents completions as a dropdown. It improves search efficiency and guides users toward queries that return results.

## Types of Suggestions

**Query completions**: Complete the current partial query
- "run" → "running shoes", "running jacket", "running watch"

**Query suggestions**: Alternative queries (not just completions)
- "red dress" → "red cocktail dress", "red maxi dress"

**Product/entity suggestions**: Jump directly to a product or category
- "iphone 1" → shows iPhone 15, iPhone 14 cards

## Data Sources

**Query logs** (most important)
- Frequent past queries as candidates
- CTR and conversion rate as quality signals
- Personalization: user's own history

**Catalog/index**
- Index-based autocomplete from product names, categories
- Ensures suggestions lead to results

**Curated/editorial**
- Hand-picked suggestions for head queries
- Holiday and promotional suggestions

## Ranking Autocomplete Suggestions

Factors to rank:
1. Query frequency (popularity)
2. Conversion rate
3. Contextual relevance to typed prefix
4. Recency (trending queries)
5. Personalization signals

## Implementation

- Trie-based indexes for prefix matching (fast, memory-efficient)
- Inverted index with prefix queries
- Redis for real-time trending suggestions

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Autocomplete]]
- [[Query Understanding]]
- [[Click Signals]]
- [[Search Intent]]

## People

- [[Daniel Tunkelang]]
