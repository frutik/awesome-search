---
title: "PROMPTAGATOR"
type: concept
aliases:
  - Promptagator
  - Few-Shot Dense Retrieval From 8 Examples
tags:
  - concept
  - synthetic-data
  - few-shot
  - llm
  - dense-retrieval
  - zero-shot
created: 2026-07-30
---

# PROMPTAGATOR

A few-shot approach to domain-specific retrieval from Google Research: prompt a very large language
model with a handful of labeled examples, generate synthetic in-domain training data, and train a
retriever and reranker on it. Published as *Promptagator: Few-shot Dense Retrieval From 8 Examples*
(arXiv:2209.11755).

It is the reference point the Vespa zero-shot series measures itself against, in both directions —
first as the stronger few-shot method that a zero-shot pipeline cannot quite reach, then as the
method a much smaller generator matches.

---

## Position Relative to Zero-Shot Hybrid

From [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]], averaged over the subset
of [[BEIR]] datasets PROMPTAGATOR reports:

| Model | Average nDCG@10 |
|---|---|
| Vespa hybrid (zero-shot, no in-domain data) | 0.456 |
| PROMPTAGATOR (dense retriever) | 0.478 |
| PROMPTAGATOR (cross-encoder) | **0.528** |

Per-dataset figures available from that article:

| Dataset | Vespa Hybrid | PROMPTAGATOR (dense) | PROMPTAGATOR (cross-encoder) |
|---|---|---|---|
| TREC-COVID | 0.750 | 0.756 | 0.762 |
| FiQA-2018 | 0.292 | 0.462 | 0.494 |
| ArguAna | 0.404 | 0.594 | 0.630 |
| HotpotQA | 0.632 | 0.614 | 0.736 |

> The reported averages do not reconcile with these four rows alone, so the comparison spans more
> datasets than are captured here.

The comparison is not apples to apples, and the article says so: PROMPTAGATOR uses in-domain
synthetic data and is therefore **few-shot, not zero-shot**. Its cross-encoder also re-ranks the
top 200 and depends on billion-parameter LLM inference for the generation step. The zero-shot
hybrid's claim is efficiency — CPU-only serving, sub-60 ms latency, no per-domain training step —
rather than higher quality.

## Then Beaten by a 3B Generator

A month later, [[Improving Search Ranking with Few-Shot Prompting of LLMs]] applied the same
overall recipe to [[TREC-COVID]] with a **3B** generator ([[FLAN-T5]] xl) instead of
PROMPTAGATOR's **137B FLAN** model:

| Model | TREC-COVID nDCG@10 |
|---|---|
| Cross-encoder on 3B-generated synthetic data | **80.2** |
| PROMPTAGATOR (137B FLAN) | 76.2 |

A roughly 45× smaller generator produced better downstream ranking on this dataset. The
inference to draw is narrow — one dataset, one comparison — but it points at prompt design and
[[Consistency Filtering]] mattering more than raw generator scale.

## Related Concepts

- [[Synthetic Query Generation]] — the general technique PROMPTAGATOR is an instance of
- [[Consistency Filtering]] — the round-trip filtering idea shared across this line of work
- [[Cross-Encoder]] — PROMPTAGATOR's stronger of the two reported models
- [[Bi-Encoder]] · [[Dense Vector Retrieval]] — its dense retriever
- [[Zero-Shot Retrieval]] — the setting few-shot generation is designed to escape
- [[FLAN-T5]] — the open, much smaller generator used against it
- [[Hybrid Search]] — the zero-shot alternative it is compared with

## Datasets

- [[BEIR]] — the evaluation suite for the comparison
- [[TREC-COVID]] — the single dataset where a 3B generator beat it

## Articles

- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — [[Jo Kristian Bergum]]; the BEIR comparison
- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — [[Jo Kristian Bergum]]; the smaller-generator result

## Source

- *Promptagator: Few-shot Dense Retrieval From 8 Examples* — arXiv:2209.11755, https://arxiv.org/abs/2209.11755
- Related prior work cited alongside it: *InPars* — arXiv:2202.05144, https://arxiv.org/abs/2202.05144
