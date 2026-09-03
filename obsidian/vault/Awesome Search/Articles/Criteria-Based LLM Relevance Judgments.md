---
type: article
title: "Criteria-Based LLM Relevance Judgments"
source: "https://arxiv.org/abs/2507.09488"
pdf: "https://arxiv.org/pdf/2507.09488"
author:
  - "[[Naghmeh Farzi]]"
  - "[[Laura Dietz]]"
published: 2025-07-13
created: 2026-09-03
venue: "arXiv (cs.IR)"
datasets:
  - "[[TREC Deep Learning Track]]"
  - "[[LLMJudge]]"
concepts:
  - "[[LLM as Judge]]"
  - "[[Pointwise Relevance Evaluation]]"
  - "[[Judgment Lists]]"
  - "[[Search Evaluation]]"
  - "[[Semantic Relevance]]"
topics: []
tags:
  - article
  - search-evaluation
  - llm-judge
  - interpretability
  - trec
  - information-retrieval
---

# Criteria-Based LLM Relevance Judgments

**Authors:** [[Naghmeh Farzi]], [[Laura Dietz]] · **arXiv:2507.09488** (cs.IR, 2025)

## Summary

Prompting an LLM for a relevance label without constraints, the authors argue, "often results in not only incorrect predictions but also outputs that are difficult for humans to interpret." Their Multi-Criteria framework decomposes relevance into four separately-graded dimensions instead of asking for one holistic score, aiming at robustness and interpretability rather than raw agreement.

## The Four Criteria

Each scored 0–3 by its own dedicated prompt:

- **Exactness** — how precisely the passage answers the query
- **Topicality** — whether the passage is about the same subject as the whole query
- **Coverage** — how much of the passage discusses the query and related topics
- **Contextual fit** — whether the passage provides relevant background or context

## Aggregation

Two ways of turning four criterion grades into one 0–3 relevance label:

- **Multi-Criteria (prompt-based)** — a second LLM call sees the four scores alongside the original query-passage pair and returns the overall grade.
- **Sumdecompose** — the criterion scores are summed and the total mapped through fixed thresholds (10–12 → 3, 7–9 → 2, 5–6 → 1, 0–4 → 0).

## Evaluation

Three collections: [[TREC Deep Learning Track|TREC Deep Learning]] 2019 and 2020, plus [[LLMJudge]] (built on TREC DL 2023). Models: LLaMA-3-8B, LLaMA-3.3-70B and FLAN-T5-large.

Multi-Criteria improved system ranking/leaderboard performance over direct grading. On LLMJudge the LLaMA-3-8B configuration placed first on Spearman correlation (0.9919) and second on Kendall's τ (0.9483) in the challenge. An ablation found all four criteria together best or tied in ten of twelve experiments, though three-criterion subsets occasionally did better. The sumdecompose variant won seven of thirty-six comparisons, mostly on the earlier TREC collections.

## Costs and Limitations

- **Runtime**: roughly 5.4× direct prompting with LLaMA-3-8B, but only ~1.3× with FLAN-T5-large.
- **Leniency**: where judge and human diverged sharply, the judge scored the passage higher about 92% of the time.
- The authors flag three standard hazards: the systems being judged were submitted before 2024; TREC collections may sit in the models' training data; and model updates cause judgments to drift away from human annotators over time.

## Why It Matters

The interpretability claim is the practically useful one. A single unconstrained grade gives no account of itself; four criteria produce a grade that can be argued with, and they force the evaluation designer to state what "relevant" is supposed to mean for this collection. Some judge-human disagreement is then not model error but an unstated definition — the two parties weighting exactness against coverage differently, with nobody having said which should win.

## Related Concepts

- [[LLM as Judge]] — decomposition as an alternative to changing prompt style
- [[Pointwise Relevance Evaluation]] — the family this refines
- [[Judgment Lists]] — what the framework produces
- [[Search Evaluation]] — where the labels are consumed
- [[Semantic Relevance]] — the notion being decomposed

## Related Datasets

- [[TREC Deep Learning Track]] — DL-19/20
- [[LLMJudge]] — the challenge this framework placed first on for Spearman correlation

## Related Articles

- [[Benchmarking LLM-based Relevance Judgment Methods]] — benchmarks the prompt-style axis this paper sidesteps

## People

- [[Naghmeh Farzi]] — author
- [[Laura Dietz]] — author
