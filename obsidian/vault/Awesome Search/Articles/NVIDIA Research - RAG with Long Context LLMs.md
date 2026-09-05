---
type: article
title: "NVIDIA Research: RAG with Long Context LLMs"
source: "https://www.llamaindex.ai/blog/nvidia-research-rag-with-long-context-llms-7d94d40090c4"
author: ["Ravi Theja"]
published: 2023-10-22
tags:
  - clippings
  - rag
  - llm
  - context
  - company-blog
concepts:
  - Long-Context RAG
  - RAG
  - Needle in a Haystack Test
created: 2026-09-05
---

# NVIDIA Research: RAG with Long Context LLMs

**Source**: https://www.llamaindex.ai/blog/nvidia-research-rag-with-long-context-llms-7d94d40090c4
**Publisher**: LlamaIndex · **Published**: 22 October 2023 · **Author**: [[Ravi Theja]]

## Summary

Does a long context window make retrieval unnecessary? NVIDIA Research's answer, covered here, is no — retrieval helps *both* short- and long-context models.

## Setup

- **Models**: Nemo GPT-43B (extended to 16K), LLaMA2-70B (extended to 16K and 32K)
- **Benchmarks**: QMSum, Qasper, NarrativeQA, QuALITY, MuSiQue, HotpotQA, MultiFieldQA-en

## Findings

1. Retrieval **"significantly enhances the performance of both shorter 4K context language models and their longer 16K/32K context counterparts."**
2. LLaMA2-70B-32K with retrieval surpassed GPT-3.5-turbo-16K and matched davinci-003.
3. **Optimal retrieval is 5–10 chunks.** Retrieving 20 degraded performance, attributed to the "lost in the middle" phenomenon.
4. A 4K model with retrieval matches much longer models while inferring faster.

## Why It Matters

Point 3 is the durable one: more context is not monotonically better, so ordering and budgeting remain ranking problems even at 32K. See [[Long-Context RAG]].

## Related Concepts

- [[Long-Context RAG]] — primary topic
- [[RAG]] · [[Needle in a Haystack Test]] · [[Reranking]] · [[Prompt Compression]]

## Related Tools

- [[LlamaIndex]]

## Related People

- [[Ravi Theja]]
