---
title: "Clarification Dialogues"
source: "https://queryunderstanding.com/clarification-dialogues-69420432f451"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems can ask clarifying questions to resolve ambiguous queries and better understand user intent — part of the Query Understanding series."
tags:
  - clippings
---

# Clarification Dialogues

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Clarification dialogues enable search systems to resolve query ambiguity by asking targeted questions. Rather than guessing at intent or showing a hedged result set, the system engages the user in a brief exchange to pin down what they want.

## When to Clarify

**High ambiguity situations**
- Multiple very different interpretations: "jaguar" → car vs. animal vs. football team
- Missing critical dimension: "dress" without size, occasion, or price range
- Underspecified intent: "gift ideas"

**When clarification is worthwhile**
- When the cost of showing wrong results exceeds the friction of asking
- When asking one question dramatically narrows the search space
- When head queries have highly variable user intent

## Types of Clarification Questions

**Choice questions**
- "Are you looking for a [car] or [animal]?"

**Slot-filling questions**
- "What size are you looking for?" (e-commerce)
- "Which city?" (travel search)

**Intent confirmation**
- "Did you mean...?" (spelling, semantic)

## Design Principles

- Ask at most 1-2 questions before showing results (user patience)
- Make questions easy to answer (yes/no, multiple choice)
- Show partial results alongside clarification to reduce friction
- Learn from user responses to improve future disambiguation

## Tradeoffs

- Too many questions → friction, user abandonment
- No clarification → low-quality results for ambiguous queries
- Sweet spot: ask when confidence is low AND question is high-value

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Faceted Search]]
- [[Zero Results]]
- [[Search Intent]]

## People

- [[Daniel Tunkelang]]
