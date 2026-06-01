---
title: "Autosuggest Ranking"
aliases: ["Autocomplete Ranking", "Giovanni Autosuggest Ranking"]
tags:
  - clippings
  - search
  - autocomplete
  - ranking
  - medium
source: "https://medium.com/@dtunkelang/autosuggest-ranking"
author: "Giovanni Fernandez-Kincade"
created: 2026-05-15
concepts:
  - Autocomplete
  - Learning to Rank
  - Personalization
---

# Autosuggest Ranking

**Source:** https://medium.com/@dtunkelang/autosuggest-ranking
**Author:** [[Giovanni Fernandez-Kincade]]

## Summary

Once autocomplete candidates are retrieved (see [[Autosuggest Retrieval Data Structures and Algorithms]]), they need to be ranked. This article covers probabilistic and learning-to-rank approaches for autosuggest ranking.

### The Ranking Problem
Given a prefix and a set of candidate completions, order them by predicted utility — the completion the user most likely wants to type next.

### Baseline: Frequency-Based Ranking
Sort candidates by historical query frequency (global):
- "shoes" (10M queries) before "shoe repair near me" (50K queries)
- Simple, fast, interpretable
- Problem: ignores context (session, user, location, time)

### Probabilistic Model
Model the probability a user will complete their prefix P with candidate C:

```
P(C | P) ∝ P(P | C) × P(C)
```

Where:
- P(C) = prior probability of the candidate (frequency-based)
- P(P | C) = likelihood of typing prefix P if intending C (edit model)

This is a **noisy channel** framing similar to spelling correction.

### Feature-Based Ranking (LTR)
Key feature categories:

**Temporal features:**
- Recency of last usage
- Trending signal (spike in last 24h)
- Seasonality (Christmas gifts in December)

**Demographic/contextual features:**
- User's location → local completions ranked higher
- User's language/locale
- Session context (what has the user already searched this session?)

**Behavioral features:**
- Click-through rate of the completion
- Conversion rate if clicked
- Session abandonment rate

**Query features:**
- Length of prefix typed
- How specific vs. generic the candidate is

### Two-Phase Ranking
For latency, use two stages:
1. **Fast retrieval** (< 10ms): use edge n-grams or FST to get top-100 candidates
2. **Ranking** (< 30ms): score and reorder with a lightweight LTR model

### Personalization
Personalized autosuggest re-ranks based on user history:
- Boost completions the user has typed before
- Boost completions in categories the user frequently shops
- Decay over time (stale preferences less relevant)

### Cold-Start Mitigation
New users have no history → fall back to:
- Location-based defaults
- Demographically similar users
- Pure frequency-based ranking

## Key Concepts
- **Noisy channel model** — probabilistic framing of prefix-to-completion likelihood
- **Temporal features** — recency, trending, seasonality for ranking
- **Two-phase ranking** — fast retrieval + heavier scoring
- **Personalized autosuggest** — user-history-aware reranking
- **Cold-start fallback** — location/demographic defaults for new users

## Related Concepts
- [[Autocomplete]]
- [[Learning to Rank]]
- [[Personalization]]
- [[Position Bias]]
- [[Click Signals]]

## Related Articles
- [[Autosuggest Retrieval Data Structures and Algorithms]]
- [[Spelling Correction in Search]]

## People
- [[Giovanni Fernandez-Kincade]]
