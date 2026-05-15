---
title: "Precision and Recall"
aliases: ["precision", "recall", "P@k", "Precision at K", "F1"]
tags:
  - concept
  - search-evaluation
  - metrics
---

# Precision and Recall

## Definition

**Precision**: Of the documents retrieved, what fraction are relevant?  
**Recall**: Of all relevant documents, what fraction were retrieved?

```
Precision = |Retrieved ∩ Relevant| / |Retrieved|
Recall    = |Retrieved ∩ Relevant| / |Relevant|
```

## The Precision-Recall Tradeoff

Precision and recall are in tension:
- **Higher recall**: retrieve more documents → more relevant ones found, but also more irrelevant ones → lower precision
- **Higher precision**: be selective → top results are relevant, but some relevant docs missed → lower recall

This is the fundamental tradeoff in information retrieval. There is no "best" point — the optimal depends on the use case.

## Precision@k (P@k)

Instead of measuring over the full ranked list, measure precision at a cutoff:

```
P@k = (relevant documents in top k) / k
```

Examples:
- P@1: is the first result relevant? (Click-satisfaction proxy)
- P@5: are most of the first page relevant?
- P@10: standard IR evaluation cutoff

Unlike [[NDCG]], P@k ignores document ranking within the cutoff — all positions within k are equally weighted.

## Recall@k

Fraction of relevant documents found in top k:
```
Recall@k = (relevant documents in top k) / |all relevant documents|
```

High Recall@1000 is the target for first-stage retrieval in [[Retrieval Pipeline]]:
- First stage needs to recall nearly all relevant docs
- Second stage ([[Cross-Encoder]] reranker) handles ranking quality
- Missing a relevant doc at stage 1 = permanent recall loss

## F1 Score

Harmonic mean of precision and recall:
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

F1 treats precision and recall equally. Use when both matter and you want a single number.

## When to Use Each Metric

| Metric | Best for |
|--------|---------|
| P@1 | First result quality (navigational queries) |
| P@5 | Above-the-fold quality |
| P@10 | Standard page quality |
| Recall@1000 | First-stage retrieval coverage |
| [[NDCG]]@10 | Overall ranking quality with graded relevance |
| [[MRR]] | Known-item / QA systems |
| F1 | Classification tasks, information extraction |

## Precision vs. NDCG

P@k treats all positions equally within k — a relevant document at rank 1 = rank k.  
[[NDCG]] discounts lower ranks — a relevant document at rank 1 is worth more than at rank k.

NDCG is generally preferred for ranked retrieval evaluation.

## Related Concepts

- [[NDCG]] — more nuanced ranking metric
- [[MRR]] — position-aware precision for first relevant document
- [[Search Evaluation]] — how these feed into evaluation
- [[Judgment Lists]] — relevance labels needed
- [[Retrieval Pipeline]] — Recall@1000 critical for first stage

## People

- [[Daniel Tunkelang]] — precision/recall in search quality discussions
- [[Doug Turnbull]] — practical P@k and Recall@k usage
