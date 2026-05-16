---
title: "QLoRA"
aliases: ["Quantized LoRA", "quantized fine-tuning", "4-bit fine-tuning"]
tags:
  - concept
  - fine-tuning
  - llm
  - quantization
  - machine-learning
---

# QLoRA — Quantized Low-Rank Adaptation

[[LoRA]] fine-tuning with the frozen base model loaded in **4-bit precision**. **Dettmers et al., 2023** (arXiv:2305.14314). Makes it practical to fine-tune large models (65B+ params) on a single consumer GPU.

## What It Adds to LoRA

| Component | Description |
|-----------|-------------|
| **NF4 quantization** | NormalFloat4 — 4-bit data type optimised for weights that follow a normal distribution; theoretically optimal for normally-distributed model weights |
| **Double quantization** | Quantize the quantization constants themselves; saves ~0.37 bits/param |
| **Paged optimizers** | Use NVIDIA unified memory to page optimizer states to CPU RAM during memory spikes; prevents OOM crashes |

The LoRA adapters (A and B matrices) are still trained in **bfloat16** — only the frozen base model weights are quantized.

## Memory Impact

A 65B parameter model in float16 requires ~130 GB VRAM — impossible on a single GPU. With QLoRA:
- 65B model in NF4 ≈ 33 GB
- LoRA adapter (rank 16) ≈ minimal
- Fits on a single 48GB A100 or 2× consumer 24GB GPUs

Quality: QLoRA fine-tuned 65B is competitive with ChatGPT (GPT-3.5 level) on instruction-following benchmarks.

## Relevance to Search

QLoRA is the practical path for search practitioners who need custom LLM behaviour without enterprise GPU budgets:

- **Query understanding**: fine-tune a 7B–13B LLM on domain-specific query→intent examples
- **Judgment generation**: consistent relevance labels at scale
- **RAG synthesis**: domain vocabulary and answer format
- **Reranker**: fine-tune a small cross-encoder for domain-specific ranking

See [[Fine Tune LLM on a Custom Dataset with QLoRA]] — end-to-end tutorial (Phi-2 on custom dataset, `SFTTrainer`).

## QLoRA vs. LoRA

| | LoRA | QLoRA |
|---|---|---|
| Base model precision | bfloat16 / float16 | NF4 (4-bit) |
| VRAM needed | Large | ~4× less |
| Training speed | Faster | Slightly slower (quantization overhead) |
| Quality | Best | Near-identical to LoRA |
| Use when | Sufficient VRAM | Single consumer GPU / cost-constrained |

## Related Concepts
- [[LoRA]] — base technique; QLoRA = LoRA + 4-bit base
- [[PEFT]] — umbrella term
- [[Binary Quantization]] / [[Scalar Quantization]] — quantization at inference; QLoRA is quantization at *training* time
- [[Embedding Fine-tuning]] — domain adaptation; QLoRA applies to LLMs in the search pipeline
- [[LLM]] — primary target
