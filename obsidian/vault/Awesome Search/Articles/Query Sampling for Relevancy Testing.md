---
type: article
title: "Query Sampling for Relevancy Testing"
aliases: ["Bonsai Query Sampling", "Elasticsearch OpenSearch Query Sampling Relevancy"]
source: "https://bonsai.io/blog/elasticsearch-opensearch-query-sampling-relevancy/"
author: "[[Nick Zadrozny]]"
company: "[[Bonsai]]"
published: 2025-01-28
tags: [article, company-blog, relevance, evaluation, query-sampling, judgment-lists]
concepts: ["[[Query Sampling]]", "[[Judgment Lists]]", "[[Search Evaluation]]", "[[NDCG]]"]
topics: ["[[Relevance Program Setup]]", "[[Search Quality Assurance]]"]
created: 2026-06-27
---

# Query Sampling for Relevancy Testing

A [[Bonsai]] piece by [[Nick Zadrozny]] arguing that relevance testing should **not** choose between frequent and infrequent queries — it should sample across all frequency tiers, because each tier exposes a different class of product problem. Its distinctive contribution beyond the standard [[Query Sampling]] mechanics is a **per-tier handling strategy** and a reframing of relevance work as a *holistic product concern*, not a search-internal one.

---

## Core Argument

User search expression is "practically infinite" — you cannot test every query. The naive instincts both fail: test only head queries and you over-fit common cases; test only the tail and you drown in rare queries with little traffic. The answer is **stratified sampling** across head / torso / tail, each handled differently.

> "We are not optimizing search results, we are optimizing for the end-user experience. And that is a holistic product concern."

## The Frequency Distribution (head / torso / tail)

Queries follow an exponential / long-tail distribution:

- **Head** — few, extremely frequent, well-understood needs.
- **Torso** — moderate frequency, substantial aggregate traffic, less obvious intent.
- **Tail** — rare or *never-before-seen* queries. Cites Google: **~15% of daily Google queries had never been seen before** (the [BERT announcement](https://blog.google/products/search/search-language-understanding-bert/)).

## Per-Tier Strategy (the enriching insight)

| Tier | How to handle it |
|---|---|
| **Head** | Spend real human attention; manually optimize. Crucially, the fix may live **outside search** — navigation redesign, a prominent site feature, or recognizing a query as **navigational** rather than a discovery need. Ask whether the query signals an unmet need addressable elsewhere in the product. |
| **Torso** | Build **generalizable models from first principles** rather than special-casing. Sample representative torso queries to avoid over-fitting to the head; align user intent with index design and request structure during development. |
| **Tail** | Include in test suites despite rarity; accept the intrinsic difficulty of free-form expression; lean on **ML and engagement signals** to scale beyond what humans can label. |

## Two Testing Methodologies

1. **Direct human attention → [[Judgment Lists]]** — run queries, label results, compute metrics ([[NDCG]]), iterate on index + query structure. Can start in a spreadsheet.
2. **Scaled approaches** — derive labels from engagement signals (clicks) in server logs; build automated relevance models; use [[LLM as Judge|LLMs]] to bootstrap and scale.

## Related Concepts
- [[Query Sampling]] — the mechanics this article applies (random / stratified / PPS)
- [[Judgment Lists]]
- [[Search Evaluation]]
- [[Search Quality Assurance]]

## Related Articles
- [[Succeeding with Relevance Evaluation using PPS Sampling]] — Nate Day (OSC); the PPS technique this article points to
- [[Setting Up a Relevance Evaluation Program]] — weighted random sampling by query frequency
- [[How to Really Design Search for a Database]] — also [[Bonsai]]

## People
- [[Nick Zadrozny]]

## Source
- https://bonsai.io/blog/elasticsearch-opensearch-query-sampling-relevancy/
