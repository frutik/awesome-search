---
title: "Dense Passage Retriever"
type: concept
aliases:
  - DPR
  - Dense Passage Retrieval
tags:
  - concept
  - dense-retrieval
  - neural-ir
  - bi-encoder
  - zero-shot
created: 2026-07-30
---

# Dense Passage Retriever

**DPR** is a dual-encoder dense retrieval model — separate BERT encoders for questions and
passages, trained with a contrastive objective so that a question's vector lands near the passage
that answers it. Published by Karpukhin et al. (EMNLP 2020) at Facebook AI Research, it was one of
the results that established dense retrieval as a serious alternative to lexical search for
open-domain question answering.

In this vault it matters less as an architecture — it is a [[Bi-Encoder]], structurally — than as
the canonical **cautionary example** of in-domain success that does not transfer.

---

## The Cautionary Result

DPR is trained on [[Natural Questions]]. As reported in
[[Improving Zero-Shot Ranking with Vespa Hybrid Search]]:

- **In-domain on NQ**: strong performance
- **Zero-shot on [[MS MARCO]]**: underperforms [[BM25]]

And the pattern generalizes — the [[BEIR]] leaderboard shows dense embedding models trained on NQ
substantially underperforming BM25 across nearly all BEIR datasets.

The two corpora are not exotic relative to one another. NQ is Wikipedia passages with 9.2-word
queries; MS MARCO is web-search passages with 5.9-word queries. Similar enough that transfer
*ought* to work, different enough that it doesn't. That narrowness of the gap is the point: domain
shift does not have to be dramatic to break a single-vector model.

## Why a Dual Encoder Is Exposed

DPR pools each passage into one fixed vector, offline, with no knowledge of the query it will
eventually be matched against. The compression forces a training-time decision about which
distinctions to keep — made against the training query distribution. Move the distribution and the
discarded distinctions may be the ones now needed.

This is the general argument developed in [[Zero-Shot Retrieval]] and [[Bi-Encoder]], with
architectures that defer matching to query time ([[ColBERT]], [[Late Interaction]]) or stay in term
space ([[Learned Sparse Retrieval]]) proposed as the more transferable alternatives.

## Related Concepts

- [[Bi-Encoder]] — DPR's architecture; the general form of the same exposure
- [[Dense Vector Retrieval]] — the paradigm DPR helped establish
- [[Zero-Shot Retrieval]] — the failure mode DPR illustrates
- [[BM25]] — the baseline it loses to out-of-domain
- [[ColBERT]] · [[Late Interaction]] — the multi-vector response
- [[Hard Negative Mining]] — central to how dual encoders like DPR are trained
- [[BERT]] — the encoder backbone
- [[Asymmetric Semantic Search]] — the short-question / long-passage setting DPR was built for

## Datasets

- [[Natural Questions]] — DPR's training domain
- [[MS MARCO]] — where it loses to BM25 zero-shot
- [[BEIR]] — where the pattern is shown to be general

## Articles

- [[Improving Zero-Shot Ranking with Vespa Hybrid Search]] — [[Jo Kristian Bergum]] ([[Vespa]]);
  uses DPR as the concrete case of in-domain performance failing to predict generalization
- [[Three mistakes when introducing embeddings and vector search]] — the same argument as a general
  warning about single-vector models out-of-domain

## Source

- *Dense Passage Retrieval for Open-Domain Question Answering* — Karpukhin, Oğuz, Min, Lewis, Wu,
  Edunov, Chen, Yih (EMNLP 2020), arXiv:2004.04906
