---
title: "Answering Compositional Queries with Set-Theoretic Embeddings"
source: "https://arxiv.org/abs/2306.04133"
pdf: "https://arxiv.org/pdf/2306.04133"
author:
  - "[[Shib Sankar Dasgupta]]"
  - "[[Andrew McCallum]]"
  - "[[Steffen Rendle]]"
  - "[[Li Zhang]]"
published: 2023-06-07
created: 2026-06-22
venue: "arXiv (cs.IR)"
tags:
  - article
  - embeddings
  - box-embedding
  - set-theoretic-embeddings
  - compositional-queries
  - faceted-search
  - information-retrieval
  - recommendation
concepts:
  - "[[Box Embedding]]"
  - "[[Set-Theoretic Embeddings]]"
  - "[[Compositional Embeddings]]"
  - "[[Compositional Queries]]"
  - "[[Faceted Search]]"
topics: []
---

# Answering Compositional Queries with Set-Theoretic Embeddings

**Authors:** [[Shib Sankar Dasgupta]], [[Andrew McCallum]], [[Steffen Rendle]], [[Li Zhang]] · **arXiv:2306.04133** (cs.IR, 2023)

## Summary

The search/IR application of the [[Box Embedding]] line: it shows that representing **item–attribute relations** with [[Box Embedding|box embeddings]] — *"learnable Venn diagrams"* — answers **[[Compositional Queries|compositional queries]]** (combining attributes with AND / OR / NOT) substantially better than dot-product vector embeddings. This is the direct search-relevant payoff of [[Word2Box]]'s set-theoretic idea, by the same lead author ([[Shib Sankar Dasgupta]]), now aimed at faceted browsing and recommendation rather than word similarity.

## The Problem

Standard item/attribute embeddings score relevance by **dot product**. That works for a single attribute ("movies that are *comedies*"), but degrades on **compositional** requests that combine conditions — e.g. *"comedies **AND** British **BUT NOT** romances"*. A point vector has no notion of set membership, so AND/OR/NOT don't compose cleanly.

## The Approach

- Represent each item and attribute as a **box** (a region) instead of a point — *learnable Venn diagrams*.
- A [[Set-Theoretic Embeddings|set-theoretic]] query then maps onto **region operations**: intersection (AND), union (OR), complement (NOT), with **volume / overlap** giving the match score.
- This makes [[Compositional Embeddings|compositionality]] a first-class, geometric operation rather than an approximation over averaged vectors.

## Findings

- On **single-attribute** queries, boxes and vectors perform comparably.
- On **compositional** queries, box embeddings show **substantial advantages over vectors**, and the gap **grows with retrieval-set size** — i.e. at the moderate-to-large result sets that matter for real browsing and recommendation.
- The paper contributes a **new benchmark dataset** for compositional queries to evaluate this.

*(Exact dataset name and numeric results are not reproduced here — they're in the paper body, not the abstract that was accessible.)*

## Why It Matters for Search

- Connects the box-embedding research line directly to **[[Faceted Search]]** / faceted browsing and **recommendation**, where AND/OR/NOT attribute filtering is the core interaction.
- Demonstrates a concrete failure mode of [[Dense Embeddings|dense point vectors]] (compositional filtering) and a principled fix.

## Related Concepts
- [[Box Embedding]] — the representation used (region/Venn-diagram)
- [[Set-Theoretic Embeddings]] — intersection/union/complement as query operators
- [[Compositional Embeddings]] — compositionality via set operations
- [[Compositional Queries]] — the query type this targets
- [[Faceted Search]] — the search/UX setting (AND/OR/NOT facets)
- [[Word2Box]] — the same author's word-level set-theoretic method

## Related Articles
- [[Express Words in a Box - Understanding Box Embedding from the Basics]] — [[Shun Tsukagoshi]]; the tutorial on the box-embedding lineage this paper extends

## People
- [[Shib Sankar Dasgupta]] — lead author (also Word2Box, Gumbel Box)
- [[Andrew McCallum]] — co-author (also Gaussian Embedding)
- [[Steffen Rendle]] — co-author (recommender systems / factorization)
- [[Li Zhang]] — co-author
