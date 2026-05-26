---
title: "ESCI-S Dataset"
aliases: ["ESCI-S", "ESCI extended", "esci-s"]
tags:
  - dataset
  - search-evaluation
  - e-commerce
  - benchmark
type: dataset
source: shuttie (community)
domain: e-commerce product search
repo: https://github.com/shuttie/esci-s
---

# ESCI-S Dataset

## Overview

ESCI-S is a community-built extension of the [[Amazon ESCI Dataset]] that adds richer product metadata to the original query–product pairs. While the original ESCI release includes basic product fields, ESCI-S enriches each product record with additional attributes useful for training and evaluation.

## What It Adds

- Extended product metadata beyond the original ESCI fields (titles, descriptions, bullets)
- Additional structured attributes that support feature engineering
- Useful for experiments where richer product context improves model quality

## Use Cases

- Training embedding and ranking models that benefit from richer product features
- Ablation studies on the effect of metadata richness on retrieval quality
- Augmenting the base [[Amazon ESCI Dataset]] for more nuanced experiments

## Relationship to ESCI

ESCI-S reuses the same query–product pairs and ESCI relevance labels from the original dataset. It does not change the labels — it only enriches the product-side metadata. Evaluations remain directly comparable to the base ESCI benchmark.

## Related Concepts

- [[Amazon ESCI Dataset]] — the base dataset this extends
- [[Judgment Lists]] — shared annotation structure
- [[Semantic Search]] — primary model type evaluated with ESCI-based data
- [[Learning to Rank]] — downstream task using these labels

## Source

- Repo: https://github.com/shuttie/esci-s
