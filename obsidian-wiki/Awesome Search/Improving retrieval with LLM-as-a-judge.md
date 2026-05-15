---
title: "Improving retrieval with LLM-as-a-judge"
source: "https://blog.vespa.ai/improving-retrieval-with-llm-as-a-judge/"
author:
  - "[[Jo Kristian Bergum]]"
published: 2024-07-03
created: 2026-05-15
description: "How to build domain-specific retrieval evaluation datasets using calibrated LLM judges — covering query sampling, document pooling, LLM calibration against human labels, and scaling to thousands of judgments."
tags:
  - clippings
---
# Improving Retrieval with LLM-as-a-Judge

Build reusable relevance evaluation datasets for your data using LLMs as judges — calibrated against human preferences, then scaled to larger collections.

## Ground truth dataset components

- **Query** (from production logs — real queries are best)
- **Passage/Document** (sampled via "pooling" — top-k from multiple retrieval methods)
- **Relevance judgment** (graded: 0=irrelevant, 1=relevant, 2=highly relevant)

Minimum viable: **25 queries** (TREC standard). Single-technique pooling introduces bias.

## Evaluation metrics

- **P@k**: relevant results in top-k / k (ignores position)
- **Recall@k**: proportion of relevant docs retrieved in top-k
- **nDCG@k**: grade + position weighted, normalized to 0–1 (preferred for RAG)

## LLM-as-judge methodology

### 1. Calibration

1. Create small labeled dataset (26 queries, 90 triplets for search.vespa.ai)
2. Run GPT-4o with calibrated prompt on same pairs
3. Check confusion matrix correlation

Result: strong agreement, few disagreements >1 level. Good nDCG@10 correlation between human and GPT labels across 9 retrieval methods.

### 2. Prompt design

- Clear 0–2 scoring scale with definitions
- Two static demonstration examples
- Step-by-step reasoning instructions
- System role emphasizing relevance assessment

### 3. Scale up

With validated correlation → expand to full collection:
- search.vespa.ai: 386 queries, 6 retrieval methods, 10,372 unique query-passage pairs
- Label distribution: 4,817 irrelevant / 4,642 relevant / 913 highly relevant

## Benefits vs. human labeling

- Cost-effective and fast
- Enables rapid iteration
- Scales beyond expert capacity

## Key principle

"The main point: create your own dataset, for your own data and retrieval use case." Generic collections don't capture domain-specific relevance.

## Related Concepts
- [[LLM as Judge]] — the methodology explained and demonstrated
- [[Judgment Lists]] — the ground truth dataset built with LLM judges
- [[Search Evaluation]] — relevance evaluation framework
- [[NDCG]] — nDCG@k as the primary evaluation metric
- [[Precision and Recall]] — P@k and Recall@k explained
- [[Dense Vector Retrieval]] — one of the 6 retrieval methods benchmarked

## People
- [[Jo Kristian Bergum]] — Vespa; author