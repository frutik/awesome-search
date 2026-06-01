---
title: "Setting Up a Relevance Evaluation Program"
tags:
  - clippings
  - search
  - evaluation
  - process
  - medium
source: "https://medium.com/@jamesrubinstein/setting-up-a-relevance-evaluation-program-c955d32fba0e"
author: "James Rubinstein"
created: 2026-05-15
concepts:
  - Judgment Lists
  - Search Evaluation
---

# Setting Up a Relevance Evaluation Program

**Source:** https://medium.com/@jamesrubinstein/setting-up-a-relevance-evaluation-program-c955d32fba0e
**Author:** [[James Rubinstein]]

## Summary

Step-by-step guide to building a human relevance judgment program from scratch — the operational backbone of a serious [[Search Evaluation]] practice.

## The Six Steps

### 1. Understand Your User Task
What are users actually doing? Information gathering, shopping, navigation, comparison. Task type determines what "relevant" means.

### 2. Select Evaluation Methodology
- **Result set preference** — which set of results is better overall?
- **Document preference** — is doc A or doc B more relevant?
- **Binary relevance** — relevant or not?
- **Graded relevance** — 4-point scale (Perfect → Excellent → Good → Poor)

A 4-point scale is practical for most cases.

### 3. Gather Queries
Use **weighted random sampling** where weights = query frequency. This avoids over-representing outlier tail queries while still including some tail coverage. See [[Succeeding with Relevance Evaluation using PPS Sampling]].

### 4. Collect Documents
Run sampled queries through your search engine; capture the result sets to be judged.

### 5. Recruit Raters
> "The single most important part of a human relevance evaluation program is the _humans_."

Match rater expertise to domain: lawyers for legal, makeup enthusiasts for cosmetics. Options: internal staff, consulting firms, crowdsourcing platforms.

### 6. Execute Ratings
Use gold-rater verification tiers: standard raters escalate disagreements to expert judges. Capture structured judgments, not free text.

## Related Concepts

- [[Judgment Lists]]
- [[Search Evaluation]]
- [[A-B Testing for Search]]
- [[NDCG]]

## People

- [[James Rubinstein]]

## Related Articles

- [[What Is a Judgment List]]
- [[Evaluating Search - Using Human Judgments]]
- [[Query Triage - The Secret Weapon for Search Relevance]]
