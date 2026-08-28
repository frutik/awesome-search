---
type: company
title: "RelativeDB"
industry: search infrastructure
website: "https://relativedb.com"
category: technology-provider
search_domain: relational-data-conditioned reranking for e-commerce/enterprise search
tags:
  - company
  - reranking
  - relational-deep-learning
created: 2026-08-28
---

# RelativeDB

Company publishing research on conditioning search reranking directly on relational/structured data rather than treating candidates as text. Its research post introduces [[Relational Transformer|RT]], an 85M-parameter [[Relational Transformer]], and releases a pretrained checkpoint (`stanford-star/rt-j`) as open code. Site sections observed: Research, Cloud, and a public code repository link, suggesting a hosted product alongside the research output — not confirmed beyond what the article states.

## Research Contributions

- [[Relational Transformer]] (RT) — 85M-parameter reranker conditioning on typed "Cell" facts (`name, type, value`) and schema relationships between database rows, rather than serializing candidates to text
- LLM-based query parsing that converts free-text queries into structured Cells before reranking, reported to substantially improve RT's accuracy over unparsed text input

## Articles

- [[Relational Reranking - Scoring Search Results with Structured Facts]] — [[Daniel Henneberger]]; introduces RT, its Cell representation, ablations, and benchmark results on MTEB DeepPlanning and [[STaRK]]

## People

- [[Daniel Henneberger]] — author of the RT research post

## Concepts

[[Relational Transformer]] · [[Reranking]]

## Datasets

[[RelBench]] · [[STaRK]]
