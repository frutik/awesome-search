---
title: Search Relevance Workbench
type: tool
aliases: ["SRW", "OpenSearch Search Relevance Workbench", "OpenSearch Relevance Workbench"]
tags:
  - tool
  - search-evaluation
  - relevance-testing
  - opensearch
website: https://docs.opensearch.org/latest/search-plugins/search-relevance/using-search-relevance-workbench/
repo: https://github.com/opensearch-project/search-relevance
created: 2026-07-03
---

# Search Relevance Workbench

**Search Relevance Workbench (SRW)** is a native, open-source tool built into [[OpenSearch]] for systematically evaluating and improving search quality. It brings the offline-evaluation loop — query sets, judgments, experiments, metrics — *inside* the search engine and its dashboards, rather than as an external SaaS. Launched in **OpenSearch 3.1** (mid-2025), with dashboard visualizations added in **3.2**. Co-developed with heavy input from [[OpenSource Connections]] (the makers of [[Quepid]]), and closely tied to the [[User Behavior Insights|User Behavior Insights (UBI)]] specification.

- Docs: https://docs.opensearch.org/latest/search-plugins/search-relevance/using-search-relevance-workbench/
- GitHub: https://github.com/opensearch-project/search-relevance

---

## Why It Exists

Historically, evaluating OpenSearch/Elasticsearch relevance meant bolting on an external tool like [[Quepid]] or [[Rated Ranking Evaluator]]. SRW moves that workflow into the engine itself: judgments, query sets, and experiments are stored as OpenSearch indices, experiments run server-side against live search configurations, and results are visualized in OpenSearch Dashboards. It is an **opt-in** feature enabled through Dashboards settings.

## Core Building Blocks

The workbench is built on three primitives:

- **Query sets** — a collection of queries used as the test workload for experiments. Can be imported or sampled (e.g. from [[User Behavior Insights|UBI]] query logs), supporting realistic, production-derived query distributions.
- **Search configurations** — a reusable definition of *how* to run a query (the query template/DSL, index, pipeline). Two configurations can differ by one parameter, which is what makes A/B-style comparison possible.
- **Judgments** — (query, document ID, rating) triplets that establish ground truth relevance. Stored in a dedicated judgments index for reuse across experiments.

## Experiment Types

| Experiment | Purpose |
|---|---|
| **Search result comparison** | Diff the result sets of two search configurations on the same query set (pointwise + aggregate) |
| **Search quality evaluation** | Score one search configuration against a judgment list, computing IR metrics |
| **Hybrid search optimization** | Grid-search hybrid-search parameters to find the best lexical/neural blend |

### Hybrid search optimization

A standout feature with no direct Quepid equivalent: SRW sweeps [[Hybrid Search]] parameters automatically — two normalization techniques (`l2`, `min_max`), three combination techniques (`arithmetic_mean`, `harmonic_mean`, `geometric_mean`), and lexical vs. neural weights from 0.0–1.0 in 0.1 steps — then reports which combination maximizes the chosen metric ([OpenSearch docs: optimizing hybrid search](https://docs.opensearch.org/latest/search-plugins/search-relevance/optimize-hybrid-search/)).

## Judgments: Three Sources

SRW is notable for supporting all three judgment-generation strategies natively:

1. **Implicit** — derived from [[User Behavior Insights|UBI]] clickstream data using a **COEC (Clicks Over Expected Clicks)** model to debias by position.
2. **Explicit (human)** — uploaded as CSV directly in the Dashboards UI (up to ~10,000 rows). **Judgments exported from [[Quepid]] can be imported this way**, giving a migration path.
3. **LLM-as-judge** — supply an LLM model ID plus a query set and search configuration, and SRW generates ratings automatically (the docs demo GPT-4o mini). See [[LLM as Judge]].

All generated judgments land in the judgments index for reuse.

## Metrics

Experiments compute standard IR metrics at *k*:

- **[[Precision and Recall|Precision@k]]**
- **[[MAP|MAP@k]]** (Mean Average Precision)
- **[[NDCG|NDCG@k]]** (Normalized Discounted Cumulative Gain)
- **Judgment Coverage** — how much of the returned result set was actually rated (surfaces gaps in ground truth, echoing Relevance Studio's "unrated documents" reporting)

## Dashboards & Visualization (3.2+)

The frontend plugin adds four views for exploring experiment output:

- **Deep Dive Summary**
- **Query Scores**
- **Score Densities**
- **Score Scatterplot**

## Architecture

- **`search-relevance` plugin** — backend: stores query sets, search configurations, judgments, and experiments as OpenSearch indices; runs experiments server-side.
- **Dashboards plugin** — the UI layer for creating experiments and visualizing results.
- **UBI integration** — consumes the [[User Behavior Insights]] schema (client-side JS collectors + `ubi_queries` / `ubi_events` indices) to feed implicit judgments.

## Related Tools

- **[[Quepid]]** — the external SaaS predecessor from the same authors; SRW imports Quepid CSV judgments. See [[Relevance Evaluation Tools Compared]].
- **[[Elasticsearch Relevance Studio]]** — Elastic's parallel (experimental) in-house answer to the same problem.
- **[[Rated Ranking Evaluator]]** — Sease's CI/CD-oriented offline evaluator.
- **[[OpenSearch]]** — the host engine.

## Related Concepts

- [[Search Evaluation]] — the practice SRW operationalizes
- [[Judgment Lists]] — the ground-truth data it manages
- [[Implicit Judgments]] — UBI-derived judgments via COEC
- [[User Behavior Insights]] — the clickstream standard those judgments are built from
- [[LLM as Judge]] — automated judgment generation
- [[NDCG]] · [[MAP]] · [[Precision and Recall]] — the metrics it computes
- [[Hybrid Search]] — the target of the optimization experiment
- [[A-B Testing for Search]] — SRW's offline comparison complements online A/B tests

## People

- [[Daniel Wrigley]] — [[OpenSource Connections]]; authored the OpenSearch blog introducing SRW and the judgments workflow

## Comparison

- [[Relevance Evaluation Tools Compared]] — SRW vs. [[Quepid]] vs. [[Elasticsearch Relevance Studio]]
