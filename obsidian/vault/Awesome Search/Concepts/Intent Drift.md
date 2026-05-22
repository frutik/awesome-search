---
title: "Intent Drift"
aliases: ["query drift", "concept drift search", "relevance model staleness", "intent shift"]
tags:
  - concept
  - query-understanding
  - search-quality
  - relevance
---

# Intent Drift

## Definition

Intent drift is the gradual or sudden shift in what users expect from a query, even when the query text stays the same. The words don't change — the right answer does. A relevance model, judgment set, or click-data corpus trained at time T may quietly degrade as the world moves on.

## Types

### Temporal / Concept Drift
World events, trends, or cultural shifts change what a query means or what result is considered relevant.

- "corona" → beer brand (pre-2020) vs. virus (2020+)
- "AI" → narrow ML tool (2021) vs. broad productivity platform (2024)
- "best phone" → the correct answer rotates every 12–18 months

This is the most dangerous type because the query volume stays healthy and the model doesn't throw errors — it just silently serves stale results.

### Seasonal Drift
User intent for a query changes predictably with time of year.

- "gifts" → exploratory browsing (year-round) vs. high-urgency purchasing (November–December)
- "jacket" → lightweight (spring) vs. heavy/insulated (autumn)

Seasonal drift is recoverable with time-aware models or seasonal boosts, but easy to miss if evaluation runs at the wrong time of year.

### Population Drift
The mix of users issuing a query changes, shifting the aggregate intent even if the query text is unchanged.

- A niche technical term goes mainstream (new users have shallower intent)
- A marketing campaign drives a brand query from a new demographic
- A viral moment recontextualises an existing query

### Session Drift
Within a single session, a user's intent evolves as they explore and learn. Early queries in a session may be broad/exploratory; later queries narrow toward a specific need.

This is less about model staleness and more about session-aware retrieval — see [[Conversational Search]].

## Why It Matters

Relevance systems are trained on historical signals:
- Human judgment sets
- Click-through / engagement data
- LLM-generated labels anchored to a point in time

All of these go stale. A model with strong offline metrics on a judgment set from 18 months ago may have quietly drifted from current user expectations — with no test failure to surface it.

## Detection Signals

| Signal | What it indicates |
|--------|------------------|
| CTR drop on stable ranking positions | Users no longer find top results satisfying |
| Zero-result or low-engagement queries rising | Corpus or model lagging new terminology |
| Sudden query volume spike on existing term | Possible meaning shift (event-driven) |
| Judgment set age > 6–12 months | High staleness risk for fast-moving domains |
| NDCG degrading on recent queries vs. older ones | Temporal split reveals drift |

## Mitigations

- **Time-decay on training data** — down-weight clicks and judgments older than N months
- **Periodic re-annotation** — refresh judgment sets on a cadence, prioritising high-volume queries
- **Temporal train/test splits** — evaluate on recent queries, not a random sample
- **Online / continual learning** — incrementally update models from fresh signals
- **Monitoring dashboards** — track CTR, abandonment, and zero-result rate over time, not just at release
- **Human-reviewed reference sets** — a stable, periodically updated anchor set catches silent degradation (see Clippings note on LLM labeling at Dash)

## Relation to General ML Concept Drift

Intent drift is the search-domain instance of the broader ML concept drift problem: the joint distribution P(X, Y) shifts after training. In search, X is the query (stable) and Y is the relevance label (drifting), making it a *label drift* / *posterior drift* case rather than *covariate drift*.

## Related Concepts

- [[Search Intent]] — the baseline taxonomy that drifts
- [[Query Understanding]] — drift affects QU model accuracy over time
- [[Search Evaluation]] — evaluation methodology must account for drift
- [[Conversational Search]] — session-level drift handled differently
- [[Personalization]] — individual-level intent shifts distinct from population drift
