---
type: tool
title: "RAGAS"
aliases: ["Ragas", "ragas"]
website: https://docs.ragas.io/
repo: https://github.com/explodinggradients/ragas
tags:
  - tool
  - rag
  - evaluation
  - llm
  - open-source
related_concepts:
  - "[[Hallucination Detection]]"
  - "[[RAG]]"
  - "[[LLM as Judge]]"
  - "[[Hallucination Detection]]"
created: 2026-09-05
---

# RAGAS

An evaluation toolkit for LLM applications, Apache-2.0, originally published under `explodinggradients` and now maintained by VibrantLabs. It describes its purpose as "objective metrics, intelligent test generation, and data-driven insights for LLM apps", replacing time-consuming subjective assessment with a repeatable workflow.

🔗 https://docs.ragas.io/ · https://github.com/explodinggradients/ragas

## What It Provides

- LLM-based and traditional metrics for retrieval and generation quality
- Aspect critique (`DiscreteMetric`) — evaluating a custom aspect against allowed values
- Test data generation, so an evaluation set can be bootstrapped rather than hand-labelled
- Integrations with frameworks including [[LangChain]]

## Why It Matters Here

RAGAS is the tool that made RAG evaluation routine rather than bespoke. It splits the problem the way this vault does — retrieval quality and generation quality are separately measurable — and its reliance on [[LLM as Judge]] scoring is the same tradeoff discussed there: cheap and scalable, but the judge itself becomes a component needing validation.

## Related Tools

- [[Quepid]] · [[Rated Ranking Evaluator]] — the equivalent tooling for classical search relevance
- [[LangChain]] · [[LlamaIndex]] · [[Haystack (deepset)]] — the pipelines it evaluates

## Related Concepts

- [[RAG]] · [[Hallucination Detection]] · [[LLM as Judge]] · [[Search Evaluation]]

## Articles

- [[Measuring Hallucinations in RAG Systems]] — a complementary, model-based approach to the same question
