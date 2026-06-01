---
title: "Search: Intent, Not Inventory"
source: "https://medium.com/@dtunkelang/search-intent-not-inventory-289386f28a21"
author: ["Daniel Tunkelang"]
tags:
  - clippings
  - query-understanding
  - search-intent
  - search-philosophy
  - medium
concepts:
  - Search Intent
  - Query Understanding
  - Semantic Search
created: 2026-05-15
---

# Search: Intent, Not Inventory
> [!note] Redirect
> Canonical note: [[Search Intent Not Inventory]]


**Source**: https://medium.com/@dtunkelang/search-intent-not-inventory-289386f28a21  
**Author**: [[Daniel Tunkelang]]

## Summary

One of [[Daniel Tunkelang]]'s most cited pieces. The central argument: search systems that optimize for finding documents that match the query ("inventory") fail users who need their underlying information goal satisfied ("intent").

## The Inventory Model (What Most Systems Do)

Most search systems operate as "inventory systems":
1. User submits query
2. System finds documents containing query terms (or semantically similar)
3. System ranks documents by relevance to query
4. User presented with documents

This works when the user's intent = "find documents about X."

But most search intents are **not** "find documents about X."

## The Intent Model (What Users Actually Want)

Users search to accomplish goals:

| Query | Inventory View | Intent View |
|-------|---------------|------------|
| "flu symptoms" | Documents about flu symptoms | Determine if I have flu / what to do |
| "Paris restaurants" | Restaurant review pages | Make a reservation tonight |
| "how to tie a tie" | Tutorial pages | Learn to tie my tie right now |
| "competitor product X" | Review pages | Decide whether to buy vs. competitor |

The inventory model returns the same results for all users with "flu symptoms." The intent model might return different results for "concerned parent" vs. "person who has been sick for a week."

## Why This Matters for Search Design

**Implication 1: Retrieval is not the end**
The search system's job isn't to return relevant documents — it's to help the user achieve their goal. A relevant document that requires 10 minutes of reading is less useful than a direct answer snippet.

**Implication 2: Features beyond text relevance matter**
For "Paris restaurants" intent: recency, hours, distance, price range matter as much as text relevance.

**Implication 3: Zero-result is sometimes correct**
If no document satisfies the intent, returning poor matches is worse than returning nothing (with a helpful alternative suggestion).

**Implication 4: Conversational search is natural**
Intent-based search naturally leads to dialogue: "What's your occasion? What budget? Dietary restrictions?" Inventory-based search is one-shot; intent-based is conversational.

## Connection to [[Agentic Search]]

[[Agentic Search]] is the architectural realization of intent-based search:
- Agent understands intent (not just query)
- Agent plans retrieval strategy around intent
- Agent verifies if retrieved content satisfies intent
- Agent reformulates if intent is not yet satisfied

## Related Articles

- [[Mapping Search Queries To Search Intents]] — same author, how to map query→intent
- [[Query Understanding - Introduction]] — framework context
- [[Agentic Search as an Agile Engineering Process]] — intent-based search in practice

## Related Concepts

- [[Search Intent]] — primary topic
- [[Query Understanding]] — framework
- [[Agentic Search]] — architectural realization
- [[Semantic Search]] — moves beyond lexical matching toward meaning
- [[Bag-of-Documents Model]] — probabilistic intent modeling

## People

- [[Daniel Tunkelang]] — author
