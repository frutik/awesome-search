---
type: article
title: "Hybrid Search and Learning-to-Rank with Metarank"
source: "https://www.pinecone.io/learn/metarank/"
author: "[[Vsevolod Goloviznin]]"
published: 2023-06-30
created: 2026-06-11
concepts:
  - "[[Hybrid Search]]"
  - "[[Learning to Rank]]"
  - "[[LambdaMART]]"
  - "[[Reranking]]"
  - "[[BM25]]"
  - "[[Interleaving]]"
  - "[[Reciprocal Rank Fusion]]"
  - "[[Click Signals]]"
topics:
  - "[[Hybrid Search]]"
tags:
  - article
  - hybrid-search
  - learning-to-rank
  - reranking
  - ltr
---

# Hybrid Search and Learning-to-Rank with Metarank

**Source:** https://www.pinecone.io/learn/metarank/
**Author:** [[Vsevolod Goloviznin]] ([[Pinecone]])
**Published:** 2023-06-30

How to combine multiple retrievers (Elasticsearch/OpenSearch/Solr + [[Pinecone Vector DB|Pinecone]]) into one ranking using [[Metarank]] as a secondary [[Learning to Rank|LTR]] re-ranker.

---

## The multi-retriever problem

Running lexical ([[BM25]]) and vector retrieval side-by-side produces **non-comparable scores**: BM25 is unbounded and unevenly distributed (demonstrated on the [MSRD dataset](https://github.com/metarank/msrd)); cosine similarity (e.g. all-MiniLM-L6-v2 via SBERT) is bounded and thick-tailed. Naively summing the two scores is statistically invalid, and duplicate documents across sources must be deduplicated.

## LTR as the fusion mechanism

Treat BM25 and cosine similarity as **input ranking features** for a [[LambdaMART]] model, with implicit click feedback as labels — let the model learn how to merge the candidate sets to maximize [[NDCG]].

**Missing values:** when a doc comes from only one retriever (BM25 but no cosine, or vice versa), decision-tree LTR handles nulls natively — a null is a distinct feature value with a default split route. The article notes *"all major LambdaMART implementations like [[XGBoost]], [[LightGBM]], and [[CatBoost]] handle missing values in a very similar fashion."*

## Metarank integration flow

1. Metarank ingests feedback events (clicks, impressions) — historical for training, real-time for inference.
2. Backend fans a query out to Elasticsearch + Pinecone; concatenates both result sets unordered.
3. Metarank runs the LambdaMART model over the candidate set and returns the final ranking.

**Cold start:** you need behavioral history first — solved with [[Interleaving]] (zip-merge both result sets by relevance, optionally with sampling probabilities) as a strong, simple baseline to collect clicks. Config has four parts: state, click-through, feature, model. Events can be pulled from S3 / Kafka / Pulsar / Kinesis / Pub-Sub / Snowplow; in-memory store for demos, Redis for production.

## Beyond two features

Metarank can also compute behavioral features — CTR/conversion rates, User-Agent/GeoIP/Referer, profile interaction history, item price/category — at the cost of stateful infrastructure.

## Related Concepts

- [[Metarank]] · [[Hybrid Search]] · [[Learning to Rank]] · [[LambdaMART]] · [[Reranking]] · [[BM25]] · [[Interleaving]] · [[Reciprocal Rank Fusion]] · [[Click Signals]] · [[XGBoost]] · [[LightGBM]] · [[CatBoost]]

## Related Articles

- [[Learn-to-Rank with OpenSearch and Metarank]]
- [[Metarank - Personalized Ranking That Actually Reads Your Clicks]]
- [[RRF is Not Enough]]

## People

- [[Vsevolod Goloviznin]] — author, Metarank co-creator
