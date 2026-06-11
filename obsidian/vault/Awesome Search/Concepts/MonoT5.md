---
title: "MonoT5"
aliases: ["MonoT5", "monoT5"]
status: stub
tags:
  - concept
  - ranking
  - reranking
  - neural-ir
---

# MonoT5

> **Stub.** Created as a placeholder — expand with vault-sourced content.

## Definition

MonoT5 is a T5-based **pointwise** neural [[Reranking|reranker]]: it frames relevance as a seq2seq task, scoring a (query, document) pair by the model's probability of generating a "true" vs. "false" token.

## Vault references (existing coverage)

- [[Learning to Rank]] — listed under "Neural LTR" as a pointwise ranker

## TODO

- [ ] Add the mono/duo distinction (DuoT5 = pairwise) and cite the source paper.

## Related

- [[Reranking]] · [[Cross-Encoder]] · [[RankLLaMA]] · [[Learning to Rank]]
