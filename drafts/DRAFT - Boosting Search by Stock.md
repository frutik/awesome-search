---
type: article
title: "Boosting Search by Stock"
tags:
  - clippings
  - search
  - ranking
  - boosting
  - e-commerce
  - inventory
  - draft
source: "https://medium.com/@oleber_62556/boosting-search-by-stock-380ba199abc6"
author: "Marcos Rebelo"
published: 2026-09-12
created: 2026-09-12
concepts:
  - Results Boosting
  - Ranking Signal Selection
  - Ranking Objectives
topics:
  - E-commerce Search
---

# Boosting Search by Stock

> **DRAFT — not yet processed into the vault.** medium.com returns HTTP 403 to
> direct fetches (and to r.jina.ai / freedium mirrors), so the text was taken
> from the author's Medium RSS feed (`https://medium.com/feed/@oleber_62556`),
> which carried the full body. Run `kg-article-processing` / `kg-note-writing`
> on it to promote into the vault (entity extraction, cross-linking,
> `global_toc.md` update, History entry) once ready.

**Source:** https://medium.com/@oleber_62556/boosting-search-by-stock-380ba199abc6
**Author:** Marcos Rebelo (Medium `@oleber_62556`)
**Published:** 12 Sep 2026

## Summary

A short practitioner post on adding inventory to e-commerce ranking. The
argument is that the stock number already sitting in the product database —
total units on hand — is the wrong unit to rank on, because it says nothing
about how fast those units disappear. The fix is to convert stock into
**expected days of stock** (a time, not a count), which is comparable across
the whole catalog, and then fold it into the score as a saturating
multiplicative boost for abundance rather than a penalty for scarcity.

## The Motivating Case

A popular sofa with five units left in the warehouse counted as "in stock":
the listing page said so, the relevance model gave it full weight, and it sat
near the top of results for "grey sofa". It was also selling fifteen units a
day — so five units was closer to "gone by tonight" than "available".

The first attempt was a threshold on raw units (penalize anything below ~five
in stock) and it didn't hold up: five units of that sofa was effectively gone,
while five units of an accent chair selling twice a week was weeks of buffer.
Same number, opposite urgency. The author's framing of why the threshold
fails: any threshold on unit count is really a guess about a category's
typical pace, dressed up as a fact about one item.

## The Formula

Once stock is expressed in days, the boost is a single ratio folded into the
existing score:

```
final_score = base_relevance * boost
boost       = 1 + K * expected_days_of_stock / (expected_days_of_stock + half_life)
```

- At `expected_days_of_stock = 0` the fraction is zero and `boost = 1` — no
  bonus, the item ranks on relevance alone.
- As days of stock grow the fraction climbs toward 1 and the boost toward
  `1 + K`.
- **K** is the ceiling on how much stock can matter relative to relevance: a
  small K only breaks close ties, a larger one moves items further.
- **half_life** is the number of expected days of stock at which an item has
  earned exactly half the maximum boost (the fraction equals 0.5). It is what
  keeps the curve from being a step function: below it, gains come fast (half
  a day → two days of runway moves the needle a lot); above it, gains taper
  (thirty days → sixty barely changes anything, because thirty days was
  already comfortably safe). One knob, tuned per category to whatever
  "comfortably stocked" means for how fast that category sells.

The direction matters to the author: because it is framed as a boost for
abundance rather than a penalty for scarcity, an item is never pushed *below*
its relevance score for being low on stock — it simply stops earning the bonus
that better-stocked competitors get.

## Estimating Expected Days of Stock

```
expected_days_of_stock = total_stock / (a * M + (1 - a) * N),    0 < a < 1
```

- **M** — the item's own average daily sales; the most direct signal, when
  there is enough history behind it.
- **N** — average daily sales among the category's top sellers, standing in
  for "how fast an item like this typically moves".
- **a** — how much to trust the item's own number against the category
  benchmark. A brand-new listing has no real M (zero or one lucky sale tells
  you almost nothing), so leaning on N avoids treating an unproven item as
  either doomed or immortal; an item with months of steady history has an M
  worth trusting on its own.

The proposed way to set `a` is to let it move with how much history the item
actually has:

```
a = days_available_last_30 / 30
```

Available all 30 days → `a = 1`, the item's own sales history fully determines
its rate. Available 3 of 30 days → `a = 0.1`, almost entirely deferring to the
category benchmark. As the item accumulates selling days, `a` rises on its
own and the formula shifts its trust from the category average to the item's
proven pace — no separate rule for "new" versus "established" items, just the
same fraction recalculated as history accumulates.

## Stated Limitations

- It is an estimate, not a guarantee: M and N are both historical averages, so
  a sudden spike (a listing that goes viral overnight) burns through stock far
  faster than recent history predicts. The formula reacts a beat behind
  reality rather than ahead of it.
- `half_life` is presented as a good feature for the category owner to manage.
- `K` is tuned by hand in the described setup, though the author notes it
  could be learned.
- Closing claim: a formula built from sales counts and stock counts the system
  already tracked did more to keep search results buyable than the
  demand-forecasting model that would have been the "proper" way to solve it.

## Candidate Cross-Links (for promotion pass)

Existing notes this should attach to:

- [[Results Boosting]] — this is a field-value boost with a saturating
  transfer function; the note's boosting-types section is the natural home for
  the `d / (d + half_life)` shape.
- [[Signal Downboosting]] — direct contrast: the article's central design
  choice is boost-for-abundance instead of demote-for-scarcity.
- [[Ranking Signal Selection]] — the "raw units is the wrong unit, days of
  stock is the right one" argument is a signal-design argument.
- [[Ranking Objectives]] — buyability as an objective alongside relevance.
- [[Results Merchandising]] — business-signal promotion at query time.
- [[E-commerce Search]] (topic) — parent topic.
- [[Two-Sided Marketplace Ranking]] — adjacent, if inventory is seller-held.

Possible new notes:

- **Inventory-Aware Ranking** / **Stock-Aware Ranking** (concept) — nothing in
  `Concepts/` currently covers availability or inventory as a ranking signal;
  this is the clearest gap the article exposes.
- **Marcos Rebelo** (person) — not yet in `People/`. He has a run of related
  practitioner posts on the same Medium account worth queueing:
  *A Two-Line Formula for Freshness That Didn't Bury the Old Stuff*
  (10 Sep 2026), *Taming German Compound Words in Search (Without Breaking
  Everything Else)* (5 Sep 2026), *Let the Clicks Speak: A Simple Score for
  Popularity-Driven Ranking* (29 Aug 2026), *The cheap trick that fixed my
  Search Retrieval more than any fancy Embedding Model* (23 Aug 2026),
  *Serverless Search on AWS* (15 Aug 2024).

Note for whoever promotes this: the post names no company, no dataset, and
reports no measured result — the sofa is an anecdote and the "did more than
the demand-forecasting model" claim is unquantified. It is a design pattern
with a worked formula, not a case study, and should be written up as such.
