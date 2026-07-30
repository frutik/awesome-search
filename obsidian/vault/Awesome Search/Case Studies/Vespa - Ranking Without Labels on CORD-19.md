---
type: case-study
title: "Vespa - Ranking Without Labels on CORD-19"
domain: biomedical literature search (COVID-19 research papers)
company: "[[Vespa]]"
concepts:
  - "[[Zero-Shot Retrieval]]"
  - "[[Hybrid Search]]"
  - "[[ColBERT]]"
  - "[[Score Normalization]]"
  - "[[Synthetic Query Generation]]"
  - "[[Consistency Filtering]]"
  - "[[Cross-Encoder]]"
topics:
  - "[[Late Interaction in Vespa]]"
  - "[[Search Quality Assurance]]"
people:
  - "[[Jo Kristian Bergum]]"
tags: [case-study, zero-shot, hybrid-search, colbert, synthetic-data, cross-encoder, trec-covid, vespa]
created: 2026-07-30
---

# Vespa — Ranking Without Labels on CORD-19

## Problem

Build good ranking for a corpus with **no interaction data and no relevance labels**. The corpus is
CORD-19 — 171K COVID-19 research papers — and the constraint is the one most search teams actually
face: every model available is being used out-of-domain, and there is no click log to fine-tune on.

The work runs across three posts by [[Jo Kristian Bergum]] at [[Vespa]] between January and February
2023, each one adding a stage. The output is not only a benchmark result but a live, open-source
application at [cord19.vespa.ai](https://cord19.vespa.ai/) with selectable ranking profiles.

## The Progression

Measured on [[TREC-COVID]] (nDCG@10), the dataset built over this corpus:

| Stage | What was added | TREC-COVID |
|---|---|---|
| 0 | Published BEIR BM25 baseline | 0.656 |
| 1 | [[BM25]] tuned — k1=0.9, b=0.4, title and text scored separately then combined | 0.690 |
| 2 | Distilled 22M [[ColBERT]] reranker, alone | 0.658 |
| 3 | [[Hybrid Search\|Hybrid]] — min-max normalized BM25 + ColBERT | 0.750 |
| 4 | 22M [[Cross-Encoder\|cross-encoder]] trained on synthetic queries | **80.2** |

> Stage 4's post quotes its own baselines as 70.0 (BM25) and 76.0 (hybrid) against part two's 0.690
> and 0.750. The figures differ slightly between posts; each is recorded as its article states it.

Total human labeling across all four stages: **three queries**, used as few-shot examples in a
generation prompt.

## Stage 1 — Beat the Published Baseline First

Before any neural component, the lexical baseline was tuned: non-default BM25 parameters, and the
scoring function applied independently to title and text with a linear combination rather than over
one concatenated field. Across BEIR this lifted the average from **0.440 to 0.453**, beating the
BM25 numbers published with the benchmark.

The methodological point the series draws from this: neural gains reported against a default-configured
BM25 are measured against a weaker baseline than necessary.

## Stage 3 — Fusion, and Where the Engineering Actually Is

The hybrid is a [[Linear Score Combination|linear combination]] of **min-max normalized** BM25 and
ColBERT scores, with the ColBERT model reranking the top 2,000 BM25 hits. The non-obvious part is
that Vespa distributes queries across content nodes, so per-node min-max would normalize the same
document differently depending on its shard. The fix: a custom searcher in the query dispatcher that
collects **match-features** from the nodes, computes global min and max after the merge, scales
uniformly, then weights. See [[Score Normalization]].

Across BEIR the hybrid averaged **0.481** against 0.453 for BM25 and **0.363 for ColBERT alone** —
the neural component loses on its own and still improves the combination, because the two are wrong
about different documents.

## Stage 4 — Manufacture the Missing Labels

With no in-domain labels, generate them:

1. `flan-t5-xl` (3B, [[FLAN-T5]]) prompted with an instruction plus **3** labeled examples produces a
   query per document — 33,099 documents, ~19% of the corpus
2. [[Consistency Filtering]] keeps a pair only when the source document ranks #1 for its generated
   query, using the **stage-3 hybrid model as the filter** — 33,099 → **14,156** (43%)
3. Two negatives per query sampled from the retrieved top-100 ([[Hard Negative Mining]])
4. A 22M 6-layer MiniLM cross-encoder trained 2 epochs, exported to [[ONNX]], deployed as a rerank
   phase over the **top 30** hybrid results

Note the bootstrap: stage 3's model is what makes stage 4's training data trustworthy. Tuning the
baseline paid off twice.

## Serving Constraints Respected Throughout

- **CPU-only** inference; no GPU in the query path
- **End-to-end latency under 60 ms** for the hybrid pipeline
- Expensive models confined to shortlists — 2,000 documents for ColBERT, 30 for the cross-encoder
- Cross-encoder input shortened using **query-contextual dynamic summaries** rather than full
  abstracts, so the model reads only the query-relevant span
- Generation cost bounded and offline: ~$1/hour on one A100 40GB, ~3,600 queries/hour

The cross-encoder was chosen over a [[Bi-Encoder|bi-encoder]] partly for effectiveness and partly
for **model versioning** — replacing a cross-encoder needs no re-processing of the corpus, whereas a
new bi-encoder means re-embedding 171K documents.

## What Generalizes

- **Tune the lexical baseline before adding anything neural.** It is the cheapest gain available and
  it improves everything downstream that uses it as a filter or a fusion component.
- **A component can lose standalone and still earn its place.** ColBERT at 0.363 vs BM25's 0.453,
  yet the fusion beats both.
- **Normalization is a distributed-systems problem, not a formula.** Min-max is trivial arithmetic;
  computing it correctly across shards is where the work is.
- **Three labeled examples can be enough.** Generation plus a round-trip filter converted three
  queries into 14,156 training pairs.
- **Compression hurts more out-of-domain.** The distilled 22M ColBERT underperformed full-size
  variants by more in the zero-shot setting than in-domain evaluation would suggest.

## What to Steal

The stage-3-filters-stage-4 bootstrap is the reusable structure: your current best ranking model,
however unimpressive, is good enough to validate synthetic training data for its own successor.
Nothing about it is Vespa-specific.

## Related Concepts

- [[Zero-Shot Retrieval]] — the starting condition
- [[Hybrid Search]] · [[Score Normalization]] · [[Linear Score Combination]] — stage 3
- [[ColBERT]] · [[Late Interaction]] · [[Knowledge Distillation]] — the reranker and its compression
- [[Synthetic Query Generation]] · [[Consistency Filtering]] · [[Hard Negative Mining]] — stage 4
- [[Cross-Encoder]] · [[Bi-Encoder]] — the final ranker and the versioning argument
- [[BM25]] — the baseline that had to be beaten first
- [[Retrieval Pipeline]] — the phased architecture underneath

## Related Articles

- [[Improving Zero-Shot Ranking with Vespa Hybrid Search]] — the problem statement
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — stages 1–3
- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — stage 4

## Datasets

- [[TREC-COVID]] — the evaluation set over this corpus
- [[BEIR]] — where the hybrid model was validated more broadly

## People

- [[Jo Kristian Bergum]] — [[Vespa]] (now [[Hornet]])

## Source

- https://blog.vespa.ai/improving-zero-shot-ranking-with-vespa/
- https://blog.vespa.ai/improving-zero-shot-ranking-with-vespa-part-two/
- https://blog.vespa.ai/improving-text-ranking-with-few-shot-prompting/
- Live application — https://cord19.vespa.ai/ · Source — https://github.com/vespa-cloud/cord-19-search
