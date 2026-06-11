---
type: tool
title: "Metarank"
aliases: ["Metarank"]
website: "https://metarank.ai/"
repo: "https://github.com/metarank/metarank"
tags:
  - tool
  - ranking
  - learning-to-rank
  - reranking
  - personalization
  - open-source
---

# Metarank

Open-source, real-time **secondary re-ranker** and personalization service written in Scala. It sits between a search/recommendation engine and the user: ingest behavioral events (impressions, clicks, purchases), train a [[Learning to Rank|LTR]] model, and rerank candidate sets at serving time. Created/maintained by [[Roman Grebennikov]] and [[Vsevolod Goloviznin]].

- Website: https://metarank.ai/
- GitHub: https://github.com/metarank/metarank
- Docs: https://docs.metarank.ai/

## What it does

- Implements **[[LambdaMART]]** over an embedded feature-engineering pipeline (other models: Shuffle, Trending, MF/ALS collaborative filtering, BERT semantic; BPR & BERT4Rec on the roadmap).
- **Retrieval-agnostic**: integrates with the application, not the search engine — works downstream of Elasticsearch, [[OpenSearch]], Solr, or [[Pinecone Vector DB|Pinecone]].
- **YAML DSL** for 20+ feature extractors: CTR/conversion rates, sliding-window counts, UA/Referer/GeoIP parsing, one-hot/label encoding, scalar item fields.
- Full feedback loop: event import → training → serving, runnable as one stateless Docker service (`standalone` mode) or split sub-commands (`import`, `train`, `serve`).
- Trains on historical click-through events aggregated into **[[Implicit Judgments]]**.

## Architecture notes

- fs2 + cats-effect streaming pipeline; `ImpressionInject` synthesizes negative signals (shown-but-not-clicked).
- http4s `POST /rank/{model}`; `?explain=true` returns per-item feature values.
- **Redis** state store in production (in-memory for demos); ~20–30 ms re-ranking latency budget.
- Datasets: [RankLens](https://github.com/metarank/ranklens), [MSRD](https://github.com/metarank/msrd).

## Use cases in this vault

- [[Hybrid Search and Learning-to-Rank with Metarank]] — fusing BM25 + vector retrievers via LTR
- [[Learn-to-Rank with OpenSearch and Metarank]] — external re-ranker on OpenSearch
- [[Metarank - Personalized Ranking That Actually Reads Your Clicks]] — code-level repo review

## Related

- [[Learning to Rank]] · [[LambdaMART]] · [[Reranking]] · [[Retrieval Pipeline]] · [[Personalization]] · [[Feature Store]] · [[Implicit Judgments]] · [[Interleaving]]
- Implementations it builds on: [[XGBoost]] · [[LightGBM]]
- [[OpenSearch]] · [[Pinecone Vector DB]]

## People

- [[Roman Grebennikov]] · [[Vsevolod Goloviznin]] — creators
