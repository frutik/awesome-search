---
type: article
title: "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models"
source: "https://arxiv.org/abs/2405.14831"
author: ["Bernal Jiménez Gutiérrez", "Yiheng Shu", "Yu Gu", "Michihiro Yasunaga", "Yu Su"]
published: 2024-05-23
tags:
  - clippings
  - rag
  - knowledge-graph
  - retrieval
  - paper
concepts:
  - HippoRAG
  - RAG
  - GraphRAG
created: 2026-09-05
---

# HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models

**Source**: https://arxiv.org/abs/2405.14831
**Venue**: NeurIPS 2024 · **Submitted**: 23 May 2024 (v1); revised 14 January 2025 (v3)
**Authors**: Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, [[Yu Su]]

## Abstract (verbatim)

> In order to thrive in hostile and ever-changing natural environments, mammalian brains evolved to store large amounts of knowledge about the world and continually integrate new information while avoiding catastrophic forgetting. Despite the impressive accomplishments, large language models (LLMs), even with retrieval-augmented generation (RAG), still struggle to efficiently and effectively integrate a large amount of new experiences after pre-training. In this work, we introduce HippoRAG, a novel retrieval framework inspired by the hippocampal indexing theory of human long-term memory to enable deeper and more efficient knowledge integration over new experiences. HippoRAG synergistically orchestrates LLMs, knowledge graphs, and the Personalized PageRank algorithm to mimic the different roles of neocortex and hippocampus in human memory.

## Results

| Claim | Figure |
|---|---|
| Improvement over prior SOTA on multi-hop QA | up to **20%** |
| Cost reduction vs iterative retrieval (IRCoT) | **10–30×** |
| Speed improvement vs iterative retrieval | **6–13×** |

Single-step retrieval reaches parity with iterative approaches while being substantially cheaper and faster.

## Why It Matters

Multi-hop retrieval as graph propagation rather than an agentic loop — the connections are precomputed into the index instead of discovered by repeated LLM calls at query time. See [[HippoRAG]] for the fuller treatment.

## Related Concepts

- [[HippoRAG]] — primary topic
- [[RAG]] · [[GraphRAG]] · [[Knowledge Graph Search]] · [[Agentic Search]]

## Related People

- [[Yu Su]]
