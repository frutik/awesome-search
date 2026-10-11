---
title: "Bag of Decisions Reranker"
type: article
tags: [article, reranking, e-commerce, llm, experiment]
source: "https://softwaredoug.com/blog/2026/10/08/bag-of-decisions.html"
author:
  - "[[Doug Turnbull]]"
published: 2026-10-08
created: 2026-10-11
concepts:
  - "[[Bag of Decisions]]"
  - "[[Reranking]]"
  - "[[BM25]]"
  - "[[NDCG]]"
  - "[[Query Understanding]]"
topics:
  - "[[Reasoning Reranking]]"
  - "[[E-commerce Search]]"
tools:
  - "[[Jev]]"
datasets:
  - "[[WANDS Dataset]]"
  - "[[Amazon ESCI Dataset]]"
---

# Bag of Decisions Reranker

**Source:** https://softwaredoug.com/blog/2026/10/08/bag-of-decisions.html
**Author:** [[Doug Turnbull]] · 2026-10-08
**Experiment details:** https://github.com/softwaredoug/search-experiments/blob/main/research/decisions/ecom.md

## Summary

A short experiment that swaps a "bag of terms" view of a query for a **[[Bag of Decisions|bag of decisions]]**. Instead of asking [[Jev]] the single question "is this document relevant for {query}?", an LLM first writes a per-query rubric: about ten yes/no questions where "yes" indicates relevance. For *desk for kids*, these include whether the document is about desks designed for children, whether it mentions child-sized dimensions or ergonomics, and whether it lists brands or models of children's desks. Each question becomes a Jev Noul, and the rerank score is the **sum of the P(yes) values**. That sum can be used directly or added to [[BM25]].

Turnbull describes this as **per-query feature creation**: the LLM suggests what matters for this query, and Jev measures whether each candidate covers it.

## Results

Compared with BM25 and a plain single-question Jev reranker, with the single-question approach pointing back at [[Hev meets Jev]]:

| Dataset | Strategy | Mean NDCG | Median NDCG |
|---|---|---|---|
| [[WANDS Dataset\|WANDS]] | BM25 | 0.5407 | 0.475 |
| WANDS | Jev reranker | 0.574 | 0.561 |
| WANDS | bag of decisions | **0.610** | 0.561 |
| [[Amazon ESCI Dataset\|ESCI]] | BM25 | 0.289 | 0.171 |
| ESCI | Jev reranker | 0.314 | 0.205 |
| ESCI | bag of decisions | **0.360** | **0.341** |

On both datasets the bag of decisions has the best mean. On ESCI the median roughly doubles over BM25. On WANDS the median is the same as the single-question reranker's.

## Reading It

- **It is framed as a toy.** The author calls it a fun experiment and "a promising approach worth deeper study", not a production recipe. No query count or confidence intervals are given in the post.
- **The rubric is the weak point he names himself.** Some generated questions are repetitive (two of the ten for *desk for kids* restate "is it about kids' desks"). An unweighted sum lets near-duplicate questions count the same criterion twice. Getting more incisive and diverse questions is his open question.
- **It sits next to Elastic's multi-signal policy.** [[Using Jev as a Search Reranker - Benchmarks and How to Implement]] also asks several Jev questions per pair, but with hand-written, query-independent questions combined by a weighted policy. Here the questions are generated per query and simply summed.

## Related Concepts

- [[Bag of Decisions]] — the method this post introduces
- [[Reranking]] · [[BM25]] · [[NDCG]]
- [[Query Understanding]] — the rubric is an LLM's reading of what the query needs
- [[Pointwise Relevance Evaluation]] — every question is judged independently per document

## Related Notes

- [[Jev]] · [[TypeSafe]] — the model scoring the questions
- [[Hev meets Jev]] — the single-question reranker used as a comparator
- [[Using Jev as a Search Reranker - Benchmarks and How to Implement]] · [[Jevjitsu - How We Tried Generalized Classifiers on Everything]] — the same week's other Jev reranking experiments
- [[WANDS Dataset]] · [[Amazon ESCI Dataset]]
- [[Reasoning Reranking]] · [[Reception of Jev]]

## People

- [[Doug Turnbull]]
