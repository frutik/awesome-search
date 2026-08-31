---
type: article
title: "How Etsy Uses LLMs to Improve Search Relevance"
tags:
  - clippings
  - search
  - relevance
  - llm
  - case-study
  - company-blog
  - draft
source: "https://www.etsy.com/codeascraft/how-etsy-uses-llms-to-improve-search-relevance"
author: "Yuqing Zhang, Congzhe Su, Susan Liu"
published: 2026-01-16
created: 2026-08-30
concepts:
  - LLM-as-a-Judge
  - Knowledge Distillation
  - Semantic Relevance
  - Query Understanding
topics:
  - E-commerce Search
---

# How Etsy Uses LLMs to Improve Search Relevance

> **DRAFT — not yet processed into the vault.** Fetched from a local PDF because
> the live URL is blocked by a bot/CAPTCHA wall (DataDome), so this note is
> parked at the repo root instead of `Articles/`. Run `kg-article-processing` /
> `kg-note-writing` on it to promote into the vault (entity extraction,
> cross-linking, `global_toc.md` update, History entry) once ready.

**Source:** https://www.etsy.com/codeascraft/how-etsy-uses-llms-to-improve-search-relevance
**Author:** Yuqing Zhang, Congzhe Su, Susan Liu (Etsy Search Relevance team)
**Published:** 16 Jan 2026

## Summary

Etsy's search models historically relied on engagement signals (clicks,
add-to-carts, purchases) as relevance proxies — objective but biased toward
already-popular listings. Etsy built a **Semantic Relevance Evaluation and
Enhancement Framework** powered by LLMs to add semantic relevance (does the
listing actually match query intent?) as a complementary signal. The
framework has three parts: high-quality data (human golden labels + LLM-scaled
training data), a family of semantic relevance models trading off accuracy vs.
latency/cost, and model-driven applications integrated into both offline
evaluation and real-time production search.

## Relevance Categories

Three categories, defined from user research:
- **Relevant** — listing matches all parts of the query (meaning + proper nouns)
- **Partially relevant** — matches part of the query or is thematically related
- **Irrelevant** — no meaningful connection; presence in top results feels broken

## Data: Anchored by Humans, Scaled by LLMs

Pure LLM-as-a-judge has two problems: **domain shift** (off-the-shelf LLMs
don't know Etsy's vocabulary/preferences) and a **performance-cost tradeoff**
(bigger LLMs reason better but are too expensive to run at scale). Etsy's fix:
human-curated "golden" labels anchor and validate a powerful LLM, which is
then used to scale labeling across millions of query-listing pairs. Humans
define what "good" looks like; the LLM scales it — not a replacement for
human judgment.

- Maintains an evolving relevance labeling guideline (relevance shifts with
  culture/time — e.g. "face masks" meant costume masks pre-2020, protective
  masks post-2020).
- Query-listing pairs sampled via random/stratified sampling (broad coverage)
  + targeted sampling (hard cases); double-labeled by Etsy admins with
  disagreement-rate tracking.
- **LLM annotator**: few-shot chain-of-thought prompting on the o3 model,
  implemented in LangGraph, fed title/images/text/attributes/variations/
  extracted entities, with self-consistency sampling. Validated against golden
  data before being trusted to generate training data at scale.

## Models: Three-Tier Cascaded Distillation

1. **LLM annotator** — most accurate, most expensive; aligned to golden data.
2. **Teacher model** — Qwen 3 VL 4B, supervised fine-tuned on LLM-annotator
   output; high-throughput enough for daily labeling of millions of pairs.
3. **Student model** — lightweight BERT-based two-tower model, distilled from
   the teacher, for real-time inference (<10ms added latency).

All three evaluated on the same golden dataset via multi-class Macro F1 (plus
per-class F1). Reported figures: Macro F1 0.72 / 0.71 / 0.65 (annotator /
teacher / student); Relevant F1 0.81 / 0.78 / 0.64; Partial F1 0.75 / 0.74 /
0.71; Irrelevant F1 0.60 / 0.62 / 0.59 (student "under dev, best up till
today").

## Applications: From Evaluation to Action

**Evaluation**: teacher model runs daily offline inference over sampled
search requests → aggregated relevance metrics reviewed by the team; also
used to check A/B test treatment/control relevance neutrality/positivity.
vLLM used for high-throughput inference across millions of pairs/day.

**Production (student model, embedded in real-time search stack)**:
1. **Filtering** — drop listings predicted irrelevant before ranking
2. **Feature enrichment** — relevance score as a ranking-model feature
3. **Loss weighting** — adjust ranking-model training weights by predicted relevance
4. **Relevance boosting** — heuristic promotion of highly-relevant listings in
   final results

## Results

Fully-relevant listing share rose from 58% to 62% between August and October
2025. Example: "fall decor" queries now surface seasonal decor instead of
loosely related items like clothing.

## What's Next (per the article)

- Better modeling of relevance-vs-engagement tradeoffs (engagement sometimes
  *drops* even as relevance improves — noted elsewhere in e-commerce too);
  exploring adaptive, query-type-specific treatments instead of uniform ones.
- Finer-grained partial-relevance subcategories (complements vs. substitutes),
  inspired by Amazon's ESCI framework.
- Using LLM self-consistency as a signal to route only "hard" cases to humans,
  reducing annotation effort.
- Simplifying the three-tier distillation stack (merging tiers).
- Pushing relevance modeling upstream into retrieval, not just post-retrieval
  filtering.

## Candidate Cross-Links (for promotion pass)

- [[Etsy]] (company)
- [[Etsy - Search Quality and Query Understanding]] (case study)
- [[E-commerce Search]] (topic)
- Possible new concept notes: LLM-as-a-Judge, Knowledge Distillation /
  Teacher-Student Distillation, Semantic Relevance (vs. engagement-based
  relevance)
- Amazon ESCI framework is referenced as external inspiration — worth a
  concept/reference note if not already present.

## Acknowledgments (from source)

Search Relevance Team, with ML Enablement and Merchandising. Named
contributors: Susan Liu, Jugal Gala, David Blincoe, Yuqing Zhang, Taylor Hunt,
Liz Mikolaj, Oriane Cavrois, Orson Adams, Grant Sherrick, Kaushik Bekal,
Haoming Chen, Patrick Callier, Davis Kim, Marcus Daly; product leadership
Julia Zhou, Willy Huang, Argie Angeleas; engineering leadership Yinlin Fu,
Congzhe Su, Xiaoting Zhao.
