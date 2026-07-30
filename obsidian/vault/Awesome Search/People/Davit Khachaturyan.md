---
title: "Davit Khachaturyan"
type: person
aliases:
  - Khachaturyan
role: "Senior AI Search and Retrieval Engineer"
website: "https://medium.com/@davit.khachaturyan.03"
tags:
  - person
  - search-practitioner
  - rag
created: 2026-07-30
---

# Davit Khachaturyan

By his own description, a *"Senior AI Search and Retrieval Engineer focused on building and
improving production search, RAG, and knowledge-driven AI systems."* No employer is named in the
material held here.

Writes at [medium.com/@davit.khachaturyan.03](https://medium.com/@davit.khachaturyan.03).

## Contributions in This Vault

- [[Hybrid Fusion Failure - BM25 Displacing Reference Documents]] — a production post-mortem on
  adding [[BM25]] to a vector retriever and losing the correct document from the candidate set
  entirely, because a `bool`/`should` query sums an unbounded lexical score with a bounded vector
  score

The write-up is notable for locating the failure at **candidate selection** rather than in either
retrieval branch, and for reporting an honest partial remedy — capping BM25's contribution to the
merged set at three documents — described as a patch rather than a fix.

## Concepts

- [[Hybrid Search]]
- [[Linear Score Combination]]
- [[BM25]]
- [[Retrieval Pipeline]]
- [[Reranking]]
- [[RAG]]
