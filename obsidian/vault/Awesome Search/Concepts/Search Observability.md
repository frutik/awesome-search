---
title: "Search Observability"
aliases: ["search monitoring", "search instrumentation", "production search monitoring", "search telemetry"]
tags:
  - concept
  - search-quality
  - metrics
  - monitoring
  - production
created: 2026-06-01
---

# Search Observability

## Definition

Search observability is the practice of instrumenting a live search system so that its behavior, health, and quality are continuously visible in production. It is the operational counterpart to [[Search Quality Assurance]]: SQA asks "is this version better than that version?" using offline evaluation; observability asks "what is the running system doing right now, and is it drifting?" using live signals.

The central challenge is that search failure is mostly silent — users abandon or reformulate instead of triggering errors, so standard infrastructure monitoring misses most quality problems.

## Three Planes of Signals

| Plane | Question | Key signals |
|---|---|---|
| **User behavior** | Are users finding what they want? | CTR, zero-result rate, abandonment rate, query reformulation rate, dwell time |
| **System health** | Is the system up and performing? | P50/P99 latency, error rate, indexing lag, cache hit rate, shard availability |
| **Quality trends** | Is relevance drifting over time? | CTR trend by query tier, zero-click growth, clicks residual, NDCG on a reference set |

## Key Concepts

- **[[Click Signals]]** — primary behavioral signal; always available but position-biased
- **[[Clicks Residual]]** — expected vs. actual clicks per query; detects silent quality degradation
- **[[Zero Results]]** — the one unambiguous failure: no results returned for a query
- **[[Intent Drift]]** — gradual quality degradation observable only through longitudinal monitoring
- **[[Session-Based Evaluation]]** — session-level signals as higher-fidelity observability

## Relationship to Adjacent Concepts

- **[[Search Quality Assurance]]** — offline evaluation; shares metrics but different purpose and cadence
- **[[A-B Testing for Search]]** — controlled experiments as a reactive complement to passive monitoring
- **[[Intent Drift]]** — observability is the detection mechanism for drift

## Deep Dive

See [[Search Observability]] (Topic) for instrumentation patterns, alerting design, diagnostic workflows, and failure modes.
