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

A side-by-side comparison of four tools that operationalize offline [[Search Evaluation]] — turning [[Judgment Lists|judgments]] into ranking metrics you can iterate against:

- **[[Quepid]]** — the incumbent, engine-agnostic external dashboard from [[OpenSource Connections]].
- **[[Search Relevance Workbench]]** (SRW) — [[OpenSearch]]'s native, in-engine workbench.
- **[[Elasticsearch Relevance Studio]]** (ESRS) — Elastic's experimental, agentic lifecycle tool for [[Elasticsearch]].
- **[[Rated Ranking Evaluator]]** (RRE) — [[Sease]]'s CI/CD-first evaluation *library* for Solr and Elasticsearch.

All four share the same core loop: define a **query set / scenarios**, attach **judgments**, define one or more **search configurations / strategies**, run an **experiment / benchmark**, and read **IR metrics** ([[NDCG]], [[Precision and Recall|P@k / R@k]], [[MRR]], [[MAP]]). The split that matters most: **Quepid** and **RRE** are external and engine-neutral (dashboard vs. build library), while **SRW** and **ESRS** are locked to one engine but gain tighter integration and new judgment sources.

---

## At a Glance

| Dimension | [[Quepid]] | [[Search Relevance Workbench]] | [[Elasticsearch Relevance Studio]] | [[Rated Ranking Evaluator]] |
|---|---|---|---|---|
| **Maker** | [[OpenSource Connections]] | [[OpenSearch]] project (OSC-influenced) | [[Elastic]] | [[Sease]] |
| **Maturity** | Mature, widely used in production | GA feature (OpenSearch 3.1+, 2025) | Experimental / demonstrator | Mature (since 2018); RRE Enterprise commercial layer |
| **Where it runs** | External web app (SaaS or self-host) | Inside OpenSearch + Dashboards | Standalone React+Flask app over ES | JVM/Maven **library** in your build (+ RRE Server dashboard) |
| **Engine coupling** | Engine-agnostic — any HTTP endpoint (ES, OpenSearch, Solr, and demonstrated with [[Vespa]], [[Qdrant Vector DB\|Qdrant]], custom APIs) | OpenSearch only | Elasticsearch only | Solr + Elasticsearch (pluggable search-platform API) |
| **Judgment store** | Quepid's own DB (MySQL) | OpenSearch judgments index | Elasticsearch index | JSON ratings files in the project repo |
| **License / cost** | Open source (o19s/quepid), free SaaS tier | Apache 2.0, bundled with OpenSearch | Open source demo (elastic/relevance-studio) | Apache 2.0 (RRE Enterprise commercial) |

## Judgment Sources

| Source | Quepid | SRW | ESRS | RRE |
|---|---|---|---|---|
| **Human (manual)** | ✅ Collaborative UI, books of judgements, information needs | ✅ CSV upload (~10k rows) | ✅ Drag-slider UI | ✅ Ratings authored as JSON files |
| **LLM-as-judge** | ✅ (v8+) | ✅ Native (model ID + query set) | ✅ Agent-generated, human-reviewed | ➖ Not native |
| **Implicit (clickstream)** | ➖ Not native | ✅ Via [[User Behavior Insights|UBI]] + COEC debiasing | ➖ Not native | ➖ Not native |
| **Import path** | — | ✅ Imports Quepid CSV | — | — |

SRW is the only one of the four that natively derives **implicit judgments** from user behavior ([[User Behavior Insights|UBI]] clickstream, debiased with Clicks-Over-Expected-Clicks). Both SRW and ESRS report **unrated/uncovered documents** to expose gaps in ground truth — Quepid surfaces this less directly.

> [!note] Quepid's engine-agnosticism is real, not just theoretical
> Because Quepid talks to a search engine over HTTP, practitioners have used it for relevance tracking well beyond ES/Solr/OpenSearch — including **[[Vespa]]**, **[[Qdrant Vector DB|Qdrant]]**, and arbitrary **custom search APIs** (registered as a custom endpoint). The vault's [[Vector Search Evaluation]] series ([[How to Evaluate Image Search in Qdrant Using Quepid Part 2]]) is a worked example of the Qdrant + custom-API case. This engine-neutrality is Quepid's main structural advantage over the two engine-locked native tools.

## Experiment / Optimization Capabilities

