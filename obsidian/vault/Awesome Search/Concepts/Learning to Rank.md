---
title: "Learning to Rank"
aliases: ["LTR", "machine learned ranking", "MLR", "supervised ranking", "lambdaMART", "LambdaRank"]
tags:
  - concept
  - ranking
  - machine-learning
  - search
---

# Learning to Rank

## Definition

Learning to Rank (LTR) is the application of machine learning to the ranking problem in information retrieval — training models to produce optimal rankings given a query and a set of candidate documents, using labeled (query, document, relevance) training data.

## Why LTR?

Hand-tuned ranking formulas (BM25 weights, field boosts) are:
- Brittle: require manual adjustment for new query types
- Suboptimal: can't model complex non-linear feature interactions
- Domain-specific: no transfer across product categories or query types

LTR learns the ranking function from data, capturing complex signals (TF-IDF × freshness × popularity × semantic similarity) that are impossible to tune manually.

## LTR Formulations

### Pointwise
Score each document independently. Treat as regression/classification.
- Loss: MSE on relevance grade
- Simple but ignores relative ordering

### Pairwise
For each query, learn that doc A should rank above doc B.
- Input: (query, doc_A, doc_B, which_is_better)
- Loss: hinge loss / logistic loss on pairwise preferences
- **[[RankNet]]** (2005): foundational pairwise approach

### Listwise
Optimize a ranking metric directly (NDCG, MAP) over the full ranked list.
- Loss: gradient of NDCG (tricky — NDCG is non-differentiable)
- **LambdaMART** (2010): dominant practical algorithm
- Uses NDCG gain as gradient weighting

## LambdaMART

LambdaMART is the dominant LTR algorithm in production:
1. **MART** (Multiple Additive Regression Trees) = gradient boosted decision trees (GBDTs)
2. **Lambda** = gradient weighting by NDCG improvement of swapping two documents

```python
from lightgbm import LGBMRanker

model = LGBMRanker(
    objective="lambdarank",
    metric="ndcg",
    ndcg_eval_at=[5, 10],
    num_leaves=31,
    n_estimators=100
)
model.fit(X_train, y_train, group=query_sizes)
```

Features used:
- BM25 score (title, body, description)
- Semantic similarity (embedding cosine)
- Popularity (click rate, sales)
- Freshness (recency)
- Price, rating
- User features (if personalized)

## Two-Phase: Retrieval → Ranking

LTR is almost always the second stage in a [[Retrieval Pipeline]]:
```
Fast first-stage (BM25 or bi-encoder) → top-1000
    ↓
LTR reranker (LambdaMART or neural) → top-20
```

The first stage uses simple fast signals; LTR adds expensive-to-compute features.

## Neural LTR

More recent: neural rerankers replace LambdaMART:
- [[Cross-Encoder]]: joint query-document encoding, listwise softmax loss
- [[MonoT5]]: T5-based pointwise ranker
- [[RankLLaMA]]: LLaMA fine-tuned for ranking
- [[RankGPT]]: listwise LLM permutation reranker

## Training Data

LTR requires labeled data:
- **Explicit judgments**: [[Judgment Lists]] with annotated (query, doc, grade) triples
- **Click data**: position-debiased click labels from query logs ([[Click Signals]])
- **Conversion data**: purchase signals for e-commerce

## Position Bias in LTR Training

Click data has position bias — documents at rank 1 get many clicks regardless of quality. Must correct with:
- **IPS** (Inverse Propensity Scoring): weight clicks by inverse position probability
- **Counterfactual evaluation**: compare click rates controlling for position

Unbiased training data → significantly better LTR models.

## Related Concepts

- [[Retrieval Pipeline]] — LTR is the reranking stage
- [[NDCG]] — metric LTR directly optimizes
- [[Cross-Encoder]] — neural LTR alternative
- [[Judgment Lists]] — training data source
- [[Click Signals]] — implicit training signal
- [[BM25]] — feature in LTR model
- [[Dense Vector Retrieval]] — embedding cosine as LTR feature
- [[Personalization]] — personalized LTR uses user features
- [[LambdaMART]] — dominant production LTR algorithm
- [[RankNet]] — foundational pairwise approach
- [[Ranking Objectives]] — pointwise/pairwise/listwise losses
- **Implementations**: [[LightGBM]], [[XGBoost]], [[CatBoost]], [[RankLib]]
- **Serving**: [[Metarank]] — open-source LambdaMART secondary re-ranker
- [[Feature Store]] — where ranking features are persisted/served
- [[Implicit Judgments]] — behavioral labels for training

## Articles

- [[What AI Engineers Should Know about Search]] — [[Doug Turnbull]]; accessible LTR primer covering SVMRank, LambdaMART, feature orthogonality, multi-stage reranking
- [[Learn-to-Rank with OpenSearch and Metarank]] — [[Roman Grebennikov]]; LambdaMART secondary re-ranking on OpenSearch
- [[Hybrid Search and Learning-to-Rank with Metarank]] — [[Vsevolod Goloviznin]]; LTR as multi-retriever fusion
- [[Metarank - Personalized Ranking That Actually Reads Your Clicks]] — [[Florian Narr]]; Metarank repo review

## People

- [[Doug Turnbull]] — "How LambdaMART works" post; LTR in production
