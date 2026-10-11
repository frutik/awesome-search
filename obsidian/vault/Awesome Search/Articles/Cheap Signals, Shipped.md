---
title: "Cheap Signals, Shipped: Marcos Rebelo's E-commerce Search Series"
type: article
tags:
  - article
  - e-commerce
  - ranking
  - retrieval
  - reading-list
  - opinion
author:
  - "[[Andrew Kornilov]]"
published: 2026-10-11
created: 2026-10-11
concepts:
  - "[[Learning to Rank]]"
  - "[[Position Bias]]"
  - "[[Click Signals]]"
  - "[[Results Boosting]]"
  - "[[Ranking Signal Selection]]"
  - "[[Synonyms]]"
  - "[[Hybrid Search]]"
  - "[[Dense Embeddings]]"
  - "[[LLM as Judge]]"
topics:
  - "[[E-commerce Search]]"
  - "[[Query Classification]]"
  - "[[Search Result Diversity]]"
  - "[[Synonyms and Vocabulary Management]]"
---

# Cheap Signals, Shipped: Marcos Rebelo's E-commerce Search Series

*A reading recommendation. If you work on [[E-commerce Search|e-commerce search]], follow [Marcos Rebelo on Medium](https://medium.com/@oleber_62556). The posts are member-only, so below is just what each one argues. The detail is worth reading in the originals.*

Most search writing right now is about the newest model: bigger embeddings, LLM rerankers, agentic retrieval. Since August, Marcos Rebelo has been writing the opposite kind of post. Each one is short, starts from a real failure (a sofa about to sell out, "gato" bringing up furniture, "garden hose" returning no hoses), and ends with a fix built from data the shop already had: conversion logs, click positions, stock counts, session reformulations.

The posts share a view I agree with. The improvements that last tend to be small, easy to explain, and based on what users actually did. Before reaching for a bigger model, check whether a GROUP BY already answers the question. Each fix comes with one or two tuning parameters that a merchandiser could understand, and each post says honestly where the trick stops working.

Here are the seven posts, in the order they were published.

## 1. The cheap trick that fixed my Search Retrieval more than any fancy Embedding Model (Aug 2026)

**Query-to-category probabilities.** Estimate, for each query, which product categories its searchers actually convert in ([[Query Classification]]). Then use that distribution twice: as a hard filter that removes wrong-category candidates before ranking, and as a soft feature in [[Learning to Rank|learning-to-rank]]. For head queries you need no model. Aggregate the logs, sort categories by conversion share, and keep adding them until a high cumulative threshold (95–98%) is reached, with a cap on how many. A query whose conversions spread across many categories is ambiguous, and that is a reason not to filter it. For the tail, a small fastText-style multilabel model extends the same logic to typos, rephrasings and other languages. The real failures it fixed make the case: "tisch" returning lamps, "gato" returning furniture from a brand with a similar name, and "espelho retrovisor" returning whole cars. Embeddings measure similarity. Conversion data measures what people buy.

## 2. Let the Clicks Speak: A Simple Score for Popularity-Driven Ranking (Aug 2026)

**Clicks relative to position.** For each product, add up the average click-through rate of every position it was shown at. That is how many clicks an average product would have earned from the same placements. Divide the clicks it actually got by that number, and add a smoothing constant to both sides so items with few impressions settle near 1.0 instead of producing extreme ratios. The result is a model-free score that corrects for [[Position Bias|position bias]] using [[Click Signals|clicks]]. You can rank by it directly or feed it into LTR as a feature. The "men jeans" example is the interesting part. A model that generalizes fills the top results with nearly identical blue jeans. A black pair at position 9 that gets more clicks than position 9 predicts moves up. [[Search Result Diversity|Diversity]] comes from correcting position bias, not from a separate diversification rule.

## 3. Boosting Search by Stock (Sep 2026)

**Count stock in days, not units.** Five units means nothing until you know how fast they sell. Convert stock to *expected days of stock* and the number becomes comparable across the whole catalog. The sales rate mixes the item's own sales history with a category benchmark, and the item's own history gets more weight the more days it has been available, so new listings lean on the category average. The [[Results Boosting|boost]] is a saturating curve with two parameters: a ceiling on how much stock can matter compared with relevance, and a per-category "half-life" for the point where the boost is half earned. It is framed as a bonus for having plenty of stock, not a penalty for having little, so nothing ever ranks below its relevance score. A formula built from stock and sales counts the system already tracked did more than the demand-forecasting model that would have been the "proper" solution.

## 4. The Leash That Kept Vector Search on Topic (Sep 2026)

**Guard vector search instead of retraining it.** Blending in nearest-neighbour results ([[Hybrid Search]]) fixed vocabulary mismatches ("warm jacket" vs "insulated shell parka") but also brought in nonsense, such as dog collars for "apple watch band". Retraining [[Dense Embeddings|embeddings]] meant retraining and hoping. The fix that shipped sits in front of vector search: a nightly SQL lookup of which L2 categories each frequent query's purchases fall into, plus a lightweight fastText classifier for queries the table doesn't cover. The vector results are filtered to plausible categories, and the embeddings are left untouched. The classifier only has to rule out impossible categories, not work out exactly what the shopper meant. The hard part is choosing how strict the filter is. This is post #1's idea applied as a guard on dense retrieval.

## 5. Fading Out of Stock from Search, Instead of Yanking It (Sep 2026)

**Fade sold-out items gradually.** Removing items the moment stock hits zero, or after a fixed three days, treats "gone for an hour" and "gone for two months" the same way. A model that predicts restock timing was rejected as too noisy and impossible to explain to merchandisers. What shipped is exponential decay: an out-of-stock item loses a share of its score every day, at a per-category half-life (short for phone cases, long for furniture). Recently sold-out items stay visible, so shoppers can still sign up for restock alerts. Long-gone items sink without anyone deleting them. That gives one parameter per category, and it can be explained in a sentence.

## 6. Synonyms Are a Maintenance Nightmare — Here's the Shortcut That Mostly Works (Sep 2026)

**Mine [[Synonyms|synonyms]] from reformulations.** A hand-maintained synonyms file goes out of date and only ever gets longer ([[Synonyms and Vocabulary Management]]). Users already solve the problem themselves: within one session they search, get no click, rephrase, and click. Mine those pairs. Drop pairs that don't recur, and drop pairs that are only a few characters apart (typos, plurals). Then ask an LLM one narrow question about each remaining pair ([[LLM as Judge]]): same intent or not? It catches cases a string-distance check misses, like "sofa" → "sofa bed", where the second query is narrower rather than a synonym. Spot-check before shipping. The limits are stated honestly: this finds nothing for brand-new terms until users have already been frustrated, and it never sees users who give up instead of retrying. A thin manual layer still covers what is new or high-stakes.

## 7. The Weekly Hour that beat a Relevance Model — Reading the Top Queries that get no Clicks (Oct 2026)

**Rank queries by lost clicks, then look at them.** A relevance model scored "garden hose" as fine while it returned only connectors and reels. A category migration had left a filter pointing at the wrong category. A relevance model assumes the right products are in the result set and checks the order. It cannot see a broken eligibility rule. Sorting queries by CTR surfaces junk, and sorting by volume surfaces healthy queries. What works is sorting by clicks lost compared with a typical query's CTR. Each Monday, an analyst and a merchandiser go through the top 50, run each search live, and assign it to one of four causes: broken filter or rule, bad data, missing product, or ranking. Ranking turned out to be the smallest group. Its stated limits: it only sees busy queries, it needs a list of zero-click queries that are known to be fine, it catches problems after shoppers hit them, and it only works as long as the hour keeps happening.

## Why read them together

Read together, the posts form a working toolkit. You get query→category priors for filtering and guarding retrieval (#1, #4). You get two behaviour-based [[Ranking Signal Selection|ranking signals]]: clicks corrected for position (#2) and stock measured in days (#3). You get a stock policy based on decay instead of a hard cutoff (#5), a synonyms list that maintains itself (#6), and a weekly routine that catches what models miss (#7). None of it needs a GPU, and almost all of it can be explained to a merchandiser in a sentence. The posts are short and specific, and they have clearly been run in production.
