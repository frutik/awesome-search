---
type: concept
title: "Bag of Decisions"
aliases: ["Bag of Questions", "Bag-of-Decisions Reranking", "Per-Query Relevance Rubric"]
tags: [concept, reranking, llm, query-understanding]
created: 2026-10-11
---

# Bag of Decisions

A reranking idea from [[Doug Turnbull]] ([[Bag of Decisions Reranker]]): represent a query not as a *bag of terms* but as a **bag of yes/no questions** whose affirmative answers indicate relevance, and score a document by how many of them it satisfies.

---

## How It Works

1. **Generate the rubric.** Prompt an LLM to write yes/no questions for this specific query. For *desk for kids*, these include "Is the document about desks designed for children?", "Does it mention child-sized or age-appropriate dimensions or ergonomics?" and "Are brands or models of children's desks listed?"
2. **Answer each question per document.** Each becomes a [[Jev]] Noul over the candidate, returning P(yes).
3. **Sum.** The rerank score is the sum of the probabilities. It can be used directly or added to [[BM25]].

The author calls this **per-query feature creation**: the LLM proposes what matters for the query, and a cheap decision model measures coverage. It is the query-specific counterpart to hand-written, query-independent signals such as the `explicit_constraints` and `requested_item` Nouls in [[Using Jev as a Search Reranker - Benchmarks and How to Implement]].

## Evidence

In the one published run, it beat both BM25 and a single-question Jev reranker on mean NDCG for [[WANDS Dataset|WANDS]] (0.610 vs 0.574 vs 0.5407) and [[Amazon ESCI Dataset|ESCI]] (0.360 vs 0.314 vs 0.289). The author presents this as a toy experiment worth deeper study.

## Open Problems

- **Rubric quality.** Generated questions can be repetitive. Making them more incisive and diverse is the author's own open question.
- **Equal weights.** As published, every question counts the same in the sum, so a restated criterion counts twice and a minor one counts as much as the core intent.
- **Cost scales with questions × candidates**, plus one generation call per query.

## Related Concepts

- [[Reranking]] — where the score is used
- [[Query Understanding]] — the rubric is an explicit reading of query intent
- [[Pointwise Relevance Evaluation]] — each question is judged per document, independently
- [[LTR Feature Engineering]] — generating features per query rather than per collection
- [[Calibrated Relevance Probability]] — summing probabilities assumes they are comparable

## Related Articles

- [[Bag of Decisions Reranker]]
- [[Using Jev as a Search Reranker - Benchmarks and How to Implement]] — fixed multi-question policy, for contrast

## People

- [[Doug Turnbull]]
