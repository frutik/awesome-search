---
title: "You Say Search, I Say Recs: A Scalable Agentic Approach to Query Understanding and Exploratory Search at Spotify"
source: "https://research.atspotify.com/publications/you-say-search--i-say-recs-a-scalable-agentic-approach-to-query-understanding-and-exploratory-search-at-spotify"
author: "Spotify Research"
published: 2025
tags: [agentic-search, query-understanding, exploratory-search, spotify, recommendations, LLM]
---

# You Say Search, I Say Recs: Spotify Agentic Query Understanding

**Authors:** Spotify Research  
**Venue:** ACM (dl.acm.org/doi/10.1145/3705328.3748127)

## Problem

**Exploratory search** ("new releases for me", "similar artists to X") doesn't fit traditional search — it requires personalized retrieval that lexical/semantic matching alone can't provide. Recommendation systems handle these better, but traditional search can't route to them.

## System Design

- **LLM router**: interprets complex query intent and routes to appropriate downstream service (search API vs. recommendation API)
- **Post-training adaptation**: router fine-tuned for production scale
- **Specialized sub-agents**: handle specific exploratory intents
- **Search + recommendation APIs**: parallel backend services

## Results

| Use Case | Improvement |
|---|---|
| Similar artists discovery | +115% |
| New music releases | +91% |
| Broad music searches | +25% |
| Broad podcast searches | +15% |

## Key Insight

The boundary between search and recommendations is blurry — users say "search" but mean "recommend." An agentic LLM router can identify which intent is truly at play and delegate to the right system.

## Related Concepts

- [[Agentic Search]]
- [[Query Understanding]]
- [[Search Intent]]
- [[Personalization]]
