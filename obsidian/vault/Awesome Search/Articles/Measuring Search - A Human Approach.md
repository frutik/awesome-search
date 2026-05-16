---
title: "Measuring Search: A Human Approach"
source: "https://jamesrubinstein.medium.com/measuring-search-a-human-approach-acf54e2cf33d"
author: ["James Rubinstein"]
tags:
  - clippings
  - search-evaluation
  - human-judgment
  - annotation
concepts:
  - Judgment Lists
  - Search Evaluation
  - NDCG
created: 2026-05-15
---

# Measuring Search: A Human Approach

**Source**: https://jamesrubinstein.medium.com/measuring-search-a-human-approach-acf54e2cf33d  
**Author**: [[James Rubinstein]]

## Summary

[[James Rubinstein]] makes the case for human-centered search evaluation as the irreplaceable foundation of any measurement program — and provides a practical framework for organizing and running annotation.

## The Human Judgment Argument

Some practitioners treat human judgment as a bottleneck to automate away. Rubinstein argues the opposite: **human judgment is not a bottleneck; it is the signal**.

All behavioral metrics (clicks, conversions) are noisy proxies for human satisfaction. All automated metrics ([[NDCG]], [[MRR]]) are computed from human-labeled data. The only way to know if a search system is good is to ask humans — everything else is a proxy.

The goal is to make human judgment more efficient, not to replace it.

## Four Roles in a Human Evaluation Program

### 1. Annotation Designer
Creates the annotation guidelines. Most important role.
- Guidelines should be clear enough that any annotator (not domain expert) can apply them consistently
- Test guidelines with 2–3 pilot annotators before full rollout
- Update guidelines when inter-annotator agreement drops

### 2. Annotator
Applies guidelines to (query, document) pairs.
- Should not know which system produced the results (blind evaluation)
- Speed: 50–100 judgments/hour with good tooling
- Track annotator disagreement rates to identify struggling annotators

### 3. Adjudicator
Resolves disagreements between annotators.
- Spot-checks 5–10% of agreed judgments to prevent drift
- Final word on edge cases

### 4. Analyst
Computes metrics, interprets results, drives decisions.

## Annotation at Scale: Practical Choices

| Option | Cost | Quality | Speed |
|--------|------|---------|-------|
| Internal domain experts | Low cost, high expertise | Highest | Slow |
| Freelance specialists | Medium cost | High | Medium |
| Crowdsourcing (MTurk, Scale AI) | Low | Variable | Fast |
| [[LLM as Judge]] | Very low | Medium | Instant |

Rubinstein recommends internal experts for high-stakes decisions, LLM judges for rapid prototyping.

## Maintaining Annotation Quality Over Time

Human annotations decay in quality without maintenance:
1. **Monthly calibration**: re-judge 5% of existing judgments, compare to original
2. **Product change review**: when catalog/content changes, flag affected judgments
3. **Metric trend monitoring**: if NDCG trends up without system changes, judgments are inflating

## Related Articles

- [[Evaluating Search - Using Human Judgments]] — Tunkelang's view
- [[What Is a Judgment List]] — practical creation guide
- [[Measuring Search - Metrics Matter]] — same author, metrics focus

## Related Concepts

- [[Judgment Lists]] — primary topic
- [[Search Evaluation]] — context
- [[LLM as Judge]] — complement to human judgment
- [[NDCG]] — computed from human judgments
- [[Session-Based Evaluation]] — human judgment can be session-level too

## People

- [[James Rubinstein]] — author
