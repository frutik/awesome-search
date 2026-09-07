---
type: concept
title: "Model Context Protocol"
aliases: ["MCP", "MCP server", "Model Context Protocol (MCP)"]
tags:
  - concept
  - agentic-search
  - infrastructure
  - protocol
created: 2026-09-07
---

# Model Context Protocol

## Definition

**Model Context Protocol (MCP)** is an open protocol that standardises how an LLM-based agent connects to external systems — data sources, tools, and services — so that a capability is exposed once and consumed by any compliant client, rather than reimplemented per agent.

In a search context it matters because it fixes the boundary between the agent and the engine: the agent does not hold engine credentials or construct privileged calls directly, it asks an MCP server which exposes a defined surface.

## Why It Shows Up in Search Systems

Search stacks are an awkward fit for direct LLM access. The engine speaks a query DSL, holds production data, and is operationally sensitive — three reasons not to hand a model a raw connection. An MCP server in front of it gives:

- **A stable surface.** Tools are declared with typed inputs, so the agent's access is enumerable rather than open-ended.
- **A security boundary.** The [[OpenSearch Relevance Agent]] routes *every* agent call through the OpenSearch MCP server, described there as a secure translator between the AI and the search engine.
- **Reuse across clients.** The same server serves whatever agent or IDE speaks the protocol.

## In This Vault

- **[[OpenSearch Relevance Agent]]** — all three of its agents communicate with the engine exclusively over the OpenSearch MCP server (`opensearch-mcp-server-py`); multi-platform data source connectivity over MCP is on its roadmap.
- **[[Elasticsearch Relevance Studio]]** — also exposes its capabilities over MCP.

## Related Concepts

- [[Agentic Search]] — the pattern MCP is plumbing for
- [[Agentic Memory]] — the other half of what an agent needs beyond tool access
- [[Search Observability]] — what an enumerable tool surface makes measurable

## Related Tools

- [[OpenSearch Relevance Agent]] · [[Elasticsearch Relevance Studio]] · [[OpenSearch]]

## Articles

- [[Introducing OpenSearch Relevance Agent]] — MCP as the mandatory abstraction between agents and engine
