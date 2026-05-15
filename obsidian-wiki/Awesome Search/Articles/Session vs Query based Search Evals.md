---
title: "Session vs Query Based Search Evals"
source: "https://softwaredoug.com/blog/2026/03/30/session-vs-query-based-search-evals"
author: ["Doug Turnbull"]
tags:
  - clippings
  - search-evaluation
  - session-evaluation
  - metrics
concepts:
  - Session-Based Evaluation
  - Search Evaluation
  - NDCG
created: 2026-05-15
---

# Session vs Query Based Search Evals

**Source**: https://softwaredoug.com/blog/2026/03/30/session-vs-query-based-search-evals  
**Author**: [[Doug Turnbull]]

## Summary

[[Doug Turnbull]] makes the case that query-based evaluation (the standard NDCG@k approach) is insufficient for modern search, and that session-based evaluation captures real user experience that query metrics miss.

## The Core Argument

Query-based evaluation treats every query as independent. But users don't search in isolation — they search in sessions with a goal:

```
Session: user wants to buy a "standing desk"
Query 1: "standing desk" → clicks result → reads page → returns to results
Query 2: "standing desk ergonomic" → clicks → buys → SUCCESS
```

Query-based evaluation says:
- Query 1: NDCG@10 = 0.75 (good)
- Query 2: NDCG@10 = 0.82 (good)

Session-based evaluation says:
- User needed to reformulate once to accomplish goal
- First query FAILED to serve the user's session goal

## What Query Metrics Miss

1. **Reformulation cost**: user had to type again = system failed
2. **Zero-click waste**: user got results but found none useful
3. **Session abandonment**: user gave up entirely
4. **Cross-query intent**: the meaning of query 2 is shaped by query 1

## Session Success Signals

[[Doug Turnbull]] identifies key session-level signals:
- **Terminal click + dwell**: user clicked, read, didn't come back = success
- **Zero reformulations**: single query → success = better UX
- **Session conversion**: reached purchase/goal = business success
- **Abandonment**: left without engaging = failure

## Practical Guidance

Turnbull doesn't advocate abandoning query-based metrics — rather, both are needed:

| Phase | Metric | Why |
|-------|--------|-----|
| Component testing | NDCG@10 | Reproducible, fast iteration |
| UX changes | Session success rate | Captures multi-query effects |
| Business reporting | Conversion, abandonment | Aligns with business outcomes |
| Pre-launch check | Both NDCG + session | Belt and suspenders |

## Relation to [[Agentic Search]]

[[Agentic Search]] systems are inherently session-based — the agent's multi-turn retrieval is one "session." This makes session-based thinking mandatory for evaluating agentic search.

## Related Articles

- [[Measuring Search Effectiveness]] — Tunkelang's complementary view
- [[Evaluating Search - Using Human Judgments]] — offline evaluation counterpart
- [[Flavors of NDCG]] — same author, deep-dive on NDCG

## Related Concepts

- [[Session-Based Evaluation]] — primary topic
- [[Search Evaluation]] — broader context
- [[NDCG]] — query-level complement
- [[Click Signals]] — session signals used
- [[Agentic Search]] — inherently session-based
