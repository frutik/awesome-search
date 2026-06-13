---
title: Elasticsearch Learning to Rank
aliases:
  - Elasticsearch LTR
  - ES LTR
  - in-engine LTR
  - native LTR
tags:
  - concept
  - ranking
  - learning-to-rank
  - elasticsearch
  - search
type: concept
---

# Elasticsearch Learning to Rank

In-engine [[Learning to Rank|LTR]]: running a learned ranking model **inside** Elasticsearch as a second-stage rescorer, rather than in an external service. The model is trained offline (a [[LambdaMART]] / GBDT), uploaded into the cluster, and applied to rescore the top-N hits of a cheap first-pass query. Features are computed at query time from **templated Query DSL queries** — the relevance score of `match`/`multi_match` etc. becomes a feature value.

Elasticsearch offers **in-engine** LTR: the model runs inside the cluster as a `rescore` phase, not as a separate service. There are two distinct modules — the third-party [[OpenSource Connections]] plugin and Elastic's **native** LTR (8.12+) — and this note focuses on that ES-specific distinction.

The broader architectural question — in-engine LTR vs. an external, engine-agnostic secondary re-ranker like [[Metarank]] — is not Elasticsearch-specific and is covered in [[Learning to Rank]]. Both modules below are in-engine options.

## Two Elasticsearch LTR modules

There is no single "Elasticsearch LTR." Two distinct implementations exist, separated by ~7 years.

### 1. OpenSource Connections plugin (2017)

The original `o19s/elasticsearch-learning-to-rank` plugin from [[OpenSource Connections]] — for years the *only* way to do LTR in Elasticsearch, and still in wide use (it powered Wikipedia search).

- Integrates **[[RankLib]]** (the `RankyMcRankFace` o19s fork): trains LambdaMART/RankNet from a judgment file.
- Ships a custom Elasticsearch script language (`ranklib`) to store the model, and a custom **`ltr` query** that takes a list of Query DSL queries as features plus a model name.
- Applied through `rescore` over the top-N (running the `ltr` query directly over a whole collection is too slow).
- Community-maintained; must be installed as a plugin.
- See [[We're Bringing Learning to Rank to Elasticsearch]].

### 2. Native Elastic LTR (8.12+)

Elastic shipped first-party LTR in **8.12** (2024), removing the need for the third-party plugin (subscription-gated).

- Model trained **outside** Elasticsearch as a GBDT — Elastic recommends **[[XGBoost]]**'s `XGBRanker` (a LambdaMART implementation); inference runs in-engine.
- Models uploaded with **[[eland]]** (Elastic's Python helper).
- Features extracted via templated `query_extractor` queries (e.g. `title_bm25`), grouped into a feature set; three feature categories — document, query, and query-document.
- Served as a **`learning_to_rank` rescorer** (8.12+), or as a **`rescorer` retriever** (9.1+) inside the retriever pipeline.
- `window_size` is mandatory for the rescorer (LTR scores aren't comparable to first-pass scores) and must stay constant across paginated requests.
- See [[Learning To Rank (LTR) - Elasticsearch Native]] and [[Search using LTR - Elastic Docs]].

Both modules share the same shape — train a GBDT offline, store it, rescore the top-N with query-derived features — and differ in training library (RankLib vs XGBoost), packaging (plugin vs built-in), and support model (community vs Elastic subscription).

## Related Concepts

- [[Learning to Rank]] — the general technique this specializes
- [[LambdaMART]] — the model both modules serve
- [[Reranking]] — LTR is the rescoring stage
- [[Retrieval Pipeline]] — first-pass retrieval → LTR rescore
- [[Feature Store]] — what external re-rankers add and in-engine LTR avoids
- [[Judgment Lists]] · [[Implicit Judgments]] — training data
- [[Hybrid Search]] — multi-retriever fusion, where external LTR has an edge

## Related Tools

- [[Elasticsearch]] · [[Metarank]] · [[RankLib]] · [[XGBoost]] · [[eland]] · [[OpenSearch]]

## Articles

- [[We're Bringing Learning to Rank to Elasticsearch]] — [[OpenSource Connections]]; the 2017 RankLib-based plugin
- [[Learning To Rank (LTR) - Elasticsearch Native]] — Elastic docs; native 8.12+ overview
- [[Search using LTR - Elastic Docs]] — Elastic docs; rescorer & retriever usage
- [[Learn-to-Rank with OpenSearch and Metarank]] — external re-ranker contrast
- [[Hybrid Search and Learning-to-Rank with Metarank]] — multi-retriever fusion case

## Companies

- [[OpenSource Connections]] — authored the original plugin
- [[Elastic]] — ships native LTR
