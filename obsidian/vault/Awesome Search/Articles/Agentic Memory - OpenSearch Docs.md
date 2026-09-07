---
type: article
title: "Agentic Memory - OpenSearch Docs"
source: "https://docs.opensearch.org/latest/ml-commons-plugin/agentic-memory/"
author: "[[OpenSearch]]"
published:
created: 2026-09-07
concepts:
  - Agentic Memory
  - Personalization
  - Multi-Tenancy in Search
tools:
  - OpenSearch
tags:
  - article
  - documentation
  - agentic-memory
  - opensearch
  - ml-commons
---

# Agentic Memory - OpenSearch Docs

**Source**: https://docs.opensearch.org/latest/ml-commons-plugin/agentic-memory/
**Author**: [[OpenSearch]] project documentation · **Introduced 3.3**

## Summary

The canonical reference for [[Agentic Memory]] in OpenSearch's ml-commons plugin. It positions agentic memory against "simple conversation memory that only stores message history": persistent, structured storage that lets an agent learn preferences, retain context across sessions, and keep factual knowledge extracted from conversations. Explicitly designed for both OpenSearch's own agents and external frameworks — **LangChain and LangGraph** are named.

## Memory Containers

The organising unit. A **memory container** holds all memory types for one use case (a chatbot, a research assistant, a customer service agent) and is configured with:

- **Text embedding models** — for semantic search
- **LLMs** — for inference and knowledge extraction
- **Memory processing strategies** — how memories get processed or extracted
- **Namespaces** — partitioning by context, user, agent, or session

```
POST /_plugins/_ml/memory_containers/_create
```

## The Four Memory Types

| Type | Holds |
|---|---|
| `sessions` | Conversation sessions and their **metadata** — start time, participants, session state |
| `working` | Active conversation data — recent messages, current context, agent state, **execution traces**, temporary data |
| `long-term` | Processed knowledge and facts extracted from conversations over time; with inference on, the LLM promotes insights and preferences here **from working memory** |
| `history` | An audit trail of memory **operations** (add, update, delete) across the container |

Note the division of labour: recent messages live in `working`, not in `sessions` — `sessions` carries session metadata. And `history` logs how memories changed, not what the agent reasoned.

## Payload Types and Inference

Memories are added with a `payload_type`:

- `conversational` — messages between users and assistants
- `data` — structured, non-conversational content such as agent state, checkpoints, or reference information

```
POST /_plugins/_ml/memory_containers/{container_id}/memories
```

The `infer` parameter controls processing:

- `false` (**default**) — stores raw messages and data in `working` memory, no LLM involvement
- `true` — the configured LLM extracts key information and knowledge from the content

## Memory Processing Strategies

Optional; containers can be created without them for simple storage.

| Strategy | Behaviour |
|---|---|
| `SEMANTIC` | Groups related memories by meaning and content similarity |
| `USER_PREFERENCE` | Extracts and stores user preferences from conversations |
| `SUMMARY` | Creates condensed summaries of conversation content |

Each strategy declares the namespace it operates over, e.g. `USER_PREFERENCE` over `["user_id"]` and `SUMMARY` over `["user_id", "session_id"]`.

## Namespaces

Namespaces group memories by identifiers such as `user_id`, `session_id` or `agent_id`, separating one user's or one session's memories from another's. Searches filter on them directly:

```
GET /_plugins/_ml/memory_containers/{container_id}/memories/long-term/_search
{"query": {"bool": {"must": [{"term": {"namespace.user_id": "user123"}}]}}}
```

## Security Is the Operator's Responsibility

The page carries an unusually blunt notice: agentic memory is *a framework*, and the container owner is responsible for its configuration and security. Specifically called out —

- **Data access control** is the administrator's job: index-level permissions, document-level security (DLS), or other mechanisms. This is flagged as "especially critical" when `use_system_index` is set to `false`, because data then lands in a standard index requiring explicit permission management.
- **Custom system prompts** are the user's responsibility; OpenSearch disclaims outputs resulting from user-defined prompts.

Failure to configure this properly is said to risk unauthorized access, data leakage, or unintended agent behaviour. Namespaces partition memories, but they are not by themselves an access control mechanism.

## Related Concepts

- [[Agentic Memory for Search Personalization]] — applying these primitives to search personalization
- [[Agentic Memory]] — the concept this documents
- [[Multi-Tenancy in Search]] — namespaces partition, DLS enforces
- [[Personalization]] — the `USER_PREFERENCE` strategy's purpose

## Related Tools

- [[OpenSearch]]

## Related Notes

- [[Hajer Bouafif - Personalize Search Results with OpenSearch Agentic Memory]] — the applied version, in a search-personalization setting
- [[AI Agent Memory - Creating Smart Agents with Elasticsearch Managed Memory]] — the same problem on [[Elasticsearch]], with a different memory taxonomy
