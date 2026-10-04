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

### Criteo's Framing: Accuracy vs Outcome

[[Criteo]] uses the same split under different names. *Accuracy* is semantic relevance, and [[Outcome-Based Relevance]] is the engagement side, judged by clicks and purchases. Its emphasis runs the other way from Etsy's. Semantic match is treated as necessary but not sufficient, and its largest reported gain comes from re-ranking on recent sales on top of semantic retrieval. In its Sponsored Products ads, the semantic score from [[CLEPR]] serves as a guardrail threshold that candidates must pass before performance optimization ranks them ([[Introducing CLEPR, our model for semantic understanding]], [[Leveraging Commerce Data for Outcome-Based Relevancy in Agentic Recommendation Systems]]).
## Related Concepts

- [[ESCI Label Scheme]] — the Exact/Substitute/Complement/Irrelevant grading the planned partial-relevance split draws on
- [[LLM as Judge]] — the mechanism used to scale semantic relevance labeling
- [[Knowledge Distillation]] — how the judgment gets compressed into a real-time-usable model
- [[Amazon ESCI Dataset]] — a public annotation scheme with a similar Exact/Substitute/Complement/Irrelevant split

- [[Outcome-Based Relevance]] — the engagement-based counterpart

## Articles

- [[How Etsy Uses LLMs to Improve Search Relevance]] — the framework this concept is drawn from

- [[Introducing CLEPR, our model for semantic understanding]] — semantic relevance as an ad guardrail
- [[Leveraging Commerce Data for Outcome-Based Relevancy in Agentic Recommendation Systems]] — accuracy vs outcome-based relevance
## Related Topics
- [[Outcome-Based vs Semantic Relevance]] — semantic and engagement relevance compared, with the patterns for combining them
