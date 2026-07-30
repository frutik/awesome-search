---
type: tool
title: "Sentence Transformers"
aliases: ["sentence-transformers", "SBERT", "sentence_transformers"]
website: https://sbert.net/
repo: https://github.com/UKPLab/sentence-transformers
tags:
  - tool
  - embeddings
  - fine-tuning
  - open-source
related_concepts:
  - "[[Embeddings]]"
  - "[[Bi-Encoder]]"
  - "[[Cross-Encoder]]"
  - "[[Embedding Fine-tuning]]"
  - "[[SPLADE]]"
created: 2026-07-27
---

# Sentence Transformers

The de facto Python library for training and running embedding models — bi-encoders, cross-encoders, and (since v5) sparse encoders. Maintained under Hugging Face; originally from UKP Lab (SBERT).

🔗 https://sbert.net/ · https://github.com/UKPLab/sentence-transformers

It is the toolchain assumed by most fine-tuning work in this vault: [[Embedding Fine-tuning]], [[Matryoshka Embeddings]] (`MatryoshkaLoss`), [[Multimodal Embeddings]], and the [[SPLADE]] training described below.

## Why It Matters Here

The library's role is that it makes retrieval-model training a configuration exercise rather than a research one. Loss functions, negative sampling strategies, and evaluators ship as composable pieces, so the practitioner question shifts from "can I train this?" to "do I have the data?"

## Sparse Encoder Support (v5)

Version 5 added first-class sparse embedding training, which is what makes [[SPLADE]] fine-tuning accessible without hand-rolling the architecture. SPLADE decomposes into two modules:

| Module | Role |
|---|---|
| `MLMTransformer` | Base encoder + MLM head — logits over the full vocabulary |
| `SpladePooling` | Max over tokens, ReLU activation — vocabulary-axis [[Pooling\|pooling]] |

Training uses `SpladeLoss`, combining `SparseMultipleNegativesRankingLoss` (in-batch negatives) with sparsity regularization under separately tunable query and document weights — in [[Fine-Tuning Sparse Embeddings for E-Commerce Search]], 5e-5 for queries and 3e-5 for documents, the asymmetry reflecting that product descriptions need more surviving terms than queries do.

It also supports **multi-domain training**, the lever for trading peak in-domain accuracy against cross-catalog consistency.

## Common Losses

| Loss | Data shape |
|---|---|
| `MultipleNegativesRankingLoss` (MNRL) | (anchor, positive) pairs — in-batch negatives |
| `TripletLoss` | (anchor, positive, negative) |
| `CoSENTLoss` | Scored pairs |
| `MatryoshkaLoss` | Wrapper for nested-dimension embeddings |
| `SpladeLoss` | Sparse encoders, with sparsity regularization |

## Related Tools

- [[Qdrant Vector DB]] · [[Elasticsearch]] — where the trained representations get indexed
- [[qdrant-sparse-finetune]] — wraps Sentence Transformers for catalog-specific SPLADE training

## Related Concepts

- [[Embeddings]] · [[Dense Embeddings]] · [[Sparse Embeddings]]
- [[Bi-Encoder]] · [[Cross-Encoder]] · [[SPLADE]]
- [[Embedding Fine-tuning]] · [[Hard Negative Mining]] · [[Matryoshka Embeddings]]

## Articles

- [[The Complete Guide to Fine-Tuning Embedding Models]]
- [[Fine-Tuning Text Embeddings For Domain-Specific Search]]
- [[Fine-Tuning an Embedding Model for Semantic Search]]
- [[Introduction to Matryoshka Embedding Models]]
- [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] — sparse-encoder path
