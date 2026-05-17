---
title: "The Mathematics of Google's TurboQuant"
source: "https://prateekchandrajha.github.io/turboquant-math.html"
author: "[[Prateek Chandra Jha]]"
published: 2026-03-01
tags: [TurboQuant, vector-quantization, LLM, KV-cache, Johnson-Lindenstrauss, Lloyd-Max, information-theory]
---

# The Mathematics of Google's TurboQuant

**Author:** [[Prateek Chandra Jha]] (blog post explaining the Google Research paper)

## Summary

A deep mathematical walkthrough of TurboQuant — Google's algorithm that compresses LLM KV-cache vectors to ~3 bits per value (6x reduction) with effectively no quality loss. The post derives the mathematics from first principles: random rotations, Lloyd-Max optimal quantization, and the Johnson-Lindenstrauss lemma.

## The Problem: LLM KV Cache Memory

For Llama 3.1 70B with 128K context, the KV cache consumes ~40 GB of GPU memory — often more than the model weights. Naive quantization introduces systematic bias in attention scores.

## Three-Paper Arc Behind TurboQuant

1. **QJL (AAAI 2025)** — sign of random projection preserves angular information; 1 bit/dimension bias correction
2. **PolarQuant (AISTATS 2026)** — random rotation makes each coordinate follow a known Beta distribution; enables zero-calibration Lloyd-Max quantization
3. **TurboQuant (ICLR 2026)** — combines PolarQuant + QJL for near-optimal distortion with unbiased inner products

## Stage 1: PolarQuant — Rotation Makes Everything Predictable

Apply a random orthogonal rotation `x̃ = Qx`. After rotation, each coordinate follows approximately `N(0, 1/d)` regardless of the input direction.

**Why this helps:** The distribution is now known analytically — we can precompute the optimal Lloyd-Max quantizer once, before seeing any data. No calibration set needed.

### Lloyd-Max Quantizer
Minimizes MSE for a known distribution `p(z)` with `b` bits (`2^b` levels). The optimal partition boundaries and representatives satisfy: boundaries = midpoints of adjacent representatives; representatives = conditional means within intervals. Precomputed as a lookup table — at runtime, quantization is just 7 comparisons and a table index.

## Stage 2: QJL — Fixing the Bias with One Bit

PolarQuant gives low MSE, but MSE-optimal quantizers introduce **systematic bias** in inner products: `E[⟨q, k̂⟩] ≠ ⟨q, k⟩`. QJL fixes this.

### The Sign-Projection Identity
For random Gaussian `g ~ N(0, I)` and fixed vectors `e, q`:
```
E[sign(⟨g, e⟩) · ⟨g, q⟩] = √(2/π) · ⟨q, e⟩ / ‖e‖
```

The `√(2/π)` comes from `E[|g|]` for a standard Gaussian — mean of the half-normal distribution.

### Building the Unbiased Estimator
Store `m` 1-bit sketches: `sᵢ = sign(⟨gᵢ, e⟩)` where `e = k - k̂` (quantization residual).

At query time:
```
⟨q, k⟩ ≈ ⟨q, k̂⟩ + (1/m) Σ √(π/2) · ‖e‖ · sᵢ · ⟨gᵢ, q⟩
```

This is **unbiased**: the two stages cancel perfectly, recovering the true inner product in expectation.

## Full Pipeline

```
Input x → Random Rotation (Q) → Lloyd-Max Quantize (b bits) 
       → Compute Residual e → QJL 1-bit sketch (sᵢ)
Storage: b-bit codes + 1-bit sketch + ‖x‖
Query:   ⟨q, k⟩ ≈ ⟨q, k̂⟩ + (π/2m) Σ sᵢ · ⟨gᵢ, q⟩
```

Total: `b + 1` bits per coordinate (e.g., 3+1=4 bits vs 16 bits FP16 → 4x compression)

## Information-Theoretic Analysis

Shannon's rate-distortion bound: `MSE_min ≥ C · 4^(-b)` (no quantizer can beat this).

TurboQuant achieves: `MSE ≤ (√3π/2) · 4^(-b) ≈ 2.7 · 4^(-b)`

**Within 2.7x of the theoretical optimum at every bitwidth.** The remaining gap is scalar vs. vector quantization — full vector quantization would need `2^(bd)` codewords (infeasible).

## Practical Results

| Config | Bits/value | KV cache (Llama 70B, 128K) | Quality |
|---|---|---|---|
| FP16 | 16 | ~40 GB | Full |
| TurboQuant 4-bit | 4 | ~10 GB | Matches FP16 |
| TurboQuant 3.5-bit | 3.5 | ~8.75 GB | Quality-neutral |
| TurboQuant 3-bit | 3 | ~7.5 GB | Near quality-neutral |

No training, fine-tuning, or calibration data required.

## Broader Applications

- **Vector databases** — compress embeddings for similarity search at lower memory cost
- **Embedding storage** — compress sentence/image embeddings for retrieval
- **Streaming quantization** — online algorithm, each vector quantized independently

## Related Concepts

- [[TurboQuant]] — the concept note
- [[Vector Quantization]] — the broader category
- [[Scalar Quantization]] — what TurboQuant uses (vs. full vector quantization)
- [[Dense Vector Retrieval]] — vector databases benefit from TurboQuant

## Related Articles

- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]]
- [[TurboQuant in Qdrant]]

## People

- [[Prateek Chandra Jha]]
