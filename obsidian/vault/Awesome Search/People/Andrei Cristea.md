---
type: person
title: "Andrei Cristea"
affiliation: "[[Qdrant]]"
tags:
  - person
  - hybrid-search
  - query-routing
  - qdrant
created: 2026-09-26
---

# Andrei Cristea

Developer relations engineer at [[Qdrant]]. Presented a hybrid-routing project at [[Haystack EU]]: rather than fusing sparse and dense results with [[Reciprocal Rank Fusion]] on every query, a lightweight classifier trained on ~230,000 labelled queries decides per query whether to send it to the sparse retriever, the dense retriever, or RRF — beating hybrid RRF on relevance, hit@1 and NDCG on held-out data.

## Talks & Videos
- [[Andrei Cristea - Qdrant Vector Search and Hybrid Routing]] — [[Haystack EU]] lightning talk

## Related Concepts
- [[Query Routing]]
- [[Hybrid Search]]
- [[Reciprocal Rank Fusion]]
- [[Query Classification]]

## Colleagues
- [[Dylan Couzon]] — Qdrant's hybrid search tuning guide (RRF vs DBSF)
- [[Evgeniya Sukhodolskaya]]
