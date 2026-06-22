---
title: "Semantic IDs for Recommendation Systems"
type: article
source: "https://januverma.substack.com/p/semantic-ids-for-recommendation-systems"
author: "Janu Verma"
published: 2025-08-04
tags:
  - article
  - generative-retrieval
  - quantization
  - recommendation
  - embeddings
concepts: ["Semantic IDs", "RQ-VAE", "Generative Retrieval", "Vector Quantization", "TIGER"]
topics: ["Generative Retrieval"]
created: 2026-06-22
---

# Semantic IDs for Recommendation Systems

A hands-on explainer by [[Janu Verma]] (*Incomplete Distillation*, 4 Aug 2025) that builds [[Semantic IDs]] from the ground up — from vector quantization through [[RQ-VAE]] — and reproduces a [[TIGER]]-style [[Generative Retrieval|generative recommendation]] pipeline on a real dataset.

> **Vault framing.** This note is anchored to retrieval, not recsys: semantic IDs are the identifier scheme behind [[Generative Retrieval]] and its IR-native origin [[Differentiable Search Index]]. The article is the accessible *reference*; the conceptual weight lives in the [[Semantic IDs]] and [[RQ-VAE]] notes.

Source: https://januverma.substack.com/p/semantic-ids-for-recommendation-systems

---

## What It Covers

- **The problem with atomic IDs** — cold start, long-tail bias, sparsity, and poor cross-dataset generalization when identifiers are opaque numbers.
- **Vector Quantization (VQ)** — mapping continuous embeddings to discrete codewords via nearest-neighbour codebook lookup; codebooks via the Linde–Buzo–Gray (k-means) algorithm.
- **Residual Quantization (RQ)** — staged refinement quantizing successive residuals; two 256-entry stages express 256² = 65,536 vectors. See [[RQ-VAE]].
- **VQ-VAE → RQ-VAE** — encoder / VQ layer / decoder, the straight-through estimator for the non-differentiable lookup, and the reconstruction + codebook + commitment loss.
- **Application to recommendation** — a seq2seq Transformer predicts the next item's semantic ID from a user session ([[TIGER]], [arXiv:2305.05065](https://arxiv.org/pdf/2305.05065)); semantic IDs also used for ranking at YouTube ([arXiv:2306.08121](https://arxiv.org/pdf/2306.08121)).

## The Experiment

- **Dataset**: Amazon Beauty (UCSD). Products converted to text (title, brand, category, price) and embedded with a T5 sentence-transformer → 768-d vectors (32,892 × 768).
- **Quantization**: 3 RQ levels, codebook size 256 → semantic IDs of shape 32,892 × 3.
  - MSE 0.000122, improving across levels; perplexity 230.84 (level 1) → 154.12 (level 3).
  - Uses **RQ-KMeans**, a memory-efficient k-means variant.
- **Result**: the author's seq2seq model reaches **NDCG@10 = 0.018**, versus a YouTube baseline of **0.038** (RQ-VAE + user-specific tokens, 100k training steps).

## Why It's in This Vault

It bridges the existing [[Embeddings]] / [[Vector Quantization]] cluster into [[Generative Retrieval]] — a retrieval paradigm where a model *generates* identifiers instead of scoring an ANN index. The recsys framing is incidental; the transferable ideas are semantic IDs and RQ-VAE.

## Related Concepts
- [[Semantic IDs]]
- [[RQ-VAE]]
- [[Generative Retrieval]]
- [[Differentiable Search Index]]
- [[TIGER]]
- [[Vector Quantization]]
- [[Embeddings]]

## People
- [[Janu Verma]] — author
