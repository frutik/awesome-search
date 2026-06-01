---
title: "Choosing Your Search Relevance Evaluation Metric"
source: "https://opensourceconnections.com/blog/2020/02/28/choosing-your-search-relevance-metric/"
author: ["OpenSource Connections"]
tags:
  - clippings
  - search-evaluation
  - metrics
  - ndcg
  - mrr
  - company-blog
concepts:
  - Search Evaluation
  - NDCG
  - MRR
  - Precision and Recall
created: 2026-05-15
---

# Choosing Your Search Relevance Evaluation Metric

**Source**: https://opensourceconnections.com/blog/2020/02/28/choosing-your-search-relevance-metric/  
**Publisher**: OpenSource Connections

## Summary

A decision guide for choosing between [[NDCG]], [[MRR]], [[Precision and Recall]], and behavioral metrics for search quality evaluation — emphasizing that the right metric depends on use case, not convention.

## The Decision Framework

### Step 1: What Kind of Relevance Do You Have?

**Graded relevance** (0–4 scale, different quality levels):
- Use [[NDCG]] — captures grade differences
- Examples: e-commerce (perfect match vs. acceptable), enterprise search

**Binary relevance** (relevant or not):
- Use [[MRR]] or Precision@k — simpler, appropriate for binary
- Examples: QA systems, navigational search

### Step 2: How Many Relevant Documents Exist?

**One correct answer** (navigational, QA):
- Use [[MRR]] — focused on finding that one result
- Example: "what is the company's refund policy?" → single document is correct

**Multiple acceptable answers** (product search, informational):
- Use [[NDCG]]@k or Precision@k — rewards finding multiple relevant docs
- Example: "running shoes" → many relevant products

### Step 3: Does Rank Order Matter?

**Yes — higher rank = more important**:
- Use [[NDCG]] or [[MRR]] — position-sensitive

**No — just care about recall at cutoff**:
- Use Recall@k or Precision@k — position-insensitive

### Step 4: Do You Have Judgment Labels?

**Yes, with grades**: [[NDCG]]  
**Yes, binary**: [[MRR]] or Precision@k  
**No (behavioral data only)**: CTR, conversion rate, session success ([[Click Signals]])

## Metric Selection Summary

| Search Type | Recommended Primary | Recommended Secondary |
|-------------|--------------------|-----------------------|
| E-commerce product search | NDCG@10 | Conversion rate |
| QA / knowledge base | MRR@10 | P@1 |
| Enterprise document search | NDCG@5 | Session success |
| Navigational | P@1 | MRR |
| Exploratory/discovery | NDCG + diversity | Session depth |

## Common Mistakes in Metric Selection

1. **Copying academic benchmarks blindly**: MS MARCO uses NDCG@10 — appropriate for passage retrieval, may not suit your use case
2. **Metric without business alignment**: high NDCG doesn't always mean business success
3. **Single metric tyranny**: no single metric captures everything; always track 2–3

## Related Articles

- [[Flavors of NDCG]] — NDCG implementation variants
- [[Demystifying nDCG and ERR]] — NDCG vs. ERR choice
- [[Measuring Search - Metrics Matter]] — broader metrics discussion

## Related Concepts

- [[Search Evaluation]] — context for metric selection
- [[NDCG]] — primary option
- [[MRR]] — secondary option
- [[Precision and Recall]] — foundational options
- [[Judgment Lists]] — required for all offline metrics
