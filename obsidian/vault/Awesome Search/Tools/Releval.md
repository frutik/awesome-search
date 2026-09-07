---
title: Releval
type: tool
aliases: ["Releval platform"]
tags:
  - tool
  - search-evaluation
  - relevance-testing
  - llm-judge
  - behavioral-signals
  - proprietary
website: https://releval.co/
docs: https://releval.co/docs/
created: 2026-09-07
---

# Releval

**Releval** is a self-hosted search relevance evaluation platform: connect a search system, run a fixed query set against it, grade the results by hand or with an LLM, and track [[NDCG]], [[MAP]], [[MRR]], ERR and [[Precision and Recall|precision/recall]] across configuration changes. It occupies the same ground as [[Quepid]], [[Rated Ranking Evaluator]], [[Search Relevance Workbench]] and [[Elasticsearch Relevance Studio]] — see [[Relevance Evaluation Tools Compared]].

- Website: https://releval.co/
- Documentation: https://releval.co/docs/

Two things separate it from the four tools already covered. It is the only one that is **engine-agnostic and carries native clickstream capture** — [[User Behavior Insights|UBI]] telemetry is built in rather than inherited from the host engine, so implicit judgments are available without committing to [[OpenSearch]]. And it is the only **closed-source** entry in that comparison.

## Licensing and Deployment

Releval is **proprietary**. There is no public source repository; the software ships as a Docker image (`releval/releval`) and the container refuses to start without `ACCEPT_EULA=Y`. Every other tool in [[Relevance Evaluation Tools Compared]] is open source, so this is the first thing to know when weighing it against them.

Deployment is self-hosted via Docker Compose. PostgreSQL is required. ClickHouse is optional and powers [[User Behavior Insights|UBI]] — omit it and the tracking APIs return 404 while the rest of the product is unaffected.

It is also **new**. First release 1.0.0 on 12 July 2026, followed by 1.0.1 and then 1.1.0 on 7 September 2026, which added Slack notifications for runs, security hardening across the REST and MCP surfaces, and a published browser tracker for UBI. Treat maturity claims accordingly; there is no independent evaluation of it yet.

## The Evaluation Loop

An **Evaluation** binds three objects, each reusable independently:

| Object | What it fixes |
|---|---|
| **Search Endpoint** | which system is queried |
| **Query Set** | which queries are run |
| **Query Template** | how a query becomes a request |

An evaluation is then executed as repeatable **runs**, each pinned to a relevance scale and metric set, so the same queries can be re-scored as the endpoint changes.

Separating the endpoint from the queries is what makes production-versus-staging comparison, engine-version A/B tests, and ranking-model swaps a matter of pointing the same evaluation somewhere else — the same design decision [[Rated Ranking Evaluator]] makes with its versioned configurations.

### Endpoints

An endpoint carries a URL, HTTP method, type ([[Elasticsearch]], [[OpenSearch]], or a generic REST API), authentication (Bearer, Basic, AWS SigV4), a TLS-validation toggle, and a **candidates mapping** that transforms the engine's response shape into the structure Releval scores. The documentation states support for Elasticsearch, OpenSearch, [[Solr]], [[Vespa]], any HTTP-based search API, and rendered search results pages. Request bodies are supported on `GET` where the endpoint allows it, so evaluation credentials can be scoped to read-only privileges.

### Query Sets

A query is either a plain string or a JSON object with a `query` property plus arbitrary additional fields (filters, facets, context) — but a set must be uniformly one or the other. The JSON form is what lets a query set carry the filter state a real session would have, rather than bare keywords.

## Judgments

**Judgment Lists** are uploaded rather than collected in-app, in the **TREC qrels shape** (`qid`, `iteration`, `candidate_id`, `grade`) as JSON Lines, CSV/TSV or Parquet. Grades attach to results by matching `candidate_id` against what the endpoint returned, and queries by hashing the query text or object. Three scales are offered — binary, graded, detailed. Documented sources include click logs, previous campaigns, crowdsourced assessments and expert annotation. See [[Judgment Lists]].

**AI Judges** implement the [[LLM as Judge]] pattern as saved configurations — an AI provider (OpenAI, Anthropic, Bedrock among them), a model, and a prompt template — applied to every unjudged query/candidate pair on a completed run, producing a grade and optionally its reasoning. Metrics recompute when the judging run finishes.

The documentation is unusually careful about what this is for: AI judging is positioned for query sets too large to grade exhaustively, for fast iteration, as a consistent re-runnable baseline rater, and for seeding a list that humans then refine — with the explicit caveat that it "is not a replacement for thoughtful human judging on smaller, high-value query sets." That is the correct framing of the technique, and worth noting because vendor material on LLM judges often is not.

## User Behavior Insights

Releval implements [[User Behavior Insights|UBI]], the open search-telemetry standard, capturing client-side events and server-side queries into ClickHouse. It links a user's query causally to everything they do until their next search — the join that makes click models and implicit judgment lists possible. APIs are exposed over both REST and gRPC, with gRPC recommended for high-volume ingestion, and 1.1.0 shipped a browser tracker.

This makes Releval a **third-party implementation of the UBI specification outside the OpenSearch ecosystem** — a concrete instance of the portability the spec was written for, given that UBI exists precisely to keep clickstream data from being locked to one vendor's analytics.

## Interfaces

REST and gRPC APIs, authenticated app clients for programmatic access, and an **MCP server** — putting it alongside [[Elasticsearch Relevance Studio]] as one of the two tools in the comparison exposing an agent-facing interface over its evaluation data.

## Caveats

- **Closed source.** No repository to read, fork, or audit; internals are known only from the documentation.
- **Pricing not verified here.** Tier structure is presented on pages that require JavaScript, and the documentation's own "License tiers" link 404s. The vendor states an individual tier is free with all features; that has not been independently checked.
- **No third-party coverage.** No independent write-ups, benchmarks or deployment reports were found.

## Related Tools

- [[Quepid]] — the engine-agnostic incumbent; open source, no native clickstream
- [[Rated Ranking Evaluator]] — CI/CD-first library rather than a platform
- [[Search Relevance Workbench]] — the other tool with native UBI-derived implicit judgments, but OpenSearch-only
- [[Elasticsearch Relevance Studio]] — the other tool with an MCP server, Elasticsearch-only
- [[User Behavior Insights]] — the telemetry standard Releval implements

## Related Concepts

- [[Search Evaluation]] — the practice it operationalizes
- [[Judgment Lists]] — its ground truth, uploaded in qrels form
- [[LLM as Judge]] — the AI Judges feature
- [[Implicit Judgments]] — what UBI capture is for
- [[NDCG]] · [[MAP]] · [[MRR]] · [[Precision and Recall]] — the metrics it reports

## Comparison

- [[Relevance Evaluation Tools Compared]] — Releval against Quepid, SRW, Relevance Studio and RRE
