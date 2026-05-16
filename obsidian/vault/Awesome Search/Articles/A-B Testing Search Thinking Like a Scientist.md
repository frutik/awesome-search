---
title: "A/B Testing Search: Thinking Like a Scientist"
tags:
  - clippings
  - search
  - evaluation
  - experimentation
source: "https://medium.com/@jamesrubinstein/a-b-testing-search-thinking-like-a-scientist-1cc34b88392e"
author: "James Rubinstein"
created: 2026-05-15
concepts:
  - A-B Testing for Search
  - Search Evaluation
---

# A/B Testing Search: Thinking Like a Scientist

**Source:** https://medium.com/@jamesrubinstein/a-b-testing-search-thinking-like-a-scientist-1cc34b88392e
**Author:** [[James Rubinstein]]

## Summary

Applies scientific thinking to search A/B testing — how to form proper hypotheses, design tests, and interpret results without p-hacking or confirmation bias.

## Core Principles

### Pre-registration of Hypotheses
Define success criteria **before** running the experiment. Post-hoc interpretation ("we expected this result") leads to confirmatory bias and false positives.

### Statistical Rigor
- Set minimum detectable effect size based on business significance, not just statistical significance
- Account for multiple comparisons (testing 10 metrics means false positive rate multiplies)
- Run experiments for a full week cycle to avoid day-of-week effects

### The Scientist's Mindset
Treat each experiment as a chance to learn, not just to confirm a belief. A "failed" experiment that reveals a hidden interaction or explains user behavior has value.

## Search-Specific Complications

- Query volume varies enormously — tail queries have low power
- Session context means one query's result affects the next
- Different user segments may respond oppositely to the same change

## Key Complement to Offline Evaluation

A/B tests confirm or refute what [[Search Evaluation]] and [[Judgment Lists]] predicted offline. The two methods together catch both relevance regressions AND user experience issues that don't show up in static judgment sets.

## Related Concepts

- [[A-B Testing for Search]]
- [[Search Evaluation]]
- [[Session-Based Evaluation]]
- [[Click Signals]]
- [[NDCG]]

## People

- [[James Rubinstein]]

## Related Articles

- [[A-B Testing for Search is Different]]
- [[The Launch Review]]
- [[Session vs Query based Search Evals]]
