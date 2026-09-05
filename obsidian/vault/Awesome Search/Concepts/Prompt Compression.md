---
type: concept
title: "Prompt Compression"
aliases: ["prompt compression", "context compression", "LLMLingua", "LongLLMLingua", "AutoCompressors", "Selective Context"]
tags:
  - concept
  - rag
  - llm
  - performance
  - cost
related_concepts:
  - "[[RAG]]"
  - "[[Long-Context RAG]]"
  - "[[Text Chunking]]"
created: 2026-09-05
---

# Prompt Compression

## Definition

Shrinking the retrieved context before it reaches the model, so a RAG pipeline pays for fewer input tokens without losing the information the answer depends on. It sits between retrieval and generation — after [[Reranking]] has chosen what to include, and before the model reads it.

## Why It Exists

RAG's cost is dominated by input tokens, and [[Long-Context RAG]] makes that worse: a larger window invites stuffing it. Compression attacks the bill directly rather than by retrieving less.

## Three Approaches

### AutoCompressors
Convert long text into **summary vectors** that act as soft prompts. The pre-trained model stays frozen; trainable tokens are prepended at the input and optimized end-to-end for the task. The compressed form is no longer human-readable text.

### Selective Context
Assign **self-information** values to lexical units (tokens, phrases, sentences) using a base model such as Llama or GPT-2, rank units by entropy, and keep those above a percentile threshold. Purely information-theoretic — and query-blind, which is its weakness. In [[Iulia Brezeanu]]'s test it discarded the very fact the question was about, at every compression level tried.

### LongLLMLingua
Extends LLMLingua with **question-aware** compression, which is the decisive difference: it compresses relative to the query rather than in the abstract. Three mechanisms —
- coarse-to-fine document analysis against the user's question,
- document reordering by importance,
- **subsequence recovery**, repairing entities corrupted by compression (e.g. "2009" truncated to "209").

## Results

| Measure | Value |
|---|---|
| Original tokens | 2,362 |
| Compressed tokens | 344 |
| **Compression ratio** | **6.87×** |
| Projected saving per 1B tokens | ~$850 (from ~$1,000 to ~$150) |

The query was still answered correctly after compression — the claim being that question-aware compression is close to free, while query-blind compression is not.

## The Takeaway

Compression quality tracks query-awareness, not compression ratio. Selective Context and LongLLMLingua both shrink text; only the one that knows the question reliably keeps the part that matters. This is the same principle as [[Reranking]] — relevance is a relation between document and query, never a property of the document alone.

## Related Concepts

- [[RAG]] · [[Long-Context RAG]] · [[Reranking]] · [[Text Chunking]] · [[Clean Context]]

## Articles

- [[How to Cut RAG Costs by 80% Using Prompt Compression]] — [[Iulia Brezeanu]]
