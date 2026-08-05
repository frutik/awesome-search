---
title: "LoTTE"
aliases: ["LoTTE benchmark", "Long-Tail Topic-stratified Evaluation"]
tags:
  - dataset
  - benchmark
  - retrieval
  - long-tail
  - search-evaluation
type: dataset
source: Stanford — introduced with ColBERTv2 (Santhanam, Khattab et al., NAACL 2022)
domain: long-tail topic-stratified retrieval over StackExchange
website: https://github.com/stanford-futuredata/ColBERT
created: 2026-08-05
---

# LoTTE

## Overview

**LoTTE** (Long-Tail Topic-stratified Evaluation) is a retrieval benchmark introduced alongside [[ColBERT|ColBERTv2]], built from StackExchange communities and deliberately stratified toward **long-tail topics** rather than the head-heavy distributions that dominate web-search corpora like [[MS MARCO]].

It spans five topical domains — writing, recreation, science, technology, and lifestyle — plus a pooled setting, and provides two query types per domain:

- **Search queries** — short, keyword-like, resembling what users type into a search box
- **Forum queries** — longer, natural-language questions as posted by community members

Having both against the same corpus is unusually useful, because it isolates query *form* from topic: the same information need expressed two ways, so you can see how much of a model's performance depends on query phrasing rather than retrieval capability.

## Why It Matters

Head-query and tail-query performance diverge sharply, and most benchmarks over-sample the head. That matters practically because the head is where click signals are abundant and lexical matching already works well — the tail is where a better retrieval model actually earns its keep, and where most benchmarks are quietest.

LoTTE also covers domains where the relevant vocabulary is specialized and sparse, which is exactly the regime where [[Zero-Shot Retrieval]] tends to degrade and where [[Embedding Fine-tuning|domain fine-tuning]] pays off most.

For teams, the transferable idea is the *stratification itself*: when building your own [[Judgment Lists|judgment set]], sampling head/torso/tail separately and reporting them separately catches regressions that an aggregate metric hides. See [[Query Sampling]] and [[Model Selection and Fine-Tuning Evaluation]].

## Related

- [[Retrieval Benchmarks and Leaderboards]] — the wider landscape
- [[ColBERT]] · [[Late Interaction]] — LoTTE was introduced with ColBERTv2
- [[BEIR]] — the heterogeneous zero-shot counterpart
- [[MS MARCO]] — the head-heavy distribution LoTTE reacts against
- [[Query Sampling]] — the same stratification logic applied to your own queries
