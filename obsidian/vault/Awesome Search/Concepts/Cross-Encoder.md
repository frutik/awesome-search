---
type: concept
title: "Cross-Encoder"
aliases: ["Cross-encoder Reranker", "Interaction Model", "Early Interaction"]
tags:
  - concept
  - search
  - neural-ir
  - reranking
created: 2026-05-16
---

# Cross-Encoder

## Definition

A **cross-encoder** processes the **query and document jointly** in a single encoder pass, producing a relevance score from their combined representation. It captures rich query-document interactions but requires encoding each pair separately — making it too slow for first-stage retrieval over large corpora.

## How It Works

```
[Query + Document] → BERT encoder → relevance score
```

The query and document are concatenated (with separator tokens) and passed through a transformer together. The `[CLS]` token embedding is projected to a scalar relevance score.

## Key Properties

| Property | Value |
|---|---|
| Query-document interaction | Full (early interaction) |
| Document pre-computation | Not possible — must encode per query-doc pair |
| Speed | Slow — O(num_candidates) at query time |
| Quality | Highest — rich interaction captures subtle relevance |

## Role in Multi-Stage Retrieval

Cross-encoders are typically used as **rerankers** in a two-stage pipeline:

```
Stage 1: Bi-encoder retrieves top-100 candidates (fast)
Stage 2: Cross-encoder reranks top-100 (slow, but small set)
```

This pipeline gets the speed of [[Bi-Encoder]] retrieval with the quality of cross-encoder scoring.

## Training

- Trained on query-document pairs with binary or graded relevance labels
- MS MARCO is the standard training dataset
- Can use knowledge distillation from larger cross-encoders

### Training one without labels

A cross-encoder needs query–document pairs, which is exactly what a new domain lacks. Those pairs can
be manufactured: in [[Improving Search Ranking with Few-Shot Prompting of LLMs]] a 3B [[FLAN-T5]] model
generated queries for a corpus, [[Consistency Filtering]] kept the 43% whose source document ranked #1,
and two negatives per query were sampled from the retrieved top-100. A **22M-parameter 6-layer MiniLM
cross-encoder** trained two epochs on the result reached **80.2 nDCG@10** on [[TREC-COVID]] — 4 points
above the hybrid baseline it reranked, from a labeling budget of three queries.

See [[Synthetic Query Generation]] and [[Hard Negative Mining]].

## Why It's Often the Easier Model to Operate

Quality is the usual reason given for choosing a cross-encoder over a [[Bi-Encoder]]. The operational
reason is less discussed and sometimes decisive: **swapping a cross-encoder requires no re-processing of
the document corpus.** A new bi-encoder means re-embedding and re-indexing everything, so model
versioning is a data migration; a cross-encoder is stateless, so a new version is a deployment.

This is the stated rationale in
[[Improving Search Ranking with Few-Shot Prompting of LLMs]], alongside effectiveness.

The cost — per-query inference over candidates — is managed by shrinking both the candidate set and the
text. That article capped reranking depth at **30** documents and fed the model **query-contextual
dynamic summaries** rather than full abstracts, so the sequence covers only the query-relevant span of
each document. Both levers reduce work without touching the model.

## vs. Other Architectures

| | Cross-Encoder | [[Bi-Encoder]] | [[ColBERT]] |
|---|---|---|---|
| Interaction | Early (joint) | None | Late (token-level) |
| Speed | Slow | Fast | Medium |
| Quality | Best | Good | Near cross-encoder |
| Scalability | Not scalable | Scalable | Scalable |

## Related Concepts

- [[Bi-Encoder]] — faster retrieval model it complements
- [[ColBERT]] — alternative late-interaction model bridging speed and quality
- [[Late Interaction]] — between bi-encoder (none) and cross-encoder (early) interaction
- [[Retrieval Pipeline]] — cross-encoder as Stage 2 reranker
- [[ELSER]] — distilled from a cross-encoder teacher
- [[Interaction Paradigms]] — the no/late/early spectrum; cross-encoder is the early-interaction endpoint

## Articles

- [[Bi-encoder vs Cross-encoder When to Use Which One]]
- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — [[Jo Kristian Bergum]] ([[Vespa]]);
  a 22M cross-encoder trained on synthetic data, and the versioning argument for the architecture
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — [[PROMPTAGATOR]]'s
  cross-encoder as the strongest few-shot model in that comparison (0.528 avg nDCG@10)

## Case Studies

- [[Vespa - Ranking Without Labels on CORD-19]] — cross-encoder as the final stage over a 30-document shortlist
