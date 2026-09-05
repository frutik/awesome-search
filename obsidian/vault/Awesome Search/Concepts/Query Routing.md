---
type: concept
title: "Query Routing"
aliases: ["routing", "query router", "semantic router", "RAG routing", "router"]
tags:
  - concept
  - rag
  - query-understanding
  - architecture
related_concepts:
  - "[[RAG]]"
  - "[[Query Understanding]]"
  - "[[Query Classification]]"
created: 2026-09-05
---

# Query Routing

## Definition

Directing a query to one of several downstream paths based on its intent. [[Sami Maameri]]'s framing is deliberately unglamorous: **"routers are essentially just If/Else statements we can use to direct the control flow."**

Routing decides *which* index, tool, prompt or engine handles a query — as distinct from [[Query Classification]], which assigns a query to a taxonomy label. Classification is a labelling task; routing is a control-flow decision that may or may not use a classifier to make it.

## Why It Matters

Not every query should hit the vector index. Some are better served by structured filters, some by a keyword engine, some by a tool call, some by no retrieval at all. A single fixed pipeline forces one answer for every query; a router lets a system be several pipelines wearing a trenchcoat. It is the mechanism behind the "should we retrieve?" decision in [[LLM Guardrails]] and the per-query strategy choice in [[Agentic Search]].

## Router Types

| Type | How it decides | Cost |
|---|---|---|
| **LLM completion router** | Model outputs one of a set of words | LLM call |
| **LLM function-calling router** | Model picks a route via function calling | LLM call |
| **Semantic router** | Embedding similarity against example utterances | Embedding only — cheap |
| **Zero-shot classification router** | Zero-shot model assigns a label from a set | Model inference |
| **Language classification router** | Detects query language, routes accordingly | Cheap (`langdetect`) |
| **Keyword router** | Matches keywords against route lists | Trivial |
| **Logical router** | Discrete checks — string length, file type, value comparisons | Trivial |

The list is ordered roughly by cost, and the practical lesson is that the cheap end is underused: language detection and logical checks resolve a large share of routing decisions without any model call.

## Implementations

- [[LlamaIndex]] — LLM Selector router, Pydantic Router
- [[Haystack (deepset)]] — `ZeroShotTextRouter`, `TextClassificationRouter`, `ConditionalRouter`, `FileTypeRouter`
- [[LangChain]]
- `semantic-router` (standalone Python package), OpenAI Encoder, Hugging Face models, `langdetect`

## Related Concepts

- [[RAG]] · [[Query Understanding]] · [[Query Classification]] · [[Search Intent]]
- [[Agentic Search]] — routing chosen per step rather than once
- [[LLM Guardrails]] · [[Federated Search]] · [[Search Scopes]]

## Articles

- [[Routing in RAG Driven Applications]] — [[Sami Maameri]]; the seven-router taxonomy
