---
title: "Taxonomies and Ontologies"
source: "https://queryunderstanding.com/taxonomies-and-ontologies-8e4812a79cb2"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How taxonomies and ontologies structure knowledge to enable semantic query understanding and more intelligent search — part of the Query Understanding series."
tags:
  - clippings
---

# Taxonomies and Ontologies

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Taxonomy

A **taxonomy** is a hierarchical classification system.

**In search:**
- Product category trees (Electronics → Computers → Laptops → Gaming Laptops)
- Content type hierarchies
- Enables navigation, filtering, and query scoping

**Key properties:**
- Strictly hierarchical (tree structure)
- Each node has one parent (except root)
- Used for browse navigation and faceted filtering

## Ontology

An **ontology** is a richer knowledge structure including relationships, attributes, and rules — not just hierarchy.

**In search:**
- Semantic relationships ("running shoes" IS-A "athletic footwear")
- Part-of relationships ("lens" IS-PART-OF "camera")
- Compatibility (iPhone 15 COMPATIBLE-WITH "Lightning cables" vs "USB-C")
- Equivalences ("sofa" SAME-AS "couch" SAME-AS "settee")

## Applications in Query Understanding

**Query expansion via taxonomy**
- "boots" → expand to include "ankle boots", "knee-high boots", "cowboy boots"
- Navigate up/down hierarchy for recall/precision tradeoff

**Query scoping**
- Map query to taxonomy node to determine search scope

**Entity resolution**
- Map extracted entities to canonical knowledge base entries with IDs

**Facet generation**
- Taxonomy drives which facets to show for a given query/category

## Building Taxonomies

- Manual curation (expensive but high quality)
- Semi-automated from product catalogs
- Machine learning-based taxonomy induction from text

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Faceted Search]]
- [[Synonyms]]
- [[Query Relaxation]]

## People

- [[Daniel Tunkelang]]
