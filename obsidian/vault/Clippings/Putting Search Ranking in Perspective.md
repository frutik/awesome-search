---
title: "Putting Search Ranking in Perspective"
source: "https://dtunkelang.medium.com/putting-search-ranking-in-perspective-1b3094e38105"
author:
  - "[[Daniel Tunkelang]]"
published: 2021-06-04
created: 2026-05-16
description: "More"
tags:
  - "clippings"
---
For feeds and recommendations, ranking is critical. All the inputs are implicit, so machine-learned ranking is the only practical way to optimize engagement.

### Search is different.

A search engine elicits the searcher’s explicit intent, expressed as keywords, and this explicit intent is, by far, its most valuable input. Searchers, quite understandably, expect results that are relevant to their expressed intent. Ranking is still valuable, but it plays less of a role than for other applications.

### Foremost, ranking should respect query understanding.

Before a search engine retrieves and ranks results, [query understanding](https://queryunderstanding.com/introduction-c98740502103) [maps the query to a representation of searcher intent](https://dtunkelang.medium.com/search-queries-and-search-intent-1dec79ad155f). Good ranking depends on robust query understanding. Investing in sophisticated ranking models is premature if your search engine cannot understand the searcher’s query.

### Ranking should focus primarily on query-independent signals.

Once query understanding establishes a robust representation of searcher intent, a [relevance model](https://dtunkelang.medium.com/the-3-rs-of-search-relevance-recall-and-ranking-c9a785578653) should ensure that the retrieved results are all relevant. A relevance model is essentially a binary classifier. Ranking is not a substitute for a relevance model, as becomes evident when searchers override the default ranking, e.g., to [sort by price](https://dtunkelang.medium.com/why-is-it-so-hard-to-sort-by-price-2a5e63899233).

To a first approximation, query understanding and the relevance model establish relevance as a binary filter. That allows ranking to focus primarily on query-independent signals of desirability, like popularity, and secondarily on user-dependent signals that can be used for personalization.

### Two reasons to use query-dependent signals for ranking:

- **Prototypicality.** For example, a query can be associated with a category or price distribution of results. There can be query-dependent prototypicality signals reflecting how a result fits into these distributions.
- **Non-binary relevance.** There may be gradations of relevance — particularly when a search engine uses [query relaxation](https://queryunderstanding.com/query-relaxation-342bc37ad425) to increase recall. The relevance model score can serve as a query-dependent ranking signal.

But don’t invest in query-dependent ranking signals until you have at least established a robust relevance model and strong query-independent signals.

### A ranking model only learn from signals that searchers see or infer.

Ranking can draw on many sources for signals. Some content signals, such as result title or structured data fields (like brand or price), are clearly visible on the search results page. There are also signals that a searcher can often infer from the search results page, such as category or image quality. Finally, there are feedback signals, such as average rating and number of reviews, that are usually displayed on the search results page. All of these signals can influence search behavior, and thus they are fair game for training a ranking model.

But a model cannot learn from signals that searchers can neither see nor infer. If a signal is not available on the search results page, it cannot influence the searcher’s decision to click on a result. If it is not available on the listing page, then it cannot even influence further actions, like purchases.

You can use these invisible signals for ranking. **But they cannot be learned from searcher behavior.** Instead, you determine their contribution through hand-crafted business rules, e.g., demoting products with high return rates.

### A/B-testing is the gold standard, but offline evaluation is possible.

The only way to know that a ranking change is an improvement is to run an A/B test on enough traffic to obtain a statistically significant outcome. For a change that only affects a small fraction of queries, you should [scope the A/B test](https://dtunkelang.medium.com/a-b-testing-for-search-is-different-f6b0f6f4d0f5) — and the analysis — to the affected search sessions.

But you can still perform an offline evaluation as a sanity check. You can replay search logs, re-rank the displayed results (i.e., the first page) using the new model scores and see how the new positions of reranked results affect metrics like the [mean reciprocal rank](https://en.wikipedia.org/wiki/Mean_reciprocal_rank) (MRR) of clicks.

If the replay analysis shows an improvement, then the new ranking model is positive — at least when it is used as a re-ranker. If not, it’s still possible that it’s an improvement — but that you cannot learn from the replay because of presentation bias. After all, searchers can only engage with the results they see. Nonetheless, a neutral or negative result from reply should at least make us skeptical as you decide how to prioritize an A/B test.

### Summary: keep ranking in perspective, and rank wisely.

Ranking matters for search, but it is no substitute for query understanding and a robust relevance model. Ranking should focus first on query-independent signals for desirability and second on user-dependent signals for personalization. Only then should it consider query-dependent signals for prototypicality or non-binary relevance. A ranking model can only learn from signals that searchers can see or infer. Finally, while online A/B-testing is the gold standard, offline evaluation using log replay is useful as a sanity check.