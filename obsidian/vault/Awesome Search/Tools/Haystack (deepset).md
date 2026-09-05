---
type: tool
title: "Haystack (deepset)"
aliases: ["Haystack framework", "deepset Haystack", "haystack-ai"]
website: https://haystack.deepset.ai/
repo: https://github.com/deepset-ai/haystack
tags:
  - tool
  - rag
  - llm
  - orchestration
  - open-source
related_concepts:
  - "[[RAG]]"
  - "[[Query Routing]]"
  - "[[Agentic Search]]"
  - "[[Hybrid Search]]"
created: 2026-09-05
---

# Haystack (deepset)

> [!note] Not the conference
> This is deepset's Python framework. The Haystack **conference** series is
> [[Haystack US]] and [[Haystack EU]] — unrelated beyond the shared name.

An open-source AI orchestration framework for building LLM applications in Python, maintained by deepset (`deepset-ai`), Apache-2.0. It describes itself as a framework for "context-engineered, production-ready LLM applications", built around modular pipelines and agent workflows with explicit control over retrieval, routing, memory, and generation.

🔗 https://haystack.deepset.ai/ · https://github.com/deepset-ai/haystack

## Core Abstractions

| Component | Role |
|---|---|
| Pipelines | Synchronous and asynchronous composition of components |
| Agents | Tool calling with lifecycle hooks |
| Retrievers | Retrieval and indexing components |
| Routers | Conditional control flow — see [[Query Routing]] |
| Evaluation utilities | Pipeline quality measurement |

The framework supports native async execution, token-by-token streaming, and integrations across multiple model vendors (OpenAI, Mistral, Anthropic, Cohere, Hugging Face).

## Why It Matters Here

Haystack's router components are one of the more explicit treatments of [[Query Routing]] in a mainstream framework — `ZeroShotTextRouter`, `TextClassificationRouter`, `ConditionalRouter` and `FileTypeRouter` make the routing decision a declarative pipeline node rather than application code.

## Related Tools

- [[LlamaIndex]] · [[LangChain]] — the other two general-purpose RAG orchestration frameworks
- [[RAGAS]] — evaluation, commonly paired with Haystack pipelines

## Related Concepts

- [[RAG]] · [[Query Routing]] · [[Agentic Search]] · [[Hybrid Search]]

## Articles

- [[Routing in RAG Driven Applications]] — covers Haystack's four router components
