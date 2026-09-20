---
title: "Hev meets Jev"
type: article
tags: [article, reranking, benchmarks, llm, search-evaluation, calibration]
source: "https://hevmind.com/writing/jev-as-a-reranker/"
author:
  - "[[Hev]]"
published: 2026-09-16
created: 2026-09-19
concepts:
  - "[[Reranking]]"
  - "[[Calibrated Relevance Probability]]"
  - "[[Cross-Encoder]]"
  - "[[Pointwise Relevance Evaluation]]"
  - "[[Listwise Relevance Evaluation]]"
  - "[[NDCG]]"
  - "[[BM25]]"
  - "[[Zero-Shot Retrieval]]"
topics:
  - "[[Reasoning Reranking]]"
  - "[[Retrieval Benchmarks and Leaderboards]]"
companies:
  - "[[TypeSafe]]"
  - "[[Voyage AI]]"
  - "[[Cohere]]"
  - "[[Mixedbread]]"
tools:
  - "[[Jev]]"
  - "[[hev-rerank]]"
datasets:
  - "[[BEIR]]"
---

# Hev meets Jev

**Author:** [[Hev]]
**Source:** https://hevmind.com/writing/jev-as-a-reranker/
**Published:** 2026-09-16

## Summary

A benchmark of [[TypeSafe]]'s structured-output model [[Jev]] used as a search
[[Reranking|reranker]], against three [[BEIR]] subsets. The claim in the first line is the
point of the piece: *"Building your own SOTA reranker is now highly achievable."* With no
reranker training and no corpus-specific tuning, a generic true-or-false question asked once
per candidate document lands within a few thousandths of nDCG@10 of the purpose-built hosted
rerankers, at comparable price — and returns something none of them do, a
[[Calibrated Relevance Probability|calibrated probability]] per document.

## The Approach

[[Jev]] does not generate text. The caller sends a **state** plus a set of typed questions, and
the model answers every question in parallel with a probability. The question type used here is
a **Noul** — Jev's true-or-false type: a statement plus criteria for true and for false,
answered as a probability from 0 to 1.

The state is the query plus thirty candidates keyed `D00`–`D29`:

```json
{"query": "...", "documents": {"D00": {...}, "...": {}, "D29": {...}}}
```

One Noul is asked per document key, and the rank is simply the sort by probability:

```yaml
question: "Document `documents.{id}` is relevant to `query`: it contains information that answers or directly addresses it."
criteria:
  "true":  "The document contains information that answers the query or directly addresses what it asks about."
  "false": "The document is only loosely related, on a similar topic, or does not address what the query asks."
```

Two call shapes are compared:

- **Batch** — thirty Nouls in one call per query.
- **Single** — the same question, one (query, document) pair per call.

The phrasing is deliberately generic. The prompt was tuned on SciFact's *train* split only, and
a version written specifically for that corpus did no better — which the author frames as the
desired outcome for a reranker that will sit inside a search engine that does not know its
corpus in advance.

## Experimental Setup

- Three [[BEIR]] subsets with labeled queries: **SciFact** (300 scientific claims),
  **NFCorpus** (323 medical queries), **FiQA** (300 financial questions).
- [[BM25]] pulls a **top-30 shortlist** per query as the baseline; every reranker permutes that
  same list.
- Metric: **nDCG@10** against the labels, averaged over the three datasets.
- Differences tested by **paired bootstrap over queries**.
- Latency measured per query from a laptop, network included.

## Results

Mean over the three datasets:

| Reranker | nDCG@10, mean | p50 / p95 | $ per 1k queries |
|---|---|---|---|
| Jev reranker, batch | 0.501 | 223 ms / 1.4 s | $0.54 |
| Jev reranker, single | 0.502 | 131 ms / 256 ms per call | $0.87 |
| Voyage rerank-3 | 0.504 | 185 ms / 287 ms | $0.50 |
| Cohere rerank-v3.5 | 0.486 | 192 ms / 456 ms | $2.00 |
| Mixedbread mxbai-rerank-large-v2, hosted | 0.476 | 361 ms / 429 ms | $3.50 |
| MiniLM-L6 cross-encoder, local | 0.447 | | |
| BM25 order, no rerank | 0.404 | | |

Per corpus:

| Reranker | SciFact | NFCorpus | FiQA |
|---|---|---|---|
| Jev reranker, batch | 0.768 | 0.358 | 0.376 |
| Jev reranker, single | 0.772 | 0.358 | 0.376 |
| Voyage rerank-3 | 0.755 | 0.357 | 0.402 |
| Cohere rerank-v3.5 | 0.745 | 0.340 | 0.374 |
| Mixedbread mxbai-rerank-large-v2, hosted | 0.749 | 0.324 | 0.354 |
| MiniLM-L6 cross-encoder, local | 0.682 | 0.336 | 0.323 |
| BM25 order, no rerank | 0.667 | 0.310 | 0.234 |
| gpt-5.6-luna, reasoning off, listwise | 0.747 | 0.355 | 0.363 |
| Claude Haiku 4.5, listwise | 0.723 | | |
| Claude Opus 5, low effort, listwise | 0.756 | | |

Costs are each run's actual usage at list price, normalized to 1,000 queries and averaged over
the three datasets. Voyage's figure comes from its own billed `usage.total_tokens`; Cohere and
Mixedbread charge per search.

### The Honest Read

The author's own summary of the gap, rather than a win claim:

