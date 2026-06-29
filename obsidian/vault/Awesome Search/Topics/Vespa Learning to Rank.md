---
type: topic
title: Vespa Learning to Rank
aliases:
  - Vespa LTR
  - Vespa GBDT ranking
  - Vespa ranking expressions
  - Vespa phased ranking
tags:
  - topic
  - ranking
  - learning-to-rank
  - vespa
  - search
related_concepts: [Learning to Rank, LambdaMART, Ranking Objectives, LTR Feature Engineering, Cross-Encoder, Reranking, Retrieval Pipeline]
related_topics: [Late Interaction in Vespa, Elasticsearch vs OpenSearch, Search Platforms, Reasoning Reranking, Frontier of Search 2025]
related_tools: ["[[Vespa]]", "[[XGBoost]]", "[[LightGBM]]", "[[ONNX]]"]
companies: [Vespa]
created: 2026-06-29
---

# Vespa Learning to Rank

In-engine [[Learning to Rank|LTR]] in [[Vespa]]: learned ranking models run **inside** Vespa as part of its general **ranking-expression** framework, across multiple ranking phases. Where [[Elasticsearch Learning to Rank]] bolts a single GBDT rescorer onto a Lucene engine, Vespa was built ML-native — GBDT models ([[XGBoost]], [[LightGBM]]), [[ONNX]] neural models, and tensor expressions ([[Late Interaction in Vespa|MaxSim]]) are all first-class citizens of the same `rank-profile`, and can be combined into ensembles. The general in-engine-vs-external-reranker question is covered in [[Learning to Rank]]; this note covers the Vespa-specific mechanics.

## Phased Ranking

Vespa's LTR backbone is **multi-phase ranking** declared in a `rank-profile`. Each phase reranks the survivors of the previous one, spending more compute on fewer candidates:

```
rank-profile product_ltr {
    first-phase {
        expression: bm25(title) + bm25(description)
    }
    second-phase {
        expression: xgboost("my_gbdt.ubj")
        rerank-count: 1000
    }
    global-phase {
        expression: sum(onnx(cross_encoder))
        rerank-count: 20
    }
}
```

| Phase | Where it runs | Typical use |
|---|---|---|
| **first-phase** | on every matching document, per content node | cheap retrieval score (BM25, a linear combo) to pick top-k |
| **second-phase** | **locally on each content node**, over `rerank-count` candidates | the GBDT LTR model ([[LambdaMART]] via XGBoost/LightGBM) — efficient on thousands of candidates without leaving the node |
| **global-phase** | **on the container node after merging** results from all content nodes | the most expensive, highest-quality reranker (a [[Cross-Encoder]] / listwise model); also cross-hit normalization |

This is the same retrieve→rerank pattern as everywhere, but Vespa makes the stages explicit and runs the GBDT *next to the data* rather than in a separate service.

## Model Support (one unified framework)

