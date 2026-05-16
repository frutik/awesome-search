---
title: MAP (Mean Average Precision)
aliases:
  - MAP
  - Mean Average Precision
  - Average Precision
  - AP
tags:
  - concept
  - search-evaluation
  - metrics
---

# MAP (Mean Average Precision)

## Definition

MAP is a single-number summary of retrieval quality across a set of queries, averaging the **Average Precision (AP)** of each query. It captures both precision and the positions of relevant documents throughout the ranked list.

## Average Precision (AP)

For a single query with R total relevant documents:

```
AP = (1/R) × Σₖ P(k) × rel(k)
```

Where:
- `k` = rank position
- `P(k)` = precision at rank k (relevant docs in top-k / k)
- `rel(k)` = 1 if document at rank k is relevant, 0 otherwise
- Only positions where a relevant document appears contribute

This rewards finding relevant documents **early** in the ranking.

**Example**: 3 relevant docs in a corpus, found at ranks 1, 3, 5:
- P(1) = 1/1 = 1.0
- P(3) = 2/3 = 0.67
- P(5) = 3/5 = 0.60
- AP = (1.0 + 0.67 + 0.60) / 3 = **0.76**

If instead found at ranks 2, 4, 6:
- AP = (0.5 + 0.5 + 0.5) / 3 = **0.50**

## MAP

MAP is the mean of AP across all queries in a test set:

```
MAP = (1/Q) × Σ_q AP(q)
```

## MAP vs. NDCG

| Property | MAP | NDCG |
|----------|-----|------|
| Relevance | Binary (relevant/not) | Graded (0–4 scale) |
| Cutoff | Considers all ranks | Typically @k |
| Normalization | Normalizes by # relevant docs | Normalizes by ideal DCG |
| Sensitivity | More sensitive to later relevant docs | Emphasizes top positions more |

MAP is preferred when:
- Relevance is binary (a document is either relevant or not)
- All relevant documents matter (not just top-k)
- Datasets follow standard IR benchmark conventions (TREC)

NDCG is preferred when:
- Relevance is graded
- Top-k behavior matters most
- Comparing across queries with different relevant doc counts

## MAP@k

Often computed with a cutoff: MAP@10 or MAP@100, where AP is computed only over the first k positions. This is common in flight search, job search, and other domains where finding all relevant results matters.

## When to Use MAP

- **Multi-document retrieval**: when multiple relevant documents per query exist
- **Recall-oriented tasks**: patent retrieval, legal search, academic literature
- **IR benchmarks**: TREC, MS MARCO (though NDCG@10 is now more common)
- **Learning to Rank training**: MAP or a proxy (LambdaMAP) as the optimization target

## Related Concepts

- [[NDCG]] — graded-relevance alternative; more common in modern benchmarks
- [[MRR]] — simpler metric; only the first relevant result matters
- [[Precision and Recall]] — P@k and Recall@k; MAP extends average precision
- [[Search Evaluation]] — broader evaluation framework
- [[Judgment Lists]] — required input; binary labels sufficient for MAP
