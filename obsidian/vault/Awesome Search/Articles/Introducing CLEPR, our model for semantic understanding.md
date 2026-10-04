---
type: article
title: "Introducing CLEPR, our model for semantic understanding"
aliases:
  - Introducing CLEPR
source: https://medium.com/criteo-engineering/introducing-clepr-our-model-for-semantic-understanding-d3984eed84c8
author:
  - "[[Paul Coursaux]]"
company: "[[Criteo]]"
published: 2026-06-02
created: 2026-10-04
paywall: true
tools:
  - "[[CLEPR]]"
concepts:
  - "[[Semantic Relevance]]"
  - "[[Outcome-Based Relevance]]"
  - "[[Bi-Encoder]]"
  - "[[Contrastive Learning]]"
  - "[[Click Signals]]"
  - "[[Implicit Judgments]]"
  - "[[Position Bias]]"
topics:
  - "[[E-commerce Search]]"
  - "[[Multilingual Search]]"
tags:
  - article
  - paywalled
  - e-commerce
  - embeddings
  - sponsored-products
  - relevance
  - company-blog
---

# Introducing CLEPR, our model for semantic understanding

> [!warning] Paywall
> Medium member-only post. Key ideas only below; details are in the original.
> https://medium.com/criteo-engineering/introducing-clepr-our-model-for-semantic-understanding-d3984eed84c8

A [[Criteo]] Tech Blog post by [[Paul Coursaux]] (2 June 2026) on [[CLEPR]] (Contrastive Language Embedding for Product Retrieval). CLEPR is the model that scores keyword–product relevance for the Sponsored Products ads Criteo places inside retailers' own search results. It reuses the accuracy vs outcome-based relevance framing from [[Leveraging Commerce Data for Outcome-Based Relevancy in Agentic Recommendation Systems]].

## Key ideas

- **Relevance as an ad guardrail.** Ads shown beside organic results for an explicit query must match its intent closely, or they degrade the retailer's search. CLEPR therefore sets a minimum relevance threshold that candidates must pass before performance optimization ranks them. The post also stresses meaning that shifts by market and vertical, such as "chips" or "Apple". See [[Semantic Relevance]] and [[Multilingual Search]].
- **Why not an LLM.** Responses are needed in a few tens of milliseconds over billions of keyword–product pairs a day, so CLEPR is a two-tower model with separate keyword and product encoders. CLIP's text encoder was tried first and set aside, because short keywords differ too much from the descriptive product text it was trained on. See [[Bi-Encoder]] and [[Contrastive Learning]].
- **Clicks rebuilt from sessions.** Criteo does not log search-to-click events directly, so training pairs come from stitching a search to the product-page views that follow it in the same session, using timing heuristics. See [[Click Signals]] and [[Implicit Judgments]].
- **Filtering and de-biasing the signal.** Only pairs with a high exclusivity score are kept, meaning the keyword reliably leads to that product across sessions, and minimum volume and recency thresholds apply. The objective is in-batch contrastive rather than click prediction, and each pair counts once however many clicks it had, to keep popularity and [[Position Bias]] out. Quality is measured on human-labelled pairs, not on clicks. The author concedes that relevant products that never get clicked remain invisible.
- **Scale and result.** About 2B products are re-embedded as content changes, more than 10B pairs are scored a day, and training uses distributed data-parallel Ray jobs on multi-GPU clusters. Rollout went through phased A/B tests. After deployment Criteo reports +6% click-through rate and fewer relevance issues.
- **Next.** Multimodal inputs, conversational shopping assistants on retailer sites, and Criteo's Agentic Commerce Recommendation Service. See [[Conversational and Agentic Search]].

## Caveats

- All figures are Criteo's own, with no offline accuracy numbers in this post. Those are in the companion article.

## Related Notes

- [[Leveraging Commerce Data for Outcome-Based Relevancy in Agentic Recommendation Systems]] — the benchmarks
- [[CLEPR]] · [[Criteo]]
- [[E-commerce Search]]
