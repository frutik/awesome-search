---
title: "Session-Based Evaluation"
aliases: ["session evaluation", "multi-turn evaluation", "search session metrics"]
tags:
  - concept
  - search-evaluation
  - sessions
---

# Session-Based Evaluation

## Definition

Session-based evaluation measures search quality at the level of a complete user session — a sequence of queries, clicks, reformulations, and final actions — rather than evaluating each query in isolation.

## Motivation: Query-Based Evaluation Misses Context

Standard query-based [[Search Evaluation]] treats each query independently:
```
"iphone case" → NDCG@10 = 0.72  ✓
"iphone 15 case" → NDCG@10 = 0.81  ✓
```

But these queries may be from the same user who couldn't find what they wanted and reformulated. Query-based evaluation says "both queries performed well" while the user experience was poor (they had to reformulate).

Session-based evaluation captures this failure:
```
Session: "iphone case" → no click → "iphone 15 case" → no click → "buy iphone case amazon" → exit site
Session outcome: FAILURE (user abandoned to competitor)
```

## Session Signals

| Signal | Positive | Negative |
|--------|----------|---------|
| Query reformulation | None (neutral at best) | Multiple reformulations = friction |
| Click | Click occurred | No clicks = zero-click failure |
| Dwell time | Long dwell = satisfaction | Short dwell after click = poor result |
| Session depth | N/A | Deep scrolling = can't find what they want |
| Session outcome | Conversion/success | Abandonment |
| Return to results | N/A | Pogosticking = dissatisfied with result |

## Session Success Metrics

### Task Completion Rate
Binary: did the user accomplish their goal within the session?
Requires conversion event (purchase, form submit, page visit) or human judgment.

### Abandonment Rate
Percentage of sessions with no positive engagement (no click, no conversion).

### Reformulation Rate
Number of query modifications per session. High = system failed first interpretation.

### Click Residual
[[Click Signals#Click Residual]]: clicks that "should" have happened but didn't.

## Session-Based vs. Query-Based: When to Use Each

| Scenario | Recommended |
|----------|-------------|
| Ranking algorithm A/B test | Query-based (NDCG) |
| Search UX change | Session-based |
| Measuring user satisfaction | Session-based |
| Component evaluation (retrieval quality) | Query-based |
| Conversational search quality | Session-based (required) |
| E-commerce search business impact | Both |

## Relation to [[Agentic Search]]

[[Agentic Search]] is inherently session-based — the agent's multi-turn retrieval is a session. Evaluating an agentic search system requires session-level metrics:
- Was the final answer correct?
- How many retrieval turns were needed?
- Was the retrieval cost within budget?

Query-level [[NDCG]] doesn't apply to agentic search.

## Related Concepts

- [[Search Evaluation]] — broader context
- [[NDCG]] — query-level complement
- [[Click Signals]] — session behavioral signals
- [[Diversity Metrics]] — session-level diversity matters
- [[Agentic Search]] — inherently session-based

## People

- [[Doug Turnbull]] — "Session vs Query based search evals"
- [[Daniel Tunkelang]] — query vs session evaluation tradeoffs
