---
title: "What Is a Judgment List?"
source: "https://softwaredoug.com/blog/2021/02/21/what-is-a-judgment-list"
author: ["Doug Turnbull"]
tags:
  - clippings
  - search-evaluation
  - judgment-lists
  - annotation
concepts:
  - Judgment Lists
  - Search Evaluation
  - NDCG
created: 2026-05-15
---

# What Is a Judgment List?

**Source**: https://softwaredoug.com/blog/2021/02/21/what-is-a-judgment-list  
**Author**: [[Doug Turnbull]]

## Summary

[[Doug Turnbull]] explains what judgment lists are, how to create them, how to use them with Quepid to compute metrics, and common pitfalls. Aimed at practitioners building search evaluation programs for the first time.

## What Is a Judgment List?

A judgment list (qrels) is a spreadsheet/dataset pairing:
```
query                     | document_id | grade
"nike running shoes"      | prod_12345  | 3     (exact match)
"nike running shoes"      | prod_67890  | 1     (marginally relevant)
"nike running shoes"      | prod_99999  | 0     (irrelevant)
```

Grades reflect how well a document serves the query:
- **3–4**: Ideal — this is exactly what the user wants
- **2**: Good — clearly relevant and helpful
- **1**: Fair — related but not the best option
- **0**: Bad — irrelevant, off-topic

## Creating a Judgment List: Step by Step

### Step 1: Select Queries
Don't judge randomly chosen queries:
- Choose queries that represent real user needs
- Cover different query types ([[Query Types]])
- Sample from query log (stratified by frequency and type)

### Step 2: Retrieve Candidates
Run your current search system to get candidate results:
- Typically top 10–20 results per query
- Save doc IDs and the query-document pairs for annotation

### Step 3: Annotate
Options:
1. **Self-annotation** (cheapest, biased): you judge your own system
2. **Domain expert** (expensive, high quality): hired annotators with domain knowledge
3. **Crowdsourcing** (medium cost, variable quality): many annotators per pair
4. **LLM as judge** ([[LLM as Judge]]): fast, cheap, less nuanced

### Step 4: Compute Metrics
Use Quepid (open-source) or a scripting library to compute [[NDCG]], [[MRR]], [[Precision and Recall]].

## Common Mistakes

1. **Judging only your current system's results**: new system retrieves different docs → unjudged = grade 0 → unfair
2. **Annotating too few queries**: 50–100 queries is often insufficient for statistical significance
3. **Stale judgments**: judging annual product catalog → judgments become outdated monthly
4. **One annotator**: no inter-annotator agreement check → guidelines inconsistently applied

## Judgment List Size Guidelines

| Team Size | Min Queries | Notes |
|-----------|------------|-------|
| Solo/startup | 100 | Enough for direction, not statistical significance |
| Small team | 300–500 | Good baseline |
| Mid-size team | 1000+ | Supports stratified analysis by query type |
| Enterprise | 5000+ | Enables head/torso/tail analysis |

## Related Articles

- [[Flavors of NDCG]] — same author, what to compute from judgment lists
- [[Compute MRR using Pandas]] — same author, practical computation
- [[Evaluating Search - Using Human Judgments]] — human judgment methodology

## Related Concepts

- [[Judgment Lists]] — primary topic
- [[NDCG]] — metric computed from judgment lists
- [[MRR]] — another metric from judgment lists
- [[Search Evaluation]] — broader context
- [[LLM as Judge]] — alternative to human annotation

## People

- [[Doug Turnbull]] — author; Quepid co-creator
