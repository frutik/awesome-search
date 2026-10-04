---
type: article
title: "Leveraging Commerce Data for Outcome-Based Relevancy in Agentic Recommendation Systems"
aliases:
  - Outcome-Based Relevancy in Agentic Recommendation Systems
source: https://medium.com/criteo-engineering/leveraging-commerce-data-for-outcome-based-relevancy-in-agentic-recommendation-systems-717d62589ec3
author:
  - "[[Maxime Vono]]"
company: "[[Criteo]]"
published: 2026-02-05
created: 2026-10-04
paywall: true
tools:
  - "[[CLEPR]]"
concepts:
  - "[[Outcome-Based Relevance]]"
  - "[[Semantic Relevance]]"
  - "[[Click Signals]]"
  - "[[Bi-Encoder]]"
  - "[[Embedding Fine-tuning]]"
  - "[[Reranking]]"
  - "[[MRR]]"
topics:
  - "[[Conversational and Agentic Search]]"
  - "[[E-commerce Search]]"
  - "[[Model Selection and Fine-Tuning Evaluation]]"
tags:
  - article
  - paywalled
  - e-commerce
  - relevance
  - embeddings
  - reranking
  - company-blog
---

# Leveraging Commerce Data for Outcome-Based Relevancy in Agentic Recommendation Systems

> [!warning] Paywall
> Medium member-only post. Key ideas only below; details are in the original.
> https://medium.com/criteo-engineering/leveraging-commerce-data-for-outcome-based-relevancy-in-agentic-recommendation-systems-717d62589ec3

A [[Criteo]] Tech Blog post by [[Maxime Vono]] (5 February 2026, with contributions from Thibault Becker, Hamlet Jesse Medina Ruiz and Otmane Sakhi). It argues that product recommendations served to AI shopping assistants should be judged by what shoppers do, not only by textual match, and backs that with two offline benchmarks of Criteo's [[CLEPR]] embedding model.

## Key ideas

- **Two meanings of relevance.** *Accuracy* asks whether a product's content matches the query; *outcome-based relevance* (the recommender-systems literature's "performance-based recommendation") asks whether clicks and purchases confirm it. For the authors, a content match is only the entry ticket: it does not reveal which of several matching products shoppers actually buy. They cite the 64% accuracy reported for OpenAI's shopping research as an accuracy-only evaluation. See [[Outcome-Based Relevance]] and [[Semantic Relevance]].
- **Two-stage pipeline.** KNN retrieval over content embeddings tuned on commerce data, then re-ranking that mixes accuracy with commerce scores such as a product's sales, plus generated explanations. See [[Reranking]] and [[Conversational and Agentic Search]].
- **Retrieval benchmark.** Outcome-based relevance is measured as the normalized reciprocal rank of the actually clicked product among 400 candidates, with [[Hard Negative Mining|hard negatives]] taken from other queries' clicked products that share its brand or category. CLEPR (about 120M parameters, 384 dimensions) scores 0.103, against 0.049–0.072 for zero-shot Gemma, MiniLM-L12 (its own backbone), MPNet, RoBERTa and Qwen3-0.6B encoders. The post's "+37% on average" headline is the baselines' average shortfall relative to CLEPR. See [[CLEPR]], [[MRR]] and [[Embedding Fine-tuning]].
- **Re-ranking benchmark.** Over the same 400 CLEPR-retrieved candidates, ranking by a *PSales* score instead of CLEPR similarity raises the purchased product's normalized rank score from 0.029 to 0.074, about 2.5×. PSales is simply the share of sales over the previous 7 days. The table's "+60%" label appears to be measured against the new value. In effect the gain comes from a popularity signal layered on semantic ranking.
- **Accuracy is a smaller win.** On human-labelled binary query–product pairs, CLEPR reaches 83.4% ROC-AUC, against 81.09% for Gemini-Embedding-001 and 78.39% for its untuned backbone. The authors call this moderate: about 3 points over the better encoders and 6 over the backbone. They also flag the small dataset and a single train/test split. See [[Model Selection and Fine-Tuning Evaluation]].

## Caveats

- Offline only, with all figures Criteo's own. CLEPR is trained on clicks and then scored on finding clicked products, which favours it over zero-shot models by construction.
- The authors themselves decline to claim an end-to-end conversion uplift, because CLEPR carries no sales-bias terms.

## Related Notes

- [[Introducing CLEPR, our model for semantic understanding]] — the follow-up on how CLEPR is trained and deployed
- [[Click Signals]] · [[Bi-Encoder]] — the training signal and the architecture
- [[E-commerce Search]]
