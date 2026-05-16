---
title: Results Boosting
aliases:
  - results boosting
  - score boosting
  - search boosting
  - ranking boost
tags:
  - concept
  - ranking
  - e-commerce-search
---

# Results Boosting

## Definition

Results boosting is a technique for adjusting the relevance scores of search results at query time to promote or demote specific items based on business signals, behavioral data, or business rules — without changing the underlying relevance model.

Boosting operates by multiplying or adding to a document's baseline relevance score. A boosted document rises in the ranking; a "buried" document falls.

## Types of Boosting

### Field Value Boosting
Promote documents based on a numeric field:
```json
{
  "function_score": {
    "field_value_factor": {
      "field": "popularity_score",
      "modifier": "log1p",
      "factor": 1.5
    }
  }
}
```

Common signals:
- **Popularity**: sales rank, click count, conversion rate
- **Margin**: profit per item
- **Freshness**: recency of publication or inventory update
- **Rating**: average customer review score
- **Stock level**: available-to-ship quantity

### Categorical / Rule-Based Boosting
Boost or demote entire categories of results:
- Promote sponsored products
- Promote items with free shipping
- Demote out-of-stock items
- Exclude discontinued products

### Personalized Boosting
Adjust scores per user based on:
- Purchase history and brand affinity
- Browsing behavior
- Loyalty tier
- Location and delivery constraints

### Pinning and Blocking
Extreme forms of boosting:
- **Pin**: force a document to a specific rank position (rank 1, 2, …)
- **Block**: prevent a document from appearing entirely
- **Bury**: push to bottom of results

## Boosting vs. Merchandising

Boosting adjusts **scores** — the ranking algorithm still determines order, but scores are modified. [[Results Merchandising]] is a broader practice that includes pinning, campaigns, and manual curation that overrides the ranking entirely.

## Boosting in Elasticsearch

Elasticsearch `function_score` query supports multiple boost functions:
- `field_value_factor` — multiply score by a field value
- `gauss/linear/exp` decay — proximity-based boost (e.g., distance, recency)
- `script_score` — arbitrary scoring logic
- `random_score` — controlled randomization for exploration

Multiple functions can be combined with `score_mode` (multiply, sum, avg, max, min).

## Calibration

Boost factors must be calibrated so one signal doesn't overwhelm relevance:
- Use logarithmic scaling (`log1p`) to compress large value ranges
- Normalize signals to comparable ranges before combining
- A/B test boost changes to measure revenue impact vs. relevance degradation
- Monitor for **boost gaming**: sellers artificially inflating popularity signals

## Tradeoffs

| Benefit | Risk |
|---------|------|
| Aligns ranking with business objectives | Can overwhelm relevance signal |
| Responds quickly to business changes | Hard to maintain as rules multiply |
| No retraining needed | May create feedback loops (popular items get more clicks → more popular) |
| Transparent and auditable | Margin/popularity boost may conflict with user intent |

## Related Concepts

- [[Results Merchandising]] — higher-level curation that includes boosting
- [[Learning to Rank]] — model-based alternative to manual boosting
- [[Personalization]] — user-specific boosting
- [[Economics of Search]] — business motivation for boosting
- [[Position Bias]] — boosting can create or amplify position bias

## Related Articles

- [[Ecommerce search optimization with margin & popularity boosting]]
