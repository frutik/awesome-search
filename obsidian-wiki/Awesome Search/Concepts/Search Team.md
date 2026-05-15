---
title: "Search Team"
aliases: ["search team", "search leadership", "search organization", "search PM", "managing search", "search engineering team"]
tags:
  - concept
  - search
  - team
  - leadership
---

# Search Team

## Definition

The organizational structure, roles, and operating principles for teams responsible for search quality and infrastructure. Effective search requires engineering, product, data science, UX, and business stakeholders — making search teams inherently cross-functional.

## Why Search Teams Are Different

Search quality is:
- **Multidimensional** — relevance, latency, diversity, personalization all matter simultaneously
- **Hard to measure** — no single metric captures "good search"
- **End-to-end** — indexing, query understanding, ranking, and UI all affect outcomes
- **Experiment-driven** — every change requires measurement, not intuition

## Core Roles

| Role | Responsibility |
|---|---|
| Search Engineer | Indexing, retrieval, query parsing, serving infrastructure |
| ML/Relevance Engineer | Ranking models, embeddings, LTR, evaluation |
| Search PM | Business alignment, metric definition, prioritization |
| Data Scientist | Evaluation design, A/B test analysis, metric frameworks |
| UX Researcher | User intent studies, qualitative signal |
| Relevance Annotator | [[Judgment Lists]] creation and maintenance |

## Four Principles (Tunkelang)

### 1. Combine Product and Engineering
Separate "search product" vs. "search engineering" orgs create friction. Best teams have hybrid roles or extremely tight collaboration — PMs need technical depth, engineers need product intuition.

### 2. Be Data-Driven
Define metrics before building features. Run [[A-B Testing for Search\|A/B tests]] for every significant change. Build offline [[Search Evaluation]] infrastructure early — it pays for itself.

### 3. Incremental Execution
Large changes have unpredictable cross-component interactions. Prefer "ship, measure, iterate" over big-bang rewrites.

### 4. Holistic Approach
Optimize the full system, not individual components:
- Indexing quality (freshness, coverage)
- [[Query Understanding]] (parsing, intent, segmentation)
- Ranking (model quality, feature relevance)
- UI/UX (result presentation, affordances)
- Feedback loops (signal collection quality)

## Anti-Patterns

- **Metric worship** — single metric optimization at the cost of overall quality
- **Infrastructure over impact** — elaborate systems before validating value
- **Relevance by anecdote** — acting on user complaints without data
- **Siloed evaluation** — per-component measurement without system-level testing

## For Understaffed Teams

Prioritize in this order:
1. **Evaluation first** — [[Judgment Lists]] before any model
2. **Rules before ML** — deterministic fixes often beat learned models on sparse data
3. **Quick iterations** — weekly improvements, not quarterly launches
4. **Automate regressions** — [[Search Evaluation]] harness to catch breaks

## Related Concepts

- [[Search Evaluation]] — measurement culture search teams need
- [[A-B Testing for Search]] — experiment infrastructure
- [[Judgment Lists]] — annotation as core team asset
- [[Search Architecture]] — what the team builds and maintains
- [[Learning to Rank]] — ML component of relevance work

## Articles

- [[Thoughts about Managing Search Teams]] — Tunkelang: 4 principles (combined org, data-driven, incremental, holistic)
- [[On Search Leadership]] — Tunkelang: evaluation culture, avoiding quality debt
- [[Search is a Team Sport]] — cross-functional accountability across engineering, PM, data science, UX
- [[Search Relevance for Understaffed Teams]] — Turnbull: practical guide for lean teams
- [[Search Product Management - The Most Misunderstood Role]] — everything in search is an experiment