| Capability | Quepid | SRW | ESRS | RRE |
|---|---|---|---|---|
| Per-query inspection | ✅ Strong, interactive | ✅ Query Scores view | ✅ Real-time (Ctrl+Enter) | ✅ Per-query metrics in reports / RRE Server |
| Config A/B comparison | ✅ Snapshots | ✅ Search result comparison | ✅ Strategy benchmarks | ✅ Version-over-version delta tracking (core design) |
| Custom scorers | ✅ JavaScript scorers | ➖ Fixed metric set | ➖ Fixed metric set | ➖ Fixed (broad) set; extensible in Java |
| Hybrid-search auto-tuning | ➖ | ✅ Grid search over normalization/combination/weights | ➖ (manual strategies) | ➖ |
| Scheduled / drift detection | ➖ (manual re-run) | ➖ | ✅ Scheduled benchmarks | ✅ Runs in CI on every build |
| Agentic automation (MCP) | ➖ | ➖ | ✅ MCP server | ➖ |
| Native CI/CD form factor | ➖ (external) | ➖ (in-engine) | ➖ (external app) | ✅ Maven build library |

## Metrics

- **Quepid** — [[NDCG]], [[MRR]], [[Precision and Recall|P@k]], plus arbitrary custom metrics via JavaScript scorers (see [[Implementing NDCG Scorer in Quepid]]). Metric variant is configurable, which matters given the [[Flavors of NDCG|many flavors of NDCG]].
- **SRW** — [[Precision and Recall|Precision@k]], [[MAP|MAP@k]], [[NDCG|NDCG@k]], plus Judgment Coverage.
- **ESRS** — [[NDCG]], [[Precision and Recall|Precision@k / Recall@k]], [[MRR]], plus unrated-document reporting.
- **RRE** — the broadest fixed set out of the box: [[Precision and Recall|Precision/Recall]], P@1/2/3/10, [[MAP|Average Precision]], [[MRR|Reciprocal Rank]] + Expected Reciprocal Rank, [[NDCG|NDCG@10]], and F-measure (F0.5/F1/F2).

Only Quepid lets you write an arbitrary scorer in its UI; SRW, ESRS, and RRE ship fixed metric sets (RRE's is the broadest, and extensible in Java).

## How to Choose

- **Engine-agnostic or multi-engine shop, mature team workflow, non-technical raters** → **[[Quepid]]**. It is the most battle-tested, works across engines (including hacks for [[Vector Search Evaluation|vector/image search]]), and its JavaScript scorers handle bespoke business metrics. It's also the right choice when you want judgments decoupled from the engine.
- **All-in on [[OpenSearch]], want click-data-driven judgments and hybrid-search tuning with zero external infra** → **[[Search Relevance Workbench]]**. The [[User Behavior Insights|UBI]] integration and hybrid-optimization grid search are unique, and everything lives in Dashboards. You can seed it by importing existing Quepid judgments.
- **All-in on [[Elasticsearch]], building [[Agentic Search|agentic]] pipelines, want AI agents to run the relevance loop** → **[[Elasticsearch Relevance Studio]]** — but note it's an experimental demonstrator, not a supported product, so weigh that for production use.
- **JVM / Solr / Elasticsearch stack, want relevance regression tests running automatically in CI on every build, no UI required** → **[[Rated Ranking Evaluator]]**. It's a library first: immutable version-over-version deltas turn "did this change help or hurt?" into an automated build check. [[Sease]] offers **RRE Enterprise** if you later want a UI on top.

## The Bigger Picture

Both Elastic and OpenSearch are absorbing the offline-evaluation loop that Quepid pioneered *into the search engine itself*. The direction of travel is (1) **engine-native** evaluation (no external tool to stand up), (2) **behavior-driven** judgments from real clickstream data, and (3) **automated** judging via LLMs and agents. Quepid remains the most flexible and engine-neutral option; the native tools trade flexibility for tight integration and new data sources. [[Rated Ranking Evaluator]] took the opposite tack years earlier — pushing evaluation into the **CI pipeline** as a build library rather than into the engine — and remains the reference choice when relevance regression testing must be automated. Notably, [[OpenSource Connections]] — Quepid's authors — also drove SRW, so this is less a rivalry than the same community pushing the practice into the engines.

## Related Concepts

- [[Search Evaluation]] — the practice all four implement
- [[Judgment Lists]] — the shared input data
- [[Implicit Judgments]] — the click-derived judgments SRW specializes in
- [[LLM as Judge]] — automated judging (Quepid, SRW, ESRS; not RRE)
- [[NDCG]] · [[MRR]] · [[MAP]] · [[Precision and Recall]] — the shared metric vocabulary
- [[Hybrid Search]] — the target of SRW's auto-tuning experiment
- [[Agentic Search]] — ESRS's differentiator via MCP

## Related Topics

- [[Relevance Program Setup]] — how these tools fit an org's relevance program
- [[Search Quality Assurance]] — the broader QA practice they serve

## Related Tools

- [[Quepid]] · [[Search Relevance Workbench]] · [[Elasticsearch Relevance Studio]] · [[Rated Ranking Evaluator]] — the four tools compared here

## People

- [[Doug Turnbull]] — Quepid co-creator
- [[Daniel Wrigley]] — [[OpenSource Connections]]; introduced SRW and its judgments workflow, and authored the Quepid judgement-lists guide
