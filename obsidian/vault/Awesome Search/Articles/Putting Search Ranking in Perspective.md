---
type: article
tags: [article, ranking, query-understanding, relevance, personalization]
source: "https://dtunkelang.medium.com/putting-search-ranking-in-perspective-1b3094e38105"
author: [Daniel Tunkelang]
company: []
concepts: [Learning to Rank, Query Understanding, Personalization, Position Bias]
topics: [Query Understanding in Practice, Relevance Program Setup]
---

# Putting Search Ranking in Perspective

**[[Daniel Tunkelang]]** argues that ranking is valuable in search but not the primary lever — and explains the right priority order for relevance investments.

## The Priority Stack

1. **Query understanding first**: Ranking can't fix a misunderstood query. Invest in QU before sophisticated ranking.
2. **Relevance model (binary classifier) second**: Ensure retrieved results are all relevant before worrying about rank order.
3. **Query-independent signals third**: Popularity, freshness, quality — apply broadly across all queries.
4. **User-dependent signals fourth**: Personalization signals.
5. **Query-dependent signals last**: Prototypicality (how well a result fits the query's category/price distribution) and non-binary relevance from query relaxation.

## What a Ranking Model Can't Learn

A model learns only from signals that **searchers can see or infer** on the search results page. Invisible signals (e.g., return rate, profit margin) can be used as hand-crafted business rules, but **cannot be learned from click/purchase behavior**.

## Offline Evaluation

Replay search logs: re-rank the first page with the new model scores and compute MRR of clicks. A positive replay result is encouraging but not sufficient (presentation bias). A negative result is a warning sign but not definitive.

## Key Quote

"Ranking matters for search, but it is no substitute for query understanding and a robust relevance model."
