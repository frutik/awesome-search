---
type: article
title: "Search Quality Assurance with AI as a Judge"
source: "https://engineering.zalando.com/posts/2026/03/search-quality-assurance-with-llm-judge.html"
author:
  - "[[Tao Ruangyam]]"
published: 2026-03-17
created: 2026-05-31
concepts:
  - "[[LLM as Judge]]"
  - "[[Named Entity Recognition]]"
  - "[[Search Quality Evaluation]]"
  - "[[Test Case Generation]]"
  - "[[Multi-Language Search]]"
topics:
  - "[[Search Quality Assurance]]"
  - "[[E-commerce Search]]"
companies:
  - "[[Zalando]]"
tags:
  - article
  - llm-judge
  - search-evaluation
  - e-commerce
  - zalando
  - company-blog
---

# Search Quality Assurance with AI as a Judge

**[[Tao Ruangyam]]** ([[Zalando]]) describes how Zalando built a production LLM-as-a-judge pipeline to evaluate search quality at scale — with high coverage, multi-language support, and no hand-crafted test cases. The motivating use case: validating search quality for three new country launches (Luxembourg, Portugal, Greece) **before** go-live, with no real user data yet.

---

## The Problem with Manual QA

Before this framework, the process was:
1. Sample queries from existing markets, translate manually for new language
2. Human experts annotate error cases and identify poor results
3. Root cause diagnosis done by the same experts

This is **reactive** (issues found after launch), not scalable, and impossible when there are no real users yet.

## Query Selection via NER Clustering

Instead of sampling by frequency alone (which would over-represent synonymous queries), Zalando uses their **[[Named Entity Recognition]]** engine to extract structured attributes from queries:

| NER tags | Example queries |
|---|---|
| category: kids, type: jacket, season: winter | Kids Winter Jacket, Winter Jackets for Kids |
| category: shoes, brand: nike, type: sneakers | Nike Sneakers, Nike Shoes |

Queries with the same NER tag set share search intent and are grouped into segments. The top-N segments by traffic share become the test set — representative without redundant near-duplicates.

For new language markets, LLM translation preserves NER tags across languages (verified by comparing tags before and after translation).

## LLM Judge Evaluation

The judge (GPT-4o in the pre-launch run) takes:
- The search query
- Top-25 search result products (metadata + product images)

It outputs a 0–4 relevance score per result item, where 4 = perfect match, 0 = completely irrelevant. The multimodal (visual-text) approach generalizes across languages without language-specific prompts.

Scores aggregate per NER segment → identifies which query categories underperform.

## Production Pipeline (Apache Airflow)

Three-stage DAG:
1. **Test query generation** — NER-cluster past queries, translate if needed, persist to data lake
2. **Search result retrieval** — Kubernetes PodOperator submits queries to Search API, caches results in Elasticache
3. **LLM evaluation** — GPT-4o scores each (query, product) pair; results cached to avoid re-scoring duplicate products

**Caching key insight**: instead of `5000 queries × 25 results = 125,000 product fetches`, only `N unique products` are fetched. N scales much more slowly than query count as coverage grows.

Multiple markets run as parallel Airflow TaskGroups in the same DAG.

## Results: Issues Found Before Launch

**Portuguese market** — low-scoring segments revealed:
- Lemmatization bug for "desporto/desportivo/desportiva" (sport category)
- "tenis/ténis" unrecognized (tennis vs. sneaker ambiguity)
- "menina/meninas" (girls) not tagged → gender-agnostic results

**Greek market** — NER tag comparison (original vs. translated) identified unrecognized terms causing incorrect catalog filtering, confirmed by low LLM relevance scores.

**Brand discoverability pattern**: if multiple NER segments all sharing BRAND=X score low, it strongly signals that brand's product data has quality issues.

## Cost

~$250 USD per full run (1,500 segments × 25 results), mainly GPT-4o completion cost. One run takes 3–5 hours. The alternative — human evaluation — costs far more and takes days.

---

## Related Concepts

- [[LLM as Judge]] — core evaluation mechanism
- [[Named Entity Recognition]] — used for query clustering and segment definition
- [[Search Quality Evaluation]] — the goal of the framework
- [[Test Case Generation]] — automated, NER-driven, no hand-crafting needed
- [[Multi-Language Search]] — key motivation; NER tags are language-agnostic
- [[Judgment Lists]] — what the LLM judge produces at scale

## Related Articles

- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]]; complementary approach: ML on top of LLM judge outputs
- [[Improving Retrieval with LLM as a Judge]] — [[Jo Kristian Bergum]]; LLM judge for retrieval benchmarking at Vespa
- [[LLM-as-a-Judge When to Use Reasoning CoT and Explanations]] — when to add reasoning to LLM judges

## Companies

- [[Zalando]] — author organisation; Europe's largest fashion platform

## People

- [[Tao Ruangyam]] — author; Zalando Search engineering
