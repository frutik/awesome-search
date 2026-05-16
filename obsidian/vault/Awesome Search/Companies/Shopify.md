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

## Key Articles

- [[Building Smarter Search Products - 3 Steps for Evaluating Search Algorithms]]
- [[Finding the Relevance Cutoff - When to Stop Showing Search Results]]
