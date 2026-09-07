---
title: Relevance Evaluation Tools Compared
type: topic
aliases: ["Workbench vs Quepid", "Search Relevance Workbench vs Quepid", "Relevance Evaluation Tooling Comparison", "Quepid vs Relevance Studio vs Workbench"]
tags:
  - topic
  - search-evaluation
  - relevance-testing
  - comparison
related_concepts:
  - Search Evaluation
  - Judgment Lists
  - Implicit Judgments
  - LLM as Judge
related_topics:
  - Relevance Program Setup
  - Search Quality Assurance
created: 2026-07-03
---

# Relevance Evaluation Tools Compared

A side-by-side comparison of five tools that operationalize offline [[Search Evaluation]] — turning [[Judgment Lists|judgments]] into ranking metrics you can iterate against:

- **[[Quepid]]** — the incumbent, engine-agnostic external dashboard from [[OpenSource Connections]].
- **[[Search Relevance Workbench]]** (SRW) — [[OpenSearch]]'s native, in-engine workbench.
- **[[Elasticsearch Relevance Studio]]** (ESRS) — Elastic's experimental, agentic lifecycle tool for [[Elasticsearch]].
- **[[Rated Ranking Evaluator]]** (RRE) — [[Sease]]'s CI/CD-first evaluation *library* for Solr and Elasticsearch.
- **[[Releval]]** — a self-hosted commercial platform; engine-agnostic like Quepid, but with native clickstream capture and an MCP server.

All five share the same core loop: define a **query set / scenarios**, attach **judgments**, define one or more **search configurations / strategies**, run an **experiment / benchmark**, and read **IR metrics** ([[NDCG]], [[Precision and Recall|P@k / R@k]], [[MRR]], [[MAP]]). The split that matters most: **Quepid**, **RRE** and **Releval** are external and engine-neutral (dashboard, build library, and platform respectively), while **SRW** and **ESRS** are locked to one engine but gain tighter integration and new judgment sources. A second split cuts across that one: four are open source, **Releval** alone is proprietary.

---

## At a Glance

| Dimension | [[Quepid]] | [[Search Relevance Workbench]] | [[Elasticsearch Relevance Studio]] | [[Rated Ranking Evaluator]] | [[Releval]] |
|---|---|---|---|---|---|
| **Maker** | [[OpenSource Connections]] | [[OpenSearch]] project (OSC-influenced) | [[Elastic]] | [[Sease]] | Releval |
| **Maturity** | Mature, widely used in production | GA feature (OpenSearch 3.1+, 2025) | Experimental / demonstrator | Mature (since 2018); RRE Enterprise commercial layer | New — 1.0.0 released July 2026 |
| **Where it runs** | External web app (SaaS or self-host) | Inside OpenSearch + Dashboards | Standalone React+Flask app over ES | JVM/Maven **library** in your build (+ RRE Server dashboard) | Self-hosted Docker (Postgres + optional ClickHouse) |
| **Engine coupling** | Engine-agnostic — any HTTP endpoint (ES, OpenSearch, Solr, and demonstrated with [[Vespa]], [[Qdrant Vector DB\|Qdrant]], custom APIs) | OpenSearch only | Elasticsearch only | Solr + Elasticsearch (pluggable search-platform API) | Engine-agnostic — ES, OpenSearch, Solr, Vespa, any HTTP API, rendered SERPs |
| **Judgment store** | Quepid's own DB (MySQL) | OpenSearch judgments index | Elasticsearch index | JSON ratings files in the project repo | PostgreSQL; qrels-shaped uploads (JSONL/CSV/TSV/Parquet) |
| **License / cost** | Open source (o19s/quepid), free SaaS tier | Apache 2.0, bundled with OpenSearch | Open source demo (elastic/relevance-studio) | Apache 2.0 (RRE Enterprise commercial) | **Proprietary**, EULA-gated; no public source |

## Judgment Sources

