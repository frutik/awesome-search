---
type: concept
title: "RaBitQ"
aliases: ["Random Bit Quantization", "Gao Long quantization"]
tags:
  - concept
  - vector-search
  - quantization
  - performance
created: 2026-05-16
---

# RaBitQ

Rotation-based binary vector quantization algorithm. **Gao & Long, SIGMOD 2024** (arXiv:2405.12497). Shares the same "rotate then quantize" foundation as [[TurboQuant]] but with different choices: pure binarization instead of Lloyd-Max codebook, and asymmetric 1-bit scoring.

## Core Ideas

1. **Random orthogonal rotation** before quantization — same as TurboQuant; equalizes coordinate variance
2. **Per-vector length rescaling** — store one scalar per vector recording how much quantization shrank the length; multiply back at score time. Fixes the systematic length bias of rotation-based methods at cost of 4 bytes/vector (one multiplication). More efficient than TurboQuant PROD's full QJL projection.
3. **1-bit asymmetric scoring** — data stored as one bit/coordinate (sign after rotation); query stored as B-bit scalar quantization transposed into B bit-planes. Inner product = `AND + popcount` per bit-plane, weighted by `2^b`

## Relationship to TurboQuant

| | TurboQuant (MSE) | RaBitQ |
|---|---|---|
| Rotation | Random orthogonal | Random orthogonal |
| Quantization | Lloyd-Max codebook (universal, no training) | Pure binarization (sign) |
| Length correction | PROD variant (QJL, expensive) | Per-vector scalar (4 bytes, cheap) |
| 1-bit scoring | Codebook lookup | Bit-plane AND + popcount |

Qdrant's TurboQuant implementation borrows RaBitQ's **length renormalization** and **1-bit bit-plane scoring**, combining them with TurboQuant's MSE codebook and anisotropy compensation.

## Where Used
- [[Qdrant]] borrows length renormalization and 1-bit scoring for the TurboQuant 1.18 implementation

## Articles
- [[TurboQuant in Qdrant]] — explains how RaBitQ ideas are incorporated

## A Special Case of ASH

[[ASH]] (2026) reframes RaBitQ as one corner of a larger design space: RaBitQ is what you
get from ASH when you drop the dimensionality reduction, use a single cluster, and take a
**random** rotation instead of a learned one. Extended RaBitQ is the same with more than
one bit per dimension.

The reframing sharpens what RaBitQ trades away. The random rotation is why it needs no
training and carries a theoretical error bound — but that bound assumes the data is spread
evenly over the sphere, and real embeddings are not, so a rotation fitted to the corpus can
do better. ASH measures 2.3–7.1 points higher terminal recall at the same compression.

## Related Concepts
- [[ASH]] — generalizes RaBitQ with a learned projection and dimensionality reduction
- [[ITQ]] — the older learned rotation for binarization
- [[TurboQuant]] — companion rotation-based algorithm; different quantization approach
- [[Binary Quantization]] — RaBitQ is a rotation-enhanced variant of binary quantization
- [[Vector Quantization]] — parent concept
- [[BBQ]] — Elasticsearch's binary quantization (different design space)
- [[HNSW]] — the index RaBitQ-style quantization operates with
- [[Dense Vector Retrieval]]
