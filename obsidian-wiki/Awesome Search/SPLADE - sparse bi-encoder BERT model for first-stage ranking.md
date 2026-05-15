---
title: "SPLADE – a sparse bi-encoder BERT-based model achieves effective and efficient first-stage ranking"
source: "https://europe.naverlabs.com/blog/splade-a-sparse-bi-encoder-bert-based-model-achieves-effective-and-efficient-first-stage-ranking/"
author:
  - "[[Stéphane Clinchant]]"
  - "[[Thibault Formal]]"
published: 2021-07-08
created: 2026-05-15
description: "SPLADE predicts sparse keyword representations compatible with inverted indexes, achieving BERT-level ranking quality with efficient first-stage retrieval."
tags:
  - clippings
---
# SPLADE – Sparse Lexical and Expansion Model for First-Stage Ranking

## Problem

Standard two-stage search pipelines: first-stage BM25 (inverted index) → second-stage BERT reranker. BERT models produce dense vectors incompatible with efficient inverted indexes. SPLADE bridges this gap.

## How it works

SPLADE uses BERT's masked language modeling (MLM) head to map token representations back to the full vocabulary (30,522 subwords), producing **sparse vectors** where each dimension corresponds to an actual word.

Two mechanisms:
1. **Term expansion**: adds missing relevant terms, removes irrelevant ones
2. **Term weighting**: estimates importance scores (like tf-idf)

## Sparsity control

The FLOPS regularizer during training penalizes frequently predicted but irrelevant words. Heavy regularization → representations averaging **18 terms per passage** (vs ~60 average passage length).

## Result

SPLADE achieves competitive performance against dense BERT models while remaining:
- Interpretable (each dimension = a word)
- Compatible with standard inverted indexes
- Tunable for effectiveness vs. efficiency via regularization strength

## Related Concepts
- [[Embeddings]] — parent concept
- [[Sparse Embeddings]] — SPLADE produces vocabulary-space sparse vectors
- [[SPLADE]] — the model described in this paper
- [[BM25]] — classical baseline SPLADE replaces/outperforms
- [[Hybrid Search]] — SPLADE as the sparse leg of hybrid retrieval
- [[Sparse Vector Retrieval]] — inverted index compatibility
- [[Embedding Fine-tuning]] — FLOPS regularization is a form of training constraint

## People
- [[Stéphane Clinchant]] — NAVER LABS; SPLADE co-inventor
- [[Thibault Formal]] — NAVER LABS; SPLADE co-inventor