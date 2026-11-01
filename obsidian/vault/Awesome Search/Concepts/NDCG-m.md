---
type: concept
title: "NDCG-m"
aliases: ["Max NDCG", "NDCG-max"]
tags:
  - concept
  - search-evaluation
  - metrics
created: 2026-10-30
---

# NDCG-m

**NDCG-m** (Max NDCG) is a variant of [[NDCG]] that normalises against a fixed ideal in which every result slot holds the maximum grade, instead of the best ordering the corpus can actually supply. It is named in honor of [[Max Irwin]], who argued for this definition, in [[Search golden sets are anything but]].

---

## Why It Exists

Standard NDCG divides by the DCG of the best achievable ordering for that query. When a query has only a few relevant documents in the corpus, a system that returns all of them can score 1 even though most of the result list is poor and users are unhappy. A fixed all-max-grade ideal makes the score reflect corpus coverage as well as ranking quality.

## Reading It

- The best any system can score is below 1 whenever the corpus lacks enough top-graded results; the ceiling itself is informative.
- The post reports an average NDCG-m@10 of about 0.77 for [[WANDS Dataset|WANDS]] and closer to 0.93 for [[Amazon ESCI Dataset|ESCI]], suggesting WANDS contains more queries with few relevant results.
- It is complemented by [[NDCG-f]], which scores only labeled results.

## Related Concepts
- [[NDCG]] · [[NDCG-f]] · [[Judgment Lists]] · [[Search Evaluation]]

## Related Articles
- [[Search golden sets are anything but]]

## People
- [[Max Irwin]] · [[Doug Turnbull]]
