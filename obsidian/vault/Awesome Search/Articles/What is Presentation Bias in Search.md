---
type: article
title: "What is Presentation Bias in Search?"
source: "https://softwaredoug.com/blog/2022/07/16/what-is-presentation-bias-in-search.html"
author:
  - "[[Doug Turnbull]]"
published: 2022-07-16
created: 2026-05-15
concepts:
  - "[[Presentation Bias]]"
  - "[[Position Bias]]"
  - "[[Click Signals]]"
  - "[[Search Evaluation]]"
  - "[[Judgment Lists]]"
topics:
  - "[[Search Quality Assurance]]"
tags:
  - article
  - search-evaluation
  - bias
  - click-data
---

# What is Presentation Bias in Search?

**[[Doug Turnbull]]** explains presentation bias — a broader form of [[Position Bias]] where click data is corrupted not just by rank position, but by what the system chose to show at all.

> "Shoppers won't purchase what search doesn't show them!"

## Definition

When search results are limited by screen space, the historical click data captured reflects the system's prior choices about what to show, not users' true preferences. Users can only interact with what's visible.

## The Self-Reinforcing Cycle

1. System shows items A, B, C (not D, E, F)
2. Users click A, B, C — the only options they see
3. System trains on these clicks → "A, B, C are what users want"
4. D, E, F never get shown → never get clicks → never improve in ranking
5. System becomes progressively more entrenched showing A, B, C

This is **survivorship bias applied to search**: only results that were shown can generate feedback.

## Highway Sign Metaphor

A highway sign shows only 6 restaurants. A survey finds travellers prefer those 6. The sign itself skewed the result — this is presentation bias.

## Distinction from [[Position Bias]]

| Concept | Scope |
|---|---|
| **[[Position Bias]]** | Users favour top-ranked results regardless of quality |
| **[[Presentation Bias]]** | Users can only interact with what's shown — not shown = no signal |

Presentation bias is the root phenomenon; position bias is one specific manifestation.

## Solutions

- Result diversity — deliberately surface long-tail items
- [[A-B Testing for Search]] — controlled experiments to avoid feedback loops
- Active learning — randomly promote underexposed items to gather signal
- Non-click data — [[Judgment Lists]] from human evaluators bypass click bias

## Related Concepts

- [[Presentation Bias]] — concept note
- [[Position Bias]] — closely related; rank-position-specific form
- [[Click Signals]] — the feedback mechanism that gets corrupted
- [[Search Evaluation]] — why unbiased signals matter
- [[Judgment Lists]] — human-labeled alternative to click data
- [[Diversity Metrics]] — mitigation via diverse results
- [[Relevance Feedback]] — broader context of user feedback signals

## Related Articles

- [[Query Understanding - Relevance Feedback]] — [[Daniel Tunkelang]]; implicit feedback and its biases
- [[What AI Engineers Should Know about Search]] — [[Doug Turnbull]]; presentation bias as point 7 in the primer

## People

- [[Doug Turnbull]] — author; softwaredoug.com
