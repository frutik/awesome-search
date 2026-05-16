---
title: "Linear Score Combination"
aliases: ["linear combination", "score combination", "weighted score fusion", "convex combination", "alpha blending", "score-based fusion"]
tags:
  - concept
  - search
  - hybrid-search
  - ranking
created: 2026-05-16
---

# Linear Score Combination

## Definition

Linear Score Combination is a hybrid search fusion method that merges ranked lists from multiple retrieval systems by computing a weighted sum of their normalized scores:

```
score(d) = α · score_dense(d) + (1 - α) · score_sparse(d)
```

Where α ∈ [0, 1] controls the balance between dense (semantic) and sparse (lexical) signals.

## Contrast with RRF

| | [[Reciprocal Rank Fusion]] | Linear Score Combination |
|---|---|---|
| Input | Ranks only | Raw scores |
| Score calibration needed | No | Yes — scores must be normalized |
| Sensitive to score magnitude | No | Yes |
| Tunable weight | No (k parameter only) | Yes (α per retriever) |
| Robustness | High — works out of the box | Lower — requires careful normalization |
| Performance ceiling | Good | Can be higher if scores are well-calibrated |

## Score Normalization

Raw scores from different systems are not comparable. Common normalization strategies before combining:

- **Min-max normalization**: `(score - min) / (max - min)` — maps to [0, 1] but sensitive to outliers
- **Z-score**: `(score - mean) / std` — normalizes distribution shape
- **Softmax**: turns scores into probabilities — preserves relative ordering

The choice of normalization significantly affects fusion quality.

## Tuning α

α is a hyperparameter typically tuned on a held-out validation set using an offline metric ([[NDCG]], [[MRR]]). Common starting point: α = 0.5 (equal weight). In practice:
- Higher α → more semantic signal (better for paraphrase/intent matching)
- Lower α → more lexical signal (better for exact term, product code, name queries)

Some systems learn α per query type using [[Search Intent]] classification.

## When to Use vs. RRF

- **Use RRF** when you can't normalize scores reliably or want a robust no-tuning baseline
- **Use Linear Combination** when scores are well-calibrated and you need fine-grained control over the semantic/lexical tradeoff

## Related Concepts

- [[Hybrid Search]] — the broader approach this is one implementation of
- [[Reciprocal Rank Fusion]] — the rank-based alternative
- [[BM25]] — typical sparse retriever input
- [[Dense Vector Retrieval]] — typical dense retriever input
- [[Search Evaluation]] — needed to tune α
