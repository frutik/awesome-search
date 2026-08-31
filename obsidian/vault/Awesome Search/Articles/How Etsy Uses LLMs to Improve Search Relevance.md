---
type: article
title: "How Etsy Uses LLMs to Improve Search Relevance"
source: "https://www.etsy.com/codeascraft/how-etsy-uses-llms-to-improve-search-relevance"
author:
  - "[[Yuqing Zhang]]"
  - "[[Congzhe Su]]"
  - "[[Susan Liu]]"
published: 2026-01-16
created: 2026-08-30
concepts:
  - "[[LLM as Judge]]"
  - "[[Knowledge Distillation]]"
  - "[[Semantic Relevance]]"
topics:
  - "[[E-commerce Search]]"
companies:
  - "[[Etsy]]"
tags:
  - article
  - search-evaluation
  - llm-judge
  - knowledge-distillation
  - e-commerce
  - company-blog
---

# How Etsy Uses LLMs to Improve Search Relevance

**[[Yuqing Zhang]]**, **[[Congzhe Su]]**, and **[[Susan Liu]]** ([[Etsy]] Search Relevance team) describe Etsy's **Semantic Relevance Evaluation and Enhancement Framework** — an LLM-powered system that adds [[Semantic Relevance|semantic relevance]] (does the listing actually match query intent?) as a signal alongside the engagement signals (clicks, add-to-carts, purchases) Etsy's search models historically relied on, which are biased toward already-popular listings. The framework has three parts: high-quality data (human golden labels plus LLM-scaled training data), a family of relevance models trading off accuracy against latency and cost, and model-driven applications spanning offline evaluation and real-time production search.

---

## Relevance Categories

Three categories, defined from user research:
- **Relevant** — listing matches all parts of the query (meaning + proper nouns)
- **Partially relevant** — matches part of the query or is thematically related
- **Irrelevant** — no meaningful connection; presence in top results feels broken

## Data: Anchored by Humans, Scaled by LLMs

Pure [[LLM as Judge|LLM-as-a-judge]] has two problems: **domain shift** (off-the-shelf LLMs don't know Etsy's vocabulary and preferences) and a **performance-cost tradeoff** (bigger LLMs reason better but are too expensive to run at scale). Etsy's fix: human-curated "golden" labels anchor and validate a powerful LLM, which is then used to scale labeling across millions of query-listing pairs — humans define what "good" looks like, the LLM scales it, not a replacement for human judgment.

- Maintains an evolving relevance labeling guideline, because relevance shifts with culture and time — "face masks" meant costume masks pre-2020, protective masks post-2020.
- Query-listing pairs are sampled via random/stratified sampling (broad coverage) plus targeted sampling (hard cases), then double-labeled by Etsy admins with disagreement-rate tracking.
- **LLM annotator**: few-shot chain-of-thought prompting on the o3 model, implemented in LangGraph, fed title/images/text/attributes/variations/extracted entities, with self-consistency sampling. Validated against golden data before being trusted to generate training data at scale.

## Models: Three-Tier Cascaded Distillation

1. **LLM annotator** — most accurate, most expensive; aligned to golden data.
2. **Teacher model** — Qwen 3 VL 4B, supervised fine-tuned on the LLM annotator's output; high-throughput enough for daily labeling of millions of pairs.
3. **Student model** — a lightweight BERT-based two-tower model, [[Knowledge Distillation|distilled]] from the teacher, for real-time inference (under 10ms added latency).

All three are evaluated on the same golden dataset via multi-class Macro F1 (plus per-class F1). Reported figures: Macro F1 0.72 / 0.71 / 0.65 (annotator / teacher / student); Relevant F1 0.81 / 0.78 / 0.64; Partial F1 0.75 / 0.74 / 0.71; Irrelevant F1 0.60 / 0.62 / 0.59 (the student model is "under dev, best up till today" per the authors).

## Applications: From Evaluation to Action

**Evaluation**: the teacher model runs daily offline inference over sampled search requests, feeding aggregated relevance metrics the team reviews; it is also used to check A/B test treatment/control relevance neutrality and positivity. vLLM handles high-throughput inference across millions of pairs per day.

**Production** (student model, embedded in the real-time search stack):
1. **Filtering** — drop listings predicted irrelevant before ranking
2. **Feature enrichment** — relevance score as a ranking-model feature
3. **Loss weighting** — adjust ranking-model training weights by predicted relevance
4. **Relevance boosting** — heuristic promotion of highly-relevant listings in final results

## Results

Fully-relevant listing share rose from 58% to 62% between August and October 2025. Example: "fall decor" queries now surface seasonal decor instead of loosely related items like clothing.

## What's Next

- Better modeling of relevance-vs-engagement tradeoffs — engagement sometimes *drops* even as relevance improves, a pattern also noted elsewhere in e-commerce search — and exploring adaptive, query-type-specific treatments instead of uniform ones.
- Finer-grained partial-relevance subcategories (complements vs. substitutes), inspired by Amazon's [[Amazon ESCI Dataset|ESCI]] framework.
- Using LLM self-consistency as a signal to route only "hard" cases to humans, reducing annotation effort.
- Simplifying the three-tier distillation stack by merging tiers.
- Pushing relevance modeling upstream into retrieval, not just post-retrieval filtering.

---

## Related Concepts

- [[LLM as Judge]] — the annotator tier, and the domain-shift/cost problems it has to solve before it can scale
- [[Knowledge Distillation]] — the LLM annotator → teacher → student cascade
- [[Semantic Relevance]] — the signal this framework adds alongside engagement-based relevance

## Related Topics

- [[E-commerce Search]] — relevance as one of several dimensions catalog search must satisfy

## Related Case Studies

- [[Etsy - Search Quality and Query Understanding]] — earlier Etsy search-quality work (diversity, spelling correction); this framework addresses relevance instead

## Companies

- [[Etsy]] — author organisation

## People

- [[Yuqing Zhang]] — author
- [[Congzhe Su]] — author
- [[Susan Liu]] — author
