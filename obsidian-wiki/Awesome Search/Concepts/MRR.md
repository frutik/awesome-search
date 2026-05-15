---
title: "MRR (Mean Reciprocal Rank)"
aliases: ["mean reciprocal rank", "reciprocal rank", "MRR@k"]
tags:
  - concept
  - search-evaluation
  - metrics
---

# MRR (Mean Reciprocal Rank)

## Definition

MRR measures the quality of a ranked list based on the position of the **first** relevant result. It is simpler than [[NDCG]] and appropriate when there is exactly one correct answer.

## Formula

For a set of queries Q:
```
MRR = (1/|Q|) × Σ_q  1 / rank_q
```
where `rank_q` is the position of the first relevant result for query q.

**Example**:
- Query 1: first relevant at rank 1 → 1/1 = 1.0
- Query 2: first relevant at rank 3 → 1/3 = 0.33
- Query 3: no relevant result → 1/∞ = 0
- MRR = (1.0 + 0.33 + 0) / 3 = 0.44

## When to Use MRR

Best for:
- **Question answering**: one correct answer exists
- **Known-item search**: user knows exactly what they want
- **Informational queries with a single definitive source**

Not ideal for:
- **Multi-document retrieval**: multiple relevant docs (use [[NDCG]])
- **E-commerce search**: many acceptable products (use [[NDCG]] or Precision@k)
- **Exploratory search**: no single "correct" answer

## MRR vs. NDCG

| Aspect | MRR | NDCG |
|--------|-----|------|
| Relevance | Binary (relevant/not) | Graded (0–4) |
| Documents counted | First relevant only | All top-k |
| Position sensitivity | High (first position premium) | Logarithmic discount |
| Complexity | Simple | Complex |
| Best for | QA, known-item | Ranked retrieval generally |

## Computing MRR

```python
def mrr_at_k(ranked_results, relevant_docs, k=10):
    for rank, doc in enumerate(ranked_results[:k], 1):
        if doc in relevant_docs:
            return 1.0 / rank
    return 0.0

def mean_mrr(queries_results, queries_relevant, k=10):
    return sum(mrr_at_k(r, rel, k) 
               for r, rel in zip(queries_results, queries_relevant)) / len(queries_results)
```

Pandas implementation (faster for large sets):
```python
import pandas as pd

def compute_mrr_pandas(df):
    # df has columns: query_id, doc_id, rank, relevant
    relevant = df[df['relevant'] == 1]
    first_relevant = relevant.groupby('query_id')['rank'].min()
    return (1 / first_relevant).mean()
```

## MRR@k

MRR@k only counts a result if the first relevant doc appears within the top k positions:
- MRR@3: first relevant must be in top 3
- MRR@10: standard in most benchmarks

## Related Concepts

- [[NDCG]] — more comprehensive ranking metric
- [[Precision and Recall]] — related evaluation measures
- [[Search Evaluation]] — broader evaluation framework
- [[Judgment Lists]] — relevance labels needed for MRR

## People

- [[Doug Turnbull]] — "Compute MRR using Pandas" tutorial
- [[Daniel Tunkelang]] — MRR in context of search evaluation
