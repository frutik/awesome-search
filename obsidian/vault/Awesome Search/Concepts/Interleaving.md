---
type: concept
title: "Interleaving"
aliases: ["interleaving", "result interleaving", "zip merge"]
tags:
  - concept
  - ranking
  - evaluation
  - hybrid-search
---

# Interleaving

## Definition

Interleaving merges two ranked result lists into a single ranking by alternating ("zip-merge") items from each, optionally weighted by sampling probabilities so one source contributes more often. It serves two purposes:

1. **Fusion baseline** — a simple, hard-to-beat way to combine multiple retrievers (e.g. lexical + vector) when their scores are non-comparable, without training a model.
2. **Online evaluation** — interleaving two rankers and observing which side's items get clicked is a sensitive [[A-B Testing for Search|A/B testing]] alternative that needs less traffic than split testing.

## Why it matters

In a multi-retriever / [[Hybrid Search]] setup, interleaving solves the **cold-start** problem: you need behavioral history before you can train an LTR fusion model, but you need *some* unified ranking to collect clicks. Interleaving provides that initial ranking, after which a [[LambdaMART]] / [[Learning to Rank|LTR]] re-ranker (e.g. [[Metarank]]) can take over.

## Related Concepts

- [[Reciprocal Rank Fusion]] — score-free rank fusion alternative
- [[Linear Score Combination]] · [[Relative Score Fusion]] — score-based fusion
- [[Hybrid Search]] — primary use case
- [[Learning to Rank]] · [[Click Signals]] — what interleaving bootstraps
- [[A-B Testing for Search]] — interleaving as an online eval method

## Articles

- [[Hybrid Search and Learning-to-Rank with Metarank]] — interleaving as the cold-start baseline
- [[Getting Started on Search Relevance for the Understaffed Search Team]]
