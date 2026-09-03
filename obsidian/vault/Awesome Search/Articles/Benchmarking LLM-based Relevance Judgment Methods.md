---
type: article
title: "Benchmarking LLM-based Relevance Judgment Methods"
source: "https://arxiv.org/abs/2504.12558"
pdf: "https://arxiv.org/pdf/2504.12558"
author:
  - "[[Negar Arabzadeh]]"
  - "[[Charles L. A. Clarke]]"
published: 2025-04-17
created: 2026-09-03
venue: "arXiv (cs.IR)"
datasets:
  - "[[TREC Deep Learning Track]]"
  - "[[ANTIQUE]]"
concepts:
  - "[[LLM as Judge]]"
  - "[[Pointwise Relevance Evaluation]]"
  - "[[Pairwise Relevance Evaluation]]"
  - "[[Judgment Lists]]"
  - "[[Search Evaluation]]"
topics: []
tags:
  - article
  - search-evaluation
  - llm-judge
  - benchmark
  - trec
  - information-retrieval
---

# Benchmarking LLM-based Relevance Judgment Methods

**Authors:** [[Negar Arabzadeh]], [[Charles L. A. Clarke]] · **arXiv:2504.12558** (cs.IR, 2025)

## Summary

A side-by-side benchmark of the main ways of asking an LLM for a relevance judgment, on the premise that "[[LLM as Judge|use an LLM judge]]" names a family of methods rather than a method. The paper groups the methods into three families — (1) traditional judgments, binary and graded (UMBRELA-style); (2) two nugget-based methods, *document-agnostic* (Exam) and *document-dependent* (AutoNuggetizer); and (3) pairwise preference — expanded into twelve concrete variants, using GPT-4o (with Llama 3.2b results in the accompanying repository) over the [[TREC Deep Learning Track|TREC Deep Learning]] tracks of 2019, 2020 and 2021 plus [[ANTIQUE]], a non-factoid open-domain QA collection.

## The Two Axes

The evaluation separates two things usually reported as one:

1. **Agreement with human labels** — does the judge assign the grade a human would to this query-document pair?
2. **Agreement with human system rankings** — does a leaderboard built from the judge's labels order retrieval systems the way a human-labelled one does? Measured with Kendall correlations.

## Findings

**Pairwise preferences align best with human labels** — "perhaps because they directly compare two documents, preference labels consistently provide the best alignment with human labels."

**Graded and binary pointwise labels agree best with system rankings.** Kendall τ against the human-derived ordering: UMBRELA 0.920 / 0.894 / 0.890 and binary 0.869 / 0.922 / 0.904 on DL-19 / DL-20 / DL-21, versus 0.911 / 0.852 / 0.816 for preferences. The original human labels themselves reach 0.953 / 0.956 / 0.916. Nugget-based variants trail on this axis, the weakest falling to 0.685.

The nugget family is generally weaker on this axis but not uniformly so — Exam-Graded_max reaches 0.881 on DL-19, above binary's 0.869 — and the two nugget flavours split by collection rather than one dominating: the paper reports that "document-agnostic approaches, such as Exam-Binary, tended to have higher correlations on DL-20, while document-dependent approaches showed slightly better alignment on DL-19."

**Neither axis implies the other.** The paper's conclusion: "methods prioritizing alignment with human labels may not inherently optimize for agreement with system rankings, and vice versa."

The authors also note that the human baseline is not itself high — human-human κ can be above 0.5 on binary assessment, with LLM-human κ typically in the 0.3–0.5 range depending on the scale used.

## Why It Matters

An agreement number reported without saying which of the two axes it measures is ambiguous, and the method that maximizes one is not the method that maximizes the other. Paradigm choice therefore has to follow the question: judging individual documents and ranking systems are different tasks with different best instruments.

## Related Concepts

- [[LLM as Judge]] — the paradigm-choice question this paper makes concrete
- [[Pointwise Relevance Evaluation]] — the binary/graded family that wins on system-ranking agreement
- [[Pairwise Relevance Evaluation]] — the preference family that wins on label agreement
- [[Judgment Lists]] — what these methods produce
- [[Search Evaluation]] — where the resulting labels are consumed
- [[NDCG]] — the metric the system rankings are built from

## Related Datasets

- [[TREC Deep Learning Track]] — DL-19/20/21, the web-passage side of the evaluation
- [[ANTIQUE]] — the non-factoid counterweight

## Related Articles

- [[Criteria-Based LLM Relevance Judgments]] — a different response to the same unreliability: decompose the criterion rather than change the prompt style

## People

- [[Negar Arabzadeh]] — author
- [[Charles L. A. Clarke]] — author