| Source | Quepid | SRW | ESRS | RRE | Releval |
|---|---|---|---|---|---|
| **Human (manual)** | ✅ Collaborative UI, books of judgements, information needs | ✅ CSV upload (~10k rows) | ✅ Drag-slider UI | ✅ Ratings authored as JSON files | ✅ Inline judging during a run, plus qrels-shaped uploads |
| **LLM-as-judge** | ✅ (v8+) | ✅ Native (model ID + query set) | ✅ Agent-generated, human-reviewed | ➖ Not native | ✅ Saved "AI Judges" (OpenAI, Anthropic, Bedrock) with prompt templates |
| **Implicit (clickstream)** | ➖ Not native | ✅ Via [[User Behavior Insights\|UBI]] + COEC debiasing | ➖ Not native | ➖ Not native | ✅ Native [[User Behavior Insights\|UBI]] capture into ClickHouse |
| **Import path** | — | ✅ Imports Quepid CSV | — | — | ✅ TREC qrels shape (JSONL/CSV/TSV/Parquet) |

SRW and Releval are the only two that natively derive **implicit judgments** from user behavior ([[User Behavior Insights|UBI]] clickstream) — but SRW is OpenSearch-only, so **Releval is the only engine-agnostic tool here with native clickstream capture**. SRW debiases with Clicks-Over-Expected-Clicks; Releval's UBI store is the raw causal query→interaction join, leaving click modelling to the user. Both SRW and ESRS report **unrated/uncovered documents** to expose gaps in ground truth — Quepid surfaces this less directly.

## Experiment / Optimization Capabilities

| Capability | Quepid | SRW | ESRS | RRE | Releval |
|---|---|---|---|---|---|
| Per-query inspection | ✅ Strong, interactive | ✅ Query Scores view | ✅ Real-time (Ctrl+Enter) | ✅ Per-query metrics in reports / RRE Server | ✅ Query Lab |
| Config A/B comparison | ✅ Snapshots | ✅ Search result comparison | ✅ Strategy benchmarks | ✅ Version-over-version delta tracking (core design) | ✅ Repeatable runs; same evaluation re-pointed at another endpoint |
| Custom scorers | ✅ JavaScript scorers | ➖ Fixed metric set | ➖ Fixed metric set | ➖ Fixed (broad) set; extensible in Java | ➖ Fixed metric set |
| Hybrid-search auto-tuning | ➖ | ✅ Grid search over normalization/combination/weights | ➖ (manual strategies) | ➖ | ➖ |
| Scheduled / drift detection | ➖ (manual re-run) | ➖ | ✅ Scheduled benchmarks | ✅ Runs in CI on every build | ➖ (manual re-run; Slack notifications on completion) |
| Agentic automation (MCP) | ➖ | ➖ | ✅ MCP server | ➖ | ✅ MCP server |
| Native CI/CD form factor | ➖ (external) | ➖ (in-engine) | ➖ (external app) | ✅ Maven build library | ➖ (external; REST + gRPC APIs) |

## Metrics

- **Quepid** — [[NDCG]], [[MRR]], [[Precision and Recall|P@k]], plus arbitrary custom metrics via JavaScript scorers (see [[Implementing NDCG Scorer in Quepid]]). Metric variant is configurable, which matters given the [[Flavors of NDCG|many flavors of NDCG]].
- **SRW** — [[Precision and Recall|Precision@k]], [[MAP|MAP@k]], [[NDCG|NDCG@k]], plus Judgment Coverage.
- **ESRS** — [[NDCG]], [[Precision and Recall|Precision@k / Recall@k]], [[MRR]], plus unrated-document reporting.
- **RRE** — the broadest fixed set out of the box: [[Precision and Recall|Precision/Recall]], P@1/2/3/10, [[MAP|Average Precision]], [[MRR|Reciprocal Rank]] + Expected Reciprocal Rank, [[NDCG|NDCG@10]], and F-measure (F0.5/F1/F2).
- **[[Releval]]** — [[NDCG]], [[MAP]], [[MRR]], Expected Reciprocal Rank, [[Precision and Recall|Precision and Recall]], over binary, graded or detailed judgment scales.

