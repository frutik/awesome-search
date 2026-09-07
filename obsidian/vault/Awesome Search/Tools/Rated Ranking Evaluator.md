---
title: Rated Ranking Evaluator
type: tool
aliases: ["RRE", "Rated Ranking Evaluator (RRE)", "RRE Enterprise"]
tags:
  - tool
  - search-evaluation
  - relevance-testing
  - solr
  - elasticsearch
  - ci-cd
website: https://sease.io/2018/07/rated-ranking-evaluator.html
repo: https://github.com/SeaseLtd/rated-ranking-evaluator
created: 2026-07-03
---

# Rated Ranking Evaluator

**Rated Ranking Evaluator (RRE)** is an open-source, **offline** search-quality evaluation library for [[Solr|Apache Solr]] and [[Elasticsearch]], built and maintained by [[Sease]]. Where [[Quepid]] is an interactive web dashboard, RRE is a **JVM/Maven library** designed to run as part of a build — making it the natural fit for **CI/CD regression testing** of search relevance. Apache 2.0 licensed.

- Sease intro: https://sease.io/2018/07/rated-ranking-evaluator.html
- GitHub: https://github.com/SeaseLtd/rated-ranking-evaluator
- Wiki: https://github.com/SeaseLtd/rated-ranking-evaluator/wiki

---

## Why It Exists

RRE's core philosophy is **incremental, iterative, and immutable** search development: rather than mutating a config in place, you version it, and RRE tracks each version's metrics and the **delta between versions**. This turns "did my change help or hurt relevance?" into an automatable, measurable question you can run on every build — search's answer to unit/regression testing.

## Domain Model

RRE organizes an evaluation as a hierarchy, with metrics computed at the leaf (query) level and aggregated upward by arithmetic mean:

- **Corpus** — the dataset indexed for evaluation.
- **Topics** — top-level thematic groupings of information needs.
- **Query Groups** — sets of equivalent/related queries under a topic.
- **Queries** — the individual query executed against the engine.
- **Ratings / Judgments** — per-(query, document) relevance grades (the ground truth), supplied as JSON.
- **Metrics** — computed per query, then rolled up to Query Group, Topic, and whole-evaluation levels.

## Metrics

RRE ships a broad set of IR measures out of the box:

- **[[Precision and Recall|Precision]]**, **[[Precision and Recall|Recall]]**, **P@1 / P@2 / P@3 / P@10**
- **[[MAP|Average Precision]]** (and Mean Average Precision on aggregation)
- **[[MRR|Reciprocal Rank]]** and **Expected Reciprocal Rank (ERR)**
- **[[NDCG|NDCG@10]]**
- **F-Measure** (F0.5, F1, F2)

Each metric is a first-class, query-level value; the aggregated ("Mean…") variants come from averaging up the topic hierarchy.

## Architecture & Modules

RRE is a set of Maven modules on the JVM:

| Module | Role |
|---|---|
| `rre-core` | The evaluation engine (domain model + metric computation) |
| `rre-search-platform` | Pluggable abstraction over the search engine (Solr / Elasticsearch) |
| `rre-maven-plugin` | Runs evaluations inside a Maven build |
| `rre-maven-reporting-plugin` | Produces human-readable reports (spreadsheet / PDF) for non-technical stakeholders |
| `rre-persistence-plugin` | Persists evaluation output (JSON) |
| `rre-server` | Web control panel; refreshes results in real time after each build |
| `rre-maven-archetype` | Project template to bootstrap an RRE setup |

Primarily Java, with supporting Python/JS. Because the engine is behind `rre-search-platform`, the same evaluation can target different backends.

## Outputs

- **JSON** — machine-readable evaluation results (for pipelines / diffing).
- **Spreadsheet / PDF reports** — via the Maven reporting plugin, aimed at non-technical readers.
- **RRE Server** — a live web dashboard that updates after each build cycle, showing metrics and version-over-version deltas.

## RRE Enterprise

**RRE Enterprise** is Sease's commercial layer built on the open-source library — the same metrics/engine wrapped in a full UI and a simplified, less code-centric user experience.

## RRE vs. Quepid

Both come from the search-relevance consulting world but differ in shape:

| | [[Rated Ranking Evaluator]] | [[Quepid]] |
|---|---|---|
| Form | JVM/Maven **library** | Web **application** |
| Primary mode | Automated, in-build (**CI/CD**) | Interactive, exploratory |
| Audience | Engineers wiring relevance tests into pipelines | Analysts + non-technical raters, team judging |
| Engines | Solr, Elasticsearch | Engine-agnostic — any HTTP endpoint (Solr, ES, OpenSearch, [[Vespa]], [[Qdrant Vector DB\|Qdrant]], custom APIs) |
| Maker | [[Sease]] | [[OpenSource Connections]] |

See [[Relevance Evaluation Tools Compared]] for the fuller landscape including [[Search Relevance Workbench]] and [[Elasticsearch Relevance Studio]].

## Related Tools

- **[[Quepid]]** — interactive counterpart; RRE is the CI/CD-first alternative
- **[[Search Relevance Workbench]]** — OpenSearch's native in-engine evaluator
- **[[Elasticsearch Relevance Studio]]** — Elastic's experimental agentic evaluator
- **[[Solr]]** · **[[Elasticsearch]]** — the engines RRE evaluates
- **[[Releval]]** — engine-agnostic evaluation platform; where RRE puts evaluation in the build, Releval puts it in a self-hosted app with clickstream capture and an MCP server

## Related Concepts

- [[Search Evaluation]] — the practice RRE automates
- [[Judgment Lists]] — RRE's ratings/ground truth
- [[NDCG]] · [[MAP]] · [[MRR]] · [[Precision and Recall]] — the metrics it computes
- [[A-B Testing for Search]] — offline regression testing complements online A/B tests
- [[Relevance Program Setup]] — where RRE fits an org's relevance workflow

## Companies

- [[Sease]] — creator and maintainer (also offers RRE Enterprise)

## Comparison

- [[Relevance Evaluation Tools Compared]] — RRE vs. Quepid vs. Workbench vs. Relevance Studio
