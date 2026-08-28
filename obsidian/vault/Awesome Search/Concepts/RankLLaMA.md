---
type: concept
title: "RankLLaMA"
aliases: ["RankLLaMA", "Rank LLaMA"]
status: stub
tags:
  - concept
  - ranking
  - reranking
  - neural-ir
  - llm
created: 2026-06-11
---

# RankLLaMA

> **Stub.** Created as a placeholder — expand with vault-sourced content.

## Definition

RankLLaMA is a LLaMA-based **pointwise** [[Reranking|reranker]] (from the RepLLaMA/RankLLaMA line, Tevatron) — a decoder LLM fine-tuned to score query-document relevance, representing the LLM-reranker end of the cost/quality spectrum.

## Vault references (existing coverage)

- [[Learning to Rank]] — listed under "Neural LTR"

## TODO

- [ ] Cite the source paper; contrast with prompt-based [[RankGPT]] (no fine-tuning).

## Related

- [[Reranking]] · [[LLM as Judge]] · [[RankGPT]] · [[MonoT5]] · [[Learning to Rank]] · [[Relational Transformer]] — [[RelativeDB]]'s 85M RT reranker is benchmarked as quality-comparable to RankLLaMA-7B at a fraction of the FLOPs

## Articles

- [[Relational Reranking - Scoring Search Results with Structured Facts]] — positions RT against RankLLaMA-7B on a FLOPs-vs-NDCG@10 chart

## Topics

- [[Reasoning Reranking]] · [[Frontier of Search 2026]]
