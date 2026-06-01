---
title: "From Elasticsearch to Vespa: Rebuilding the Kleinanzeigen Homepage Feed — Part 1"
type: article
tags: [article, vespa, personalization, wand, homepage-feed, e-commerce, case-study, medium]
source: "https://medium.com/berlin-tech-blog/from-elasticsearch-to-vespa-rebuilding-the-kleinanzeigen-homepage-feed-part-1-b6164e366ab8"
author:
  - "[[Andre Charton]]"
company:
  - "[[Kleinanzeigen]]"
published: 2026-05-22
created: 2026-05-26
concepts:
  - "[[WAND]]"
  - "[[Personalization]]"
  - "[[Click Signals]]"
  - "[[Sparse Vector Retrieval]]"
  - "[[Dense Vector Retrieval]]"
topics:
  - "[[Personalization in Search]]"
  - "[[E-commerce Search]]"
tools:
  - "[[Vespa]]"
  - "[[Elasticsearch]]"
---

# From Elasticsearch to Vespa: Rebuilding the Kleinanzeigen Homepage Feed — Part 1

**Author:** [[Andre Charton]] ([[Kleinanzeigen]])
**Source:** https://medium.com/berlin-tech-blog/from-elasticsearch-to-vespa-rebuilding-the-kleinanzeigen-homepage-feed-part-1-b6164e366ab8
**Published:** 2026-05-22

## Summary

[[Kleinanzeigen]] rebuilt their homepage feed (the first screen millions of users see) by migrating from [[Elasticsearch]] to [[Vespa]], moving profile learning, scoring, and retrieval *inside* the search engine. This eliminates an external orchestration layer and allows user behavioral profiles to update in-process with no external profile store.

## Why They Left Elasticsearch

The core problem: too much work happened *outside* the search engine. Profile learning, scoring, and retrieval were stitched across multiple services. Every new signal (click, keyword, explicit preference) required a round-trip through their orchestration layer.

They needed a platform that could:
- Store and query user behavioral profiles alongside ads in the same engine
- Use **[[WAND]]** for fast inner-product retrieval over sparse attribute vectors without full scans
- Run embedding-based ANN search natively, close to the data
- Process click and search events as document updates within the platform itself

## Three Document Schemas

The data model uses three schemas in a single content cluster:

**`ads`** — each classified ad. Item attributes modeled as `weighted_set<string>` with a `field.value` token format (e.g., `color.red`, `brand.bmw`). This lets a single WAND query run across all structured attributes without secondary indices.

**`user_category_profile`** — one document per user per category, keyed as `{userId}:category:{categoryId}`. Contains:
- Click-derived attribute weights (L2-normalized)
- Last N search keywords
- Last clicked document IDs (for exclusion)
- Geolocation and explicit preferences

**`relations`** — a global config document per category (replicated to all nodes). Defines field importance weights and **token similarity groups with propagation coefficients** — allowing `color.red` to contribute partial weight to `color.blue` during retrieval.

## Phase 1: WAND-Based Click Profile Matching

When a user clicks an ad, a document update fires to Vespa. A **Vespa document processor** intercepts this update, asynchronously reads the clicked ad's attributes and the existing user profile, and merges them in-process:
- Existing signals decay over time
- New click is merged in
- Profile is trimmed to keep only the strongest features

The updated profile **stays inside Vespa** — no external profile store, no service hop at query time.

At query time:
1. Read user profile
2. Expand tokens through the relations graph (propagate weights to similar attributes)
3. Fire a WAND query against the ads index

Vespa's [[WAND]] implementation guarantees only promising candidates are fully evaluated — no full corpus scan even with millions of ads.

## Key Insight

> "Vespa could own the full click-profile loop end-to-end. User behavior updates, profile maintenance, and retrieval all happened inside the serving platform itself, without external orchestration or profile storage."

Click history alone only tells part of the story — Part 2 covers integrating explicit preferences, advanced ranking strategies, and semantic retrieval.

## Related Concepts

- [[WAND]] — core retrieval algorithm for sparse inner-product matching
- [[Personalization]] — click profile matching as in-engine personalization
- [[Click Signals]] — behavioral signals driving profile updates
- [[Sparse Vector Retrieval]] — attribute weights as sparse vectors
- [[Dense Vector Retrieval]] — ANN search planned for later phases

## Related Notes

- [[Adopting Vespa for Recommendation Retrieval at Vinted]] — similar Vespa migration in e-commerce
- [[Kleinanzeigen - Vespa Migration for Homepage Feed]] — case study note
- [[E-commerce Search and Recommendation with Vespa]]
