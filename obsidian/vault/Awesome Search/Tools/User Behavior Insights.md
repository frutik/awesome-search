---
title: User Behavior Insights
type: tool
aliases: ["UBI", "User Behavior Insights (UBI)", "OpenSearch UBI"]
tags:
  - tool
  - specification
  - search-evaluation
  - behavioral-signals
  - opensearch
website: https://o19s.github.io/ubi/
docs: https://docs.opensearch.org/latest/search-plugins/ubi/index/
repo: https://github.com/opensearch-project/user-behavior-insights
created: 2026-07-30
---

# User Behavior Insights

**User Behavior Insights (UBI)** is an open-source **data standard** — plus a set of search-engine plugins and client collectors — for capturing search queries and the user actions that follow them, in a form that can be joined back together. Its purpose is to let search teams answer "what did the user type, what did we show, and what did they do about it?" without a proprietary analytics stack. Licensed Apache 2.0.

- Specification: https://o19s.github.io/ubi/
- Community site: https://www.ubisearch.dev
- Spec repo: https://github.com/o19s/ubi
- OpenSearch plugin: https://github.com/opensearch-project/user-behavior-insights
- OpenSearch docs: https://docs.opensearch.org/latest/search-plugins/ubi/index/

---

## Why It Exists

Search teams routinely struggle to correlate incoming queries with outcomes. General-purpose analytics (Google Analytics, Snowplow) tracks page events but is not built around the query→results→action chain, and each vendor models it differently. UBI proposes a search-specific, portable event format that works across engines and avoids vendor lock-in — so the same clickstream can feed evaluation, [[Learning to Rank]] training, and [[A-B Testing for Search]] regardless of which engine produced the results.

## The Specification

UBI is defined as JSON Schema (2020-12 draft), in three parts:

| Schema | Captures |
|---|---|
| `query.request.schema.json` | the user's search request |
| `query.response.schema.json` | the result set that was returned |
| `event.schema.json` | what the user did afterwards (clicks, conversions, filters) |

The load-bearing identifiers are:

- **`query_id`** — the join key that ties every downstream event back to the exact query and result set that produced it.
- **`client_id`** — identifies the user/client across queries.
- **`event_attributes`** — the per-event payload. It carries the item's identity nested under `object` (`event_attributes.object.object_id`) *and* the result `position` — both required — so an event records which document was acted on as well as where it sat in the result set, alongside free-form contextual detail.

## OpenSearch Implementation

The reference implementation is the OpenSearch **`user-behavior-insights` plugin**, first released for **OpenSearch 2.15** and maintained alongside subsequent versions (recent builds target UBI specification **1.3.0**). It persists both sides of the interaction into two indexes:

- **`ubi_queries`** — `query_id`, `query_response_id`, `user_query`, `query_response_object_ids`, `client_id`, the raw `query` JSON, `timestamp`
- **`ubi_events`** — `action_name`, `user_id`, `query_id`, `session_id`, `page_id`, `timestamp`, `event_attributes`

A query is captured by adding a `ubi` section to the request's `ext` block (optionally carrying `query_id`, `user_query`, `client_id`, `object_id_field`, `query_attributes`). **If no `query_id` is supplied, the plugin generates a UUID and returns it in the response's `ext.ubi`** — that value is what the client then attaches to subsequent events.

`action_name` is open-ended; documented examples include `on_search`, `button_click`, `product_hover`, `product_sort`, `brand_filter`, `type_filter`, `login`, `logout`, `new_user_entry`.

Note the split of responsibility: the plugin persists events but does **not** capture them. Client-side collection is a separate component — the `ubi-javascript-collector`.

## Implementations Beyond OpenSearch

The standard is deliberately engine-neutral, with plugins/integrations for **[[OpenSearch]]**, **[[Solr]]**, and **[[Elasticsearch]]**, plus **Chorus** (the reference e-commerce search stack) shipping a UBI-enabled edition.

## What Consumes UBI Data

- **[[Search Relevance Workbench]]** — the flagship consumer: builds [[Implicit Judgments]] from UBI clickstream (COEC debiasing) and samples query sets from UBI query logs
- **[[Learning to Rank]]** — behavioral training data
- Offline evaluation platforms — see [[Search Evaluation]]
- Online comparison, including Team Draft [[Interleaving]]

## Governance

UBI is sponsored and led by **Eric Pugh** ([[OpenSource Connections]]), **Jeff Zemerick** (Mountain Fog), **Stavros Macrakis** (Amazon OpenSearch), and **[[Charlie Hull]]** ([[The Search Juggler]]). The project documents an intent to establish a more robust governance structure than its current individual/small-group administration.

## Related Concepts

- [[Implicit Judgments]] — what UBI clickstream is turned into
- [[Click Signals]] · [[Click Models]] — the behavioral data UBI standardizes
- [[Position Bias]] · [[Presentation Bias]] — why raw UBI clicks need debiasing
- [[Search Observability]] — the broader practice of instrumenting a search stack
- [[Query Sampling]] — UBI query logs as the sampling frame
- [[Session-Based Evaluation]] — `session_id` / `page_id` make session-level analysis possible

## Related Tools

- [[Search Relevance Workbench]] · [[OpenSearch]] · [[Quepid]] · [[Solr]] · [[Elasticsearch]]
