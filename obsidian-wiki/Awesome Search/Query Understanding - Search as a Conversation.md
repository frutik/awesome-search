---
title: "Search as a Conversation"
source: "https://queryunderstanding.com/search-as-a-conversation-bafa7cd0c9a5"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search can be reimagined as a multi-turn dialogue that progressively refines user intent through conversation — part of the Query Understanding series."
tags:
  - clippings
---

# Search as a Conversation

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Traditional search is a one-shot interaction: user types query, gets results. Conversational search reimagines this as a dialogue where the system and user jointly refine the search through multiple turns.

## The Conversational Search Model

```
User: "I'm looking for a gift for my mom"
System: "What's the occasion, and what's your budget?"
User: "Her birthday, around $50"
System: "What are her interests?"
User: "She loves gardening"
System: [Shows gardening gift options $40-60]
```

## Why Conversational Search Matters

- Reduces cognitive load of formulating precise queries
- Handles complex, multi-faceted information needs
- More natural for voice interfaces
- Enables progressive disclosure of intent

## Key Techniques

**Clarification questions**
- Ask for missing information (occasion, budget, recipient)
- System must know when to ask vs. when to show results

**Reference resolution**
- "Show me that in red" — resolve "that" to previous result
- Track entities across turns

**Intent tracking**
- Maintain dialogue state across turns
- Detect when user switches to a new intent

## Comparison to Traditional Search

| Aspect | Traditional Search | Conversational Search |
|---|---|---|
| Turns | Single | Multiple |
| Initiative | User-driven | Mixed |
| Query formulation | User's burden | Shared burden |
| Context | Stateless | Stateful |
| Interface | Results page | Dialogue + results |

## Modern Implementations

- Alexa, Google Assistant, Siri for voice
- ChatGPT-style interfaces with search grounding
- Shopping assistants (Shopify, Amazon)

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Agentic Search]]
- [[Search Intent]]
- [[Faceted Search]]

## People

- [[Daniel Tunkelang]]
