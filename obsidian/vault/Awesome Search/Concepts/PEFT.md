---
title: "PEFT"
aliases: ["Parameter-Efficient Fine-Tuning", "parameter efficient fine-tuning", "adapter methods"]
tags:
  - concept
  - fine-tuning
  - llm
  - embeddings
  - machine-learning
---

# PEFT — Parameter-Efficient Fine-Tuning

Umbrella term for fine-tuning techniques that update only a small fraction of model parameters while keeping most weights frozen. The HuggingFace `peft` library is the standard implementation. Enables domain adaptation of large models without full fine-tuning cost.

## Why PEFT

Full fine-tuning a 7B model requires storing optimizer states for 7B parameters (~84 GB for Adam). PEFT methods update 0.1–1% of parameters, making fine-tuning practical on limited hardware and enabling one base model to serve many tasks via swappable adapters.

## Main Methods

| Method | How it works | Params updated | Best for |
|--------|-------------|---------------|---------|
| **[[LoRA]]** | Low-rank matrices injected alongside frozen weights | ~0.1–1% | LLMs, embedding models — dominant method |
| **[[QLoRA]]** | LoRA + 4-bit base quantization | ~0.1–1% | Consumer GPU fine-tuning |
| **Prefix Tuning** | Learnable tokens prepended to every layer's key/value | ~0.1% | Sequence generation |
| **Prompt Tuning** | Learnable tokens at input only | <0.01% | Large models (≥11B); less effective on small models |
| **IA³** | Scale activations with learned vectors | ~0.01% | Few-shot; minimal params |
| **Adapter layers** | Small bottleneck MLP inserted between transformer layers | ~1–3% | Original PEFT approach; slower than LoRA |

**LoRA dominates in practice** — best quality/efficiency trade-off across LLMs and embedding models.

## In the Search Pipeline

| Stage | PEFT technique | Purpose |
|-------|---------------|---------|
| Embedding model | LoRA (contrastive) | Domain adaptation of bi-encoder |
| Query understanding | QLoRA | Fine-tune LLM on domain queries |
| Reranking | LoRA on cross-encoder | Domain-specific relevance scoring |
| Answer synthesis (RAG) | QLoRA | Domain vocabulary, format control |
| Judgment generation | QLoRA | Consistent relevance labels |

## Relationship to Domain Adaptation

PEFT is the primary mechanism for [[Embedding Fine-tuning|domain adaptation]] of neural search components. Before PEFT, domain adaptation required either:
- Full fine-tuning (expensive, needs large GPU cluster)
- Prompt engineering (limited effect on retrieval quality)
- Training from scratch (prohibitive)

With LoRA/QLoRA, a search team with a single GPU can produce a domain-adapted embedding model or LLM reranker in hours.

## Related Concepts
- [[LoRA]] — the dominant PEFT method
- [[QLoRA]] — LoRA + 4-bit quantization
- [[Embedding Fine-tuning]] — domain adaptation of embedding models; PEFT is the practical path
- [[LLM]] — primary target for PEFT in search pipelines
