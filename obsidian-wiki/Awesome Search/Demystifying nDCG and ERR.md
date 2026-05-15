---
title: "Demystifying nDCG and ERR"
source: "https://opensourceconnections.com/blog/2019/12/09/demystifying-ndcg-and-err/"
author:
  - "[[Max Irwin]]"
published: 2019-12-09
created: 2026-05-15
description: "Comparing nDCG and ERR through visualization — ERR's cascading user model better reflects real behavior, nDCG works well when grading is complete."
tags:
  - clippings
---
# Demystifying nDCG and ERR

Both metrics discount results by position and accumulate relevance scores — incentivizing relevant documents near the top.

## nDCG (Normalized Discounted Cumulative Gain)

- Normalizes with ideal document ranking → 0–1 scale
- Assigns perfect 1.0 when results are sorted by relevance
- No explicit maximum grade specification required
- **Weakness**: frequently returns perfect 1.0 scores, masking room for improvement

## ERR (Expected Reciprocal Rank)

Introduced ~2009 (a decade after nDCG). Key innovations:

- Requires **explicit declaration of maximum grade values**
- Uses a **cascading model**: reflects user satisfaction behavior — satisfied users stop scanning
- Penalizes queries that fail to satisfy users quickly
- **Never reaches perfect scores** — always implies improvement is possible
- Significant score drops when the first result lacks perfect relevance (reflects real user frustration)

## Recommendation

- **ERR** for most applications — better aligned with actual user behavior
- **nDCG** when comprehensive grading is complete and high baseline scores are acceptable

Both support custom discount functions to adapt to specific use cases (prioritize top-result quality vs. exploratory search).


## Related Concepts

- [[NDCG]]
- [[Search Evaluation]]
- [[Judgment Lists]]
- [[Position Bias]]

## People

- [[Max Irwin]]
