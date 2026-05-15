---
title: "The Launch Review: Bringing It All Together"
tags:
  - clippings
  - search
  - search-team
  - process
  - evaluation
source: "https://jamesrubinstein.medium.com/the-launch-review-bringing-it-all-together-2f7e4cfbf86e"
author: "James Rubinstein"
created: 2026-05-15
concepts:
  - Search Evaluation
  - A-B Testing for Search
---

# The Launch Review: Bringing It All Together

**Source:** https://jamesrubinstein.medium.com/the-launch-review-bringing-it-all-together-2f7e4cfbf86e
**Author:** [[James Rubinstein]]

## Summary

The Launch Review is the decision-making meeting that determines whether to ship a search algorithm change. It synthesizes metrics, human evaluation, and business context into a go/no-go decision.

## The Process

### 1. Launch Review Document
Prepared in advance, contains:
- Problem statement and experimental change description
- Early explorations and technical considerations
- Fixed hypothesis and success criteria (established **before** testing)
- Human Relevance Evaluation results — see [[Judgment Lists]]
- A/B test results — see [[A-B Testing for Search]]
- User feedback and survey responses

### 2. Cross-Functional Meeting
Attendees: PM, data science, engineering, experiment owner.

### 3. Decision Options
- **Ship** — deploy to all users
- **Don't ship** — revert
- **Continue collecting data** — test was inconclusive
- **Conditional launch** — ship with guardrails (segment-specific, gradual rollout)

## Key Principle

> "Data informed but not necessarily data-driven"

Mixed results require nuanced judgment — an improvement for established users that harms new users may or may not be worth shipping depending on business context.

## Related Concepts

- [[Search Evaluation]]
- [[A-B Testing for Search]]
- [[Judgment Lists]]

## People

- [[James Rubinstein]]

## Related Articles

- [[Query Triage - The Secret Weapon for Search Relevance]]
- [[A-B Testing for Search is Different]]
- [[Measuring Search - Metrics Matter]]
