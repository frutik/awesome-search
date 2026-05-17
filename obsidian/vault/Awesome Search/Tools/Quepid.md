---
title: Quepid
type: tool
tags:
  - tool
  - search-evaluation
  - relevance-testing
website: http://quepid.com/
repo: https://github.com/o19s/quepid
created: 2026-05-17
---

# Quepid

Open-source, web-based search relevance evaluation platform. Lets teams manage [[Judgment Lists|judgment lists]], run queries against a live search engine, and compute ranking metrics (NDCG, MRR, P@K) interactively. Built and maintained by [[OpenSource Connections]].

- Website: http://quepid.com/
- GitHub: https://github.com/o19s/quepid

---

## What It Does

Quepid is a "Test-Driven Relevancy" dashboard — the search equivalent of a unit test runner. You define test cases (query + expected relevant results), run them against your live search engine, and see metric scores per query and in aggregate.

Key workflows:
- **Judgment management** — create, import, and maintain relevance grades for query/document pairs
- **Metric scoring** — compute [[NDCG]], [[MRR]], [[Precision and Recall|P@K]] against your search engine in real time
- **Regression detection** — compare metric snapshots across index or config changes
- **Custom scorers** — write JavaScript scoring functions for non-standard metrics (e.g. custom NDCG@10)
- **Team collaboration** — shared cases and scores across the relevance team

## Scorer Architecture

Each Quepid test case runs a scorer — a JavaScript function with access to:
- `docs` — the result set returned by the search engine
- `bestDocs` — the ideal result set derived from judgments
- `setScore(value)` — outputs the final score for the query

This makes it straightforward to implement NDCG, DCG, or custom business metrics.

## When to Use Quepid vs. Scripts

| Quepid | Pandas / scripts |
|--------|-----------------|
| Interactive exploration | Large-scale batch evaluation (>100K results) |
| Team collaboration | CI/CD pipeline integration |
| Quick per-query inspection | Combining metrics with other signals |
| Non-technical stakeholder review | Custom analysis across many system variants |

## Related Tools
- **RRE** ([Rated Ranking Evaluator](https://github.com/SeaseLtd/rated-ranking-evaluator)) — CI/CD-oriented counterpart from [[Sease]]; batch evaluation
- **SMUI / [[Querqy]]** — complementary tool for managing query rewriting rules

## Related Concepts
- [[Judgment Lists]] — the input data Quepid manages
- [[NDCG]] — primary metric computed in Quepid
- [[MRR]] — secondary metric
- [[Search Evaluation]] — the broader practice Quepid supports
- [[A-B Testing for Search]] — offline eval in Quepid complements online A/B tests

## Related Articles
- [[Implementing NDCG Scorer in Quepid]]
- [[What Is a Judgment List]]
- [[Compute MRR using Pandas]]
- [[Probability-Proportional-to-Size Sampling for Relevance Evaluation]]
- [[Flavors of NDCG]]

## People
- [[Doug Turnbull]] — co-creator
