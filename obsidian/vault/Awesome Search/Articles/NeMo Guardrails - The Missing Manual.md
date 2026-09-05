---
type: article
title: "NeMo Guardrails: The Missing Manual"
source: "https://www.pinecone.io/learn/nemo-guardrails-intro/"
author: ["James Briggs"]
published: 2023-08-11
tags:
  - clippings
  - llm
  - safety
  - rag
  - company-blog
concepts:
  - LLM Guardrails
  - Query Routing
  - RAG
created: 2026-09-05
---

# NeMo Guardrails: The Missing Manual

**Source**: https://www.pinecone.io/learn/nemo-guardrails-intro/
**Publisher**: Pinecone · **Published**: 11 August 2023 · **Author**: [[James Briggs]]

## Summary

A working introduction to NVIDIA's NeMo Guardrails. Its definition is the one worth carrying: a guardrail is **"a semi or fully deterministic shield"** around a conversational model.

## What Guardrails Are Applied To

1. **Safety and topic guidance** — filtering malicious inputs, limiting conversation to relevant subjects
2. **Deterministic dialogue** — predictable response flows for common queries
3. **RAG** — using semantic similarity to decide *when* external retrieval is needed
4. **Conversational agents** — deciding when to invoke external tools or APIs

Items 3 and 4 make this a retrieval-architecture topic, not only a safety one — see [[Query Routing]].

## Colang

Colang is the purpose-built dialogue modelling language, with three building blocks: **user message blocks**, **bot message blocks**, and **flow blocks**. User utterances are encoded into semantic vector space (MiniLM by default) and matched against predefined patterns — so routing is mostly embedding similarity, not LLM inference.

Supporting concepts: **canonical forms** (structured message representations), **utterances** (example phrases), **variables** (`$name`), and **actions** (Python functions registered via `register_action()`).

## Related Concepts

- [[LLM Guardrails]] — primary topic
- [[Query Routing]] · [[RAG]] · [[Conversational Search]] · [[Semantic Search]]

## Related People

- [[James Briggs]]
