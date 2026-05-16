---
title: "LoRA"
aliases: ["Low-Rank Adaptation", "LoRA fine-tuning", "low-rank adapter"]
tags:
  - concept
  - fine-tuning
  - llm
  - embeddings
  - machine-learning
---

# LoRA — Low-Rank Adaptation

Parameter-efficient fine-tuning technique. **Hu et al., 2021** (arXiv:2106.09685). Instead of updating all weights of a pre-trained model, LoRA injects small trainable low-rank matrices alongside the frozen originals. The dominant approach in [[PEFT]].

## Core Idea

For a frozen weight matrix W ∈ R^(d×k), LoRA parameterises the update as:

```
W' = W + ΔW = W + A · B
where A ∈ R^(d×r),  B ∈ R^(r×k),  r << min(d, k)
```

- **W is frozen** — never updated
- **A and B are trained** — they hold the adaptation
- **r (rank)** is the key hyperparameter — typically 4–64; lower = fewer params, less capacity

At inference the adapter can be **merged** into W with no overhead: `W_merged = W + A·B`. Or kept separate and swapped per task.

## Why It Works

Full fine-tuning updates O(d×k) parameters. LoRA updates O((d+k)×r) — orders of magnitude fewer when r is small. Despite this, the update matrix ΔW = A·B can represent the relevant adaptations because weight updates in over-parameterised models tend to have low intrinsic rank.

## Practical Parameters

| Param | Meaning | Typical values |
|-------|---------|----------------|
| `r` | Rank | 4, 8, 16, 32, 64 |
| `alpha` | Scaling factor (ΔW scaled by alpha/r) | 16, 32 |
| `target_modules` | Which layers get adapters | Q, K, V projections; sometimes FFN |
| `dropout` | Adapter dropout | 0.05–0.1 |

## Applications in Search

| Use case | What's adapted | Notes |
|----------|---------------|-------|
| **Embedding fine-tuning** | Bi-encoder model | LoRA on Q/K/V; domain adaptation without full retraining |
| **LLM query rewriting** | Instruction-tuned LLM | Teach the model domain vocabulary |
| **Intent/judgment generation** | LLM | Fine-tune for consistent label format |
| **RAG synthesis** | LLM | Domain-specific answer style |

For embedding models specifically: LoRA fine-tuning with contrastive loss achieves comparable recall to full fine-tuning at a fraction of the compute. See [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]] (LoRA on 615M-param model, 0.836 macro-F1).

## vs. Full Fine-tuning

| | Full fine-tuning | LoRA |
|---|---|---|
| Params updated | All (billions) | ~0.1–1% |
| Memory | Huge (optimizer states for all params) | Small |
| Training time | Long | Fast |
| Quality | Best | Near-equivalent on most tasks |
| Multi-task | One model per task | One base + many adapters |

## Related Concepts
- [[QLoRA]] — LoRA + 4-bit quantization of base model; enables fine-tuning on consumer GPUs
- [[PEFT]] — umbrella term; LoRA is the dominant PEFT method
- [[Embedding Fine-tuning]] — domain adaptation of embedding models; LoRA is increasingly the standard approach
- [[LLM]] — primary target for LoRA in search pipelines
