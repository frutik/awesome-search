---
type: concept
title: "GraphRAG"
aliases: ["Graph RAG", "graph-based RAG", "Knowledge Graph RAG"]
tags:
  - concept
  - rag
  - knowledge-graph
  - llm
related_concepts:
  - "[[RAG]]"
  - "[[HippoRAG]]"
  - "[[Knowledge Graph Search]]"
created: 2026-09-05
---

# GraphRAG

## Definition

**GraphRAG** replaces (or supplements) flat chunk retrieval with an LLM-generated knowledge graph over the corpus, then retrieves over that graph's structure rather than over independent passage embeddings.

## The Problem It Addresses

Microsoft Research's framing identifies two failure modes of baseline [[RAG]] that no amount of embedding-quality work fixes:

1. **Connecting disparate information** — the answer requires joining facts that live in different documents, and each document alone scores poorly against the query.
2. **Holistic semantic understanding** — questions about themes across a whole collection ("what are the main topics here?") have no single passage that answers them.

Both are consequences of scoring each passage independently — a limitation of similarity ranking that no better embedding model removes.

## Mechanism

1. An LLM extracts entities and relationships from the source documents into a knowledge graph.
2. **Bottom-up clustering** organizes the graph hierarchically into semantic clusters.
3. Each cluster is pre-summarized, so thematic questions have something to retrieve against.
4. Query time traverses graph structure rather than ranking isolated chunks.

## Evidence

Microsoft Research evaluated on the **VIINA** dataset (Violent Incident Information from News Articles) — thousands of Russian and Ukrainian news articles from June 2023 — using GPT-4 Turbo for graph construction and LangChain's Q&A as the baseline. GraphRAG consistently outperformed baseline RAG on comprehensiveness, human enfranchisement and diversity, while holding similar faithfulness under SelfCheckGPT evaluation.

The graph machine learning came from the **graspologic** library.

## Related Concepts

- [[RAG]] — the baseline this modifies
- [[HippoRAG]] — a neurobiologically-motivated variant using Personalized PageRank over the graph
- [[Knowledge Graph Search]] — the underlying representation
- [[Long-Context RAG]] — the competing answer to the same "not enough context" problem

## Articles

- [[GraphRAG - Unlocking LLM discovery on narrative private data]] — [[Jonathan Larson]], [[Steven Truitt]]; the originating Microsoft Research post
