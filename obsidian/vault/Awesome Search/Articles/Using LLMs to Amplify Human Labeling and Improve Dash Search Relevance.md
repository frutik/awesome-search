---
title: "Using LLMs to Amplify Human Labeling and Improve Dash Search Relevance"
source: "https://dropbox.tech/machine-learning/llm-human-labeling-improving-search-relevance-dropbox-dash"
author: "[[Dmitriy Meyerzon]]"
published: 2026-02-26
company: "[[Dropbox]]"
tags: [LLM-as-judge, relevance-labeling, search-ranking, RAG, DSPy, human-labeling, enterprise-search, company-blog]
---

# Using LLMs to Amplify Human Labeling and Improve Dash Search Relevance

**Author:** [[Dmitriy Meyerzon]] ([[Dropbox]])

## Summary

How Dropbox Dash trains its enterprise search ranking models using a combination of human labeling and LLM-based evaluation. Small amounts of human-labeled data are used to calibrate an LLM evaluator, which then generates relevance labels at scale (100x multiplication factor).

## Context: Dropbox Dash

Dropbox Dash is an enterprise search and RAG product:
- Follows RAG pattern: retrieval → LLM generation
- Must rank results from millions (or billions) of documents
- LLMs can only receive a small subset of retrieved docs → ranking quality is critical

## The Labeling Challenge

Ranking model trained on query-document pairs with relevance scores (1-5 scale). Sources of labels:
- **User behavior** (clicks, skips) — sparse, biased, unevenly distributed
- **Human labeling** — systematic but expensive, can't evaluate customer data, requires ongoing training
- **LLM evaluation** — cheaper, more consistent, can scale, but requires careful calibration

## The Hybrid Approach: LLMs Amplify Human Judgment

1. Small team labels high-quality internal dataset (non-customer data)
2. LLM is calibrated against these human labels
3. Once performance meets quality thresholds, LLM generates hundreds of thousands to millions of labels

**The LLM acts as a force multiplier**: humans teach the LLM, the LLM generates large-scale training data.

## LLM Evaluation Quality Measurement

Error measured with **MSE** (mean squared error on 1-5 scale):
- 0 for exact agreement, 16 for maximum disagreement
- Improvements driven by: prompt refinement, reasoning-optimized models, query context injection, DSPy automated optimization

## Document Sampling Strategy

Don't sample training data uniformly. Bias toward **cases most likely to surface errors**:
- Users clicking docs LLM rated as low relevance
- Users consistently skipping docs LLM rated as highly relevant

These discrepancies are prioritized for human review and prompt refinement.

## Context-Aware Evaluation

LLMs need organizational context to evaluate accurately. Example: at Dropbox, "diet sprite" is an internal performance management tool — not a soft drink.

Solution: provide LLMs with **research tools** to look up context *before* assigning relevance labels, similar to what human evaluators do by running additional searches.

## Prompt Optimization with DSPy

[DSPy](https://dspy.ai/) automates prompt optimization:
- Given a clear objective and human-labeled examples, DSPy refines prompts to better match human judgments
- Enables systematic optimization rather than manual trial-and-error
- Reusable across different evaluation tasks and model configurations

## Key Principle

Even as models improve, human grounding remains a **structural requirement**. Prompts drift, models change, product expectations shift. A persistent human-reviewed reference set anchors evaluation over time.

LLMs make it possible to apply human judgment consistently and at scale — they don't replace it.

## Related Concepts

- [[LLM as Judge]] — the core technique
- [[Judgment Lists]] — the labeled relevance data
- [[Learning to Rank]] — the downstream ranking model trained on these labels
- [[Search Evaluation]] — the broader evaluation framework
- [[RAG]] — the retrieval-augmented generation context

## People

- [[Dmitriy Meyerzon]]
