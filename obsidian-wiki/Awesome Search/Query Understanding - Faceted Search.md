---
title: "Faceted Search"
source: "https://queryunderstanding.com/faceted-search-7d053cc4fada"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How faceted search enables users to progressively narrow results using structured attribute filters — part of the Query Understanding series."
tags:
  - clippings
---

# Faceted Search

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Faceted search (also: faceted navigation, guided navigation) allows users to filter search results by structured attributes (facets) such as category, price, brand, color, and size. It's one of the most effective UX patterns for exploratory e-commerce search.

## What Facets Are

Facets are structured attributes of items in the index:
- Category / subcategory
- Brand
- Price range
- Color, size, material (product attributes)
- Rating, reviews
- Availability, shipping speed
- New/used condition

## Faceted Search vs. Keyword Search

| Keyword Search | Faceted Search |
|---|---|
| User-initiated | System-initiated |
| Recall problem (find the right query) | Precision problem (narrow to right item) |
| Good for known-item search | Good for exploratory browse |

## Query Understanding + Facets

Faceted search is informed by query understanding:
- **Query scoping** determines which facets to show (running shoes → show surface type, not heel height)
- **Entity recognition** can pre-populate filters ("red Nike running shoes" → Brand=Nike, Color=Red)
- **Personalization** determines default facet values and ordering

## Facet Relevance

Not all facets are equally useful. Showing too many facets overwhelms users:
- Show only facets relevant to the current query and category
- Rank facets by usefulness/discriminating power
- Dynamically generate facet values based on results

## Implementation

- Elasticsearch aggregations for facet counts
- Pre-compute facet counts at index time for performance
- Facet selection updates results and remaining facet counts

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Faceted Search]]
- [[Search Intent]]

## People

- [[Daniel Tunkelang]]
