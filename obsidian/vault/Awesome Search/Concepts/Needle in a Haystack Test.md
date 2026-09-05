---
type: concept
title: "Needle in a Haystack Test"
aliases: ["Needle In A Haystack", "NIAH", "needle-in-a-haystack test"]
tags:
  - concept
  - evaluation
  - llm
  - context
related_concepts:
  - "[[Long-Context RAG]]"
  - "[[RAG Evaluation]]"
created: 2026-09-05
---

# Needle in a Haystack Test

## Definition

A diagnostic for long-context models: embed a specific, out-of-place fact (**the needle**) inside a large body of unrelated text (**the haystack**), then ask the model a question only that fact answers. Vary two axes — the needle's **depth** in the document (0–100%) and the total **context length** (1K up to the model's limit) — and chart where retrieval succeeds.

Originated by Greg Kamradt; extended by Arize, written up by [[Aparna Dhinakaran]] (February 2024).

## Why It Matters for Search

It isolates a property that retrieval metrics miss: *whether material placed in the context window is actually used*. A perfect retriever that puts the right chunk in position 14 of 20 has still failed if the model cannot see position 14. This is the mechanism behind the "lost in the middle" limit on [[Long-Context RAG]].

## Findings

| Model | Result |
|---|---|
| ChatGPT-4 | Performance declined below 64K tokens; sharp decline past 100K. Overall leader. |
| Claude 2.1 | **27%** initial retrieval accuracy — rising to **98%** with prompt adjustments |
| Mixtral-8x7B-v0.1 | Outperformed expectations relative to model size |

Arize's follow-up reduced Claude 2.1's misses from 165 to 74 through revised prompting alone.

## The Caveat

The Claude 2.1 result — 27% to 98% on a prompt change — is the most important number here, and it is a warning about the test rather than the model. A benchmark that swings 71 points on prompt phrasing is measuring [[Prompt Sensitivity]] as much as retrieval capability.

## Related Concepts

- [[Long-Context RAG]] · [[RAG Evaluation]] · [[Prompt Sensitivity]]
- [[Reranking]] — position in context is a ranking decision

## Articles

- [[The Needle In a Haystack Test]] — [[Aparna Dhinakaran]]
- [[NVIDIA Research - RAG with Long Context LLMs]] — [[Ravi Theja]]; the same effect as a retrieval-budget limit
