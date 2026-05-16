---
title: "BERT"
aliases: ["BERT", "Bidirectional Encoder Representations from Transformers", "BERT model", "bert-base", "bert-large", "transformer encoder", "masked language model", "MLM"]
tags:
  - concept
  - search
  - nlp
  - embeddings
created: 2026-05-16
---

# BERT

## Definition

BERT (Bidirectional Encoder Representations from Transformers) is a transformer-based language model introduced by Google in 2018 that became the foundation for most modern neural search architectures. It reads text bidirectionally — every token attends to all other tokens — producing rich contextual representations.

**Paper**: "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" — Devlin et al., 2018 (Google AI Language)

## Why BERT Matters for Search

Before BERT, search ranking used shallow lexical features. BERT enabled:
- **Contextual embeddings** — "bank" means different things in "river bank" vs "savings bank"
- **Semantic similarity** — understanding paraphrase and intent beyond keyword overlap
- **Cross-encoder reranking** — query + document fed jointly for deep relevance modeling

BERT is the architectural backbone behind [[Bi-Encoder]], [[Cross-Encoder]], [[ColBERT]], [[SPLADE]], [[ELSER]], and most embedding models.

## Pre-training Tasks

BERT learns language representations from unlabeled text via two tasks:

1. **Masked Language Modeling (MLM)** — randomly mask 15% of tokens, predict the masked tokens from context
2. **Next Sentence Prediction (NSP)** — predict whether sentence B follows sentence A

These tasks force BERT to learn bidirectional context and sentence-level relationships.

## Architecture

- Transformer encoder stack (no decoder)
- `bert-base`: 12 layers, 768 hidden dimensions, 110M parameters
- `bert-large`: 24 layers, 1024 hidden dimensions, 340M parameters
- Input: `[CLS] query [SEP] document [SEP]` for cross-encoder tasks
- Output: per-token contextual embeddings + `[CLS]` pooled sentence embedding

## BERT in Search

### As a Reranker (Cross-Encoder)
Feed `[CLS] query [SEP] doc [SEP]` → fine-tune on relevance labels → `[CLS]` output is relevance score. Used in [[Reranking]] pipelines.

### As an Embedding Model (Bi-Encoder)
Fine-tune with contrastive loss (e.g., Sentence-BERT) → encode query and document separately → cosine similarity for retrieval. Produces [[Dense Embeddings]].

### As a Sparse Encoder
[[SPLADE]] uses BERT's MLM head to produce sparse vocabulary-space vectors. [[ELSER]] is Elastic's production sparse encoder based on the same principle.

## Key Variants and Successors

| Model | Notes |
|---|---|
| RoBERTa | Better pre-training, no NSP |
| DistilBERT | 40% smaller, 97% of BERT quality |
| ALBERT | Parameter sharing, more efficient |
| Sentence-BERT (SBERT) | Fine-tuned for semantic similarity |
| [[ColBERT]] | Late interaction over BERT token embeddings |
| DPR | Bi-encoder for dense retrieval, BERT backbone |

Modern large language models (GPT, Llama, etc.) use decoder architectures — BERT-style encoders remain dominant for **retrieval** tasks because they are faster at inference and produce strong fixed-size representations.

## Related Concepts

- [[Bi-Encoder]] — BERT fine-tuned for dual encoding
- [[Cross-Encoder]] — BERT fine-tuned for joint query-document scoring
- [[ColBERT]] — late interaction over BERT token representations
- [[SPLADE]] — sparse retrieval using BERT's MLM head
- [[ELSER]] — Elastic's production sparse encoder
- [[Dense Embeddings]] — output of BERT-based embedding models
- [[Reranking]] — primary production use case for cross-encoder BERT
- [[Embeddings]] — BERT produces the contextual representations
