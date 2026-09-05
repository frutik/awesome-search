---
type: article
title: "How to Detect Hallucinations in LLMs"
source: "https://towardsdatascience.com/real-time-llm-hallucination-detection-9a68bb292698"
author: ["Iulia Brezeanu"]
published: 2023-12-31
tags:
  - clippings
  - llm
  - evaluation
  - rag
concepts:
  - Hallucination Detection
  - LLM as Judge
created: 2026-09-05
---

# How to Detect Hallucinations in LLMs

**Source**: https://towardsdatascience.com/real-time-llm-hallucination-detection-9a68bb292698
**Published**: 31 December 2023 · **Author**: [[Iulia Brezeanu]]

## Summary

A hands-on benchmark of four self-consistency methods for detecting hallucination without a reference answer, compared on both accuracy and latency.

## The Four Methods

| Method | Model used | Latency |
|---|---|---|
| Sentence-embedding cosine distance | all-MiniLM-L6-v2 | **~0.002 s** |
| SelfCheckGPT-BERTScore | RoBERTa-large (17 layers), MNLI | ~2 s |
| SelfCheckGPT-NLI | DeBERTa-v3-large, MNLI | ~1 s |
| SelfCheckGPT-Prompt | gpt-3.5-turbo | ~0.5 s — **best performing** |

BERTScore uses a baseline tensor from 1M Common Crawl sentence pairs; NLI classifies entailment / contradiction / neutral and takes the contradiction probability.

## Separation Achieved

On a fabricated subject vs a real one: cosine distance 0.52 vs 0.93; SelfCheckGPT-Prompt 0.0 vs 0.95.

## Evaluation Data

WikiBio — 238 Wikipedia topics; of 1,908 annotated sentences, ~40% major-inaccurate, 33% minor-inaccurate, 27% accurate. Inter-annotator agreement (Cohen's κ) 0.595.

## Related Concepts

- [[Hallucination Detection]] — primary topic
- [[LLM as Judge]] · [[RAG]] · [[Inter-Annotator Agreement]]

## Related People

- [[Iulia Brezeanu]]
