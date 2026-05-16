---
title: "Session vs Query based search evals"
source: "https://softwaredoug.com/blog/2026/03/30/session-vs-query-based-search-evals"
author:
  - "[[Doug Turnbull]]"
published: 2026-03-30
created: 2026-05-15
description: "Session-based evaluation replays individual user interactions instead of aggregating by query — better sampling accuracy and time-sensitive feature capture, at the cost of per-query debuggability."
tags:
  - clippings
---
# Session vs Query based search evals

## Traditional query-based evaluation

Create judgment lists from clickstream data, label results relevant/irrelevant for specific queries, evaluate with NDCG over aggregated signals.

## Session-based evaluation

"Replay" individual user interactions directly. Instead of "how many queries improved?", asks "would we have satisfied past users?" — evaluating whether the system would better satisfy single historical search-and-click events.

### Advantages

- **Improved sampling accuracy**: mirrors probability-based sampling (like political polling) — every user interaction has equal selection probability. Query-based methods introduce sampling bias by pre-selecting specific queries.
- **Time-sensitive features**: aggregating clicks across months masks momentary conditions (e.g., temporary sales). Session-based data captures exact feature values present when users clicked.

### Disadvantages

- Clickstream biases (position bias) remain present
- Harder to debug per-query since individual queries may contain insufficient data

## Balanced view

Both derive from historical sessions and offer different insights:
- **Query-based**: excellent for debugging specific search problems
- **Session-based**: simulates A/B testing

Neither represents absolute truth — both are imperfect but useful models of search performance.

## Related Concepts
- [[Session-Based Evaluation]] — the approach advocated
- [[Search Evaluation]] — parent concept
- [[Judgment Lists]] — query-based evaluation relies on pre-built judgment lists
- [[Click Signals]] — clickstream data underlies both approaches
- [[Position Bias]] — present in both session and query-based data
- [[A-B Testing for Search]] — session-based eval simulates A/B testing

## People
- [[Doug Turnbull]] — author