Only Quepid lets you write an arbitrary scorer in its UI; SRW, ESRS, RRE and Releval ship fixed metric sets (RRE's is the broadest, and extensible in Java).

## How to Choose

- **Engine-agnostic or multi-engine shop, mature team workflow, non-technical raters** → **[[Quepid]]**. It is the most battle-tested, works across engines (including hacks for [[Vector Search Evaluation|vector/image search]]), and its JavaScript scorers handle bespoke business metrics. It's also the right choice when you want judgments decoupled from the engine.
- **All-in on [[OpenSearch]], want click-data-driven judgments and hybrid-search tuning with zero external infra** → **[[Search Relevance Workbench]]**. The [[User Behavior Insights|UBI]] integration and hybrid-optimization grid search are unique, and everything lives in Dashboards. You can seed it by importing existing Quepid judgments.
- **All-in on [[Elasticsearch]], building [[Agentic Search|agentic]] pipelines, want AI agents to run the relevance loop** → **[[Elasticsearch Relevance Studio]]** — but note it's an experimental demonstrator, not a supported product, so weigh that for production use.
- **JVM / Solr / Elasticsearch stack, want relevance regression tests running automatically in CI on every build, no UI required** → **[[Rated Ranking Evaluator]]**. It's a library first: immutable version-over-version deltas turn "did this change help or hurt?" into an automated build check. [[Sease]] offers **RRE Enterprise** if you later want a UI on top.
- **Engine-agnostic *and* want clickstream-derived judgments without moving to [[OpenSearch]], or want an agent driving the loop over a non-Elastic stack** → **[[Releval]]**. It is the only tool here that combines engine-neutrality with native [[User Behavior Insights|UBI]] capture, and one of two with an MCP server. Against it: proprietary and EULA-gated where every other option is open source, released in July 2026 with no independent track record, and no custom scorers.

## The Bigger Picture

Both Elastic and OpenSearch are absorbing the offline-evaluation loop that Quepid pioneered *into the search engine itself*. The direction of travel is (1) **engine-native** evaluation (no external tool to stand up), (2) **behavior-driven** judgments from real clickstream data, and (3) **automated** judging via LLMs and agents. Quepid remains the most flexible and engine-neutral option; the native tools trade flexibility for tight integration and new data sources. [[Rated Ranking Evaluator]] took the opposite tack years earlier — pushing evaluation into the **CI pipeline** as a build library rather than into the engine — and remains the reference choice when relevance regression testing must be automated. Notably, [[OpenSource Connections]] — Quepid's authors — also drove SRW, so this is less a rivalry than the same community pushing the practice into the engines.
[[Releval]] is a third bet, and the one that cuts against the engine-native trend: stay outside the engine like Quepid, but absorb the *data sources* the native tools were winning on — clickstream capture, LLM judging, an agent interface — into one external platform. Whether that is worth giving up open source is the question a team evaluating it has to answer. Its adoption of [[User Behavior Insights|UBI]] outside the OpenSearch ecosystem is the more consequential detail: the spec was written to keep behavioral data portable across vendors, and this is evidence it is being used that way.

## Related Concepts

- [[Search Evaluation]] — the practice all five implement
- [[Judgment Lists]] — the shared input data
- [[Implicit Judgments]] — the click-derived judgments SRW and Releval specialize in
- [[LLM as Judge]] — automated judging (Quepid, SRW, ESRS, Releval; not RRE)
- [[NDCG]] · [[MRR]] · [[MAP]] · [[Precision and Recall]] — the shared metric vocabulary
- [[Hybrid Search]] — the target of SRW's auto-tuning experiment
- [[Agentic Search]] — the MCP differentiator, now in both ESRS and Releval

## Related Topics

- [[Relevance Program Setup]] — how these tools fit an org's relevance program
- [[Search Quality Assurance]] — the broader QA practice they serve
- [[Retrieval Benchmarks and Leaderboards]] — the public-benchmark counterpart: `mteb`, `beir`, `pytrec_eval`, `ranx` and friends run academic suites, where the four tools here run *your* queries against *your* corpus
- [[Model Selection and Fine-Tuning Evaluation]] — the methodology these tools operationalize

## Related Tools

- [[Quepid]] · [[Search Relevance Workbench]] · [[Elasticsearch Relevance Studio]] · [[Rated Ranking Evaluator]] · [[Releval]] — the five tools compared here
- [[User Behavior Insights]] — the clickstream standard SRW and Releval both build on

## People

- [[Doug Turnbull]] — Quepid co-creator
- [[Daniel Wrigley]] — [[OpenSource Connections]]; introduced SRW and its judgments workflow, and authored the Quepid judgement-lists guide
