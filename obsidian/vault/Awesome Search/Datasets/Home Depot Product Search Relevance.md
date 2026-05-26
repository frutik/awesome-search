---
title: "Home Depot Product Search Relevance"
aliases: ["Home Depot dataset", "Home Depot search relevance", "Kaggle Home Depot"]
tags:
  - dataset
  - search-evaluation
  - e-commerce
  - benchmark
  - kaggle
type: dataset
source: Home Depot / Kaggle
domain: e-commerce product search (home improvement)
website: https://www.kaggle.com/competitions/home-depot-product-search-relevance/data
---

# Home Depot Product Search Relevance

## Overview

A Kaggle competition dataset released by Home Depot for evaluating product search relevance. It provides query–product pairs labeled with crowdsourced relevance scores, focused on the home improvement retail domain.

## Dataset Structure

- **Query**: customer search query (e.g., "angle bracket", "oscillating tool blade")
- **Product**: product title and description
- **Relevance score**: continuous 1–3 scale from crowdsourced annotation (average of multiple annotators)
- **Domain**: home improvement products

## Key Characteristics

The 1–3 continuous relevance scale (with decimal values from annotator averaging) differs from the discrete 0–4 grading in typical IR [[Judgment Lists]]. This makes it well-suited for regression-based relevance prediction rather than classification.

The home improvement domain has distinctive challenges:
- Technical terminology (product codes, specifications, measurements)
- Queries mixing product type + attribute (e.g., "3/4 inch PVC elbow")
- User intent often includes installation context not visible in product descriptions

## Use Cases

- Regression models predicting relevance scores
- Feature engineering experiments (text matching, semantic similarity)
- Benchmarking retrieval systems in a vertical domain
- Transfer learning experiments (train on ESCI, evaluate on Home Depot or vice versa)

## Comparison with Other Datasets

| Dataset | Domain | Scale | Label type |
|---|---|---|---|
| [[Amazon ESCI Dataset]] | General e-commerce | Very large | 4-class (ESCI) |
| [[WANDS Dataset]] | Home goods | ~42K pairs | 3-class |
| Home Depot | Home improvement | ~74K pairs | Continuous 1–3 |

## Related Concepts

- [[Judgment Lists]] — this dataset functions as a crowdsourced judgment list
- [[NDCG]] — continuous scores can be discretized for NDCG computation
- [[Learning to Rank]] — standard use case for this dataset
- [[Amazon ESCI Dataset]] — larger counterpart for general e-commerce search evaluation
- [[WANDS Dataset]] — comparable vertically-focused annotation dataset

## Source

- Kaggle: https://www.kaggle.com/competitions/home-depot-product-search-relevance/data
