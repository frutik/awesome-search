---
type: article
title: "Metarank - Personalized Ranking That Actually Reads Your Clicks"
source: "https://www.codeline.co/thoughts/repo-review/2025/metarank-personalized-ranking-that-actually-reads-your-clicks"
author: "[[Florian Narr]]"
published: 2025-12-15
created: 2026-06-11
concepts:
  - "[[Learning to Rank]]"
  - "[[LambdaMART]]"
  - "[[Reranking]]"
  - "[[Personalization]]"
  - "[[Click Signals]]"
  - "[[Feature Store]]"
topics:
  - "[[Personalization in Search]]"
tags:
  - article
  - ranking
  - learning-to-rank
  - personalization
  - reranking
  - open-source
---

# Metarank - Personalized Ranking That Actually Reads Your Clicks

**Source:** https://www.codeline.co/thoughts/repo-review/2025/metarank-personalized-ranking-that-actually-reads-your-clicks
**Author:** [[Florian Narr]]
**Published:** 2025-12-15

A code-level "repo review" of [[Metarank]], the open-source real-time personalization / [[Learning to Rank]] service written in Scala.

---

## Summary

Metarank sits between a search engine and its users: feed it events (clicks, purchases, impressions) and it reranks results or recommendations on the fly, learning per session. It occupies a rare middle ground between massive internal ranking platforms and thin single-model wrappers — shipping 20+ built-in feature extractors (CTR, user agent, referer, interaction counts, time decay) and handling the whole feedback loop (event ingestion → model training → serving) as a single stateless service runnable in Docker. YAML-driven config lets you reach a working [[LambdaMART]] ranker without writing Scala.

## Architecture (from the code)

- **`FeatureMapping`** — turns YAML feature/model definitions into instantiated feature extractors and predictors. Predictors include `LambdaMARTPredictor`, `ShufflePredictor`, `TrendingPredictor`, `MFPredictor` (collaborative filtering via ALS), and `BertSemanticPredictor` (neural search). Bridges Metarank features to the underlying `ltrlib` LTR library.
- **`MetarankFlow`** — event-processing pipeline on fs2 streams + cats-effect. A `TrainBuffer` collects clickthrough data; `ImpressionInject` synthesizes negative signals (shown-but-not-clicked) — the feedback loop that makes the model learn.
- **`FeatureValueFlow`** — Scaffeine cache with a custom ticker; per-feature `refresh` interval so high-frequency features (click counts) update every event while slow features skip recomputation.
- **`RankApi`** — http4s `POST /rank/{model}`; `?explain=true` exposes per-item feature values for debugging.

## Rough edges (per author)

- Custom feature extractors require extending `BaseFeature` in Scala + recompiling a JAR — no plugin/scripting layer.
- Production state is **Redis-only** ([[Feature Store]] concern); in-memory store is demo-only.
- Heavy JVM/Scala Docker image, non-instant startup; slowed development since ~September 2025.

## Bottom line

The most complete open-source option for adding click-based personalization to an existing search system without building feature engineering, the feedback loop, and training from scratch — best for teams already comfortable with JVM services and Redis.

## Related Concepts

- [[Metarank]] · [[Learning to Rank]] · [[LambdaMART]] · [[Reranking]] · [[Personalization]] · [[Click Signals]] · [[Feature Store]] · [[Implicit Judgments]]

## Related Articles

- [[Learn-to-Rank with OpenSearch and Metarank]]
- [[Hybrid Search and Learning-to-Rank with Metarank]]

## People

- [[Florian Narr]] — author
- [[Roman Grebennikov]], [[Vsevolod Goloviznin]] — Metarank creators
