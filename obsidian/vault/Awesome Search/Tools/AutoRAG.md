---
type: tool
title: "AutoRAG"
aliases: ["AutoRAG 2.0", "autorag", "@autorag/librarian"]
repo: https://github.com/Marker-Inc-Korea/AutoRAG
tags:
  - tool
  - rag
  - agentic-search
  - open-source
related_concepts:
  - "[[RAG]]"
  - "[[Agentic Search]]"
  - "[[Hybrid Search]]"
created: 2026-09-05
---

# AutoRAG

Maintained by Marker Inc. Korea, MIT licensed.

> [!warning] The project pivoted
> AutoRAG was widely catalogued as "an AutoML tool for RAG — automatically
> optimize your RAG pipeline with a single YAML file". **AutoRAG 2.0 is a
> different product**: a self-evolving *librarian agent* for document
> collections, shipped as `@autorag/librarian` on npm. Older descriptions of
> it as pipeline AutoML no longer describe what the repository contains.

🔗 https://github.com/Marker-Inc-Korea/AutoRAG

## What It Is Now

Rather than returning raw file paths and line numbers, it acts as a librarian that retrieves, reads, evaluates and curates findings into structured knowledge units — searching across PDFs, wikis, notes and papers, then synthesizing numbered findings with locations. It learns from user feedback which retrieval methods work for which query types.

| Module | Role |
|---|---|
| **MinSync** | Local indexing layer for BM25 / vector / hybrid retrieval |
| **Jikji** | Discovery and initial ranking |
| **Pi Agent Loop** | The retrieve-and-curate reasoning cycle |
| **Datasource Skills** | Connectors — Slack, Discord, Gmail, GitHub, cloud drives, Obsidian |
| **dupey** | Duplicate document detection |

Runtime requires Node ≥24 or Bun; PDF parsing needs Java 11+.

## Why It Matters Here

The pivot is itself the interesting datum: a project that set out to auto-tune retrieval hyperparameters ended up as an agent that decides retrieval strategy at query time. That is the same movement described in [[Agentic Search]] — from a tuned static pipeline to a policy chosen per query.

## Related Concepts

- [[RAG]] · [[Agentic Search]] · [[Hybrid Search]]

## Related Tools

- [[Haystack (deepset)]] · [[LlamaIndex]] · [[LangChain]]
