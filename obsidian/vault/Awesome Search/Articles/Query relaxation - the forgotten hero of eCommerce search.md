---
type: article
title: "Query relaxation: the forgotten hero of eCommerce search"
aliases:
  - "Query relaxation: the forgotten hero of eCommerce search"
source: https://aronnegyesi.medium.com/query-relaxation-the-forgotten-hero-of-ecommerce-search-219786238c98
author:
  - "[[Aron Negyesi]]"
published: 2026-11-12
created: 2026-11-13
paywall: true
companies:
  - "[[Rohlik]]"
concepts:
  - "[[Query Relaxation]]"
  - "[[Zero Results]]"
  - "[[Query Rewriting]]"
topics:
  - "[[E-commerce Search]]"
  - "[[Search UX]]"
tags:
  - article
  - paywalled
  - e-commerce
  - query-relaxation
  - zero-results
  - search-ux
---

# Query relaxation: the forgotten hero of eCommerce search

> [!warning] Paywall
> Medium member-only post. Key ideas only below; details are in the original.
> https://aronnegyesi.medium.com/query-relaxation-the-forgotten-hero-of-ecommerce-search-219786238c98

A product manager's case for judging [[Query Relaxation]] by conversion rather than by the [[Zero Results]] rate, by [[Aron Negyesi]] (12 November 2026). It starts from one failed spare-part search on a home improvement retailer's site and draws on his earlier work at [[Rohlik]].

## Key ideas

- **A relaxed query can still lose the sale.** A search for a filter cartridge by brand plus model codes returned four unrelated products. The engine seems to have kept the frequent words and dropped the rare, discriminating ones (brand and model code). Relaxing to brand plus product type would have ranked the right item first, despite the product missing its brand and model number in the catalog data. The author notes this is one query seen from outside, and that other long queries on the same site worked. See [[Query Relaxation]].
- **Measure conversion of relaxed searches, not just fewer empty pages.** At [[Rohlik]] the no-results share was cut from over 10% to 3%; a first relaxation A/B test pushed it to 1%, but relaxed queries converted at only 20% of the rate of normal ones. After switching to a term-selection method taken from a paper, no-results stayed at 1% and relaxed queries reached over 60% of the non-relaxed conversion. See [[Zero Results]].
- **Which word to drop depends on the query.** Product type usually matters most (a random screwdriver beats a random product of the named brand), but for spare parts and consumables the brand decides whether the item fits at all. [[Rene Kriegler - Query Relaxation]] is recommended for going deeper.
- **Tell the shopper what changed.** A generic "no exact results" message hides which words were ignored. Showing the original and relaxed query, a link to search the original anyway, or dropped words as removable chips lets the user repair the search. See [[Search UX]].
- **Fix the product data.** Fill in brands, ask sellers for model numbers, and use AI to read model numbers off product photos when that is the only place they appear.
- **A wrong result reads like an empty page.** Zero-results rate is easy to measure; irrelevant relaxed results are harder to see, but tell the customer the same thing.

## Related Notes

- [[Query Relaxation]] · [[Zero Results]] · [[Query Rewriting]]
- [[Rene Kriegler - Query Relaxation]] — the talk the post recommends
- [[Query Understanding - Query Relaxation]]
- [[E-commerce Search]] · [[Search UX]]
- [[Aron Negyesi]] · [[Rohlik]]
