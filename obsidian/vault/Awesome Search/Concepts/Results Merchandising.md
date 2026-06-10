---
title: Results Merchandising
aliases:
  - results merchandising
  - search merchandising
  - searchandising
  - visual merchandising in search
  - search curation
tags:
  - concept
  - e-commerce-search
  - ranking
---

# Results Merchandising

## Definition

Results merchandising is the practice of applying business-driven curation to search result pages — manually or through business rules — to achieve commercial goals beyond pure relevance. It encompasses the full range of interventions between query submission and results display, from individual product pinning to campaign-level page takeovers.

Unlike pure relevance ranking or even [[Results Boosting]] (which adjusts scores algorithmically), merchandising often involves **manual editorial decisions** or **business policy enforcement** by non-engineering teams.

## Goals

Merchandising bridges the gap between what the search engine thinks is relevant and what the business needs to show:
- **Revenue optimization**: promote high-margin items
- **Inventory management**: surface overstocked items, suppress discontinued
- **Campaign support**: feature sale items, seasonal promotions, sponsored placements
- **Brand storytelling**: curate experiences that build brand affinity (see Discovery pillar)
- **Compliance**: suppress legally restricted products for certain regions/users
- **New product launch**: ensure new items get visibility before they have click signals

## Core Techniques

### Pinning
Force specific products to defined rank positions for a query or query pattern:
```
query: "running shoes" → position 1: Nike Air Max (current sale item)
```
Pins override the ranking entirely. Used for promotional campaigns, brand partnerships, A/B testing placement.

### Boosting and Burying
- **Boost**: elevate a product or category in results (see [[Results Boosting]])
- **Bury**: push to lower positions without removing
- **Block / Exclude**: prevent from appearing entirely

### Facet Merchandising
Control which filters appear on the search results page and in what order. Prominently featuring "Sale" or "New Arrival" facets drives discovery.

### Redirect Rules
Instead of showing results for a query, redirect to a curated landing page:
- `"summer sale"` → `/promotions/summer-2025`
- `"iphone 16"` → `/category/iphone/iphone-16`

### Synonym and Query Rule Overrides
Inject business intent at query understanding time:
- `"eco"` → also search for `"sustainable" OR "organic" OR "recycled"`
- `"laptop bag"` → boost `category:accessories`

### Enriched Results / Banners
Inject non-organic content into the result page:
- Promotional banners at specific positions
- "You might also like" carousels
- Editorial content or buying guides

## Merchandising Operations

In most e-commerce platforms, merchandising is managed by a business team (merchandisers or search managers), not engineers. Tooling requirements:
- **Rules engine**: query → action mappings with priority/conflict resolution
- **Preview**: see result page before rules go live
- **Scheduling**: activate/deactivate rules by date
- **Audit trail**: track who changed what and when
- **Reporting**: measure uplift from merchandising rules

## Merchandising vs. Ranking

| | Pure Ranking | Results Merchandising |
|---|---|---|
| Optimizes for | Relevance | Business outcomes |
| Owner | Search engineers | Business/merchandising team |
| Method | Model/algorithm | Rules, pins, manual curation |
| Granularity | All queries | Specific queries or categories |
| Transparency | Opaque (model) | Explicit rules |
| Risk | Ranking bugs | Rule conflicts, stale rules |

## Discovery and Visual Merchandising

Beyond functional boosting, merchandising in e-commerce encompasses the **discovery and inspiration** pillar of search quality:
- Visual presentation (image size, layout, badges like "Best Seller")
- Editorial curation that tells a product story
- Curated collections ("Complete the Look", "Staff Picks")

This extends into the search-recommendations boundary, where search becomes a discovery surface rather than purely a retrieval tool.

## Related Concepts

- [[Results Boosting]] — score-based subset of merchandising
- [[Economics of Search]] — business motivation for merchandising
- [[Personalization]] — user-specific variant of merchandising
- [[Query Understanding]] — query rules and redirects depend on query classification
- [[Faceted Search]] — facet ordering is a form of merchandising
- [[Search Intent]] — merchandising should align with detected intent

## Related Articles

- [[Ecommerce search optimization with margin & popularity boosting]]
- [[Three Pillars of Search Quality - Discovery and Inspiration]]
