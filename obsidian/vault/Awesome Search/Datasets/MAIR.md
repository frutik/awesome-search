---
type: dataset
title: "MAIR"
aliases: ["MAIR benchmark"]
tags: [dataset, instruction-following, retrieval, benchmark]
website: "https://arxiv.org/abs/2410.10127"
related_concepts:
  - "[[Reranking]]"
created: 2026-10-11
---

# MAIR

A benchmark for **instruction-following retrieval**: 123 tasks, each with a task-specific instruction that the retriever or reranker must take into account (https://arxiv.org/abs/2410.10127).

---

## Use in This Vault

[[rerank-3 and rerank-3-lite - the next generation of Voyage rerankers]] uses MAIR to check that instruction-following survived a model upgrade. [[Voyage rerank-3]] scored on par with rerank-2.5 and 3.58% above [[Cohere]] Rerank v4.0 Pro.

## Related Concepts

- [[Reranking]] · [[Search Intent]]

## Related Articles

- [[rerank-3 and rerank-3-lite - the next generation of Voyage rerankers]]
