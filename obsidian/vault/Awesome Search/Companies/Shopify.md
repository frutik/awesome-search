---
type: company
tags: [company, e-commerce, search, evaluation, ltr]
category: end-user
industry: e-commerce platform
products: [Shopify Help Center, Shopify merchant storefronts]
search_domain: [help center search, merchant product search]
use_cases: []
people:
  - "[[Doug Turnbull]]"
  - "[[Jodi Sloan]]"
  - "[[Andy Toulis]]"
created: 2026-05-16
---

# Shopify

E-commerce platform powering 2M+ merchant stores. Internally operates the Shopify Help Center search (2M+ visits/month) and provides search infrastructure for merchants.

## Search & Evaluation Work

**Help Center search** (B2B knowledge base):
- Evaluation framework: Kafka events (streaming behavioral data) + expert annotation by Shopify Support team
- Offline metrics: MAP, NDCG
- Online metrics: CTR, average rank of clicked result, abandonment, deflection (user resolved without contacting support)
- Moved from Vanilla Pagerank to **Query-specific Pagerank** (boosts historically clicked results for similar queries) → significant CTR, rank, and deflection improvements

**Relevance cutoff research** ([[Finding the Relevance Cutoff - When to Stop Showing Search Results]]):
- Progressive scroll UX requires evaluating the full result set, not just top-N
- Developed Variable Precision, F1, and Time Well Spent metrics for this scenario

**Product search / BM25 retuning** ([[Haystack US 2022 - Bayesian Optimization of Relevance at Shopify]]):
- [[Bayesian Optimization]] used to retune BM25 `b`/`k1` and match-clause boosts on the product title field
- Default length normalization (`b`) was over-punishing longer, more descriptive titles; retuning flattened the curve and shifted weight toward phrase matching
- First optimization run surfaced a presentation-bias loophole in the training data before a constrained, validated second run showed real held-out improvements

## Key Articles

- [[Building Smarter Search Products - 3 Steps for Evaluating Search Algorithms]]
- [[Finding the Relevance Cutoff - When to Stop Showing Search Results]]

## Key Talks

- [[Haystack US 2022 - Bayesian Optimization of Relevance at Shopify]] — [[Doug Turnbull]] & [[Andy Toulis]]
