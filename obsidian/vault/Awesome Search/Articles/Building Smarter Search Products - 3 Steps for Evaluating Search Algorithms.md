---
type: article
tags: [article, evaluation, ab-testing, shopify, offline-metrics, annotation]
source: "https://shopify.engineering/evaluating-search-algorithms"
author: [[[Jodi Sloan]]]
company: [Shopify]
concepts: [NDCG, MAP, Search Evaluation, Judgment Lists]
topics: [Relevance Program Setup, A-B Testing for Search, Search Quality Assurance]
---

# Building Smarter Search Products: 3 Steps for Evaluating Search Algorithms

**Shopify** describes their three-step framework for evaluating new search algorithms (specifically: Query-specific Pagerank vs. Vanilla Pagerank for Shopify Help Center search).

## The Three-Step Framework

### 1. Collect Data
Two sources:
- **Kafka events**: User interactions (clicks, queries, support contacts) piped through ETL into a search fact table. Enables real-time A/B assignment and online monitoring.
- **Annotation**: Shopify Support team rates query-document pairs on a 4-point scale (bad/ok/good/great). Explicit human judgment preferred over click models for this domain (small corpus, expert raters). Warns: annotation sets go stale as the Help Center evolves — re-run regularly.

### 2. Evaluate Offline Metrics
- **MAP** — penalizes returning irrelevant results before relevant ones; suitable with binary relevance cutoffs
- **NDCG** — preserves graded relevance; preferred when relevance isn't binary
- Both used to iterate quickly without exposing users to risk

### 3. Evaluate Online Metrics (A/B Test)
Metrics chosen for Shopify Help Center:
- **CTR** — want high
- **Average rank of clicked result** — want low
- **Abandonment** — want moderately low
- **Deflection** (user resolved without contacting support) — want high

### Results
Query-specific Pagerank users: less likely to go past page 1, less follow-up searches, higher CTR, lower average clicked rank → better algorithm confirmed.

## Key Insight
"A high-quality and reliable labelled dataset is key. Online metrics provide valuable insights on user behaviour. Offline metrics enable fast iteration."

## Related Concepts

[[NDCG]] · [[Search Evaluation]] · [[Judgment Lists]] · [[A-B Testing for Search]]
