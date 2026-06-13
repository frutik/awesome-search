---
created: 2026-05-16
type: article
tags: [article, ltr, lambdamart, e-commerce, otto, ranking, evaluation, company-blog]
source: "https://www.otto.de/jobs/en/blogs/techblog/1-learning-to-rank-for-e-commerce-search/"
author: [Andrea Schütt]
company: [Otto]
concepts: [Learning to Rank, NDCG, Search Evaluation]
topics: [E-commerce Search, Relevance Program Setup]
---

# Part 1: Learning to Rank for E-Commerce Search at Otto

**[[Andrea Schütt]]** (Otto) describes Otto's LTR implementation as Otto transitioned to a marketplace model with rapidly growing product catalog.

## Why LTR?

As catalog diversity grows, manual ranking rules can't scale. LTR uses ML models trained on customer interaction data to learn what "relevant" means for each query-product pair.

## Model Choice: LambdaMART

LambdaMART combines pairwise and listwise learning:
- Pairwise: compares pairs of documents for the same query
- Listwise weighting: weights gradients by NDCG impact

Trained using **RankyMcRankFace** (fork of RankLib), served via Solr LTR plugin.

## Label Generation Challenge

Standard crowdsourcing doesn't work for e-commerce: a crowd rater can't judge whether a product is relevant *given the intent to buy*. Labels must come from customer data.

Target metrics considered:
- Clicks only (starting point)
- Add-to-basket / add-to-wishlist events
- Orders (strongest signal)
- Combinations of the above
- Dwell time, pages browsed in SERP

## Pipeline

1. Sample query set → compute features in Solr feature store
2. Auto-generate judgments from customer interaction data
3. Combine features + judgments → LambdaMART training
4. Upload model to Solr model store → apply as reranking stage
5. Validate with Offline Metrics Analyzer (custom NDCG calculator)

## Key Insight

*"Increase recall without losing precision on visible ranks"* — the core motivation for LTR when catalog size makes manual rule management impossible.

## Related Concepts

[[Learning to Rank]] · [[NDCG]] · [[Search Evaluation]] · [[E-commerce Search]]