Vespa imports trained models into **its own ranking framework** (it does not call the original library's inference), giving accelerated GBDT inference and letting you **ensemble across frameworks** in one expression.

| Model | Ranking-expression function | Notes |
|---|---|---|
| [[XGBoost]] | `xgboost("model.ubj")` | export with `save_model(".ubj")` (recommended) or legacy `dump_model(dump_format="json")`; **not** `save_model("model.json")` |
| [[LightGBM]] | `lightgbm("model.json")` | GBDT and `lambdarank` objective |
| [[ONNX]] | `onnx(model_name)` | neural rankers / [[Cross-Encoder|cross-encoders]]; accelerated by ONNX-Runtime |

Models live in the application package's **`models/`** directory:

```
├── models/
│   ├── my_gbdt.ubj
│   └── my_gbdt-features.txt   # one Vespa rank feature per line, in training-column order
├── schemas/main.sd
└── services.xml
```

For UBJ models the `<model>-features.txt` file maps each model input to a Vespa rank feature (often via a named `function`); for legacy JSON, XGBoost's default `f0, f1, …` split names must resolve to valid rank features. Wrap in `sigmoid(xgboost(...))` for logistic objectives.

## Features (and dumping them for training)

The model's inputs are **rank features** computed at query time:

- **Document** — `attribute(price)`, `attribute(popularity)`
- **Query** — `query(name)`; tensor inputs declared in an `inputs { ... }` block
- **Match / built-in** — `bm25(title)`, `nativeRank`, `fieldMatch(title)`, `closeness`, `distance` (and tensor `MaxSim` expressions, see [[Late Interaction in Vespa]])

To build training data, Vespa **dumps feature values** alongside results:

- `match-features` — feature values emitted per matched doc (the standard way to collect a training set; can also serve features online and even cut latency by skipping the summary fetch — see [[Optimizing Vespa Latency with Match-Features at Vinted]])
- `summary-features` — feature values returned in the document summary
- `rank-features` — the full feature set exposed to external systems

## The Workflow

1. **Collect** [[Judgment Lists]] / [[Implicit Judgments]] (clicks, conversions).
2. **Dump features** for each (query, doc) with `match-features`.
3. **Train offline** — XGBoost/LightGBM with a `lambdarank` / NDCG listwise objective ([[LambdaMART]]).
4. **Deploy** — drop the model file in `models/`, reference it via `xgboost(...)` / `lightgbm(...)` in `second-phase`, redeploy the application package.
5. **Serve in-engine** — inference runs on the content nodes; no external reranker tier.

## Vespa LTR vs Elasticsearch LTR

| | [[Vespa Learning to Rank|Vespa]] | [[Elasticsearch Learning to Rank|Elasticsearch]] |
|---|---|---|
| Where the model runs | ranking-expression phases (content node + container) | `rescore` / `learning_to_rank` rescorer (top-N) |
| Phases | first / second / **global** (cross-hit) | single rescore window |
| GBDT libraries | XGBoost, LightGBM (native import) | XGBoost (native, via [[eland]]) or RankLib (OSC plugin) |
| Neural rankers | ONNX cross-encoders in the same profile | separate (e.g. `elastic-rerank`) |
| Ensembles | mix GBDT + ONNX + tensor features in one expression | not in-engine |
| Packaging | first-class; `models/` in the app package | native module (8.12+) or third-party plugin |

The throughline matches the late-interaction story: Vespa doesn't add a dedicated LTR subsystem — it exposes one tensor/expression ranking engine, and GBDT LTR, neural reranking, and MaxSim are all just expressions in it.

## Related Concepts

- [[Learning to Rank]] — the general technique; in-engine vs external re-ranker
- [[Elasticsearch Learning to Rank]] — the parallel in-engine LTR note for Elasticsearch
- [[LambdaMART]] — the GBDT/listwise model served in second-phase
- [[Ranking Objectives]] — pointwise/pairwise/listwise losses (lambdarank)
- [[LTR Feature Engineering]] — the features fed into the model
- [[Late Interaction in Vespa]] — MaxSim tensor scores as features/phases in the same framework
- [[Cross-Encoder]] — typical `global-phase` ONNX reranker
- [[Judgment Lists]] · [[Implicit Judgments]] — training data

## Related Tools

- [[Vespa]] · [[XGBoost]] · [[LightGBM]] · [[ONNX]]

## Source

- [Learning to Rank — Vespa docs](https://docs.vespa.ai/en/learning-to-rank.html)
- [Ranking with XGBoost Models — Vespa docs](https://docs.vespa.ai/en/ranking/xgboost.html)
- [Ranking with LightGBM Models — Vespa docs](https://docs.vespa.ai/en/ranking/lightgbm.html)
- [Ranking (phases & features) — Vespa docs](https://docs.vespa.ai/en/basics/ranking.html)
- [Improving Product Search with Learning to Rank (blog series) — Vespa](https://blog.vespa.ai/improving-product-search-with-ltr-part-two/)
