---
title: "Natural Questions"
aliases: ["NQ", "Natural Questions dataset", "Google Natural Questions"]
tags:
  - dataset
  - benchmark
  - information-retrieval
  - question-answering
  - zero-shot
  - search-evaluation
type: dataset
source: Google (Kwiatkowski et al., TACL 2019)
domain: open-domain question answering over Wikipedia
website: https://ai.google.com/research/NaturalQuestions
created: 2026-07-30
---

# Natural Questions

## Overview

**Natural Questions (NQ)** pairs real questions issued to Google search with passages from
Wikipedia. Published by Google (Kwiatkowski et al., TACL 2019), it became one of the standard
training and evaluation corpora for open-domain question answering and, through that, for dense
retrieval — [[Dense Passage Retriever]] is trained on it.

It is one of the 18 zero-shot datasets in [[BEIR]].

As reported in [[Improving Zero-Shot Ranking with Vespa Hybrid Search]]:

| | Natural Questions |
|---|---|
| Queries | 4,352 |
| Judgments per query | ~1.2 |
| Relevance | Binary |
| Query length | 9.2 words |
| Document length | 76.0 words |
| Document corpus | 2.68M |

## The Domain-Shift Pair

NQ's main role in this vault is as one half of a comparison. Set against [[MS MARCO]]:

| | [[MS MARCO]] | Natural Questions |
|---|---|---|
| Query length | 5.9 words | 9.2 words |
| Document length | 56.6 words | 76.0 words |
| Document corpus | 8.84M | 2.68M |
| Source | Web search results | Wikipedia passages only |

The two are close. Both English, both question-like queries over passage-length documents; the
lengths differ by a few words. And that gap is enough: a dense retriever trained on NQ performs
strongly in-domain and **loses to [[BM25]] on MS MARCO zero-shot**, with the [[BEIR]] leaderboard
showing NQ-trained dense models underperforming BM25 across nearly all its datasets.

This is why the pair is useful pedagogically — it shows that domain shift severe enough to break a
single-vector model does not look dramatic from the outside. See [[Zero-Shot Retrieval]].

## Shallow Judgments

At ~1.2 judgments per query with binary relevance, NQ sits at the opposite extreme from
[[TREC-COVID]]'s ~493.5 graded judgments. Many genuinely relevant passages are unlabeled, so
recall-oriented conclusions understate true quality — the same limitation as [[MS MARCO]], and a
reason to read a BEIR average knowing that its constituent datasets measure with very different
precision.

Hybrid ranking gains on NQ are correspondingly small: in
[[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]], BM25 scores 0.327, the
distilled [[ColBERT]] reranker 0.403, and the hybrid 0.404 — one of the few BEIR datasets where the
neural component clearly beats BM25 on its own and fusion adds almost nothing on top.

## Beyond Retrieval Benchmarks

NQ also serves as a reference point for what *trained* query distributions look like. Both
[[Agentic Query Workload]] and [[Frontier of Search 2026]] make the argument that models trained on
short, fluent MS MARCO / Natural Questions queries underperform on the long, operator-laden queries
that agents actually emit — NQ's 9.2-word average being the distribution those models learned.

## Related Concepts

- [[Zero-Shot Retrieval]] — the failure NQ-trained models illustrate
- [[Dense Passage Retriever]] — trained on NQ
- [[Judgment Lists]] — NQ's sparse binary qrels
- [[NDCG]] · [[Precision and Recall]] — metrics limited by judgment sparsity here
- [[Asymmetric Semantic Search]] — the short-question / long-passage shape of the task
- [[Agentic Query Workload]] — where NQ's query distribution stops being representative

## Related Datasets

- [[MS MARCO]] — the domain-shift counterpart
- [[BEIR]] — the suite NQ belongs to
- [[TREC-COVID]] — the deep-judgment contrast

## Articles

- [[Improving Zero-Shot Ranking with Vespa Hybrid Search]] — the NQ / MS MARCO corpus comparison and the DPR result
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — NQ results for BM25, ColBERT, and hybrid

## Source

- Official site — https://ai.google.com/research/NaturalQuestions
- *Natural Questions: A Benchmark for Question Answering Research* — Kwiatkowski et al., TACL 2019
- Via BEIR — https://github.com/beir-cellar/beir
