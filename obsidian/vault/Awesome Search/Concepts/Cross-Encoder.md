---
title: "Cross-Encoder"
aliases: ["Cross-encoder Reranker", "Interaction Model", "Early Interaction"]
tags:
  - concept
  - search
  - neural-ir
  - reranking
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
