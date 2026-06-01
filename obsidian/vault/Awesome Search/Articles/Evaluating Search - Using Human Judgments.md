---
title: "Evaluating Search: Using Human Judgments"
source: "https://dtunkelang.medium.com/evaluating-search-using-human-judgement-fbb2eeba37d9"
author: ["Daniel Tunkelang"]
tags:
  - clippings
  - search-evaluation
  - human-judgment
  - annotation
  - medium
concepts:
  - Judgment Lists
  - Search Evaluation
  - NDCG
created: 2026-05-15
---

# Evaluating Search: Using Human Judgments

**Source**: https://dtunkelang.medium.com/evaluating-search-using-human-judgement-fbb2eeba37d9  
**Author**: [[Daniel Tunkelang]]

## Summary

Part of [[Daniel Tunkelang]]'s "Evaluating Search" series. Argues that human judgment remains the gold standard for search quality evaluation despite being expensive, and explains how to design annotation programs that produce reliable signals.

## Why Human Judgment?

Automated metrics ([[NDCG]], [[MRR]]) require human relevance judgments as input — they can't exist without them. The question isn't whether to use human judgment, but how:

- **Directly**: annotate each (query, document) pair
- **Indirectly**: collect click signals and use as proxy
- **Automated**: use [[LLM as Judge]] as proxy for human judgment

Each proxy introduces error. Human direct annotation is the source of ground truth.

## Designing a Good Annotation Program

### 1. Annotation Guidelines
The most important investment. Vague guidelines → inconsistent grades → misleading metrics.

Good guidelines:
- **Domain-specific**: "relevant" for legal queries is different from fashion
- **Example-rich**: 2–3 concrete examples per grade level
- **Edge case coverage**: borderline cases explicitly addressed
- **Actionable**: annotator should be able to judge in <30 seconds

### 2. Annotator Selection
- Domain expertise required for specialized content
- Multiple annotators per query (3+ for expensive queries)
- Regular calibration sessions: re-judge the same queries periodically

### 3. Inter-Annotator Agreement
Measure Kappa/Krippendorff's Alpha. Use as ongoing health metric:
- If agreement drops: guidelines need clarification
- If agreement is consistently high: guidelines working well

### 4. Sampling Strategy
Judgment lists should cover:
- Head queries (most traffic) — highest business impact
- Torso queries — broad coverage
- Tail queries — edge cases, failure modes
- Adversarial queries — known hard cases

See [[Query Types]] for taxonomy.

## Human Judgment vs. Click Data

Tunkelang frames the comparison:

| Dimension | Human Judgment | Click Data |
|-----------|---------------|-----------|
| Scale | Limited (hundreds/day) | Massive (millions/day) |
| Quality | High (with good guidelines) | Noisy (position bias) |
| Coverage | Curated | Whatever users searched |
| Cost | High ($1–5/pair) | Free |
| Freshness | Requires update | Real-time |

Best practice: use both. Calibrate click-based proxies against human judgments periodically.

## Judgment Lists in Agentic Systems

For [[Agentic Search]], judgment is more complex:
- Not just "is this document relevant?" but "did the agent reach a correct final answer?"
- Requires multi-step evaluation
- Per-document NDCG doesn't capture full-session quality

## Related Articles

- [[Measuring Search Effectiveness]] — same author, metrics framework
- [[Measuring Search - A Human Approach]] — [[James Rubinstein]]'s complementary view
- [[What Is a Judgment List]] — practical creation guide

## Related Concepts

- [[Judgment Lists]] — primary focus
- [[Search Evaluation]] — broader context
- [[NDCG]] — computed from human judgments
- [[LLM as Judge]] — automated alternative
- [[Click Signals]] — behavioral alternative
- [[Session-Based Evaluation]] — extends to session-level human judgment

## People

- [[Daniel Tunkelang]] — author
