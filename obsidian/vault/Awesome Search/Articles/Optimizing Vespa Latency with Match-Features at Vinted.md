---
created: 2026-06-29
type: article
tags: [article, vespa, match-features, latency, learning-to-rank, feature-store, performance, company-blog]
source: "https://vinted.engineering/2025/11/06/vespa-match-features/"
author: ["Dainius Jocas"]
published: 2025-11-06
company: [Vinted]
concepts: [Vespa Learning to Rank, Feature Store, Reranking]
topics: [Search Platforms]
---

# Optimizing Vespa Latency with Match-Features at Vinted

**[[Dainius Jocas]]**, Vinted Engineering, 2025-11-06.

How [[Vinted]] used [[Vespa]]'s **`match-features`** to both serve ranking features in-engine (instead of round-tripping to Redis) and, more surprisingly, to **cut query latency** by eliminating the document-summary fetch.

## What `match-features` are

Rank features attached to **each hit during the matching phase**, returned without a separate document-summary fetch. Introduced in Vespa 2021. They carry floating-point numbers and **tensors** (not strings/booleans natively); string labels are encoded as mapped tensors via `tensorFromLabels(attribute(my_feature))`. Declared in a `rank-profile`:

```
match-features {
    my_feature
}
```

## Use 1 — Vespa as the feature store

Vinted encodes additional ranking signals that don't live in the document itself — **cross-user interactions, category statistics, contextual signals** — and computes/returns them via `match-features`. This makes Vespa both the **storage and computation layer**, removing the network round-trip to **Redis** for online features. (Compare [[Feature Store]]: this is in-engine feature serving rather than an external store.)

## Use 2 — Latency optimization (the surprising win)

The deeper result: during heavy data redistribution (**500M+ updates/hour across 50+ schemas**), the document-summary `.fill()` step — which fetches summaries *after* matching — became unreliable, with **latency spikes >100 ms** when documents moved between content nodes mid-query.

By selecting **only `match-features`** from a schema (Vespa 8.596.7+), Vinted **eliminated the summary fetch entirely**, collapsing query execution from a **two-phase scatter-gather into a single round-trip**.

### Results

- **P99 latency: ~9 ms → ~3 ms**
- Redistribution-related latency spikes **vanished**
- Mean latency stabilized at **~430 µs at 7.5k RPS per container**

## Why It Matters

A concrete, non-obvious lesson: the document-summary fetch is a hidden second phase, and pushing the values you actually need into `match-features` can both **replace an external feature store** and **remove a whole network phase** from the query path. Directly relevant to the feature-logging step of [[Vespa Learning to Rank]] — the same mechanism that dumps training features also serves them online cheaply.

## Related Concepts

[[Vespa Learning to Rank]] · [[Vespa]] · [[Feature Store]] · [[Reranking]] · [[Retrieval Pipeline]]

## Related Notes

- [[Vespa Learning to Rank]] — `match-features` as the feature-logging / online-serving mechanism
- [[Adopting Vespa for Recommendation Retrieval at Vinted]] — Vinted's other Vespa post (same author)
- [[Vinted - Migrating Search from Elasticsearch to Vespa]] — the platform migration this builds on

## People

- [[Dainius Jocas]] — Vinted; author (also co-authored the recommendation-retrieval post)
