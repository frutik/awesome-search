---
type: concept
title: "NDCG-f"
aliases: ["Filtered NDCG", "NDCG over labeled results"]
tags:
  - concept
  - search-evaluation
  - metrics
created: 2026-10-30
---

# NDCG-f

**NDCG-f** (filtered NDCG) computes [[NDCG]] after dropping every unlabeled result, so only documents with a judgment in the [[Judgment Lists|judgment list]] count. It is described in [[Search golden sets are anything but]].

---

## Why It Exists

Judgment lists are rarely complete, and labeling often covers only the current top results of the current ranking algorithm (the post's example is raters labeling the top 10 of [[BM25]]). Treating unlabeled results as irrelevant therefore penalises a system for surfacing documents nobody has judged, many of which are in fact relevant.

## What It Answers

NDCG-f asks a narrow question: does the system order known-relevant results above known-irrelevant ones? That makes it useful as a regression check, in the way a unit test is. It does not predict which variant wins an A/B test, since what the unlabeled results look like is exactly what it ignores.

## Related Concepts
- [[NDCG]] · [[NDCG-m]] · [[Judgment Lists]] · [[Search Evaluation]]

## Related Articles
- [[Search golden sets are anything but]]

## People
- [[Doug Turnbull]]
