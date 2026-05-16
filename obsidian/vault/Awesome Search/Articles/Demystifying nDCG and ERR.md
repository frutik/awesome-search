---
title: "Demystifying nDCG and ERR"
source: "https://opensourceconnections.com/blog/2019/12/09/demystifying-ndcg-and-err/"
author: ["OpenSource Connections"]
tags:
  - clippings
  - search-evaluation
  - ndcg
  - err
  - metrics
concepts:
  - NDCG
  - Search Evaluation
  - MRR
created: 2026-05-15
---

# Demystifying nDCG and ERR

**Source**: https://opensourceconnections.com/blog/2019/12/09/demystifying-ndcg-and-err/  
**Publisher**: OpenSource Connections

## Summary

A clear explainer contrasting [[NDCG]] with ERR (Expected Reciprocal Rank) — two ranking metrics that model user behavior differently. Aimed at search practitioners who have heard of both but aren't sure when to use each.

## NDCG Review

[[NDCG]] assumes:
- All relevant documents are worth finding
- Position matters (logarithmic discount)
- Documents don't "compete" — each has independent value

This is the **independent utility model**: each document contributes its relevance independently.

## ERR (Expected Reciprocal Rank)

ERR models users as a cascade: they read results from top to bottom, and their probability of being satisfied at rank i depends on not having been satisfied at ranks 1 through i-1.

```
ERR = Σᵢ  (1/i) × Rᵢ × Πⱼ<ᵢ (1 - Rⱼ)
```

Where Rᵢ is the probability of satisfaction at rank i (function of relevance grade).

**Intuition**: If the first result is perfect (Rᵢ = 1.0), the user is satisfied and doesn't look further. A highly relevant document at rank 3 contributes almost nothing if ranks 1 and 2 are also highly relevant.

## NDCG vs. ERR: Key Difference

| Scenario | NDCG | ERR |
|----------|------|-----|
| Perfect result at rank 1, more relevant at rank 5 | Rewards rank 5 (adds to DCG) | Minimal reward (user already satisfied) |
| Two good results at rank 1 and 2 | Sums both | Rank 2 partially discounted (user may stop at 1) |
| Ambiguous query needing multiple angles | Rewards diversity of good results | Stops at first satisfaction |
| Known-item search | Equivalent to MRR | Similar behavior |

## When to Use Each

**NDCG** is better for:
- Research evaluation (multiple relevant docs expected)
- Exploratory/informational queries
- E-commerce (user wants to see multiple options)

**ERR** is better for:
- Navigational queries (user wants one specific result)
- Known-item search
- When "one great result > two good results" is the right model

## Normalized vs. Unnormalized

Both NDCG and ERR can be computed normalized (by ideal) or unnormalized:
- **Normalized**: [0,1] range, enables comparison across query sets with different difficulty
- **Unnormalized DCG**: measures absolute quality; harder to compare across queries

## Related Articles

- [[Flavors of NDCG]] — NDCG formulation variants
- [[Measuring Search - Metrics Matter]] — metric selection in practice
- [[Session vs Query based Search Evals]] — ERR relates to session models

## Related Concepts

- [[NDCG]] — primary metric discussed
- [[MRR]] — related cascade model
- [[Search Evaluation]] — where these fit
- [[Session-Based Evaluation]] — ERR models session-like behavior
