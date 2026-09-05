---
type: article
title: "Routing in RAG Driven Applications"
source: "https://towardsdatascience.com/routing-in-rag-driven-applications-a685460a7220"
author: ["Sami Maameri"]
published: 2024-05-09
tags:
  - clippings
  - rag
  - query-understanding
  - architecture
concepts:
  - Query Routing
  - RAG
created: 2026-09-05
---

# Routing in RAG Driven Applications

**Source**: https://towardsdatascience.com/routing-in-rag-driven-applications-a685460a7220
**Published**: 9 May 2024 · **Author**: [[Sami Maameri]]

## Summary

A taxonomy of seven router types for RAG applications, framed deliberately plainly: **"Routers are essentially just If/Else statements we can use to direct the control flow."**

## The Seven Router Types

1. **LLM completion routers** — the model outputs one of a set of predefined words
2. **LLM function-calling routers** — route selection via function calling
3. **Semantic routers** — embeddings and similarity search against example utterances
4. **Zero-shot classification routers** — assign a label from a predefined set
5. **Language classification routers** — detect query language and route accordingly
6. **Keyword routers** — match keywords against route lists
7. **Logical routers** — discrete checks: string length, file names, value comparisons

## Implementations Named

[[LlamaIndex]] (LLM Selector router, Pydantic Router) · [[LangChain]] · `semantic-router` · [[Haystack (deepset)]] (`ZeroShotTextRouter`, `TextClassificationRouter`, `ConditionalRouter`, `FileTypeRouter`) · OpenAI Encoder · Hugging Face models · `langdetect`

## Related Concepts

- [[Query Routing]] — primary topic
- [[RAG]] · [[Query Understanding]] · [[Query Classification]] · [[Agentic Search]]

## Related Tools

- [[LlamaIndex]] · [[LangChain]] · [[Haystack (deepset)]]

## Related People

- [[Sami Maameri]]
