---
title: "Measuring Search: Metrics Matter"
source: "https://jamesrubinstein.medium.com/measuring-search-metrics-matter-de124c2f6f8c"
author: ["James Rubinstein"]
tags:
  - clippings
  - search-evaluation
  - metrics
  - ndcg
  - mrr
concepts:
  - Search Evaluation
  - NDCG
  - MRR
  - Precision and Recall
  - Click Signals
created: 2026-05-15
---

# Measuring Search: Metrics Matter

**Source**: https://jamesrubinstein.medium.com/measuring-search-metrics-matter-de124c2f6f8c  
**Author**: [[James Rubinstein]]

## Summary

Part of [[James Rubinstein]]'s "Measuring Search" series. Explains the major search evaluation metrics, when to use each, and the traps practitioners fall into when relying on a single metric.

## The Metrics Landscape

### Offline Ranking Metrics

**[[NDCG]]** — The standard. Use when:
- You have graded relevance (0–4 scale)
- You care about position (higher = more important)
- You're comparing ranking algorithms

**[[MRR]]** — Simpler. Use when:
- There's exactly one correct answer
- Question-answering systems
- Binary relevance is sufficient

**[[Precision and Recall]]@k** — Fundamental. Use when:
- Understanding precision/recall tradeoff
- Quick sanity checks

### Online Behavioral Metrics

**CTR (Click-Through Rate)**:
- Easy to collect, always available
- Biased by position, presentation, novelty
- Can game: provocative titles get clicks without satisfying users

**Dwell time**:
- Better satisfaction proxy than click alone
- "Bounce rate" (return < 30s) = pogo-sticking = dissatisfied

**Session abandonment**:
- User left without successful outcome
- Powerful signal if you can define "successful"

**Zero-result rate**:
- Queries with no results = certain failure
- Easy to measure, high signal for recall gaps

## Metric Traps

### The Single Metric Trap
Optimizing a single metric eventually breaks something else:
- Optimize CTR → clickbait titles → user dissatisfaction
- Optimize NDCG → overfit to judgment set → production regression
- Optimize zero-result rate → return everything → precision collapses

### The Proxy Trap
Confusing the proxy with the goal:
- CTR is a proxy for satisfaction
- NDCG is a proxy for CTR is a proxy for satisfaction
- Optimize the proxy ≠ optimize the goal

### The Freshness Trap
Judgment lists go stale. A metric of 0.83 on a 2-year-old judgment set may not reflect current system quality.

## Rubinstein's Measurement Hierarchy

1. **User outcome** (task success, satisfaction survey)
2. **Behavioral proxy** (CTR, dwell, conversion)
3. **Offline rating** ([[NDCG]], [[MRR]] on fresh judgments)

Each level is faster/cheaper than the one above, and less reliable. Use all three; don't replace upper levels with lower.

## Related Articles

- [[Measuring Search Effectiveness]] — Tunkelang's parallel framework
- [[Measuring Search - A Human Approach]] — same author, human judgment focus
- [[Flavors of NDCG]] — Doug Turnbull, NDCG implementation details

## Related Concepts

- [[Search Evaluation]] — broader context
- [[NDCG]] — primary offline metric
- [[MRR]] — simpler offline metric
- [[Precision and Recall]] — foundational
- [[Click Signals]] — behavioral proxies
- [[Judgment Lists]] — required for offline metrics

## People

- [[James Rubinstein]] — author
- [[Daniel Tunkelang]] — parallel measurement work
