---
type: tool
title: CLEPR
aliases:
  - Contrastive Language Embedding for Product Retrieval
company: "[[Criteo]]"
tags:
  - tool
  - embeddings
  - e-commerce
  - bi-encoder
  - proprietary
created: 2026-10-04
website: https://medium.com/criteo-engineering/introducing-clepr-our-model-for-semantic-understanding-d3984eed84c8
---

# CLEPR

[[Criteo]]'s proprietary query–product embedding model (Contrastive Language Embedding for Product Retrieval). It scores how well a search keyword matches a product. Criteo uses that score as a relevance guardrail for Sponsored Products ads in retailers' onsite search, and as the retrieval stage of its agentic commerce recommendation service. Not open source.

---

## Architecture

- A two-tower [[Bi-Encoder|bi-encoder]] with separate keyword and product encoders, trained with an in-batch [[Contrastive Learning|contrastive]] objective.
- About 120M parameters and 384-dimensional embeddings, built on Multilingual-MiniLM-L12-H384.
- Each product is represented by its brand, category and full title. The score is the inner product of the query and product embeddings.
- CLIP's text encoder was tried first and dropped, because short keywords are too unlike the descriptive product text it learned from.
- An LLM was ruled out as the primary scorer: the job needs answers in tens of milliseconds across billions of pairs a day.

## Training signal

Criteo has no explicit search-to-click log, so it rebuilds pseudo-clicks by joining a search to the product-page views that follow it in the same session ([[Click Signals]], [[Implicit Judgments]]). Noise is cut by keeping only pairs whose keyword reliably leads to the same product, and by minimum volume and recency thresholds. Each pair counts once regardless of click volume, which keeps popularity and [[Position Bias]] from dominating. Quality is checked against human-labelled pairs rather than clicks. Relevant products that are never clicked stay invisible to the training data.

## Reported results (Criteo's own)

- **Retrieval, outcome-based:** finding the clicked product among 400 brand- or category-matched candidates, CLEPR scores 0.103 normalized reciprocal rank, against 0.049–0.072 for zero-shot Gemma, MiniLM, MPNet, RoBERTa and Qwen3 encoders. Criteo reports this as about +37% on average.
- **Accuracy:** 83.4% ROC-AUC on human-labelled pairs, against 81.09% for Gemini-Embedding-001 and 78.39% for its untuned backbone. Criteo calls this gain moderate.
- **Production:** about 2B products re-embedded as content changes, more than 10B pairs scored a day, training on Ray multi-GPU clusters, and +6% click-through rate after a phased A/B rollout.

The retrieval benchmark rewards finding clicked products, which is exactly what CLEPR was trained on. Zero-shot baselines are at a structural disadvantage there.

## Related Concepts

- [[Outcome-Based Relevance]] · [[Semantic Relevance]] — the two targets CLEPR is measured against
- [[Bi-Encoder]] · [[Contrastive Learning]] · [[Embedding Fine-tuning]]
- [[Click Signals]] · [[Implicit Judgments]] · [[Position Bias]]

## Related Articles

- [[Introducing CLEPR, our model for semantic understanding]] — training and deployment
- [[Leveraging Commerce Data for Outcome-Based Relevancy in Agentic Recommendation Systems]] — the benchmarks

## People

- [[Paul Coursaux]]
- [[Maxime Vono]]

## Company

- [[Criteo]]
