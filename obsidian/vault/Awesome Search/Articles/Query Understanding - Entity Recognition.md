---
title: "Entity Recognition"
source: "https://queryunderstanding.com/entity-recognition-763cae840a20"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems identify named entities within queries (brands, products, people, places) to enable structured understanding and retrieval — part of the Query Understanding series."
tags:
  - clippings
---

# Entity Recognition

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Entity recognition (Named Entity Recognition / NER for search) identifies and classifies named entities within queries. This transforms free-text queries into structured representations that enable more precise retrieval.

## Entity Types in Search

**E-commerce examples**
- Brand: "Nike", "Apple", "Levi's"
- Product: "iPhone 15", "Air Jordan 1"
- Category: "running shoes", "denim jacket"
- Color: "navy blue", "burgundy"
- Size: "XL", "32x32", "US 10"
- Price: "under $50", "around $100"
- Material: "leather", "cotton"
- Person: "LeBron James" (for signature items)
- Location: "Paris", "Tokyo" (for travel/location-specific search)

## Approaches

**Dictionary/gazetteer lookup**
- Match against known entity lists (brand catalogs, product databases)
- Fast but requires maintaining comprehensive lists

**Statistical sequence labeling**
- CRF, BiLSTM-CRF trained on labeled queries
- Can generalize to unseen entities

**Neural NER**
- BERT-based models achieve state-of-the-art
- Fine-tuned on domain-specific data

## Integration with Query Understanding

Entity recognition feeds into:
- Query Segmentation (entities are segments)
- Query Scoping (entity type determines scope)
- Query Resolution (entities mapped to knowledge base IDs)
- Faceted search (entities become filter values)

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Query Segmentation]]
- [[Faceted Search]]

## People

- [[Daniel Tunkelang]]
