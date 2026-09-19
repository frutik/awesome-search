---
title: "TypeSafe Cookbook - Re-ranking"
type: article
tags: [article, reranking, cookbook, legal-search, vendor-docs, evaluation]
source: "https://docs.typesafe.ai/cookbooks/rerank_typesafe"
author:
  - "[[TypeSafe]]"
published: 2026-08
created: 2026-09-19
concepts:
  - "[[Reranking]]"
  - "[[BM25]]"
  - "[[Precision and Recall]]"
  - "[[Pointwise Relevance Evaluation]]"
  - "[[Calibrated Relevance Probability]]"
  - "[[Retrieval Pipeline]]"
topics:
  - "[[Reasoning Reranking]]"
companies:
  - "[[TypeSafe]]"
tools:
  - "[[Jev]]"
datasets:
  - "[[CLERC]]"
---

# TypeSafe Cookbook - Re-ranking

**Source:** https://docs.typesafe.ai/cookbooks/rerank_typesafe
**Publisher:** [[TypeSafe]] (documentation, "How-to" section — no byline)
**Model:** `jev-1.12`, priced as of 2026-08

## Summary

TypeSafe's own walkthrough of using [[Jev]] as a [[Reranking|reranker]], on [[CLERC]] legal
case retrieval rather than the [[BEIR]] subsets used in the independent run
([[Hev meets Jev]]). It is vendor documentation, and the numbers are the vendor's — but it is
a runnable notebook with its cost and token counts printed from the actual run, which makes it
more checkable than most vendor material.

Its most interesting result is not the improvement it headlines but the ceiling it reveals: on
a shortlist that contained the correct passage **100% of the time**, reranking still put that
passage first only **18%** of the time.

## Setup

- **Corpus:** 3,565 US court opinion passages, pooled from 170 [[CLERC]] rows.
- **Queries:** 40, each an opinion excerpt with a citation removed. The *gold* passage is the
  one the removed citation pointed to. The other 130 rows appear only as candidates.
- **First stage:** [[BM25]] (via `bm25s`) over the full corpus, taking a **top-30** shortlist.
- **Reranker:** one `Noul` per (query, candidate) pair — 40 × 30 = **1,200 independent calls**,
  fired concurrently through a 12-worker thread pool.

The question asked of each pair is whether the candidate could be the cited precedent — framed
tightly around *establishing the specific legal proposition* the excerpt invokes, with criteria
that explicitly reject a passage merely on a similar doctrine.

## Results

| | Fast search (BM25) | + Jev rerank |
|---|---|---|
| Correct passage in top 1 | 5% | **18%** |
| Correct passage in top 5 | 15% | **35%** |
| Correct passage in top 10 | 38% | **62%** |

Cost for the whole run: 1,200 calls consuming 1,536,002 input and 25,200 output tokens, for
**$0.0645** — output tokens being free at this model's pricing.

## Reading the Numbers

**The reranker's ceiling was 100%, and it reached 18%.** The cookbook states that the top-30
shortlist contained the correct passage for every one of the 40 queries. So unlike the usual
failure mode — where a reranker cannot recover what retrieval never surfaced, the point of
[[When Reranking Becomes a System Boundary]] — here retrieval did its job perfectly and
ranking was the entire bottleneck. Legal citation matching is simply hard: the
[[CLERC]] paper reports zero-shot IR models reaching only 48.3% recall@1000 on the full task.

**This is the single shape, not the batch shape.** One call per pair, which is the variant
[[Hev meets Jev]] found had the better latency tail at thirty times the request volume. The
cookbook notes that a real application would ask several questions about the same pair in one
call, pointing at its parallel-questions cookbook and a "Speculative Fan-Out" pattern.

**Cost per query is higher than the BEIR run, for a legible reason.** Derived from the figures
above: $0.0645 over 40 queries is roughly **$1.61 per 1,000 queries** — against $0.87 for the
single shape in [[Hev meets Jev]]. The input averages about 1,280 tokens per call, because court
opinion passages are long. Reranking cost scales with passage length, not just candidate count.

**Forty queries, no confidence intervals.** The independent run used ~300 queries per corpus
with paired bootstrap ([[Statistical Significance in Search Evaluation]]). At n=40, the gap
between 5% and 18% is two queries' worth of movement per percentage point, and no error bars
are given. The direction is clear; the precision implied by the figures is not.

## What It Is Good For

As documentation it is unusually honest about scope — it says outright that BM25 alone was
chosen to keep attention on reranking, that the choice of first stage is a side issue because
the reranker only ever sees the shortlist, and that the one-question-per-pair structure is for
clarity rather than production. As evidence it is a vendor demonstrating its own product on a
hard task and reporting modest absolute numbers, which is more informative than a flattering
benchmark would be.

## Related Concepts

- [[Reranking]] — the stage demonstrated
- [[BM25]] — the first stage supplying the shortlist
- [[Precision and Recall]] — the 100%-recall / 18%-top-1 split is the cleanest illustration in this vault
- [[Pointwise Relevance Evaluation]] — one independent judgment per pair
- [[Calibrated Relevance Probability]] — what the returned noul is
- [[Retrieval Pipeline]] — the two-stage structure the cookbook teaches
- [[Statistical Significance in Search Evaluation]] — what 40 queries cannot support

## Related Notes

- [[CLERC]] — the dataset
- [[Jev]] · [[TypeSafe]] — the model and its vendor
- [[Hev meets Jev]] — the independent evaluation, on [[BEIR]] and with the batch call shape
- [[Introducing System One Models & Jev]] — the model class announcement
- [[When Reranking Becomes a System Boundary]] — the usual retrieval-ceiling argument, inverted here