- **Voyage rerank-3 is a hair better and a hair cheaper.**
- Jev's **batch tail is worse** — p95 near 1.4 s against under half a second for the
  purpose-built rerankers. The single shape fixes the tail at the cost of thirty times the
  requests.
- Paired per query, the batch shape is **at or above Cohere on all three** datasets, **above
  Mixedbread on all three**, and **trades with Voyage** — an edge on SciFact, a tie on
  NFCorpus, a loss on FiQA.

## Calibrated Probabilities — the Actual Differentiator

What Jev returns that the purpose-built rerankers do not is a
[[Calibrated Relevance Probability|calibrated probability]] per document. On SciFact:

- documents scored **above 0.9** were judged relevant **76%** of the time;
- documents scored **below 0.1**, **half a percent** of the time.

A [[Cross-Encoder]] gives a logit that has to be thresholded per corpus. A probability, by
contrast, lets you prune an overfetched pool, compare scores across shards and retrieval legs,
and gate a downstream step — with one number you did not have to calibrate yourself. One call
over the pool is a rerank *and* a prune in the same round trip.

## Do You Even Need a Reranker?

The piece also tests whether a general LLM can simply do the job listwise. It can — the catch
is latency and, at the top end, price. On SciFact, the one dataset all of them ran:

| Reranker | nDCG@10, SciFact | p50 / p95 | $ per 1k queries |
|---|---|---|---|
| Jev reranker, batch | 0.768 | 224 ms / 1.8 s | $0.60 |
| Claude Opus 5, low effort, listwise | 0.756 | 5.0 s / 7.5 s | $94.68 |
| gpt-5.6-luna, reasoning off, listwise | 0.747 | 3.2 s / 5.8 s | $2.36 |
| Claude Haiku 4.5, listwise | 0.723 | 2.9 s / 11.6 s | $13.93 |

`gpt-5.6-luna` lands at nearly the same quality *and* cost as the purpose-built models, and
Opus 5 ties Voyage outright — but at seconds per query instead of a fifth of a second, and Opus
costs nearly two hundred times what Voyage does. Opus also **refused 12 of the 300 scientific
claims** outright.

## What Was Checked

A set of validity checks that are worth copying for any reranker evaluation:

- **Determinism** — re-issuing 30 of the batch calls moved scores by 0.004 on average, 0.14 at
  worst, and changed zero top-1 results.
- **[[Position Bias]]** — reversing the candidate order kept per-document scores at Spearman
  0.83 and nDCG@10 within 0.005.
- **A floor** — on SciFact, a random permutation of the same shortlist scores 0.12; BM25's own
  order scores 0.667.
- **Question shape** — a single *Choice* over the documents ("which one answers this?") is
  slightly better when exactly one document is relevant and much worse when many are. One Noul
  per document is the shape to ship.

## Caveats

Stated by the author:

- These are public benchmarks, so **training-set contamination is possible for every model in
  the table**.
- **Rerank depth was 30.** The hosted rerankers accept much deeper lists per call, while Jev's
  32k-token request budget holds about 50 passages.
- Latency was measured **from a laptop with network included**.
- **Jev is hosted only**, so the documents leave your environment.

## Release

The implementation is open at https://github.com/hev/reranker — the prompt, the request schema,
a 90-line wrapper with chunking and a prune threshold, and the results with confidence
intervals. It is on PyPI as [[hev-rerank]]:

```python
# pip install hev-rerank
from hev_rerank import rerank

hits = rerank(query, shortlist, top_n=10, threshold=0.1)
```

## Related Concepts

- [[Reranking]] — the stage being replicated
- [[Calibrated Relevance Probability]] — the property that distinguishes this reranker
- [[Cross-Encoder]] — the incumbent architecture, and the logit-vs-probability contrast
- [[Pointwise Relevance Evaluation]] — one question per (query, document) pair, the shape used here
- [[Listwise Relevance Evaluation]] — the shape the LLM baselines used instead
- [[NDCG]] — the reported metric
- [[BM25]] — the first-stage retriever supplying the top-30 shortlist
- [[Zero-Shot Retrieval]] — no corpus-specific tuning, by design
- [[Position Bias]] — one of the validity checks run
- [[Statistical Significance in Search Evaluation]] — paired bootstrap over queries
- [[Retrieval Pipeline]] — where this reranker would sit

## Related Notes

- [[Jev]] · [[TypeSafe]] — the model and the company behind it
- [[hev-rerank]] — the released wrapper
- [[BEIR]] — the benchmark suite the three subsets come from
- [[Voyage AI]] · [[Cohere]] · [[Mixedbread]] — the purpose-built rerankers compared against
- [[Reasoning Reranking]] — the topic this sits in
- [[When Reranking Becomes a System Boundary]] — the caution that scales with reranker power
- [[Cross-Encoders ColBERT and LLM-Based Re-Rankers]] — the architecture comparison
- [[Introducing System One Models & Jev]] — the vendor announcement published the day before this benchmark; the primary source for why Jev's scores are calibrated
- [[System One Model]] · [[Reinforcement Learning for Calibrated Decisions]] — the model class and the training method behind it
- [[TypeSafe Cookbook - Re-ranking]] — the vendor's own reranking walkthrough, on [[CLERC]] rather than BEIR and using the single call shape
- [[Adapting Jev to Your Domain with GEPA]] — the other independent measurement: calibration on a classification task, and the reminder that these numbers came from an untuned prompt
