---
type: article
title: "Introducing OpenSearch Relevance Agent: AI-powered search tuning"
source: "https://opensearch.org/blog/introducing-opensearch-relevance-agent-ai-powered-search-tuning/"
author: ["Bobby Mohammed", "Daniel Wrigley"]
published: 2026-08-25
tags:
  - clippings
  - opensearch
  - relevance-tuning
  - agentic-search
  - evaluation
concepts:
  - Agentic Search
  - Search Evaluation
  - Model Context Protocol
tools:
  - OpenSearch
  - User Behavior Insights
  - Search Relevance Workbench
  - OpenSearch Relevance Agent
people:
  - Bobby Mohammed
  - Daniel Wrigley
created: 2026-09-07
---

# Introducing OpenSearch Relevance Agent: AI-powered search tuning

**Source**: https://opensearch.org/blog/introducing-opensearch-relevance-agent-ai-powered-search-tuning/
**Published**: 25 August 2026 · **Authors**: [[Bobby Mohammed]], [[Daniel Wrigley]]

## Summary

The [[OpenSearch]] project's announcement of the [[OpenSearch Relevance Agent]] — a multi-agent system that does relevance diagnosis and tuning through natural-language conversation in OpenSearch Dashboards. It targets three stated problems: decoding ambiguous user queries, handling incomplete or noisy metadata, and carrying a fix from a test environment into production.

The headline claim is that it *"reduces relevance diagnosis from days to hours — no deep search expertise required"*, with human oversight retained throughout.

## The Three Agents

An orchestrator coordinates three specialists:

| Agent | Role |
|---|---|
| **User Behavior Analysis** | Identifies relevance gaps by analyzing [[User Behavior Insights|UBI]] data when available, or query patterns when it isn't |
| **Hypothesis Generator** | Interprets those results into data-driven tuning strategies |
| **Evaluator** | Validates the strategies by running automated tests against offline evaluation sets |

UBI improves the analysis but is explicitly *not* a prerequisite — the announcement states UBI "is not required to begin transforming your relevance workflow."

## Architecture

- Built on the **Strands SDK**, integrating into an existing OpenSearch deployment.
- Uses the **AG-UI** standard for the OpenSearch Dashboards chat surface.
- All agents reach the engine **exclusively** through the [[Model Context Protocol|OpenSearch MCP server]], described as *"a secure translator between the AI and your search engine"*.

One design decision is worth isolating: metric computation is **offloaded from the LLM to deterministic tools**, specifically to stop the model estimating numbers it should be measuring. The announcement refers to "standard relevance metrics" and to quantifying impact within [[Search Relevance Workbench]], but names no specific metric.

## Usage

Entry point is an **"Ask AI"** button in OpenSearch Dashboards. The single worked example is the prompt *"What are 'underperforming' queries of the past two years?"*, after which the agent analyzes the sample UBI data indexed by a quickstart script and returns a summary of findings.

## Status and Scope

Shipped in **OpenSearch 3.6** as an **experimental release**, within the OpenSearch Agent Server.

Supported today: **query-DSL-level optimizations** — refining search fields, adjusting weights, tuning boost functions.

On the roadmap: online [[Interleaving|interleaving]] tests in production, schema evolution recommendations, vector and [[Hybrid Search|hybrid search]] parameter optimization, automated [[Learning to Rank|LTR]] model training, and multi-platform data source connectivity via MCP.

Repositories: `opensearch-agent-server`, `opensearch-mcp-server-py`, `ag-ui-protocol`.

## Related Concepts

- [[Agentic Search]] — agents operating the search stack rather than querying it
- [[Search Evaluation]] · [[Interleaving]] — the validation half of the loop
- [[Model Context Protocol]] — the abstraction every agent here talks through
- [[Learning to Rank]] — roadmap item

## Related Tools

- [[OpenSearch]] · [[OpenSearch Relevance Agent]] · [[User Behavior Insights]] · [[Search Relevance Workbench]]

## Related People

- [[Bobby Mohammed]] · [[Daniel Wrigley]]
