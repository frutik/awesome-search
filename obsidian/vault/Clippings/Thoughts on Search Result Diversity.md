---
title: "Thoughts on Search Result Diversity"
source: "https://dtunkelang.medium.com/thoughts-on-search-result-diversity-1df54cb5bf4a"
author:
  - "[[Daniel Tunkelang]]"
published: 2021-10-25
created: 2026-05-16
description: "More"
tags:
  - "clippings"
---
Regular readers know that search is about much more than ranking. If you’re new here, you might want to read this post about [ranking vs. relevance](https://dtunkelang.medium.com/ranking-vs-relevance-ba672c79625e).

But a topic I’ve neglected is search result diversity. I’ll remedy that in this post.

### Search result diversity is not for ambiguous queries.

Let’s start by clearing up a common misconception: search result diversity is **not** the right way to address query ambiguity. [Ambiguous queries are different from broad queries](https://dtunkelang.medium.com/broad-and-ambiguous-search-queries-1bbbe417dcc): ambiguous queries have unclear intent (e.g., does “mixer” refer to a kitchen appliance or an audio component?), while broad queries are unambiguous but underspecified (e.g., “shoes”).

Search result diversity is sometimes — but not always! — useful for broad queries, but never for ambiguous ones. ==The best way to address an ambiguous query is through a== ==[clarification dialogue](https://queryunderstanding.com/clarification-dialogues-69420432f451)== ==that establishes the searcher’s intent.== [A good query](https://dtunkelang.medium.com/better-search-through-better-queries-c192412a86e9) — that is, a query that the search engine can robustly map to an unambiguous intent — is a prerequisite for good results.

So search result diversity is a way to address some, but not all, broad queries. We’ll explore which broad queries benefit from result diversity, which aspects to diversify, and how to trade off result diversity against result desirability.

### Sometimes query refinements are better than result diversity.

When is is search result diversity appropriate? We’ve already explained that it’s not good for ambiguous queries, since a result set should not try to hedge between unclear, mutually exclusive intents. But some broad queries, even though they are unambiguous, create a similar challenge.

Consider the query “shoes”. It’s unambiguous, at least for practical purposes. But most people searching for shoes are looking specifically for men’s shoes, women’s shoes, or children’s shoes. They aren’t interested in seeing a diverse result set that jumbles all these kinds of shoes; rather, they want to see shoes that they (or the intended recipient) can wear.

For this and similar queries, search result diversity is not the right approach. Instead, searchers would benefit from [query refinements](https://queryunderstanding.com/faceted-search-7d053cc4fada) that allow them to narrow their results to men’s shoes, women’s shoes, etc.

### Result diversity works best for aspects that aren’t constraints.

Let’s turn to the query “men’s shoes”. Men’s shoes come in many styles and colors. Should we present these as query refinements?

There’s nothing wrong with offering [faceted search](https://queryunderstanding.com/faceted-search-7d053cc4fada) refinements. But many searchers don’t see the choice of style, color, or material as a hard constraint. They may have preferences, but they want to see all the available options.

This is where search result diversity shines. Searchers would like to see a diverse selection of relevant results that showcase the variety across a few aspects ([though not too many!](https://dtunkelang.medium.com/searching-for-goldilocks-12cb21c7d036)). Some searchers may want to use faceted navigation to treat one or more aspects as constraints. But search result diversity doesn’t force searchers to treat aspects as constraints.

### There’s a trade-off between result desirability and result diversity.

We’ve established that, for men’s shoes, result diversity is a great way to showcase the variety of styles and colors. But should we try to show all of these styles and colors on the first page of search results? Perhaps a few searchers want to buy lime green moccasins, but it’s likely that far more of them want to buy brown loafers. A completely random distribution of styles and colors would be unlikely to serve the majority of searchers well.

At the same time, the point of search result diversity is to serve a variety of preferences — to reflect not only the differences among searchers, but also the desire of an individual searcher to have diverse options. Even if brown loafers are the most desirable color-style combination, we wouldn’t want to show a whole page of them to everyone who searches for “men’s shoes”.

Instead we want to balance result desirability against result diversity. But how do we achieve an optimal balance between these two competing objectives?

### Use a framework to parameterize the balance between objectives.

Unfortunately, there’s no single answer on how to achieve an optimal balance. But there is a framework that you can use to parameterize it.

At one extreme, all that matters is result desirability. If diversity doesn’t matter at all, then the search engine can simply return relevant results in descending order of their desirability scores.

At the other extreme, diversity completely dominates desirability — that is, the most important concern is achieving a target distribution of aspect values, regardless of the desirability of any particular result. In that case, search should return an appropriately [stratified sample](https://en.wikipedia.org/wiki/Stratified_sampling) of results.

Note that the target isn’t necessarily a [uniform distribution](https://en.wikipedia.org/wiki/Discrete_uniform_distribution), e.g., some colors or styles may receive larger allocations than others. The target distribution could be based on historical searcher behavior, e.g., purchase behavior.

### Use a greedy algorithm to manage the trade-off.

In between these two extremes, there is a trade-off between result desirability and result diversity. We can model this trade-off as a [convex combination](https://en.wikipedia.org/wiki/Convex_combination) of desirability (e.g., a position-weighted average of the desirability of the ranked results) and diversity. We can compute the diversity score by penalizing the divergence (e.g., the [Kullback-Leibler](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence) divergence) of the distribution of aspect values on the first page of results from the target distribution.

Achieving an optimal trade-off is computationally expensive, since it involves exploring a [combinatorial explosion](https://en.wikipedia.org/wiki/Combinatorial_explosion) of options; but a practical alternative is to use a [greedy](https://en.wikipedia.org/wiki/Greedy_algorithm) approach that starts with the original order of results ranked by desirability and then sequentially reranks them to improve their diversity by reducing the divergence of the top-ranked results from the target distribution.

**To sum it up, be thoughtful about search result diversity.**

Search result diversity is a deceptively subtle topic. It doesn’t address ambiguous search queries. Nor is it helpful for aspects that represent searcher constraints, which are better served by query refinements. It’s useful for aspects that don’t represent constraints, but it still requires managing a trade-off with result desirability, as well as managing computational resources.

By all means, implement search result diversity when it’s appropriate. It can vastly improve the search experience. Just be thoughtful about it.