---
title: "Query Understanding: Introduction"
source: "https://queryunderstanding.com/introduction-c98740502103"
author: ["Daniel Tunkelang"]
tags:
  - clippings
  - query-understanding
  - search
concepts:
  - Query Understanding
  - Search Intent
  - Query Segmentation
created: 2026-05-15
---

# Query Understanding: Introduction

**Source**: https://queryunderstanding.com/introduction-c98740502103  
**Author**: [[Daniel Tunkelang]] (queryunderstanding.com)

## Summary

The introductory post of [[Daniel Tunkelang]]'s comprehensive Query Understanding series — defining what query understanding is, why it matters, and how it fits into the overall search architecture.

## What Is Query Understanding?

Tunkelang's definition: **"Query understanding is the process of mapping user queries to actions, rather than just to words."**

This framing is important: the goal isn't to understand the query's linguistic structure but to determine what the search system should *do* in response.

## The Query-Action Pipeline

```
User types query
    ↓
[Query Understanding]
    ├── Spell correction
    ├── Query segmentation
    ├── Intent classification
    ├── Entity extraction
    └── Context analysis
    ↓
Action determination
    ├── Modify query (rewrite, expand)
    ├── Route to specialized search
    ├── Return direct answer
    └── Run standard retrieval
    ↓
Search execution + results
```

## Why Query Understanding Is Hard

1. **Brevity**: queries average 2–3 words — very little signal
2. **Ambiguity**: most words have multiple meanings
3. **Context dependence**: "apple" means different things on a food site vs. tech site
4. **Vocabulary mismatch**: user terms may not match document terms
5. **Evolving language**: slang, neologisms, brand names change constantly

## Query Understanding vs. NLU

Query understanding is specialized NLU (Natural Language Understanding):
- NLU handles full sentences with grammatical structure
- Query understanding handles telegraphic, keyword-style input
- Query understanding is more context-dependent (domain, session, user)

## The Business Case

Tunkelang cites data: improving query understanding by 10% translates to roughly 5–8% improvement in search success metrics — far more than equivalent investment in ranking or retrieval improvements.

This reflects that **understanding what users want** is more fundamental than **finding good matching content once you know what they want**.

## Series Structure

The queryunderstanding.com series covers:
1. Introduction (this article)
2. Query formulation (spell correction, segmentation)
3. Query intent
4. Entity understanding
5. Contextual query understanding
6. Conversational search

## Related Articles

- [[Query Understanding - Divided into Three Parts]] — structural framework
- [[AI for Query Understanding]] — LLM-era update
- [[Mapping Search Queries To Search Intents]] — intent component
- [[Food Discovery with Uber Eats]] — industrial application

## Related Concepts

- [[Query Understanding]] — primary topic
- [[Search Intent]] — key component
- [[Query Segmentation]] — linguistic component
- [[Query Types]] — taxonomy of queries
- [[Agentic Search]] — query understanding in multi-turn context

## People

- [[Daniel Tunkelang]] — author; queryunderstanding.com
