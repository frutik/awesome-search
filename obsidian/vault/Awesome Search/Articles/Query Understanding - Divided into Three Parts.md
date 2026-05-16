---
title: "Query Understanding, Divided into Three Parts"
source: "https://medium.com/@dtunkelang/query-understanding-divided-into-three-parts-d9cbc81a5d09"
author: ["Daniel Tunkelang"]
tags:
  - clippings
  - query-understanding
  - search
  - framework
concepts:
  - Query Understanding
  - Search Intent
  - Query Segmentation
created: 2026-05-15
---

# Query Understanding, Divided into Three Parts

**Source**: https://medium.com/@dtunkelang/query-understanding-divided-into-three-parts-d9cbc81a5d09  
**Author**: [[Daniel Tunkelang]]

## Summary

[[Daniel Tunkelang]] proposes dividing [[Query Understanding]] into three distinct components — formulation analysis, intent determination, and contextualization — each with different techniques and system requirements.

## The Three Parts Framework

### Part 1: Query Formulation Analysis
**What the user typed, interpreted literally.**

Goal: extract structured information from the raw query string.

Techniques:
- **Spell correction**: "macbbook pro" → "macbook pro"
- **Tokenization**: decide word boundaries
- **[[Query Segmentation]]**: "new york times" → single entity
- **Named entity recognition**: identify products, brands, places
- **Part-of-speech tagging**: distinguish modifiers from head terms

This is largely a linguistic/NLP problem.

### Part 2: Intent Determination
**What the user is trying to accomplish.**

Goal: classify the query into intent categories that drive retrieval strategy.

Techniques:
- Intent classifier (navigational / informational / transactional)
- Query type classification ([[Query Types]])
- Specificity assessment (head/torso/tail)
- Ambiguity detection

This is a semantic/ML problem.

### Part 3: Contextualization
**What this specific user in this specific context actually wants.**

Goal: personalize the interpretation based on:
- User history and preferences
- Location and device
- Session context (previous queries)
- Temporal context (trending, seasonal)

This is a personalization/data problem.

## Why Separate the Three Parts?

Each part has different:
- **Failure modes**: mis-tokenization ≠ wrong intent ≠ wrong personalization
- **Solutions**: NLP tools ≠ ML classifiers ≠ user models
- **Update frequency**: NLP rarely; intent classifiers monthly; personalization real-time
- **Required data**: text data ≠ labeled intent data ≠ user behavior data

Mixing them together creates unmaintainable, untestable systems.

## Part Interactions

The three parts aren't independent:
- Formulation analysis feeds into intent determination
- Intent modulates contextualization (navigational queries need less personalization)
- Context can feed back to formulation (previous session queries influence parsing)

## Example: "apple watch bands"

| Part | Analysis |
|------|---------|
| Formulation | Entities: "Apple Watch" (product) + "bands" (accessory type) |
| Intent | Transactional (shopping intent, specific product + accessory) |
| Context | User previously searched "smartwatch" → probably new to Apple ecosystem → show beginner options |

Final action: structured search over Apple Watch bands, filtered by user's apparent experience level.

## Related Articles

- [[Query Understanding - Introduction]] — foundational post
- [[AI for Query Understanding]] — LLM approach to all three parts
- [[Mapping Search Queries To Search Intents]] — deep dive on Part 2

## Related Concepts

- [[Query Understanding]] — the framework being defined
- [[Search Intent]] — Part 2 of the framework
- [[Query Segmentation]] — Part 1 technique
- [[Query Types]] — Part 2 taxonomy
- [[Bag-of-Documents Model]] — probabilistic interpretation of Part 2

## People

- [[Daniel Tunkelang]] — author; defined this framework
