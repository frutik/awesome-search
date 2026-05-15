---
title: "Symmetric vs. Asymmetric Semantic Search"
source: "https://www.sbert.net/examples/applications/semantic-search/README.html#symmetric-vs-asymmetric-semantic-search"
author: []
published: 
created: 2026-05-15
description: "Critical distinction in semantic search setup: symmetric search matches similar-length query/corpus pairs, while asymmetric search matches short queries to long answers — each requires different models."
tags:
  - clippings
---
# Symmetric vs. Asymmetric Semantic Search

A **critical distinction** that determines which embedding model to use.

## Symmetric Semantic Search

Query and corpus entries are **about the same length** with the same amount of content.

Example: finding similar questions
- Query: "How to learn Python online?"
- Match: "How to learn Python on the web?"

You could flip query and corpus entries and the task still makes sense.

- Training example: Quora Duplicate Questions
- Suitable models: Pre-Trained Sentence Embedding Models

## Asymmetric Semantic Search

A **short query** (question or keywords) matched against a **longer paragraph** that answers it.

Example:
- Query: "What is Python"
- Match: "Python is an interpreted, high-level and general-purpose programming language..."

Flipping query and corpus usually does **not** make sense.

- Training example: MS MARCO
- Suitable models: Pre-Trained MS MARCO Models

## Key rule

**Choose the right model for your type of task.** Using a symmetric model for asymmetric search (or vice versa) significantly degrades retrieval quality.

## Related Concepts
- [[Asymmetric Semantic Search]] — the core concept explained
- [[Semantic Search]] — parent concept
- [[Dense Embeddings]] — the representation used for both symmetric and asymmetric search
- [[Bi-Encoder]] — architecture; model choice depends on task symmetry
- [[Dense Vector Retrieval]] — downstream retrieval infrastructure
- [[Embeddings]] — training data (MS MARCO vs Quora Duplicate Questions) shapes model behaviour