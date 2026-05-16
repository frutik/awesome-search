---
type: company
category: end-user
industry: [music streaming, audio, podcasts]
products: [Spotify music search, podcast search, artist discovery]
search_domain: music and audio content discovery, exploratory search
use_cases: ["[[Spotify - Agentic Query Understanding]]"]
tags: [company, end-user, streaming, agentic-search, recommendations]
created: 2026-05-16
---

# Spotify

Global music and audio streaming platform. Search challenge: the boundary between search and recommendations is blurry — users say "search" but often mean "recommend."

## Search Context

Exploratory queries like "new releases for me" or "similar artists to X" don't fit traditional search — they require personalized retrieval that lexical or semantic matching alone can't provide.

## Key Engineering Work

### Agentic LLM Router
- **LLM router** interprets complex query intent and routes to the appropriate downstream service: search API vs. recommendation API
- Post-training adaptation: router fine-tuned for production scale
- Specialized sub-agents handle specific exploratory intents

### Results

| Use Case | Improvement |
|---|---|
| Similar artists discovery | +115% |
| New music releases | +91% |
| Broad music searches | +25% |
| Broad podcast searches | +15% |

### Key Insight
Users express exploratory intent through a search interface. An agentic LLM router can identify whether the intent is truly a search or a recommendation, then delegate accordingly.

## Articles

- [[You Say Search I Say Recs - Spotify Agentic Query Understanding]] — LLM routing architecture, results

## Related Concepts

- [[Agentic Search]] · [[Query Understanding]] · [[Search Intent]] · [[Personalization]]
