---
type: article
title: "AI agent memory: Creating smart agents with Elasticsearch managed memory"
source: "https://www.elastic.co/search-labs/blog/ai-agent-memory-management-elasticsearch"
author: ["Gustavo Llermaly", "Jeffrey Rengifo"]
published: 2026-03-18
tags:
  - clippings
  - agentic-memory
  - elasticsearch
  - personalization
  - security
concepts:
  - Agentic Memory
  - ELSER
  - Hybrid Search
  - Reciprocal Rank Fusion
  - RAG
tools:
  - Elasticsearch
people:
  - Gustavo Llermaly
  - Jeffrey Rengifo
created: 2026-09-07
---

# AI agent memory: Creating smart agents with Elasticsearch managed memory

**Source**: https://www.elastic.co/search-labs/blog/ai-agent-memory-management-elasticsearch
**Published**: 18 March 2026 · **Authors**: [[Gustavo Llermaly]], [[Jeffrey Rengifo]] ([[Elastic]] Search Labs)

## Summary

A working implementation of [[Agentic Memory]] on [[Elasticsearch]], organised around a three-way memory taxonomy and — the part that distinguishes it — using **document-level security as the memory isolation mechanism** rather than application-level filtering.

## The Three Memory Types

| Type | What it holds | Where it lives |
|---|---|---|
| **Procedural** | How the agent *behaves* — when to store a memory, when to retrieve one, how to summarize, how to use tools | Application code and prompts; **not** stored in Elasticsearch |
| **Episodic** | Specific experiences tied to an entity and a context — *"Peter's birthday is tomorrow and he wants steak"* | Documents in Elasticsearch, with user, role, timestamp and context metadata |
| **Semantic** | Abstracted, generalized world knowledge independent of any single interaction — a company handbook | Retrieved through the same system, with a different retrieval strategy |

The article singles out episodic memory as *"the most dynamic and personal"* and the one *"most prone to context pollution if handled incorrectly"* — which is what motivates the isolation work below.

## Memory Isolation via Document-Level Security

The demo is framed on the TV show *Severance*: one agent, "Mark", whose work-self ("innie") and personal-self ("outie") memories must never mix.

Rather than filtering in the agent, each user's credentials carry a role whose descriptor pins a filter onto the `memory_type` field:

```json
"query": {"bool": {"filter": [{"term": {"memory_type": "innie"}}]}}
```

The outie role is identical but for `"memory_type": "outie"`. Elasticsearch then enforces the separation itself — the agent issues the same query regardless, and the engine returns only what those credentials permit. Cross-context access requires a separate user or an additional role, which the article leaves as an exercise.

## Index and Retrieval

Memory documents carry:

- `user_id` — keyword
- `memory_type` — keyword (the security discriminator)
- `created_at` — date
- `memory_text` — text, with a multi-field semantic subfield

The multi-field setup indexes the same content twice, for full-text search and for semantic search via [[ELSER]]. Retrieval is [[Hybrid Search|hybrid]], combining the two with [[Reciprocal Rank Fusion|RRF]] at `rank_window_size: 50` and `rank_constant: 20`.

## Agent Tools

Three functions are exposed to the model, which chooses among them via OpenAI's Response API function calling:

- **`GetKnowledge`** — conventional [[RAG]]-style context search
- **`GetMemories`** — hybrid semantic + keyword retrieval over memories, using the RRF retriever above
- **`SetMemory`** — writes a new memory after the LLM converts the exchange into a structured record

Results are injected into the conversation context before the final response is generated.

## Caveats

Memory compression is named as an open problem and left unimplemented. Selective filtering is credited with reducing context pollution and yielding lower latency and token usage; no scale, latency or dimensionality figures are given.

## Related Concepts

- [[Agentic Memory for Search Personalization]] — the search-personalization application of this pattern
- [[Agentic Memory]] — the pattern implemented here; contrast its memory taxonomy with OpenSearch's four-type split
- [[ELSER]] · [[Hybrid Search]] · [[Reciprocal Rank Fusion]] — the retrieval stack
- [[RAG]] — what `GetKnowledge` does, and what memory is positioned against
- [[Multi-Tenancy in Search]] — document-level security as the isolation primitive

## Related Tools

- [[Elasticsearch]]

## Related People

- [[Gustavo Llermaly]] · [[Jeffrey Rengifo]]
