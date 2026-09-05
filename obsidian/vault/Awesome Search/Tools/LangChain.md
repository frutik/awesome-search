---
type: tool
title: "LangChain"
aliases: ["langchain", "LangChain AI"]
website: https://www.langchain.com/
repo: https://github.com/langchain-ai/langchain
tags:
  - tool
  - rag
  - llm
  - orchestration
  - open-source
related_concepts:
  - "[[RAG]]"
  - "[[Conversational Memory]]"
  - "[[Text Chunking]]"
  - "[[Query Routing]]"
created: 2026-09-05
---

# LangChain

A framework for building agents and LLM-powered applications by chaining interoperable components and third-party integrations. Maintained by `langchain-ai`, MIT licensed. It now describes itself as "the agent engineering platform".

🔗 https://www.langchain.com/ · https://github.com/langchain-ai/langchain

## Core Abstractions

Chat models · embeddings · vector stores · retrievers · tools and toolkits · model providers.

The wider ecosystem includes **LangGraph** (agent orchestration), **Deep Agents**, and **LangSmith** (observability and deployment).

## Why It Matters Here

Two things make LangChain relevant to this vault beyond being a popular wrapper. Its text splitters (`CharacterTextSplitter`, `RecursiveCharacterTextSplitter`) are the de facto reference implementations that most [[Text Chunking]] writing benchmarks against. And its memory classes are the clearest taxonomy of [[Conversational Memory]] strategies available in code.

## Related Tools

- [[Haystack (deepset)]] · [[LlamaIndex]] — comparable orchestration frameworks
- [[RAGAS]] — evaluation, integrates with LangChain
- [[DSPy]] — the declarative counter-position to prompt chaining

## Related Concepts

- [[RAG]] · [[Conversational Memory]] · [[Text Chunking]] · [[Query Routing]]

## Articles

- [[Conversational Memory for LLMs with Langchain]] — the memory-class taxonomy
- [[Chunking Strategies for LLM Applications]] — uses LangChain splitters throughout
