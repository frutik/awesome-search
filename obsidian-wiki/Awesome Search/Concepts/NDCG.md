---
title: "NDCG (Normalized Discounted Cumulative Gain)"
aliases: ["nDCG", "normalized discounted cumulative gain", "DCG", "discounted cumulative gain"]
tags:
  - concept
  - search-evaluation
  - metrics
---

# NDCG (Normalized Discounted Cumulative Gain)

## Definition

NDCG is the most widely used ranking quality metric in information retrieval. It measures how well a ranked list puts the most relevant results at the top, accounting for the diminishing value of lower-ranked positions.

## Formula

**DCG (Discounted Cumulative Gain)**:
```
DCG@k = Σᵢ₌₁ᵏ  rel_i / log₂(i + 1)
```
where `rel_i` is the relevance score of the document at rank i.

**IDCG** (Ideal DCG): DCG of the perfect ranking.

**NDCG**:
```
NDCG@k = DCG@k / IDCG@k
```

Range: [0, 1]. NDCG@k = 1.0 means perfect ranking.

## Relevance Grades

NDCG supports graded relevance (unlike binary metrics):
| Grade | Meaning |
|-------|---------|
| 0 | Not relevant |
| 1 | Marginally relevant |
| 2 | Relevant |
| 3 | Highly relevant |
| 4 | Perfect match |

The logarithmic discount means position 1 is worth much more than position 10 — reflecting user behavior (users rarely scroll far).

## Variants: "Flavors of NDCG"

Confusion arises because there are multiple valid formulations:

### Variant 1: Standard (Jarvelin & Kekalainen)
```
DCG = rel₁ + Σᵢ₌₂ᵏ rel_i / log₂(i)
```

### Variant 2: Burges (Microsoft/LightGBM default)
```
DCG = Σᵢ₌₁ᵏ (2^rel_i - 1) / log₂(i + 1)
```
The `2^rel - 1` transform emphasizes high-relevance documents more strongly.

Both normalize to NDCG the same way; the IDCG changes accordingly. Be explicit about which variant you use when comparing systems.

## NDCG@k Choices

- **NDCG@3**: measures top-3, relevant for autocomplete/instant answers
- **NDCG@5**: common for web search (above the fold)
- **NDCG@10**: most common standard benchmark (MS MARCO, BEIR)
- **NDCG@100**: measures recall quality in first-stage retrieval

## Computing NDCG

```python
import numpy as np

def dcg_at_k(relevances, k):
    relevances = np.asarray(relevances[:k], dtype=float)
    n = len(relevances)
    if n == 0:
        return 0.0
    discounts = np.log2(np.arange(2, n + 2))
    return np.sum((2**relevances - 1) / discounts)

def ndcg_at_k(relevances, k):
    ideal = sorted(relevances, reverse=True)
    return dcg_at_k(relevances, k) / dcg_at_k(ideal, k) if dcg_at_k(ideal, k) > 0 else 0.0
```

## NDCG in Practice

NDCG requires **relevance judgments** ([[Judgment Lists]]) — human-rated (query, document) pairs. Creating judgments is expensive; sampling strategy matters enormously ([[Search Evaluation]]).

**Benchmark usage**: MS MARCO, TREC, BEIR benchmarks use NDCG@10 as primary metric for comparing retrieval systems. [[ELSER]] reports 17% NDCG@10 improvement over BM25; [[Matryoshka Embeddings]] compares at 99% NDCG relative to full-dimension embeddings.

## Related Concepts

- [[MRR]] — simpler ranking metric (binary relevance, first relevant result)
- [[Precision and Recall]] — non-ranking variants
- [[Judgment Lists]] — required input for NDCG computation
- [[Search Evaluation]] — broader evaluation framework
- [[LLM as Judge]] — automated relevance judgments

## People

- [[Daniel Tunkelang]] — frequent NDCG commentary; Evaluating Search series
- [[Doug Turnbull]] — "Flavors of NDCG" post; practical NDCG guidance
