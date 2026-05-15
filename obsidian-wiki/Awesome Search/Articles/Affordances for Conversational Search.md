---
title: "Affordances for Conversational Search"
aliases: ["Conversational Search Affordances", "Tunkelang Conversational"]
tags:
  - clippings
  - search
  - conversational-search
  - ux
source: "https://queryunderstanding.com/affordances-for-conversational-search-3e7f1c2d9b5a"
author: "Daniel Tunkelang"
created: 2026-05-15
concepts:
  - Query Understanding
  - Search Intent
  - Autocomplete
---

# Affordances for Conversational Search

**Source:** https://queryunderstanding.com/affordances-for-conversational-search-3e7f1c2d9b5a
**Author:** [[Daniel Tunkelang]]

## Summary

Conversational search promises to handle ambiguity through dialogue — but it fails in practice because of an **affordance gap**: users don't know what kinds of clarifying questions or reformulations the system can handle.

### What Is an Affordance?
In UX, an affordance is a design element that communicates how it can be used. A door handle affords pulling; a flat plate affords pushing. Good affordances make valid actions obvious.

### The Conversational Search Affordance Gap
Traditional search boxes have clear affordances: type keywords, get results. Conversational interfaces claim to understand natural language — but users don't know:
- What can I ask?
- Will it understand follow-up questions?
- What reformulations are valid?

This leads to over-trust (users phrase queries the system can't handle) and under-use (users revert to keyword search out of caution).

### Shopify Example: Clarifying Questions
Tunkelang cites Shopify's search feature that asks structured clarifying questions:
- "Are you looking for a product or a store?"
- "Do you mean X or Y?"
These are **designed affordances** — the system signals exactly what it can distinguish.

### Design Principles for Conversational Affordances
1. **Surface the query space** — show examples of what kinds of queries work
2. **Offer structured clarifications** — multiple choice > open-ended follow-up
3. **Progressive disclosure** — start with keyword search, escalate to dialogue only when needed
4. **Fail gracefully** — when the system doesn't understand, say so and suggest alternatives

### Relationship to Autocomplete
Autocomplete is a form of affordance: it shows users what queries are in-vocabulary. Conversational systems need analogous mechanisms.

## Key Concepts
- **Affordance** — design element communicating valid interactions
- **Affordance gap** — mismatch between system capability and user mental model
- **Clarifying questions** — structured dialogue to resolve ambiguity
- **Progressive disclosure** — escalate to richer interaction only when needed

## Related Concepts
- [[Query Understanding]]
- [[Search Intent]]
- [[Autocomplete]]
- [[Query Types]]
- [[Zero Results]]

## Related Articles
- [[Semantic Equivalence of e-Commerce Queries]]
- [[Thoughts about Managing Search Teams]]

## People
- [[Daniel Tunkelang]]
