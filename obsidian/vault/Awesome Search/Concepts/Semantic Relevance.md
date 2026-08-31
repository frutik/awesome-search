---
type: concept
title: "Semantic Relevance"
aliases: ["semantic relevance signal", "intent-based relevance"]
tags:
  - concept
  - search-evaluation
  - e-commerce
  - llm
created: 2026-08-31
---

# Semantic Relevance

## Definition

Whether a search result actually matches what the query is asking for — meaning and proper nouns included — as distinct from **engagement-based relevance**: proxies like clicks, add-to-carts, and purchases that measure what users interact with rather than whether it was the right thing to show them.

## Why It's a Separate Signal

Engagement signals are objective and easy to collect at scale, but they're biased toward already-popular results: an item can accumulate clicks and purchases because it's a good general product, not because it matches a specific query's intent. Optimizing ranking purely on engagement entrenches that bias — popular listings keep winning regardless of fit. Semantic relevance is introduced as a complementary signal precisely to correct for this, not to replace engagement data.

The two signals can genuinely conflict: engagement sometimes *drops* even as semantic relevance improves, since a highly relevant but less familiar result may get fewer clicks than a popular-but-loosely-related one. This tension shows up across e-commerce search generally, not just at any single company, and pushes toward adaptive, query-type-specific treatments rather than a uniform relevance/engagement tradeoff.

## Etsy's Framework

[[How Etsy Uses LLMs to Improve Search Relevance]] builds a Semantic Relevance Evaluation and Enhancement Framework around a three-way category scheme (relevant / partially relevant / irrelevant), defined from user research rather than engagement data. It uses an [[LLM as Judge|LLM judge]], anchored and validated against human "golden" labels, to scale semantic relevance labeling to millions of query-listing pairs, then [[Knowledge Distillation|distills]] that judgment into a cascade of progressively smaller, faster models so the signal can run in real-time production search — filtering irrelevant listings, feeding ranking-model features, weighting training loss, and boosting highly-relevant results. Between August and October 2025, the fully-relevant listing share rose from 58% to 62%.

A planned refinement is splitting "partially relevant" into finer subcategories (complements vs. substitutes), taking inspiration from Amazon's [[Amazon ESCI Dataset|ESCI]] annotation scheme, which already distinguishes Substitute from Complement.

## Related Concepts

- [[LLM as Judge]] — the mechanism used to scale semantic relevance labeling
- [[Knowledge Distillation]] — how the judgment gets compressed into a real-time-usable model
- [[Amazon ESCI Dataset]] — a public annotation scheme with a similar Exact/Substitute/Complement/Irrelevant split

## Articles

- [[How Etsy Uses LLMs to Improve Search Relevance]] — the framework this concept is drawn from
