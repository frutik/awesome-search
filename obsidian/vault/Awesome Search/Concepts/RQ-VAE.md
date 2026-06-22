---
title: "RQ-VAE"
aliases: ["Residual Quantization", "Residual-Quantized VAE", "RQ", "RQ-VAE"]
tags:
  - concept
  - quantization
  - embeddings
  - generative-retrieval
---

# RQ-VAE

**Residual-Quantized Variational Autoencoder** — an autoencoder whose discrete bottleneck is a stack of [[Vector Quantization|vector-quantization]] codebooks applied to *successive residuals*. It turns a continuous content embedding into a short sequence of discrete codes, the standard recipe for building [[Semantic IDs]].

---

## Residual Quantization (RQ)

Plain vector quantization snaps a vector to its single nearest codeword — coarse, and expressive only up to the codebook size. **Residual quantization** refines iteratively across stages, quantizing the error left over by the previous stage:

```
x̂₁ = Q₁(x)              # first approximation
r₁ = x − x̂₁             # residual
r̂₁ = Q₂(r₁)             # quantize the residual
x̂  = x̂₁ + r̂₁ + …        # sum of per-stage codewords
```

Each stage contributes one codebook index. The codes are **hierarchical**: early stages capture coarse structure, later stages add fine detail.

**Expressiveness.** Two stages of 256 codewords each represent 256 × 256 = 65,536 distinct vectors, versus 256 for single-stage VQ — combinatorial capacity from small codebooks. (Classic codebooks are built with k-means / the Linde–Buzo–Gray algorithm.)

## From VQ-VAE to RQ-VAE

A **VQ-VAE** has three parts: an encoder mapping input → continuous latent, a VQ layer snapping that latent to the nearest codebook entry, and a decoder reconstructing from the code. The argmin lookup is non-differentiable, so training uses the **straight-through estimator** (copy gradients past the lookup) and a loss with three terms: reconstruction `‖x − x̂‖²`, codebook loss, and commitment loss.

**RQ-VAE** replaces the single VQ layer with the multi-stage residual quantizer above, yielding a coarse-to-fine sequence of codes instead of one. That sequence is exactly what gets used as a [[Semantic IDs|semantic ID]].

## RQ-KMeans

A memory-efficient alternative to a learned RQ-VAE: represent large cluster centroids via residual-quantization principles rather than storing them explicitly — a lighter way to obtain residual codebooks without full autoencoder training.

## Relation to Other Quantization

RQ-VAE sits in the [[Vector Quantization]] family alongside [[Scalar Quantization]], [[Binary Quantization]], and Product Quantization (PQ). The key distinction is *purpose*: SQ/PQ/binary exist to **compress** vectors for fast ANN search; RQ-VAE exists to produce **generatable, hierarchical tokens** that a sequence model can predict in [[Generative Retrieval]]. RQ (residual) and PQ (sub-vector split) are complementary decompositions — RQ splits along *magnitude/residual*, PQ splits along *dimensions*.

## Related Concepts
- [[Semantic IDs]] — the primary application: codes become item/document identifiers
- [[Vector Quantization]] — parent family (SQ, PQ, binary, RQ)
- [[Generative Retrieval]] — consumes RQ-VAE codes as generation targets
- [[TIGER]] — uses RQ-VAE semantic IDs for generative recommendation
- [[Embeddings]] — the continuous input that RQ-VAE discretizes

## Articles
- [[Semantic IDs for Recommendation Systems]] — [[Janu Verma]]; walks through VQ → RQ → VQ-VAE → RQ-VAE with a worked example
