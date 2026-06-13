---
created: 2026-05-15
title: "Why Are Embeddings So Cheap?"
source: "https://www.tensoreconomics.com/p/why-are-embeddings-so-cheap"
author: "[[Piotr Mazurek]]"
published: 2025-09-24
tags: [embeddings, GPU, inference, economics, FLOPS, quantization]
---

# Why Are Embeddings So Cheap?

**Author:** [[Piotr Mazurek]] (tensoreconomics.com)

## Core Finding

Embedding generation is **compute-bound** (not memory-bound). This has two major consequences:

1. The cost of processing a token is tiny → prices have collapsed to near zero
2. Unlike autoregressive generation, batching provides *minimal* throughput benefit (and increases per-user latency severely)

## Why Compute-Bound

An embedding = single forward pass through a transformer, extracting the hidden state at the `[EOS]` token. No autoregressive decode loop.

Using Qwen3-Embedding-8B on H100 SXM:
- Forward pass ≈ 16.4 TFLOPs for S=1024 tokens
- Memory load for model (15 GB) ≈ 4.6ms
- Compute time ≈ 21ms → **compute bottleneck**

~90%+ of execution time is in large matrix multiplication kernels (`nvjet_tst_*`). Flash attention is only 6-15% at typical sequence lengths.

## Cost Calculation

At $2/hr for H100, processing 1040-token sequences at batch=4 (33k tokens/s):

$$\text{Cost} = \frac{\$2/\text{hr}}{33488 \text{ tok/s} \times 3600} \times 10^6 = \$0.0166 \text{ per 1M tokens}$$

At 100% utilization: ~1.6¢/1M tokens. At realistic 10% utilization: ~16¢/1M tokens — close to market rates.

## FLOPS/Dollar as Key Metric

Since embedding is compute-bound, optimize for **FLOPS per dollar**, not VRAM or memory bandwidth.

| GPU | Real TFLOPS | $/hr | TFLOPS/$ |
|---|---|---|---|
| H100 SXM | ~750 | $2.00 | 375 |
| RTX 4090 | ~165 | $0.37 | 445 |

**RTX 4090 has better FLOPS/$ than H100 for embedding workloads.** Performance ratio (~4.5x) is smaller than price ratio (~5.4x), so 4090 is 36% cheaper per million tokens.

A single RTX 4090 rented at $0.37/hr can process ~**1B tokens/day** at continuous load.

## No Sustainable Moat

All major embedding models converge to similar semantic representations (MTEB leaderboard convergence). If all models capture semantics similarly, no provider can charge premium prices. Embedding serving is a commodity → prices approach cost of compute → near zero.

## Contrast with Autoregressive Generation

| | Embeddings | Text Generation |
|---|---|---|
| Bottleneck | Compute (FLOPs) | Memory bandwidth |
| Batching benefit | Minimal, hurts latency | Large, amortizes memory |
| Single user latency impact | Severe with larger batches | Manageable |

## Related Concepts

- [[Dense Vector Retrieval]]
- [[Semantic Search]]
- [[Embedding Fine-tuning]]
