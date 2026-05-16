---
title: "Cross-Encoders, ColBERT, and LLM-Based Re-Rankers: A Practical Guide"
tags:
  - clippings
  - search
  - ranking
  - reranking
source: "https://medium.com/@aimichael/cross-encoders-colbert-and-llm-based-re-rankers-a-practical-guide-a23570d88548"
author: "Michael Ryaboy"
created: 2026-05-15
concepts:
  - Cross-Encoder
  - ColBERT
  - Learning to Rank
  - Retrieval Pipeline
---

# Cross-Encoders, ColBERT, and LLM-Based Re-Rankers

**Source:** https://medium.com/@aimichael/cross-encoders-colbert-and-llm-based-re-rankers-a-practical-guide-a23570d88548
**Author:** [[Michael Ryaboy]] (Developer Advocate, KDB.AI)

## Summary

Practical comparison of three reranking approaches for production search systems, with guidance on when to use each.

## The Three Approaches

### Cross-Encoders
- Process query-document pairs jointly through transformer
- State-of-the-art accuracy (MRR@10 > 40 on MS MARCO)
- Each document requires a full forward pass → high latency, high GPU cost
- **Use when**: high-stakes queries, small result sets, quality > speed

### [[ColBERT]] (Late Interaction)
- Pre-compute token-level document embeddings offline
- Query-time: compute query token embeddings, then MaxSim vs. stored document tokens
- Middle ground: more nuanced than vector similarity, cheaper than cross-encoder
- Storage: can reach **tens of gigabytes** for large catalogs
- **Use when**: large-scale reranking where cross-encoder latency is prohibitive

### LLM-Based Re-Rankers
- Apply flexible, dynamic criteria (freshness, authority, custom logic) without retraining
- Individual requests: "might cost a few cents and add over a second of latency"
- **Use when**: rare high-value queries, or criteria that change frequently

## Layered Pipeline Strategy

```
BM25 / vector retrieval (thousands)
    ↓
ColBERT refinement (hundreds)
    ↓
Cross-encoder or LLM polishing (top 20-50)
```

## Success Metrics

MRR, [[NDCG]], precision@5, user conversion rates, support ticket reduction

## Related Concepts

- [[Cross-Encoder]]
- [[ColBERT]]
- [[Late Interaction]]
- [[Retrieval Pipeline]]
- [[Multi-Stage Ranking]]
- [[NDCG]]

## Related Articles

- [[Multi-Stage Ranking]]
- [[What is ColBERT and Late Interaction and Why They Matter in Search]]
- [[Bi-encoder vs Cross-encoder When to Use Which One]]
