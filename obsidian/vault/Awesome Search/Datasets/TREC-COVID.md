---
title: "TREC-COVID"
aliases: ["TREC COVID", "trec-covid", "CORD-19", "TREC-COVID Complete"]
tags:
  - dataset
  - benchmark
  - information-retrieval
  - biomedical
  - zero-shot
  - search-evaluation
type: dataset
source: TREC / NIST, over the CORD-19 corpus (Allen Institute for AI)
domain: biomedical literature — COVID-19 research papers
website: https://ir.nist.gov/covidSubmit/
created: 2026-07-30
---

# TREC-COVID

## Overview

**TREC-COVID** is a biomedical retrieval benchmark built during the COVID-19 pandemic over the
**CORD-19** corpus of coronavirus research papers. It is one of the 18 zero-shot datasets in
[[BEIR]] and, within this vault, the dataset that appears most often when a retrieval method is
being demonstrated on a specialized domain.

Its distinguishing feature among BEIR subsets is **judgment depth**. Where most subsets are shallow
and binary, TREC-COVID carries graded relevance and hundreds of judgments per topic — the product of
an organized TREC assessment effort rather than incidental labels.

| | TREC-COVID | [[Natural Questions]] |
|---|---|---|
| Queries | 50 | 4,352 |
| Judgments per query | **~493.5** | ~1.2 |
| Relevance | **Graded** | Binary |

Corpus size is reported as **171K documents** in
[[Improving Search Ranking with Few-Shot Prompting of LLMs]].

## Why the Judgment Depth Matters

Deep graded judgments make TREC-COVID one of the few BEIR subsets where nDCG@10 measures roughly
what it claims to. Elsewhere in the suite, unjudged-but-relevant documents are common and
recall-oriented conclusions understate real quality — the caveat recorded in [[BEIR]] and
[[MS MARCO]].

The cost is the other axis: **50 queries**. Per-dataset differences of a point or two on TREC-COVID
are not obviously meaningful, and averaging it into a BEIR mean silently gives one deeply judged
50-query set the same weight as a shallow 4,352-query one. See
[[Improving Zero-Shot Ranking with Vespa Hybrid Search]], which makes this asymmetry its argument
for reading per-dataset tables rather than averages.

## Reported Results in This Vault

TREC-COVID as a progression across the Vespa zero-shot series, nDCG@10:

| Method | Score | Source |
|---|---|---|
| Published BEIR BM25 | 0.656 | part two |
| Tuned [[BM25]] (k1=0.9, b=0.4, title+text) | 0.690 | part two |
| Distilled 22M [[ColBERT]] rerank | 0.658 | part two |
| [[Hybrid Search\|Hybrid]] BM25 + ColBERT | 0.750 | part two |
| [[PROMPTAGATOR]] (137B FLAN, few-shot) | 0.762 | part two |
| 22M [[Cross-Encoder\|cross-encoder]] on synthetic data | **80.2** | few-shot prompting post |

> The third article quotes its baselines as 70.0 (BM25) and 76.0 (hybrid) where part two's table
> gives 0.690 and 0.750. The figures differ slightly between the two posts; both are recorded as
> stated.

Elsewhere: [[Announcing the Vespa ColBERT Embedder]] reports 0.8003 compressed vs 0.7939
uncompressed on trec-covid, and [[ColBERT-Zero - To Pre-train Or Not To Pre-train ColBERT Models]]
and [[What is ColBERT and Late Interaction and Why They Matter in Search]] both include it in their
BEIR tables.

## CORD-19 as a Deployment

The corpus is not only a benchmark — it is indexed and searchable at
[cord19.vespa.ai](https://cord19.vespa.ai/) with selectable ranking strategies, which makes it one
of the few places in the vault where a benchmark's ranking profiles can be compared interactively
rather than only read off a table. See [[Vespa - Ranking Without Labels on CORD-19]].

## Related Concepts

- [[NDCG]] — the reported metric; graded judgments are what make it well-posed here
- [[Judgment Lists]] — TREC-COVID's qrels as an unusually deep public judgment set
- [[Zero-Shot Retrieval]] — its role as a domain no model is trained on
- [[Search Evaluation]] — the surrounding practice
- [[Synthetic Query Generation]] — the technique demonstrated on this corpus

## Related Datasets

- [[BEIR]] — the suite it belongs to
- [[MS MARCO]] — the shallow-judgment contrast
- [[Natural Questions]] — the other end of the queries/judgments tradeoff

## Articles

- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — the synthetic-data experiment ran entirely on this dataset
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search]] — TREC-COVID vs NQ as the judgment-depth contrast
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — BM25 / ColBERT / hybrid results

## Source

- TREC-COVID — https://ir.nist.gov/covidSubmit/
- Via BEIR — https://github.com/beir-cellar/beir
- Live index — https://cord19.vespa.ai/
