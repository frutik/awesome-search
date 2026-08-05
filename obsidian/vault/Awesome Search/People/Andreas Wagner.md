---
type: person
title: "Andreas Wagner"
aliases: []
tags:
  - person
  - search-practitioner
  - e-commerce-search
created: 2026-05-16
---

# Andreas Wagner

## Background

Andreas Wagner is a search expert at SearchHub who authors the "Three Pillars of Search Quality in E-commerce" series. His framework organizes e-commerce search quality into three independent but related pillars.

## Key Contribution: Three Pillars Framework

Wagner's framework for e-commerce search quality:

1. **Findability** — can users find what they're looking for at all?
   - Zero results, spelling correction, synonym coverage
   - Measured by: zero results rate, task success rate

2. **Ranking / Relevance** — are the results in the right order?
   - [[NDCG]], precision, conversion correlation
   - Measured by: [[NDCG]]@k, CTR by rank

3. **Discovery & Inspiration** — do users find things they didn't know they wanted?
   - [[Diversity Metrics]], serendipity, exploration
   - Measured by: discovery rate, basket size, session depth

Each pillar requires different optimization strategies and different metrics — a system can excel at findability but fail at discovery.

## Second Line of Work: Evaluation at Scale

Distinct from the quality taxonomy above, Wagner also writes on the **economics** of relevance evaluation — how to run [[LLM as Judge|LLM judgments]] across billions of query-document pairs when judging everything with a frontier model is not affordable at any budget.

The architecture: prune the pair space using [[Implicit Judgments|implicit feedback]] to separate easy positives from candidate hard negatives, cascade the survivors through cheap quantized embedding judges before escalating disagreements to an LLM ([[Staged Judging]]), then [[Knowledge Distillation|distill]] the LLM's judgments into a small model with sub-20ms CPU inference.

Where the Three Pillars framework answers *what quality means*, this answers *how you can afford to measure it*.

## Articles in Vault

- [[Three Pillars of Search Quality - Findability]] — Findability pillar
- [[Three Pillars of Search Quality - Discovery and Inspiration]] — Discovery pillar: diversity, product exposure, multi-objective ranking
- [[Common Pitfalls of Onsite Search Experimentation]]
- [[Towards Scalable Relevance Engineering]] — judge economics: 93% problem reduction, staged judging, distillation to CPU-servable models

## Topics

- [[Search Result Diversity]] — [[MICES]] talk on result positioning and basket composition; Discovery pillar framework

## Affiliation

- [[searchHub]]

## Related People

- [[Daniel Tunkelang]] — overlapping quality framework
- [[Doug Turnbull]] — shared e-commerce search focus

## Related Concepts

- [[Staged Judging]] — cascade architecture for affordable relevance judging
- [[LLM as Judge]] — the expensive stage his architecture economizes
- [[Search Evaluation]] — three pillars provide structure
- [[Diversity Metrics]] — discovery pillar
- [[NDCG]] — ranking/relevance pillar
- [[Query Understanding]] — findability pillar
