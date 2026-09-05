---
type: article
title: "How to Cut RAG Costs by 80% Using Prompt Compression"
source: "https://towardsdatascience.com/how-to-cut-rag-costs-by-80-using-prompt-compression-877a07c6bedb"
author: ["Iulia Brezeanu"]
published: 2024-01-04
tags:
  - clippings
  - rag
  - llm
  - cost
  - performance
concepts:
  - Prompt Compression
  - RAG
  - Long-Context RAG
created: 2026-09-05
---

# How to Cut RAG Costs by 80% Using Prompt Compression

**Source**: https://towardsdatascience.com/how-to-cut-rag-costs-by-80-using-prompt-compression-877a07c6bedb
**Published**: 4 January 2024 · **Author**: [[Iulia Brezeanu]]

## Summary

Three approaches to shrinking retrieved context before generation, and a demonstration that query-awareness — not compression ratio — determines whether compression is safe.

## The Three Methods

**AutoCompressors** — convert text into summary vectors acting as soft prompts; the pre-trained model stays frozen while prepended trainable tokens are optimized end-to-end.

**Selective Context** — assign self-information values to lexical units using a base model (Llama, GPT-2), rank by entropy, keep above a percentile threshold. In testing it **failed** to preserve the fact the question concerned, at every compression level.

**LongLLMLingua** — extends LLMLingua with question-aware compression: coarse-to-fine document analysis against the query, document reordering by importance, and subsequence recovery to repair corrupted entities (e.g. "2009" → "209").

## Numbers

| Measure | Value |
|---|---|
| Original tokens | 2,362 |
| Compressed tokens | 344 |
| Compression ratio | **6.87×** |
| Cost saving per query | $0.00202 |
| Projected per 1B tokens | ~$1,000 → ~$150 |

The query was answered correctly after compression.

## Related Concepts

- [[Prompt Compression]] — primary topic
- [[RAG]] · [[Long-Context RAG]] · [[Reranking]] · [[Clean Context]]

## Related People

- [[Iulia Brezeanu]]
