---
title: "Building a Better Search Engine for Semantic Scholar"
tags:
  - clippings
  - search
  - case-study
  - ranking
  - medium
source: "https://medium.com/ai2-blog/building-a-better-search-engine-for-semantic-scholar-ea23a0b661e7"
author: "Sergey Feldman"
created: 2026-05-15
concepts:
  - Learning to Rank
  - Search Evaluation
  - Judgment Lists
---

# Building a Better Search Engine for Semantic Scholar

**Source:** https://medium.com/ai2-blog/building-a-better-search-engine-for-semantic-scholar-ea23a0b661e7
**Author:** [[Sergey Feldman]] (Senior Applied Research Scientist, AI2)

## Summary

How AI2 built an ML reranker on top of Elasticsearch for Semantic Scholar (190M+ papers), going from evaluation score 0.7 to 0.93 and +8% clicks per query.

## Technical Architecture

- **First stage**: Elasticsearch retrieval (190M papers indexed)
- **Reranking layer**: [[LightGBM]] with [[LambdaMART|LambdaRank]] optimization
- **Features**: 22 engineered features — query text matching across title, abstract, venue, author fields; KenLM language model scoring
- Training data: human-annotated judgment lists

## Key Practical Innovations

### 1. Data Filtering
Removed ~1/3 of training data that failed "sensibility checks" (comparing citation counts, recency, textual matches). Yielded **10-15% evaluation improvement** — data quality mattered more than data quantity.

### 2. Custom Evaluation Metric
Instead of standard NDCG on held-out test set, created manually-annotated benchmark of 250 real queries with component-level criteria (author, venue, year, text). More predictive of production performance than generic metrics.

### 3. Post-hoc Rule Corrections
Rule-based fixes for known model errors: boost exact year matches, boost quoted phrase matches.

## Results

- Custom metric: 0.7 → 0.93
- A/B test: **+8% clicks per query**, **+9% MRR**

## Lessons

1. Evaluation metric design is as important as model design — see [[Judgment Lists]]
2. Training data filtering beats more data
3. Rules + ML beats ML alone

## Related Concepts

- [[Learning to Rank]]
- [[LambdaMART]]
- [[LightGBM]]
- [[Search Evaluation]]
- [[Judgment Lists]]
- [[NDCG]]
- [[MRR]]

## People

- [[Doug Turnbull]] — LambdaMART explainer referenced

## Related Articles

- [[How LambdaMART Works]]
- [[Evaluating Search - Using Human Judgments]]
