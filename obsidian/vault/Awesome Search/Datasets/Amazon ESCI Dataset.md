---
title: "Amazon ESCI Dataset"
aliases: ["ESCI", "Shopping Queries Dataset", "Amazon Shopping Queries", "ESCI benchmark"]
tags:
  - dataset
  - search-evaluation
  - e-commerce
  - benchmark
type: dataset
source: Amazon
domain: e-commerce product search
repo: https://github.com/amazon-science/esci-data
---

# Amazon ESCI Dataset

## Overview

The Shopping Queries Dataset is a large-scale e-commerce search benchmark released by Amazon. It provides human-annotated query–product pairs labeled with ESCI relevance grades, designed to improve and evaluate product search systems.

## ESCI Relevance Scale

Each (query, product) pair is labeled with one of four grades:

| Grade | Label | Meaning |
|---|---|---|
| E | **Exact** | The product directly matches the query |
| S | **Substitute** | The product could substitute for the intent, but isn't an exact match |
| C | **Complement** | The product complements (goes with) the query intent |
| I | **Irrelevant** | The product is not relevant to the query |

This 4-class schema is richer than binary relevance and captures typical e-commerce nuances (e.g., accessories, near-misses).

## Key Facts

- Large scale: hundreds of thousands of labeled pairs
- Multi-locale: covers English, Japanese, and Spanish
- Product metadata: titles, descriptions, bullets, product type
- Designed for ranking, classification, and retrieval tasks

## Supported Tasks

1. **Query–Product Ranking** — rank products by relevance for a given query
2. **Query–Product Classification** — predict the ESCI label for a (query, product) pair
3. **Product Substitute Identification** — identify substitute products from the S-labeled pairs

## Use in Search Evaluation

The ESCI dataset serves as a public [[Judgment Lists|judgment list]] for benchmarking retrieval and ranking models. It's commonly used to evaluate:
- Embedding models for product search
- [[Learning to Rank]] models
- [[Hybrid Search]] systems combining lexical and semantic signals

Because it uses multi-class labels (not binary), it supports [[NDCG]] evaluation natively.

See [[ESCI-S Dataset]] for extended metadata built on top of this dataset.

## Related Concepts

- [[Judgment Lists]] — ESCI is a large-scale public judgment list
- [[NDCG]] — ESCI's graded labels map naturally to NDCG evaluation
- [[Learning to Rank]] — a primary use case for this dataset
- [[Semantic Search]] — embedding models evaluated against ESCI
- [[WANDS Dataset]] — comparable annotation dataset from Wayfair

## Source

- Repo: https://github.com/amazon-science/esci-data
