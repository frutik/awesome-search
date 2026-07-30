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
- **L2 normalization**: divide by the vector norm of the score set — steadier than min-max on noisy corpora

The choice of normalization significantly affects fusion quality.

**Min-max is only as stable as your extremes.** A single [[BM25]] outlier stretches the range and
flattens every other document toward zero, so the normalization is hostage to one score. L2 is the
steadier choice where the corpus produces occasional extreme lexical scores.

## The Combining Operator

The weighted sum is not the only option, and arithmetic addition has a specific weakness: a
document can win on one branch alone. **Geometric mean often behaves better**, because it requires
a document to score reasonably on *both* branches and pushes keyword-only matches toward zero.

Skipping normalization entirely — summing raw scores from two branches — is a real production
failure mode rather than a theoretical one: unbounded BM25 added to bounded cosine similarity lets
the lexical branch decide the ranking outright. See
[[Hybrid Fusion Failure - BM25 Displacing Reference Documents]].

## Tuning α

α is a hyperparameter typically tuned on a held-out validation set using an offline metric ([[NDCG]], [[MRR]]). Common starting point: α = 0.5 (equal weight). In practice:
- Higher α → more semantic signal (better for paraphrase/intent matching)
- Lower α → more lexical signal (better for exact term, product code, name queries)

Some systems learn α per query type using [[Search Intent]] classification. This is the principled
answer to the tradeoff a single global α creates — exact-term queries lean lexical, conceptual ones
lean semantic — but it costs a classifier you then have to maintain. If that classifier is an LLM
call, it adds latency to *every* request, which is worth budgeting before committing to routing.

## When to Use vs. RRF

- **Use RRF** when you can't normalize scores reliably or want a robust no-tuning baseline
- **Use Linear Combination** when scores are well-calibrated and you need fine-grained control over the semantic/lexical tradeoff

## Related Concepts

- [[Hybrid Search]] — the broader approach this is one implementation of
- [[Reciprocal Rank Fusion]] — the rank-based alternative
- [[Relative Score Fusion]] — closely related normalization-based fusion
- [[Hybrid Fusion Failure - BM25 Displacing Reference Documents]] — what happens when the normalization step is skipped
- [[BM25]] — typical sparse retriever input
- [[Dense Vector Retrieval]] — typical dense retriever input
- [[Search Evaluation]] — needed to tune α
