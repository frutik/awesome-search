---
title: "RankGPT"
aliases: ["RankGPT", "Rank GPT"]
status: stub
tags:
  - concept
  - ranking
  - reranking
  - llm
---

# RankGPT

> **Stub.** Created as a placeholder — **not currently referenced in the vault** (net-new concept).

## Definition

RankGPT is a **listwise** LLM [[Reranking|reranker]] that prompts an instruction-tuned LLM to reorder a candidate list directly (permutation generation), typically using a sliding-window strategy to handle lists longer than the context window. No fine-tuning required.

## Vault references

None yet — gap. (Mentioned only in `planned/reranker-types.md`.)

## TODO

- [ ] Cite the source paper; contrast with fine-tuned [[RankLLaMA]] and pointwise LLM judging.

## Related

- [[Reranking]] · [[LLM as Judge]] · [[Listwise Relevance Evaluation]] · [[RankLLaMA]]
