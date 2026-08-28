---
title: "STaRK"
aliases: ["STaRK benchmark"]
tags:
  - dataset
  - benchmark
  - relational-deep-learning
  - search-evaluation
type: dataset
source: "Wu et al. (2024), NeurIPS 2024 — STaRK: Benchmarking LLM Retrieval on Textual and Relational Knowledge Bases"
domain: retrieval/search over combined textual and relational (graph) knowledge bases
website: "https://stark.stanford.edu"
created: 2026-08-28
---

# STaRK

Benchmark for retrieval over knowledge bases that combine text with relational/graph structure (Wu et al., NeurIPS 2024). Used in [[Relational Reranking - Scoring Search Results with Structured Facts]] to demonstrate [[RelativeDB]]'s [[Relational Transformer]] (RT): on an Amazon product graph recording frequent co-purchases, RT resolves a named product in the query to its row, adds the `also_buy` relational edge into the candidate context, and uses that edge to move the correct matching product from rank #2 (under title-similarity alone) to rank #1.

## Related Concepts

- [[Relational Transformer]] — reranker evaluated on this benchmark

## Articles

- [[Relational Reranking - Scoring Search Results with Structured Facts]]

## Companies

- [[RelativeDB]]
