---
type: company
industry: classifieds marketplace
category: e-commerce
website: "https://www.kleinanzeigen.de"
search_domain: personalized homepage feed, classified ad retrieval
---

# Kleinanzeigen

Germany's largest online classifieds marketplace, serving millions of users daily. Formerly known as eBay Kleinanzeigen. Operates one of the highest-traffic homepage personalized feeds in European e-commerce.

## Search Engineering

Kleinanzeigen migrated their homepage feed from [[Elasticsearch]] to [[Vespa]], moving user behavioral profile management, scoring, and retrieval inside the search engine itself. The key motivation was eliminating an external orchestration layer that required round-trips for every new behavioral signal.

### Architecture Highlights

- **Three document schemas in Vespa**: `ads`, `user_category_profile`, `relations`
- **WAND retrieval**: sparse inner-product matching over `field.value` attribute tokens (e.g., `color.red`, `brand.bmw`) without full corpus scan
- **In-engine profile updates**: a Vespa document processor intercepts click events and updates user profiles in-process — no external profile store
- **Token similarity propagation**: a `relations` document defines similarity coefficients between attribute tokens, allowing partial weight sharing (e.g., `color.red` → `color.blue`)
- **Signal decay**: click-derived attribute weights decay over time and are L2-normalized

## People

- [[Andre Charton]] — engineer, author of the Vespa migration writeup

## Case Studies

- [[Kleinanzeigen - Vespa Migration for Homepage Feed]]

## Articles

- [[From Elasticsearch to Vespa - Rebuilding the Kleinanzeigen Homepage Feed Part 1]]

## Concepts

[[WAND]] · [[Personalization]] · [[Click Signals]] · [[Sparse Vector Retrieval]] · [[Vespa]]
