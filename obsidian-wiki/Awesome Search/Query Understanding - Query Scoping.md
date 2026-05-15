---
title: "Query Scoping"
source: "https://queryunderstanding.com/query-scoping-ed61b5ec8753"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems determine the appropriate scope or domain of a query to route it to the right search index or filter results appropriately — part of the Query Understanding series."
tags:
  - clippings
---

# Query Scoping

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Query scoping determines the appropriate "scope" or domain for a query — which category of the product catalog, which index, or which subset of documents should be searched.

## What Scoping Does

- Maps queries to product categories or taxonomic nodes
- Routes queries to specialized search indexes
- Pre-filters the search space before ranking
- Informs which features/facets to show

## Example

Query: "running shoes"
- Scope: Sports & Outdoors → Footwear → Athletic Shoes → Running Shoes
- Shows running-specific facets: surface type (road/trail), pronation, cushioning
- Doesn't show unrelated footwear facets: heel height, formal occasion

## Approaches

**Category classification**
- Train a classifier to map queries to taxonomy nodes
- Hierarchical classification (coarse to fine)
- Multi-label for ambiguous queries

**Query-to-category mapping**
- Use historical click data: queries → categories clicked
- Taxonomy-aware query expansion

**Neural approaches**
- Fine-tuned BERT classifiers achieve strong performance
- Embedding-based nearest-neighbor to category exemplars

## Challenges

- Ambiguous queries ("apple" → electronics or food?)
- Tail queries with little training data
- Taxonomy changes require retraining
- Multi-category queries ("gift for her under $50")

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Faceted Search]]
- [[Query Types]]
- [[Search Intent]]

## People

- [[Daniel Tunkelang]]
