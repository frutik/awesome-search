---
type: article
title: "GraphRAG: Unlocking LLM discovery on narrative private data"
source: "https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/"
author: ["Jonathan Larson", "Steven Truitt"]
published: 2024-02-13
tags:
  - clippings
  - rag
  - knowledge-graph
  - llm
  - company-blog
concepts:
  - GraphRAG
  - RAG
  - Knowledge Graph Search
created: 2026-09-05
---

# GraphRAG: Unlocking LLM discovery on narrative private data

**Source**: https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/
**Publisher**: Microsoft Research · **Published**: 13 February 2024
**Authors**: Jonathan Larson (Partner Data Architect), Steven Truitt (Principal Program Manager)

## Summary

The originating write-up of [[GraphRAG]]: using LLM-generated knowledge graphs to answer questions over private data that baseline [[RAG]] cannot.

## The Two Failures of Baseline RAG

1. **Connecting disparate information** — where the answer requires joining facts across documents that each score poorly alone.
2. **Holistic semantic understanding** — questions about themes across a whole collection, which no single passage answers.

## Method

An LLM builds a knowledge graph from the private corpus, then **"bottom-up clustering that organizes the data hierarchically into semantic clusters"** produces pre-summarized themes. Retrieval traverses that structure instead of ranking isolated chunks.

## Evaluation

- **Dataset**: VIINA (Violent Incident Information from News Articles) — thousands of Russian and Ukrainian news articles from June 2023
- **Graph construction**: GPT-4 Turbo
- **Baseline**: LangChain's Q&A
- **Graph ML**: graspologic

GraphRAG "consistently outperforms baseline RAG" on comprehensiveness, human enfranchisement and diversity, holding similar faithfulness under SelfCheckGPT evaluation.

Applied domains named: social media, news articles, workplace productivity, chemistry.

## Related Concepts

- [[GraphRAG]] — primary topic
- [[RAG]] · [[Knowledge Graph Search]] · [[HippoRAG]] · [[Long-Context RAG]]

## Related People

- [[Jonathan Larson]] · [[Steven Truitt]]
