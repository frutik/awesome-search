---
type: concept
title: "Long-Context RAG"
aliases: ["Long Context RAG", "long-context retrieval"]
tags:
  - concept
  - rag
  - llm
  - context
related_concepts:
  - "[[RAG]]"
  - "[[Needle in a Haystack Test]]"
  - "[[Prompt Compression]]"
created: 2026-09-05
---

# Long-Context RAG

## The Question

If a model's context window grows to 32K, 128K or a million tokens, is retrieval still necessary — or can the whole corpus simply be pasted in?

## The Empirical Answer: Both

NVIDIA Research (covered by [[Ravi Theja]] for LlamaIndex, October 2023) evaluated Nemo GPT-43B and LLaMA2-70B at extended 16K and 32K contexts across seven datasets — QMSum, Qasper, NarrativeQA, QuALITY, MuSiQue, HotpotQA and MultiFieldQA-en. The findings:

- Retrieval **significantly improves** both short-context (4K) and long-context (16K/32K) models. Long context does not make retrieval redundant.
- LLaMA2-70B-32K with retrieval surpassed GPT-3.5-turbo-16K and matched davinci-003.
- A 4K model **with retrieval** performs comparably to a much longer model, at faster inference.

## The Lost-in-the-Middle Constraint

Retrieving *more* is not monotonically better. Top 5–10 chunks was optimal; retrieving 20 chunks **degraded** performance, attributed to the "lost in the middle" phenomenon — material placed in the middle of a long context is attended to less reliably than material at either end.

This is the same effect the [[Needle in a Haystack Test]] measures directly, and it is why long context does not dissolve the ranking problem: position within the context window is itself a ranking decision.

## Practical Consequence

Long context changes the *budget*, not the *task*. You still need to decide what goes in and in what order — and [[Prompt Compression]] becomes attractive precisely because filling a large window is expensive.

## Related Concepts

- [[RAG]] · [[Needle in a Haystack Test]] · [[Prompt Compression]]
- [[Reranking]] — what decides the order material enters the window
- [[GraphRAG]] — the alternative response to "one chunk isn't enough context"

## Articles

- [[NVIDIA Research - RAG with Long Context LLMs]] — [[Ravi Theja]]
- [[The Needle In a Haystack Test]] — [[Aparna Dhinakaran]]
- [[How to Cut RAG Costs by 80% Using Prompt Compression]] — [[Iulia Brezeanu]]
