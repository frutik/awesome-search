---
title: "Question Answering"
source: "https://queryunderstanding.com/question-answering-94984185c203"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems detect question queries and return direct answers rather than lists of documents — part of the Query Understanding series."
tags:
  - clippings
---

# Question Answering

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Question answering (QA) in search detects when users ask natural language questions and returns direct answers rather than (or in addition to) a list of documents. It's the "what users really want" for many queries.

## Types of Questions

**Factoid questions** ("What is the capital of France?")
- Single, definitive answer
- Can be answered from a knowledge base or document extraction

**Definition questions** ("What is machine learning?")
- Paragraph-length explanations
- Featured snippets, knowledge panels

**List questions** ("What are the best programming languages for AI?")
- Multiple items
- Structured list presentation

**Procedural questions** ("How do I tie a tie?")
- Step-by-step instructions
- Recipe/how-to cards

**Comparison questions** ("iPhone vs Samsung — which is better?")
- Side-by-side comparison tables

## QA Pipeline

```
Question → Question Type Classification → Answer Extraction/Generation → Answer Presentation
```

**Retrieval-based QA**
1. Retrieve candidate passages (BM25 + dense retrieval)
2. Reader model extracts answer span (BERT-based)

**Generative QA**
1. Retrieve context passages
2. Generate answer using T5/GPT with retrieval augmentation (RAG)

## Modern Developments

- Google Featured Snippets, People Also Ask
- ChatGPT / Perplexity AI style conversational QA
- RAG (Retrieval-Augmented Generation) combines search + LLM generation

## Challenges

- Hallucination in generative QA
- Attribution and source citations
- Multi-hop reasoning ("Who is the CEO of the company that makes iPhone?")

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[RAG]]
- [[Agentic Search]]
- [[Search Intent]]

## People

- [[Daniel Tunkelang]]
