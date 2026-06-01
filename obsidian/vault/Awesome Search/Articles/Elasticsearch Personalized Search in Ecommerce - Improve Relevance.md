---
title: "Elasticsearch Personalized Search in Ecommerce: Improve Relevance"
source: "https://www.elastic.co/search-labs/blog/elasticsearch-personalized-search-governed-ecommerce"
author:
  - "[[Alexander Marquardt]]"
  - "[[Honza Král]]"
  - "[[Taylor Roy]]"
published: 2026-05-11
company: "[[Elastic]]"
tags: [ecommerce-search, personalization, purchase-history, cohort-search, search-governance, company-blog]
series: "Governed Search Patterns (Part 6)"
---

# Elasticsearch Personalized Search in Ecommerce: Improve Relevance

**Authors:** [[Alexander Marquardt]], [[Honza Král]], [[Taylor Roy]] ([[Elastic]])

## Summary

Part 6 of the Governed Search Patterns series. Introduces two personalization mechanisms that extend the governed control plane: **individual purchase history boosting** and **cohort-aware policy activation**. Both integrate with the governance layer rather than replacing it — governance controls what appears; personalization adjusts ordering within the governed result set.

## Core Principle

Personalization is not a separate system bolted alongside search; it's a **natural extension of the policy-driven control plane**. Governance still fires, constraints are still enforced, conflicts are still resolved — personalization signals compose multiplicatively on top.

## Mechanism 1: Individual Purchase History Boosting

If a shopper bought a product before, boost it when they search for related terms.

### How It Works
When a search request includes a user ID, the control plane runs two Elasticsearch queries **in parallel**:
1. Percolator query against policy index (governance)
2. Purchase history query against `user_purchases` index (personalization)

Neither waits for the other — no latency impact.

### Boost Weight Formula
- **Frequency**: logarithmic scaling (prevents one heavily-purchased item from dominating)
- **Recency**: exponential decay (older purchases fade naturally)

### Key Design Choice
Query Elasticsearch on every search rather than cache — uses Elasticsearch's text analysis (stemming, tokenization) to match "cookies" against past purchase "brownie cookies".

### Governance Holds
A purchase history boost for "orange juice" has no effect if governance has constrained "oranges" to produce category (filtering out orange juice). Governance controls the result set; personalization adjusts ordering within it.

## Mechanism 2: Cohort-Aware Policy Activation

For new/anonymous shoppers, cohort membership provides personalization based on who the shopper is, not what they've done.

### Cohorts as Policies (Not Product Tags)
Rather than hard-coding `if user.is_vegan: boost dietary_restrictions:vegan`, cohort logic lives in the **policy engine** as a governed document:
- **Cohorts**: `["vegan"]`
- **Match criteria**: any query (or specific category)
- **Action**: soft boost on `dietary_restrictions: "vegan"` with weight 2

### How It Works at Query Time
The percolator query includes a `terms` filter:
```json
{ "terms": { "cohorts": ["_all", "vegan", "health_conscious"] } }
```

Universal policies (_all) + user's cohort-specific policies — clean, no special handling needed.

### Benefits
- Adding a new cohort = creating one policy, no product reindexing
- Cohort policies use full rule engine (filters, boosts, synonyms, routing)
- Managed through same Admin UI as all other policies

## Layered Query Architecture

From innermost to outermost:
1. **Base query** — keyword/semantic match
2. **Governance policy layer** — hard filters + soft boosts
3. **Business-signal boosts** — margin and popularity (Part 7)
4. **Purchase history boosts** — outermost layer

This ordering ensures governance controls the result set; business signals and personalization adjust ordering within it.

## Operational Properties Preserved

- **Zero-deploy** — cohort policies created/promoted through admin UI, no engineering
- **Auditability** — every cohort policy is a discrete, versioned document
- **Conflict resolution** — cohort policies participate in same per-field conflict resolution
- **Measurability** — individually toggleable → independent impact measurement

## Related Concepts

- [[Personalization]] — the broader concept
- [[Search Governance]] — the governance layer that personalization extends
- [[Click Signals]] / [[Results Boosting]] — related personalization signals

## Series

- Part 1: [[Why Ecommerce Search Needs Governance and How It Improves Retrieval]]
- Part 2: [[Ecommerce Search Governance - Move Faster Not Slower]]

## People

- [[Alexander Marquardt]]
- [[Honza Král]]
- [[Taylor Roy]]
