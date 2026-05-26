---
title: "WANDS Dataset"
aliases: ["WANDS", "Wayfair ANnotation Dataset", "Wayfair search dataset"]
tags:
  - dataset
  - search-evaluation
  - e-commerce
  - benchmark
type: dataset
source: Wayfair
domain: e-commerce product search (home goods)
repo: https://github.com/wayfair/WANDS
---

# WANDS Dataset

## Overview

WANDS (Wayfair ANnotation Dataset) is a search relevance annotation dataset released by Wayfair. It provides human-annotated query–product relevance judgments for the home goods / furniture domain, designed to support search evaluation and ranking research.

## Dataset Structure

- ~42,000 annotated query–product pairs
- Queries drawn from real Wayfair search traffic
- Products: furniture, home décor, and home goods
- Relevance labels: 3-class (Exact, Partial, Irrelevant)

## Label Schema

| Label | Meaning |
|---|---|
| **Exact** | Product directly satisfies the query intent |
| **Partial** | Product is related but doesn't fully satisfy intent |
| **Irrelevant** | Product is not relevant to the query |

## Domain Characteristics

Home goods search has distinct challenges compared to general e-commerce:
- Highly visual product categories (color, style, material matter)
- Queries often blend attribute combinations ("mid-century modern sofa gray")
- Long-tail product variants (same item in 20 finishes)
- Style and taste are subjective — relevance judgments can be noisy

## Use Cases

- Benchmarking lexical vs. semantic retrieval in a vertical domain
- Training and evaluating [[Learning to Rank]] models
- Studying vertical domain transfer from general datasets like [[Amazon ESCI Dataset]]
- Evaluating [[Hybrid Search]] systems in e-commerce contexts

## Comparison with Other Datasets

| Dataset | Domain | Scale | Label type |
|---|---|---|---|
| [[Amazon ESCI Dataset]] | General e-commerce | Very large | 4-class (ESCI) |
| WANDS | Home goods | ~42K pairs | 3-class |
| [[Home Depot Product Search Relevance]] | Home improvement | ~74K pairs | Continuous 1–3 |

## Related Concepts

- [[Judgment Lists]] — WANDS is a publicly released judgment list
- [[NDCG]] — graded labels directly support NDCG computation
- [[Learning to Rank]] — primary use case
- [[Hybrid Search]] — commonly evaluated against WANDS
- [[Amazon ESCI Dataset]] — larger counterpart for broader e-commerce domains

## Source

- Repo: https://github.com/wayfair/WANDS
