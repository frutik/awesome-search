---
title: "Compute Mean Reciprocal Rank (MRR) using Pandas"
source: "https://softwaredoug.com/blog/2021/04/21/compute-mrr-using-pandas.html"
author: ["Doug Turnbull"]
tags:
  - clippings
  - search-evaluation
  - mrr
  - python
  - pandas
concepts:
  - MRR
  - Search Evaluation
  - Judgment Lists
created: 2026-05-15
---

# Compute Mean Reciprocal Rank (MRR) using Pandas

**Source**: https://softwaredoug.com/blog/2021/04/21/compute-mrr-using-pandas.html  
**Author**: [[Doug Turnbull]]

## Summary

A practical tutorial by [[Doug Turnbull]] showing how to compute [[MRR]] efficiently from search evaluation data using Pandas — useful for teams building their own lightweight evaluation tooling.

## The Data Model

Start with a DataFrame representing search results:
```python
import pandas as pd

# Each row = one result in a ranked list
results_df = pd.DataFrame({
    'query_id': ['q1', 'q1', 'q1', 'q2', 'q2'],
    'doc_id': ['d1', 'd2', 'd3', 'd1', 'd4'],
    'rank': [1, 2, 3, 1, 2],
    'relevant': [0, 1, 0, 1, 0]  # from judgment list
})
```

## Computing MRR

```python
def compute_mrr(results_df, k=10):
    # Filter to within cutoff k
    top_k = results_df[results_df['rank'] <= k]
    
    # For each query, find the rank of the first relevant result
    relevant = top_k[top_k['relevant'] == 1]
    first_relevant = relevant.groupby('query_id')['rank'].min()
    
    # Reciprocal rank for each query
    rr = 1.0 / first_relevant
    
    # Queries with no relevant result in top-k get RR=0
    all_queries = results_df['query_id'].unique()
    rr = rr.reindex(all_queries, fill_value=0.0)
    
    return rr.mean()

mrr = compute_mrr(results_df, k=10)
print(f"MRR@10: {mrr:.4f}")
```

## Comparing Two Systems

```python
system_a = pd.read_csv('system_a_results.csv')
system_b = pd.read_csv('system_b_results.csv')

mrr_a = compute_mrr(system_a)
mrr_b = compute_mrr(system_b)

print(f"System A MRR: {mrr_a:.4f}")
print(f"System B MRR: {mrr_b:.4f}")
print(f"Delta: {mrr_b - mrr_a:+.4f}")
```

## Statistical Significance

MRR differences need significance testing before claiming "improvement":

```python
from scipy.stats import wilcoxon

# Per-query reciprocal ranks for each system
rr_a = compute_per_query_rr(system_a)
rr_b = compute_per_query_rr(system_b)

stat, p_value = wilcoxon(rr_a, rr_b)
print(f"Wilcoxon test p-value: {p_value:.4f}")
print("Significant improvement!" if p_value < 0.05 else "Not significant")
```

## When Pandas Approach is Better than Quepid

- Custom analysis combining MRR with other signals (CTR, dwell)
- Large-scale batch evaluation (>100K results)
- Integration into CI/CD pipelines
- Scripted comparison between many system variants

Quepid (UI-based) is better for interactive exploration and team collaboration.

## Related Articles

- [[What Is a Judgment List]] — same author, setting up the judgment data
- [[Flavors of NDCG]] — same author, companion metric
- [[Session vs Query based Search Evals]] — same author, broader evaluation framework

## Related Concepts

- [[MRR]] — metric being computed
- [[Search Evaluation]] — context
- [[Judgment Lists]] — input data
- [[NDCG]] — companion metric

## People

- [[Doug Turnbull]] — author; Quepid creator
