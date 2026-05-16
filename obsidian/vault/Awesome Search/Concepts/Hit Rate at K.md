---
title: "Hit Rate@K"
aliases: ["Hit Rate", "Hit Rate@K", "HR@K", "accuracy at K", "at K", "at@K"]
tags:
  - concept
  - search-evaluation
  - metrics
---

# Hit Rate@K

## Definition

**Hit Rate@K** (HR@K) measures whether **at least one relevant document appears in the top K results** for a given query. It is a binary, per-query metric.

```
Hit(query) = 1  if any relevant doc is in top K results
           = 0  otherwise

HR@K = mean(Hit) across all queries
```

Unlike [[NDCG]] or [[MRR]] (which reward ranking relevant docs higher), Hit Rate@K only asks: *"did we find anything useful at all?"*

## When to Use

| Scenario | Why HR@K fits |
|---|---|
| RAG / question answering | Retriever must surface at least one answer passage |
| Recommendation systems | At least one good recommendation above the fold |
| Autocomplete | At least one correct suggestion in top K |
| Retrieval health check | Fast sanity check — HR@10 < 0.7 = retrieval is broken |

HR@K is especially common in **RAG evaluation**: if the retriever misses all K candidates, the LLM has no chance of answering correctly.

## Hit Rate vs. Other Metrics

| Metric | Question | Granularity |
|---|---|---|
| **HR@K** | Was anything relevant found? | Binary per query |
| [[Precision and Recall\|P@K]] | What fraction of top K are relevant? | Continuous per query |
| [[MRR]] | How far down is the *first* relevant doc? | Position-aware |
| [[NDCG]]@K | How well are relevant docs ranked overall? | Graded + position-aware |

HR@K is the weakest signal (binary, no position info) but the fastest diagnostic.

## Typical Thresholds

| HR@K | Interpretation |
|---|---|
| > 0.90 | Healthy retrieval; ranking is the bottleneck |
| 0.70–0.90 | Retrieval gaps on tail queries |
| < 0.70 | Retrieval is broken or index coverage poor |

## HR@K vs. MRR

Both are per-query binary in spirit, but differ in reward:
- **HR@K**: cares only that *something* relevant landed in top K
- **MRR**: rewards finding that relevant doc *as early as possible*

A system with high HR@10 but low MRR is retrieving relevant docs but burying them at ranks 8–10.

## Related Concepts

- [[MRR]] — position-aware companion metric
- [[NDCG]] — graded ranking quality
- [[Precision and Recall]] — P@K and Recall@K family
- [[Search Evaluation]] — evaluation framework context
- [[RAG]] — primary use case for HR@K in modern systems
- [[Retrieval Pipeline]] — first-stage recall where HR matters most

## Articles

- [[Maximal Marginal Relevance (MMR) - How to Calculate]] — covers Hit Rate alongside MRR and MMR
