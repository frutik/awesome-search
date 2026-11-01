---
title: "Search golden sets are anything but"
type: article
tags: [article, search-evaluation, metrics, judgment-lists, ndcg]
source: "https://softwaredoug.com/blog/2026/10/26/search-golden-sets-fail"
author:
  - "[[Doug Turnbull]]"
published: 2026-10-26
created: 2026-10-30
concepts:
  - "[[NDCG]]"
  - "[[NDCG-m]]"
  - "[[NDCG-f]]"
  - "[[Rank-Biased Overlap]]"
  - "[[Judgment Lists]]"
  - "[[Search Evaluation]]"
  - "[[Session-Based Evaluation]]"
  - "[[LLM as Judge]]"
  - "[[Precision and Recall]]"
  - "[[BM25]]"
  - "[[BlitzRank]]"
topics:
  - "[[Relevance Program Setup]]"
datasets:
  - "[[Amazon ESCI Dataset]]"
  - "[[WANDS Dataset]]"
  - "[[BEIR]]"
people:
  - "[[Max Irwin]]"
---

# Search golden sets are anything but

[[Doug Turnbull]]'s argument that offline evaluation against a golden set of query-document judgments often fails to predict what users experience, and that the way out is narrower, more conservative evals rather than one headline number.

---

## Judgment Lists and the Metrics

A golden set is a [[Judgment Lists|judgment list]]: queries paired with graded results, the "classic research eval regime" of [[BEIR]]-style retrieval datasets that the post sets out to critique. The examples use [[Amazon ESCI Dataset]] (3 for relevant, 0 for irrelevant, with intermediate grades) and [[WANDS Dataset]], with the query "!awnmower tires without rims". A worked example walks through Precision@5, DCG@5 and [[NDCG]]@5 ([[Precision and Recall]]), weighting by 1/rank for simplicity — the post notes real DCG uses 1/log2(rank): DCG@5 of 4.0 against an ideal of 6.35 gives an NDCG of about 0.63.

## Problem 1: A Poor Ideal

When a query has few relevant results in the corpus, NDCG can reach 1 while users are still unhappy, because the ideal ordering is built from whatever the corpus holds. The fix proposed is [[NDCG-m]] (Max NDCG), named in honor of [[Max Irwin]], who argued for this definition: normalise against a fixed ideal of all maximum grades, so the score reflects corpus coverage as well as ranking. The post reports an average NDCG-m@10 of about 0.77 for WANDS and closer to 0.93 for ESCI, which suggests WANDS has more queries with few relevant results.

## Problem 2: Missing Labels

Unlabeled results are often relevant, and labeling often covers only the current top results of the current ranking algorithm — the post's example is raters labeling the top 10 of [[BM25]]. The post ties this to feature discovery: labeling and feature discovery move hand in hand, so measure where labels systematically miss and introduce new features worth exploring with users.

## NDCG-f

[[NDCG-f]] (filtered) ignores unlabeled results and computes NDCG over the labeled ones only. It answers a narrower question — does the system order known-relevant results above known-irrelevant ones? — which makes it useful for catching regressions, not for predicting A/B test winners.

## Evals as Unit Tests

NDCG is most useful for checking that your own implementation behaves as intended. Problems start when search metrics are communicated outside the search team: offline evals then stop serving well, because management has to be educated on sampling bias.

## Don't Rely on One Evaluation

Alternatives named: [[Rank-Biased Overlap]] to measure the quantity of change in results, side-by-side expert review, unit-test-style checks (results for "red shoes" should be footwear), [[Session-Based Evaluation|session-level clickstream evaluation]], and [[LLM as Judge]] approaches such as [[BlitzRank]]. The recommendation is to keep evals narrow, conservative and manageable, with ongoing labeling.

## Related Concepts
- [[NDCG]] · [[NDCG-m]] · [[NDCG-f]] · [[Rank-Biased Overlap]] · [[Judgment Lists]] · [[Search Evaluation]]
- [[Session-Based Evaluation]] · [[LLM as Judge]] · [[BlitzRank]]

## Related Articles
- [[Session vs Query based Search Evals]] — the session-versus-query argument the post points to
- [[Bag of Decisions Reranker]] — another Turnbull experiment on WANDS and ESCI

## People
- [[Doug Turnbull]] · [[Max Irwin]]
