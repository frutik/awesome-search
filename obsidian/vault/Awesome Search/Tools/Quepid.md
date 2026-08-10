---
title: Quepid
type: tool
tags:
  - tool
  - search-evaluation
  - relevance-testing
website: http://quepid.com/
repo: https://github.com/o19s/quepid
created: 2026-05-17
---

# Quepid

Open-source, web-based search relevance evaluation platform. Lets teams manage [[Judgment Lists|judgment lists]], run queries against a live search engine, and compute ranking metrics (NDCG, MRR, P@K) interactively. Built and maintained by [[OpenSource Connections]].

- Website: http://quepid.com/
- GitHub: https://github.com/o19s/quepid

---

## What It Does

Quepid is a "Test-Driven Relevancy" dashboard — the search equivalent of a unit test runner. You define test cases (query + expected relevant results), run them against your live search engine, and see metric scores per query and in aggregate.

Key workflows:
- **Judgment management** — create, import, and maintain relevance grades for query/document pairs
- **Metric scoring** — compute [[NDCG]], [[MRR]], [[Precision and Recall|P@K]] against your search engine in real time
- **Regression detection** — compare metric snapshots across index or config changes
- **Custom scorers** — write JavaScript scoring functions for non-standard metrics (e.g. custom NDCG@10)
- **Team collaboration** — shared cases and scores across the relevance team

## Scorer Architecture

Each Quepid test case runs a scorer — a JavaScript function with access to:
- `docs` — the result set returned by the search engine
- `bestDocs` — the ideal result set derived from judgments
- `setScore(value)` — outputs the final score for the query

This makes it straightforward to implement NDCG, DCG, or custom business metrics.

## When to Use Quepid vs. Scripts

| Quepid | Pandas / scripts |
|--------|-----------------|
| Interactive exploration | Large-scale batch evaluation (>100K results) |
| Team collaboration | CI/CD pipeline integration |
| Quick per-query inspection | Combining metrics with other signals |
| Non-technical stakeholder review | Custom analysis across many system variants |

## Related Tools
- **[[Search Relevance Workbench]]** — [[OpenSearch]]'s native, in-engine successor to this workflow (query sets / judgments / experiments); it can **import Quepid CSV judgments**, and adds [[User Behavior Insights|UBI]]-based implicit judgments and hybrid-search auto-tuning
- **[[Elasticsearch Relevance Studio]]** — Elastic's experimental, agentic in-house counterpart for [[Elasticsearch]]
- **[[Rated Ranking Evaluator]]** (RRE) — CI/CD-oriented counterpart from [[Sease]]; a JVM/Maven library for batch, in-build evaluation
- **SMUI / [[Querqy]]** — complementary tool for managing query rewriting rules

See [[Relevance Evaluation Tools Compared]] for a full Quepid vs. Workbench vs. Relevance Studio breakdown.

## Related Concepts
- [[Judgment Lists]] — the input data Quepid manages
- [[NDCG]] — primary metric computed in Quepid
- [[MRR]] — secondary metric
- [[Search Evaluation]] — the broader practice Quepid supports
- [[A-B Testing for Search]] — offline eval in Quepid complements online A/B tests

## Practical Use Cases

Because Quepid drives any search engine over **HTTP**, it isn't tied to Elasticsearch/Solr — there are known cases of using it for relevance tracking against **[[Vespa]]**, **[[Qdrant Vector DB|Qdrant]]**, and arbitrary **custom search APIs** (wired in as a custom endpoint); see [[Quepid Beyond Supported Engines]] for the full landscape of documented cases and what breaks in each. Beyond the canonical lexical/Elasticsearch workflow, practitioners push Quepid toward harder cases:

- **Collaborative team judging** — cases, teams, and books of judgements with explicit *information needs*; see [[Creating Judgement Lists with Quepid]].
- **AI-generated judgements** — as of v8, an LLM can generate judgements to scale annotation ([[LLM as Judge]]).
- **[[Vector Search Evaluation]]** — Quepid was built for text queries, so evaluating semantic/vector search needs workarounds: dimension reduction to fit the 2048-char query limit, injecting embeddings via query options (`#$qOption...##`) to dodge the JSON-validity catch-22, and generating whole case files via an [unofficial HTTP API wrapper](https://github.com/frutik/quepid-api-unofficial) (see [Community Tooling](#community-tooling)).
- **Image / cross-modal search** — registering a vector DB ([[Qdrant Vector DB]]) as a custom endpoint and hacking the scorer (or patching Quepid) to render image results in the rating UI.

## Community Tooling

- **[quepid-api-unofficial](https://github.com/frutik/quepid-api-unofficial)** ([[Andrew Kornilov]]) — an unofficial, **stateless** HTTP/REST API wrapper over a self-hosted Quepid (compatible with Quepid 7.18.1). Quepid's official API has no endpoint to add queries/cases programmatically one at a time; this wrapper closes that gap. It exposes Swagger/OpenAPI docs at `/api/docs`, reuses Quepid's own API tokens, talks to Quepid's MySQL backend, and ships Docker Compose + Kubernetes/Helm deployment (published as the `frutik777/quepid-api-unofficial` Docker Hub image). It's the machinery behind the case-file automation in [[Oops, I Did It Again]] and the [[Vector Search Evaluation]] / image-search series.

## Related Articles
- [[Implementing NDCG Scorer in Quepid]]
- [[What Is a Judgment List]]
- [[Compute MRR using Pandas]]
- [[Probability-Proportional-to-Size Sampling for Relevance Evaluation]]
- [[Flavors of NDCG]]
- [[Creating Judgement Lists with Quepid]] — collaborative team workflow
- [[Why Setting Up Quepid for Vector Search Evaluation Went Wrong]] — vector-search blockers
- [[Oops, I Did It Again]] — case-file workaround
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 1]]
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 2]]
- [[How to Securely Hook Up Quepid to Vespa]] — [[Charlie Hull]] wiring Quepid to [[Vespa]] Cloud as a custom endpoint (token auth)

## People
- [[Doug Turnbull]] — co-creator
- [[Andrew Kornilov]] — author of the unofficial API wrapper; vector/image-search evaluation hacks
