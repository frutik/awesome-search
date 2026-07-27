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

## Known Issues — Image Link Rot

The extended metadata includes product image URLs, but a large share of them are
no longer usable in practice:

- **131,054 products** in the extended dataset have no image at all.
- Of the products that *do* carry an image URL, roughly **46% of the links are
  dead** — measured by [[Andrew Kornilov]] while downloading two independent
  samples of ~20,000 products: 9,195 and 9,216 failures respectively.

Practical consequence: image URLs in ESCI-S cannot be trusted as-is. Anyone
building an image-based pipeline has to **download and validate every image
before indexing**, and over-sample to hit a target corpus size. In
[[How to Evaluate Image Search in Qdrant Using Quepid Part 1]], sampling 40,000
products yielded only **21,589** with a working image.

The text-side metadata and the ESCI relevance labels are unaffected — this only
bites [[Multimodal Embeddings]] / image-search work.

## Related Concepts

- [[Amazon ESCI Dataset]] — the base dataset this extends
- [[Judgment Lists]] — shared annotation structure
- [[Semantic Search]] — primary model type evaluated with ESCI-based data
- [[Learning to Rank]] — downstream task using these labels
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 1]] — hands-on use of the image metadata, and where the link-rot numbers come from

## Source

- Repo: https://github.com/shuttie/esci-s
