---
title: "A/B Testing for Search"
aliases: ["A/B testing", "online experimentation", "search experimentation", "interleaving"]
tags:
  - concept
  - search
  - evaluation
created: 2026-05-15
---

# A/B Testing for Search

Online experimentation framework for measuring the real-world impact of ranking and retrieval changes on user behavior.

## Why It's Hard for Search

- **Low query volume** for tail queries — statistical power issues
- **Position bias** confounds click signal interpretation (see [[Position Bias]])
- **Session effects** — a change to one query affects satisfaction with the whole session
- **Novelty effects** — users react differently to new results just because they're different

## Core Methods

### Standard A/B
Random user split; measure click rate, dwell time, reformulation rate between control and treatment.

### Interleaving
Mix results from two rankers within a single SERP; infer preference from which system's results get more clicks. Far more statistically efficient than A/B.

### Quasi-Experiments
Use query or time-based splits when random user assignment isn't feasible.

## Key Metrics

- **CTR** (Click-Through Rate)
- **MRR** / **NDCG** on sampled queries — see [[MRR]], [[NDCG]]
- **Session abandonment rate**
- **Query reformulation rate** — proxy for dissatisfaction
- **Zero results rate** — see [[Zero Results]]

## Relationship to Offline Evaluation

- Offline evaluation ([[Search Evaluation]], [[Judgment Lists]]) is cheap and fast but doesn't capture real user behavior
- A/B testing is slow and expensive but captures actual impact
- Best practice: use offline eval to filter candidates, A/B to confirm winners

## Related Concepts

- [[Search Evaluation]]
- [[Click Signals]]
- [[Position Bias]]
- [[NDCG]]
- [[MRR]]
- [[Session-Based Evaluation]]
