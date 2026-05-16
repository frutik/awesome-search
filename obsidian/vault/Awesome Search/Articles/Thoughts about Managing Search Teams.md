---
title: "Thoughts about Managing Search Teams"
aliases: ["Managing Search Teams", "Tunkelang Search Management"]
tags:
  - clippings
  - search
  - team-management
  - search-architecture
source: "https://queryunderstanding.com/thoughts-about-managing-search-teams-7b3e9f1c4d2a"
author: "Daniel Tunkelang"
created: 2026-05-15
concepts:
  - Search Architecture
  - Search Evaluation
  - A-B Testing for Search
---

# Thoughts about Managing Search Teams

**Source:** https://queryunderstanding.com/thoughts-about-managing-search-teams-7b3e9f1c4d2a
**Author:** [[Daniel Tunkelang]]

## Summary

Practical advice for leading search engineering teams. Tunkelang distills his experience into four core recommendations for search team management.

### Recommendation 1: Combine Product and Engineering
Search is a product discipline, not just an engineering one. Teams that separate "search product" from "search engineering" create friction:
- PMs without technical depth make poor trade-off decisions
- Engineers without product intuition build the wrong things
- Best teams have hybrid roles or extremely tight collaboration

### Recommendation 2: Be Data-Driven
Search quality is measurable. Teams that operate without measurement are flying blind:
- Define metrics before building features
- Run A/B tests for every significant change
- Build offline evaluation infrastructure early — it pays for itself
- Don't rely solely on anecdotes ("users told us search is bad")

### Recommendation 3: Incremental Execution
Avoid big-bang rewrites. Search systems are complex enough that:
- Large changes have unpredictable interactions
- Incremental improvements compound over time
- Smaller experiments are easier to measure and roll back
- "Ship, measure, iterate" beats "design, build, launch"

### Recommendation 4: Holistic Approach
Search quality is end-to-end, not just the ranking model:
- Indexing quality matters (what's indexed, freshness)
- Query understanding matters (how queries are parsed)
- UI/UX matters (how results are presented)
- Feedback loops matter (how signals are collected)
- Teams that optimize one component in isolation miss cross-component leverage

### Search PM Skills
A good search PM needs to understand:
- How indexing and query parsing work
- What the ranking features are and their trade-offs
- How to design and interpret A/B tests
- How to prioritize across relevance, latency, and UX

## Key Concepts
- **Combined product-engineering** — avoid org silos in search teams
- **Data-driven search** — measurement and A/B testing as core practice
- **Incremental execution** — prefer small experiments over big rewrites
- **Holistic search quality** — end-to-end thinking across indexing, ranking, UX

## Related Concepts
- [[Search Architecture]]
- [[Search Evaluation]]
- [[A-B Testing for Search]]
- [[Learning to Rank]]

## Related Articles
- [[Search Product Management - The Most Misunderstood Role]]
- [[Affordances for Conversational Search]]
- [[Setting Up a Relevance Evaluation Program]]

## People
- [[Daniel Tunkelang]]
