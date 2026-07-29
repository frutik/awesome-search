---
type: person
title: "Evgeniya Sukhodolskaya"
aliases: ["Jenny Sukhodolskaya"]
role: Senior Developer Advocate
affiliation: "[[Qdrant]]"
tags:
  - person
  - sparse-retrieval
  - developer-advocacy
created: 2026-07-27
---

# Evgeniya Sukhodolskaya

Senior Developer Advocate at [[Qdrant]], based in Munich. Works on [[Learned Sparse Retrieval]] — she authored Qdrant's [[miniCOIL]] work and describes sparse neural retrieval as a personal research interest: *"I really love sparse neural retrieval."* Co-hosts a search meetup in Munich and speaks at community conferences including [[MICES]] and [[Berlin Buzzwords]].

She also authored Qdrant's index-native [[Relevance Feedback]] work — a survey of the feedback literature followed by a mechanism that carries feedback into [[HNSW]] traversal, shipped in Qdrant 1.17.

Her recurring argument is accessibility: that sparse neural retrieval, model fine-tuning and relevance tuning are treated as ML-specialist territory when practitioners could be using them, and that tooling should close that gap. A second, related theme is that search engines shouldn't be black boxes you build *around* — *"search engines are here just to serve you a useful tooling and adapt to your needs and adapt to your users, be they humans or agents."*

## Talks in this vault

- [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] — [[MICES]] 2026; walks from sparse vectors to a working [[SPLADE]] fine-tuning framework
- [[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]] — [[Berlin Buzzwords]] 2026; relevance feedback propagated into the [[HNSW]] hop-selection function

## Articles in this vault

- [[Relevance Feedback in Informational Retrieval]] (2025) — survey of the feedback literature; the two-axis taxonomy and the research/production gap
- [[Relevance Feedback in Qdrant]] (2026) — the follow-through: formula, training procedure, [[BEIR]] results

## Topics

- [[Learned Sparse Retrieval]] · [[Sparse Embeddings]] · [[SPLADE]] · [[miniCOIL]]
- [[Relevance Feedback]] · [[HNSW]] · [[Knowledge Distillation]] — the index-native feedback line of work
- [[E-commerce Search]] — intent-heavy retrieval as the motivating domain

## Related

- [[Qdrant]] — employer
- [[Thierry Damiba]] — Qdrant colleague; she presented his fine-tuning experiments ([[Fine-Tuning Sparse Embeddings for E-Commerce Search]])
- [[miniCOIL]] — her sparse retriever with BM25 fallback for out-of-vocabulary terms
- [[qdrant-relevance-feedback]] — the parameter-fitting package behind the relevance feedback query
