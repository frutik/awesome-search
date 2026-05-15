---
title: "Compute Mean Reciprocal Rank (MRR) using Pandas"
source: "https://softwaredoug.com/blog/2021/04/21/compute-mrr-using-pandas.html"
author:
  - "[[Doug Turnbull]]"
published: 2021-04-21
created: 2026-05-15
description: "How to compute Mean Reciprocal Rank using Pandas on the MSMarco QA dataset — concept, formula, and step-by-step implementation."
tags:
  - clippings
---
# Compute Mean Reciprocal Rank (MRR) using Pandas

MRR measures "how far down the ranking the first relevant document is." MRR → 1: relevant results cluster near the top. MRR → 0: poor quality.

Primarily applies when **one correct answer exists per query** — question-answering systems.

## Formula

Reciprocal Rank = 1 / rank_of_first_relevant_document

MRR = mean(Reciprocal Rank) across all queries

## Example

- "How far away is Mars?" → correct at rank 2 → RR = 0.5
- "Who is PM of Canada?" → correct at rank 3 → RR = 0.333

MRR = (0.5 + 0.333) / 2 = **0.417**

## Pandas implementation (MSMarco dataset)

```python
# 1. Load judgment data (query, doc_id, relevant)
# 2. Merge search results with judgments
# 3. Find minimum rank where relevant == 1 per query
min_rank = results.groupby('query_id')['rank'].min()
# 4. Compute reciprocal ranks
rr = 1 / min_rank
# 5. Mean across queries
mrr = rr.mean()
```


## Related Concepts

- [[MRR]]
- [[Search Evaluation]]
- [[Judgment Lists]]

## People

- [[Doug Turnbull]]
