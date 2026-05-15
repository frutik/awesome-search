---
title: "Flavors of NDCG - normalized to what!?"
source: "https://softwaredoug.com/blog/2024/05/22/flavors-of-ndcg"
author:
  - "[[Doug Turnbull]]"
published: 2024-05-22
created: 2026-05-15
description: "Four NDCG normalization variants — local, recall, global, max — and how the choice fundamentally shapes what your metric optimizes for."
tags:
  - clippings
---
# Flavors of NDCG - normalized to what!?

NDCG measures how well search results perform against labeled relevant documents, discounting by rank position. But "normalized to what" has four distinct answers — each answering a different question.

## The four variants

### NDCG-local
Normalizes against ideal DCG from only the **top N retrieved results**, sorted optimally. Focuses purely on **ranking quality** — "given what we returned, did we order it well?"

### NDCG-recall
Extends the ideal window to a larger **recall set** (top K documents) before computing ideal ordering. Middle ground between local and global.

### NDCG-global
"Our ideal is computed from the labels for a query — whether or not they were retrieved." Blends **recall and ranking** into one metric. May mask whether improvements come from better ranking or broader recall.

### NDCG-max
Assumes maximum possible labels in all positions. Measures the entire system's ability to provide relevant content overall.

## Practical implications

| Variant | Answers | Risk |
|---|---|---|
| Local | "Did we rank well?" | Ignores what wasn't retrieved |
| Recall | Hybrid ranking + coverage | Middle ground, less clear |
| Global | "Overall performance?" | Conflates ranking and recall improvements |
| Max | "How good is our catalog coverage?" | Very sensitive to label quality |

Choosing the wrong variant can mislead optimization efforts if misaligned with actual business goals.


## Related Concepts

- [[NDCG]]
- [[Search Evaluation]]
- [[Judgment Lists]]
- [[Precision and Recall]]

## People

- [[Doug Turnbull]]
