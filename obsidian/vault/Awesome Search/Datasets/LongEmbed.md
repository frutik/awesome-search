---
type: dataset
title: "LongEmbed"
tags: [dataset, long-documents, retrieval, benchmark]
related_concepts:
  - "[[Reranking]]"
  - "[[Text Chunking]]"
created: 2026-10-11
---

# LongEmbed

A long-document retrieval benchmark. In Voyage's reranker evaluation it consists of three subsets: **NarrativeQA**, **SummScreenFD** and **QMSum**.

---

## Use in This Vault

[[rerank-3 and rerank-3-lite - the next generation of Voyage rerankers]] uses it as the long-document domain for 32K-context rerankers. There, [[Voyage rerank-3]] led rerank-2.5 by 3.35% NDCG@10 and [[Cohere]] Rerank v4.0 Pro by 13.84%. The gains came from NarrativeQA and QMSum. Every Voyage reranker scored above 99% on SummScreenFD, so that subset has stopped discriminating between models at the top. An average over the three subsets hides this.

## Related Concepts

- [[Reranking]] · [[Text Chunking]] — long documents are what chunking otherwise avoids

## Related Articles

- [[rerank-3 and rerank-3-lite - the next generation of Voyage rerankers]]
