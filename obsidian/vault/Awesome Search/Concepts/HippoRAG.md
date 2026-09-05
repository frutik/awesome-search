---
type: concept
title: "HippoRAG"
aliases: ["Hippo RAG"]
tags:
  - concept
  - rag
  - knowledge-graph
  - retrieval
related_concepts:
  - "[[RAG]]"
  - "[[GraphRAG]]"
  - "[[Knowledge Graph Search]]"
created: 2026-09-05
---

# HippoRAG

## Definition

**HippoRAG** is a retrieval framework modelled on the *hippocampal indexing theory* of human long-term memory. It orchestrates an LLM, a knowledge graph, and the **Personalized PageRank** algorithm to mimic the division of labour between neocortex and hippocampus.

Introduced in *HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models* (Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, [[Yu Su]]), arXiv May 2024, NeurIPS 2024.

## The Argument

Mammalian brains integrate new experience continuously without catastrophic forgetting. LLMs — even with [[RAG]] — do not: integrating a large body of new experience after pre-training remains inefficient. HippoRAG's claim is that the *indexing* structure, not the model, is where that capability lives.

## Results

| Claim | Figure |
|---|---|
| Multi-hop QA improvement over prior state of the art | up to **20%** |
| Cost reduction vs iterative retrieval (IRCoT) | **10–30×** |
| Speed improvement vs iterative retrieval | **6–13×** |

The headline efficiency argument is that a *single-step* retrieval over the right graph structure matches what iterative retrieval achieves by making many LLM calls.

## Why It Matters

It reframes multi-hop retrieval as a graph propagation problem rather than an agentic loop. Where [[Agentic Search]] and [[Search-R1]] answer multi-hop questions by retrieving repeatedly, HippoRAG answers them once against an index that already encodes the connections — a substantially different cost profile.

## Related Concepts

- [[RAG]] · [[GraphRAG]] · [[Knowledge Graph Search]]
- [[Agentic Search]] — the iterative alternative it benchmarks against
- [[Dense Vector Retrieval]]

## Articles

- [[HippoRAG - Neurobiologically Inspired Long-Term Memory for Large Language Models]]
