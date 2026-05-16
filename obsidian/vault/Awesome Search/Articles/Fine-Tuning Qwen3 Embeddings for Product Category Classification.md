---
title: "Fine-Tuning Qwen3 Embeddings for Product Category Classification"
source: "https://blog.ivan.digital/fine-tuning-qwen3-embeddings-for-product-category-classification-on-the-large-scale-product-corpus-3a0919506bc8"
author: "Ivan"
published: 2025-07-20
tags: [embeddings, fine-tuning, LoRA, e-commerce, product-classification, Qwen3]
---

# Fine-Tuning Qwen3 Embeddings for Product Category Classification

**Author:** Ivan (blog.ivan.digital)  
**Dataset:** LSPC (Large-Scale Product Corpus) from Web Data Commons / University of Mannheim

## Task

6-class product category classification on LSPC V2020: Automotive, Baby, Books, Clothing, Jewelry, Shoes.

## Approach

**Qwen3-Embedding-0.6B + LoRA** (r=16, alpha=32)

- LSPC arrives self-labelled — merchants include SEO category markup, so ground truth is free
- LoRA (Low-Rank Adaptation) fine-tunes without updating full 615M parameters
- AdamW optimizer, lr=5e-5, 1 epoch

## Results

- **Macro F1: 0.836** (83.6%)
- **Accuracy: 87.91%**
- Inference: ~300 titles/sec at 3.3-3.9ms latency per title on RTX 5090 (batch size 32)

## Qwen3 Embedding Architecture

Qwen3 Embedding = dense Qwen3 LLM backbone fine-tuned with causal attention. Final embedding = hidden state of `[EOS]` token at the last layer.

Three-stage training:
1. Weak supervision pre-training (150M pairs, synthetic via Qwen3-32B)
2. Supervised fine-tuning on high-quality data (~19M pairs: MS MARCO, NQ, MIRACL, etc.)
3. Checkpoint merging via slerp for robustness

## Key Insight

A self-labelled web corpus (LSPC) with merchant-provided category annotations enables domain adaptation without expensive human labelling. Open-source model + LoRA + free data = production-grade product classifier.

## Related Concepts

- [[Embedding Fine-tuning]]
- [[LoRA]] — technique used for fine-tuning without updating full 615M parameters
- [[PEFT]] — parameter-efficient fine-tuning family
- [[Dense Vector Retrieval]]
- [[Semantic Search]]
