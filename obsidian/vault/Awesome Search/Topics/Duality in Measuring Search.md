---
type: topic
aliases:
  - "Two Approaches to Measuring Search"
  - "online vs offline evaluation"
  - "quant and qual search measurement"
  - "metrics-driven vs human-centered search"
tags: [topic, evaluation, search-quality, human-judgment, metrics]
related_concepts: ["[[Search Evaluation]]", "[[Judgment Lists]]", "[[Click Signals]]", "[[Implicit Judgments]]", "[[NDCG]]", "[[Interleaving]]", "[[LLM as Judge]]"]
related_topics: ["[[A-B Testing for Search]]", "[[Relevance Program Setup]]", "[[Search Quality Assurance]]"]
articles: ["[[Statistical and Human-Centered Approaches to Search Improvement]]", "[[Measuring Search - A Human Approach]]", "[[Measuring Search - Metrics Matter]]", "[[Evaluating Search - Using Human Judgments]]"]
people: ["[[James Rubinstein]]", "[[Daniel Tunkelang]]"]
created: 2026-06-27
---

# Duality in Measuring Search

A recurring theme in search practice: **there are two complementary ways to know whether search is working — the quantitative/behavioral and the qualitative/human — and you need both.** [[James Rubinstein]] frames it as "qual + quant magic": online metrics tell you *what* users did; human judgment tells you *why*. It's "not one-or-the-other, it's *yes, and!*"

The duality shows up under two different lenses depending on whether you are *improving* search or *measuring* it.

---

## Lens 1 — Improving search: statistical vs. human-centered

From [[Statistical and Human-Centered Approaches to Search Improvement]]:

| | Statistical / metrics-driven | Human-centered / user-centered |
|---|---|---|
| **Stance** | Treat users as a black box; observe behavior, tune to maximize it | Talk to users, understand tasks, find points of failure |
| **Tooling** | Machine learning, [[Learning to Rank]], log analysis | User research, interviews, qualitative observation |
| **Optimizes** | Metrics (DCG/MAP — see [[NDCG]], [[MAP]]) | Real, articulated user needs |
| **Failure alone** | Optimizes the metric, not user value (eBay: "items sold" → cheap accessories) | An intuition that may not drive broad, sized impact |

**Synthesis**: the strongest wins hand-tune statistical systems to human-discovered needs — technology "push" meets user-need "pull." (eBay appliance example: human insight that fridge searches drown in accessories → ML on price brackets per category to fix it.)

## Lens 2 — Measuring search: online vs. offline

From [[Measuring Search - A Human Approach]]:

| | Online (log-based) | Offline (human-rated) |
|---|---|---|
| **Source** | Live user behavior, [[A-B Testing for Search\|A/B tests]] | Raters judging (query, document) pairs → [[Judgment Lists]] |
| **Signal** | [[Click Signals]], conversion, session success | Explicit relevance grades; [[Implicit Judgments]] as a hybrid |
| **Strength** | Real users, causal inference | The *why*; catches corner cases & ambiguous queries |
| **Weakness** | Metric-dependent (CTR rewards clickbait, not relevance) | Only a proxy — raters don't know the user's task |

**Synthesis**: the [[The Launch Review\|launch review]] is where the two meet — weighing A/B results and human ratings together (e.g. human DCG up but engagement DCG down: ship or not?).

---

## Why neither half is sufficient

- **Quant alone** → optimizing a proxy. CTR-maximization promotes the cute-pug result over the actually-relevant sweater; you tune to the lowest common denominator and never learn *why*.
- **Qual alone** → unscalable intuition. Without metrics you can't size a problem ("X is low-DCG and 20% of searches") or confirm broad impact.
- **Together** → human judgment is the *foil* that keeps metric-tuning honest, and metrics give human insight the reach and prioritization it lacks.

## How it fits the broader evaluation stack

This duality is the conceptual backbone of a full program: [[Search Evaluation]] formalizes the online/offline axes, [[Relevance Program Setup]] operationalizes collecting both signal types, and [[A-B Testing for Search]] / [[Interleaving]] are the online experimentation layer. Emerging twist: [[LLM as Judge]] blurs the line by generating offline-style judgments at near-online scale.

---

## Key Articles

- [[Statistical and Human-Centered Approaches to Search Improvement]] — the improvement duality (statistical vs. human-centered)
- [[Measuring Search - A Human Approach]] — the measurement duality (online vs. offline)
- [[Measuring Search - Metrics Matter]] — choosing online metrics that don't mislead
- [[Evaluating Search - Using Human Judgments]] — [[Daniel Tunkelang]]'s complementary case for the offline half
- [[Choosing Your Search Relevance Evaluation Metric]] — picking the metric for the quant half
- [[Evaluating the Best AB Testing Metrics for Search]] — online-metric selection in practice
- [[Measuring Searcher Behavior]] — reading behavioral signal
- [[The Launch Review]] — where quant and qual are reconciled before shipping

## Related Topics

- [[A-B Testing for Search]] — the online experimentation half, in depth
- [[Relevance Program Setup]] — standing up both signal types as a program
- [[Search Quality Assurance]] — metrics taxonomy and evaluation modes

## People

- [[James Rubinstein]] — "qual + quant"; the two-approaches framing
- [[Daniel Tunkelang]] — search evaluation philosophy; human judgment advocate
