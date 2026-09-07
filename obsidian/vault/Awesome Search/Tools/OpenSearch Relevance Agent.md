---
title: OpenSearch Relevance Agent
type: tool
aliases: ["Relevance Agent"]
tags:
  - tool
  - opensearch
  - relevance-tuning
  - agentic-search
  - experimental
website: https://opensearch.org/blog/introducing-opensearch-relevance-agent-ai-powered-search-tuning/
repo: https://github.com/opensearch-project/opensearch-agent-server
created: 2026-09-07
---

# OpenSearch Relevance Agent

A multi-agent system inside [[OpenSearch]] Dashboards that diagnoses and tunes search relevance through natural-language conversation, shipped **experimentally in OpenSearch 3.6** as part of the OpenSearch Agent Server.

- Announcement: https://opensearch.org/blog/introducing-opensearch-relevance-agent-ai-powered-search-tuning/
- Agent Server: https://github.com/opensearch-project/opensearch-agent-server
- MCP server: https://github.com/opensearch-project/opensearch-mcp-server-py

---

## What It Does

Targets three stated obstacles to relevance work: ambiguous user queries, incomplete or noisy metadata, and moving a fix from a test environment to production. The pitch is that it *"reduces relevance diagnosis from days to hours — no deep search expertise required"*, with a human kept in the loop.

An orchestrator coordinates three specialised agents:

| Agent | Role |
|---|---|
| **User Behavior Analysis** | Finds relevance gaps from [[User Behavior Insights|UBI]] data where available, query patterns where not |
| **Hypothesis Generator** | Turns those findings into data-driven tuning strategies |
| **Evaluator** | Tests the strategies against offline evaluation sets |

UBI sharpens the analysis but is not required to start.

## Architecture

- **Strands SDK** — the agent framework it is built on, deployed into an existing OpenSearch environment.
- **AG-UI** — the standard behind the Dashboards chat surface.
- **[[Model Context Protocol]]** — every agent reaches the engine *exclusively* through the OpenSearch MCP server, characterised as a secure translator between the AI and the search engine.

The notable constraint: **metric computation is offloaded from the LLM to deterministic tools**, so numbers are measured rather than estimated by a model. The announcement cites "standard relevance metrics" and impact quantification via [[Search Relevance Workbench]] without naming specific measures.

## Scope in 3.6

Supported: query-DSL-level optimizations — refining search fields, adjusting weights, tuning boost functions.

Roadmap: online [[Interleaving|interleaving]] tests in production, schema evolution recommendations, vector and [[Hybrid Search|hybrid]] parameter optimization, automated [[Learning to Rank|LTR]] training, and multi-platform data sources over MCP.

## Related Tools

- [[OpenSearch]] — the engine it tunes
- [[User Behavior Insights]] — behavioural input to the analysis agent
- [[Search Relevance Workbench]] — where impact is quantified
- [[Quepid]] — the manual counterpart to this kind of relevance iteration

## Related Concepts

- [[Agentic Search]] · [[Search Evaluation]] · [[Interleaving]] · [[Learning to Rank]]

## Articles

- [[Introducing OpenSearch Relevance Agent]] — [[Bobby Mohammed]] and [[Daniel Wrigley]]'s announcement
