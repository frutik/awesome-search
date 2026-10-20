---
type: article
title: "Click Residuals – A Clever Way to Find Underperforming Queries"
source: "https://thesearchjuggler.com/click-residuals-a-clever-way-to-find-underperforming-queries/"
author:
  - "[[Charlie Hull]]"
published: 2026-10-20
created: 2026-10-20
description: "A practitioner's guide to Click Residuals — actual minus expected clicks per query — as a cheap, proactive way to find underperforming e-commerce queries, then enrich them with business value, exit rate, per-category CTR and pipeline data to prioritise and diagnose fixes."
tags:
  - search
  - search-evaluation
  - ecommerce
  - clicks
  - search-tuning
  - blog
concepts:
  - Clicks Residual
  - Click Signals
  - NDCG
topics:
  - Search Quality Assurance
  - Search Observability
---

# Click Residuals – A Clever Way to Find Underperforming Queries

[[Charlie Hull]] ([[The Search Juggler]]) writes up how he uses and extends **[[Clicks Residual|Click Residuals]] (CR)**, the query success metric first described by [[Walter Underwood]] in 2022 (see [[Click Residual - A Query Success Metric]]). CR is the difference between expected and actual clicks for a query; a negative value means people searched but didn't click as much as they should have.

---

## Why CR

Search teams tend to fix whichever failing query a senior person happens to report (the HiPPO effect). Tying individual queries to business outcomes like purchases is hard, and leadership often asks for conversion uplift without a clear way to get there. CR is a simple, proactive way to surface underperforming queries without that machinery.

## Computing It

Ask the analytics team for per-query frequency and clicks. Expected clicks = query frequency × site-wide average click rate (total clicks ÷ total searches); CR = actual − expected.

Hull's toy example, "My Online Chip Shop" (45,803 searches, 102,750 clicks, average 2.243 clicks per search):

| Query | Frequency | Actual clicks | Expected clicks | CR |
|---|---|---|---|---|
| fish | 885 | 2708 | 1985 | 723 |
| chips | 2207 | 6650 | 4950 | 1700 |
| vinegar | 320 | 223 | 717 | -494 |
| sosages | 187 | 102 | 419 | -317 |

Negative residuals point at problems such as weak typo handling ("sosages") or thin product range. Sorting by residual and frequency shows trends, and clustering queries exposes whole underperforming groups. In past client work these included misspellings, queries about animals and football teams, and "functional" queries like "returns policy". Some low CR comes from outside search, such as category-like searches that return irrelevant products or distracting banner ads.

## Prioritising

To judge business benefit, add query volume, business value by subject area, average order value, and exit rate. Negative CR plus a high exit rate is a strong dissatisfaction signal. Low-volume problems may not be worth fixing.

## Adding More Data

The basic method assumes one average CTR for the whole site, but behaviour varies by intent. Computing CTR per category (e.g. kitchen appliances vs. cleaning supplies) gives fairer expectations. Further context:
- which query pipeline stages fired, such as [[Spelling Correction|spell correction]] or business rules
- relevance metrics such as [[NDCG]], because results can be relevant yet rarely clicked due to price or stock

## Acting on Findings

Log issues in a tracker. Discuss options with the business, which may be stock, UX or algorithm changes. Test fixes offline on a sample of queries, then monitor online with fresh click data.

## Takeaway

CR tells you *that* a query underperforms, not *why*. Layering in more data is what turns it into a tool for prioritisation and diagnosis.

---

## Related Concepts
- [[Clicks Residual]] — the metric itself
- [[Click Signals]] — the behavioural data CR is built from
- [[NDCG]] — complementary judgement-based relevance metric
- [[Zero Results]] — another query-level failure signal

## Related Articles
- [[Click Residual - A Query Success Metric]] — Underwood's original definition
- [[How to Securely Hook Up Quepid to Vespa]] — another Hull piece on offline relevance testing

## People
- [[Charlie Hull]] — author
- [[Walter Underwood]] — originator of the metric

## Topics
- [[Search Quality Assurance]] · [[Search Observability]]
