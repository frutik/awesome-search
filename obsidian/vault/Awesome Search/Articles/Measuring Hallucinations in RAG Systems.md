---
type: article
title: "Measuring Hallucinations in RAG Systems"
source: "https://vectara.com/measuring-hallucinations-in-rag-systems/"
author: ["Shane Connelly"]
published: 2023-11-06
tags:
  - clippings
  - rag
  - llm
  - evaluation
  - company-blog
concepts:
  - Hallucination Detection
  - RAG
created: 2026-09-05
---

# Measuring Hallucinations in RAG Systems

**Source**: https://vectara.com/measuring-hallucinations-in-rag-systems/
**Publisher**: Vectara · **Published**: 6 November 2023 · **Author**: [[Shane Connelly]]

## Summary

Introduces Vectara's **Hallucination Evaluation Model (HEM)** and the accompanying public **Hallucination Leaderboard**. The measured question is narrow and therefore tractable: given retrieved evidence, does the model **"only use the data provided to it in generating its output"**?

## Leaderboard Results

| Model | Answer rate | Accuracy | Hallucination rate | Avg summary length |
|---|---|---|---|---|
| GPT-4 | 100% | 97.0% | **3.0%** | 81.1 words |
| GPT-3.5 | 99.6% | 96.5% | 3.5% | 84.1 words |
| Llama 2 70B | 99.9% | 94.9% | 5.1% | 84.9 words |
| Llama 2 13B | 99.8% | 94.1% | 5.9% | 82.1 words |
| Llama 2 7B | 99.6% | 94.4% | 5.6% | 119.9 words |
| Cohere-Chat | 98.0% | 92.5% | 7.5% | 74.4 words |
| Cohere | 99.8% | 91.5% | 8.5% | 59.8 words |
| Claude 2 | 99.3% | 91.5% | 8.5% | 87.5 words |
| Mistral 7B | 98.7% | 90.6% | 9.4% | 96.1 words |
| Google PaLM | 92.4% | 87.9% | 12.1% | 36.2 words |
| Google PaLM-Chat | 88.8% | 72.8% | 27.2% | 221.1 words |

## The Length Correlation

PaLM-Chat produced the longest summaries by a wide margin and hallucinated most — every extra sentence is another chance to exceed the evidence. Worth reading alongside the answer-rate column, which shows how often a model declined to answer at all.

## Related Concepts

- [[Hallucination Detection]] — primary topic
- [[RAG]] · [[LLM as Judge]] · [[Search Evaluation]]

## Related Tools

- [[RAGAS]]

## Related People

- [[Shane Connelly]]
