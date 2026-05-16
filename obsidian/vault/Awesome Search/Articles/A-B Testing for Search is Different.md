---
title: "A/B Testing for Search is Different"
tags:
  - clippings
  - search
  - evaluation
  - experimentation
source: "https://dtunkelang.medium.com/a-b-testing-for-search-is-different-f6b0f6f4d0f5"
author: "Daniel Tunkelang"
created: 2026-05-15
concepts:
  - A-B Testing for Search
  - Search Evaluation
  - Session-Based Evaluation
---

# A/B Testing for Search is Different

**Source:** https://dtunkelang.medium.com/a-b-testing-for-search-is-different-f6b0f6f4d0f5
**Author:** [[Daniel Tunkelang]]

## Summary

Why search A/B testing requires different methodology than standard product experimentation. The core problem: search changes don't affect all queries equally, and user behavior spans multiple queries within a session.

## Core Challenges

### Query Sparsity
Not all queries are affected by a given change. Analyzing aggregate metrics dilutes signal from the queries that actually matter.

### Session Effects
Changes may produce unintended consequences within the same user session. A narrowly-scoped improvement on target queries "might come at the expense of performance on other queries."

### Effect Size vs. Duration Tension
- Large effect sizes (doubling conversion): less testing time needed
- Small effect sizes (1% lift): require longer test duration
- Most real improvements are small → slow iteration cycle

## Key Recommendations

1. **Scope by sessions, not individual queries** — analyze at session level to catch cross-query effects
2. **Target narrow query sets** — focus improvements on specific query types for faster statistical power
3. **Balance speed with validity** — keep test scopes narrow for rapid iteration, but measure holistic session impact
4. **"A/B testing search isn't just a switch that you flip on — it's a science"**

## Related Concepts

- [[A-B Testing for Search]]
- [[Search Evaluation]]
- [[Session-Based Evaluation]]
- [[Click Signals]]
- [[Position Bias]]

## People

- [[Daniel Tunkelang]]

## Related Articles

- [[Session vs Query based Search Evals]]
- [[Measuring Search - Metrics Matter]]
