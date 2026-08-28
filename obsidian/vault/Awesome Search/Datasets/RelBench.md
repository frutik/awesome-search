---
title: "RelBench"
aliases: ["RelBench benchmark"]
tags:
  - dataset
  - benchmark
  - relational-deep-learning
type: dataset
source: "Robinson et al. (2024) — RelBench: A Benchmark for Deep Learning on Relational Databases"
domain: deep learning tasks over relational databases (15 tasks cited)
website: "https://relbench.stanford.edu"
created: 2026-08-28
---

# RelBench

Benchmark for deep learning directly on relational databases (Robinson et al., 2024), cited in [[Relational Reranking - Scoring Search Results with Structured Facts]] as precedent for conditioning models on relational structure rather than hand-engineered tabular features. Per that article, relational deep learning systems that learn across primary/foreign-key links matched or beat tuned tabular-model baselines on 11 of RelBench's 15 tasks, because the relational models gain access to fields outside a task's target table — the architectural motivation behind [[RelativeDB]]'s [[Relational Transformer]] (RT) reranker.

## Related Concepts

- [[Relational Transformer]] — RT's Cell-attention mechanism extends the cross-table structure RelBench demonstrates value for, into reranking

## Articles

- [[Relational Reranking - Scoring Search Results with Structured Facts]]

## Companies

- [[RelativeDB]]
