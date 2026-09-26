---
type: article
title: "DAT: Dynamic Alpha Tuning for Hybrid Retrieval in Retrieval-Augmented
  Generation"
source: https://arxiv.org/abs/2503.23013
author:
  - Jengnan Tzeng
  - Hsin-Ling Hsu
published: 2025-03-29
tags:
  - article
  - paper
  - hybrid-search
  - query-routing
  - score-fusion
  - rag
concepts:
  - "[[Hybrid Search]]"
  - "[[Linear Score Combination]]"
  - "[[Query Routing]]"
  - "[[BM25]]"
  - "[[Dense Vector Retrieval]]"
  - "[[LLM as Judge]]"
created: 2026-09-26
---

# DAT: Dynamic Alpha Tuning for Hybrid Retrieval in RAG

**Authors:** Jengnan Tzeng, Hsin-Ling Hsu (National Chengchi University, Taipei)
**Source:** [arXiv 2503.23013](https://arxiv.org/abs/2503.23013), March 2025 (preprint)

## Summary

[[Linear Score Combination|Weighted hybrid retrieval]] mixes [[BM25]] and [[Dense Vector Retrieval|dense]] scores with one global α, so keyword-shaped and meaning-shaped queries get the same blend. DAT picks **α per query**: a soft version of [[Query Routing]] — instead of sending the query to one retriever, it decides how much to trust each.

## Mechanism

1. Retrieve the **top-1** result from BM25 and from dense retrieval.
2. An LLM scores each against the query on a 0–5 rubric: 5 = direct hit; 3–4 = close, the answer is likely nearby; 1–2 = loosely related and misleading; 0 = off-track.
3. Set α from the two scores: both 0 → 0.5; dense scores 5 and BM25 does not → 1.0 (dense only); BM25 scores 5 and dense does not → 0.0 (BM25 only); otherwise α = dense score / (dense + BM25), rounded to one decimal.
4. Final score = α · normalised dense + (1 − α) · normalised BM25.

Judging only the top-1 of each list keeps the LLM cost to two short judgments per query — an [[LLM as Judge]] used online, as a router.

## Results

On SQuAD (English) and DRCD (traditional Chinese), with GPT-4o, GPT-4o-mini and DeepSeek-R1-Distill-Qwen-14B as the judge:

- Over the full query sets DAT beats BM25-only, dense-only and the best fixed hybrid; the gain in Precision@1 over fixed α is about 2% on SQuAD even with the 14B model, and about 3.3% on DRCD with GPT-4o.
- On **hybrid-sensitive** subsets — queries where BM25 and dense disagree on the top result (1,111 SQuAD, 1,523 DRCD) — the best variant gains about **7.5%** Precision@1 on SQuAD and **6.4%** on DRCD over fixed α; the 14B model gains 5.4% and 4.6%.
- Dense is stronger on SQuAD and BM25 on DRCD, which is the per-dataset (and per-query) variance a fixed α cannot follow.

## Caveats

- Adds LLM calls to every query — the latency trade-off [[Linear Score Combination]] warns about for any LLM-based router.
- Reading-comprehension datasets where each query has one gold passage; the rubric and top-1 sampling are tuned to that setting.

## Related Concepts

- [[Hybrid Search]] · [[Linear Score Combination]] · [[Score Normalization]]
- [[Query Routing]] — soft routing: weights instead of a single route
- [[Reciprocal Rank Fusion]] — the rank-only alternative that has no α to tune
- [[LLM as Judge]]

## Related Notes

- [[Andrei Cristea - Qdrant Vector Search and Hybrid Routing]] — hard routing between sparse, dense and RRF with a trained classifier
- [[RRF is Not Enough]] — intent-based allocation between retrieval strategies
