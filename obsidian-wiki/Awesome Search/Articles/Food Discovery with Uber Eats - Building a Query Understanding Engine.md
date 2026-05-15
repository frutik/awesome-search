---
title: "Food Discovery with Uber Eats: Building a Query Understanding Engine"
source: "https://eng.uber.com/uber-eats-query-understanding/"
author: ["Uber Engineering"]
tags:
  - clippings
  - query-understanding
  - uber-eats
  - case-study
  - food-search
concepts:
  - Query Understanding
  - Search Intent
  - Semantic Search
  - Hybrid Search
created: 2026-05-15
---

# Food Discovery with Uber Eats: Building a Query Understanding Engine

**Source**: https://eng.uber.com/uber-eats-query-understanding/  
**Author**: Uber Engineering

## Summary

Uber Eats engineering describes building a production query understanding engine for food search — covering intent classification, entity extraction, query rewriting, and the specific challenges of food domain search.

## Food Search Domain Challenges

Food search has unique QU challenges:
1. **Cuisine ambiguity**: "Thai" = Thai food OR Thai restaurant specifically?
2. **Dish-category gap**: "pad see ew" (specific dish) → "Thai food" (category) → "noodles" (broader)
3. **Ingredient queries**: "no gluten" → filter + ranking adjustment, not text matching
4. **Contextual meaning**: "spicy" means different things to different users
5. **Hybrid search need**: "McDonald's near me" (navigational) vs. "healthy salad" (semantic)

## Uber Eats Query Understanding Architecture

### Layer 1: Query Classification
Multi-label classifier assigns query categories:
- Dish-level ("pad thai")
- Restaurant-level ("Shake Shack")
- Cuisine-level ("Japanese food")
- Attribute-level ("vegan options")
- Combo ("cheap Thai near me")

Multiple labels can apply simultaneously.

### Layer 2: Entity Extraction
NER extracts:
- Restaurant names: "McDonald's", "Chipotle"
- Dish names: "Chicken Tikka Masala", "Pho"
- Cuisines: "Thai", "Italian", "Indian"
- Attributes: "vegan", "gluten-free", "spicy"
- Location terms: "near me", "downtown"

### Layer 3: Query Rewriting
Transform extracted entities into structured search:
```
Input: "cheap Thai food near me"
Output: {
    "cuisine": "Thai",
    "price_filter": "low",
    "location": "user_coordinates",
    "sort": "relevance"
}
```

### Layer 4: Fallback and Expansion
If structured query returns few results:
- Expand cuisine synonyms ("Thai" → ["Thai", "Southeast Asian"])
- Relax filters
- Expand geofence

## Key Technical Choices

### BERT-based NER
Fine-tuned on Uber Eats domain data (dish names, restaurant names):
- Base BERT misses "pad see ew" (recognizes "see" and "ew" as separate tokens)
- Domain-fine-tuned BERT correctly identifies multi-word dish names

### Semantic Search Integration
For exploratory queries ("comfort food", "something different tonight"):
- Pure keyword matching fails (no keyword overlap)
- Semantic [[Bi-Encoder]] embedding retrieves restaurants matching the intent

### Results

Post-QU system deployment:
- +15% search session success rate
- -20% zero-result queries
- +8% order conversion for "discovery" queries (exploratory, non-specific)

## Lessons for Other Food/E-commerce Search

1. **Domain entities are critical**: invest in domain-specific NER
2. **Intent-first architecture**: classify intent before retrieval, not after
3. **Fallback strategy**: over-constraining queries is the main failure mode
4. **Hybrid mandatory**: navigational (exact) + semantic (exploratory) both needed

## Related Articles

- [[Query Understanding - Introduction]] — foundational framework
- [[AI for Query Understanding]] — LLM approach to the same problem
- [[Migrating to Elasticsearch with Dense Vector for Carousell Spotlight]] — similar e-commerce semantic search migration

## Related Concepts

- [[Query Understanding]] — primary topic
- [[Search Intent]] — multi-class intent classification
- [[Semantic Search]] — exploratory query handling
- [[Hybrid Search]] — exact + semantic
- [[Entity Extraction]] — NER in search

## People

- [[Daniel Tunkelang]] — theoretical framing this implements
