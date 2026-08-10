---
type: concept
title: "ITQ"
aliases: ["Iterative Quantization", "iterative quantization"]
tags:
  - concept
  - vector-search
  - quantization
  - dimensionality-reduction
created: 2026-08-10
---

# ITQ — Iterative Quantization

**ITQ (Iterative Quantization)** is a classic learning-to-hash method: reduce dimensions
with [[PCA]], then **rotate the reduced space so that rounding each coordinate to one bit
loses as little as possible**. Gong & Lazebnik, CVPR 2011, extended in TPAMI 2013.

## The Idea

PCA gives you the directions that carry the most variance, but it says nothing about what
happens when you then round each coordinate to a single bit. Two coordinate systems can
retain identical variance while one of them binarizes far more cleanly — it depends on how
the data sits relative to the axes.

ITQ fixes that with a rotation. Rotating a space does not change any distance or variance
in it, so the rotation is "free" in information terms — but it changes where the points
fall relative to the axes, and therefore how much is lost when each axis is collapsed to a
sign. ITQ searches for the rotation that minimizes exactly that loss.

The search alternates: given the current rotation, compute the binary codes; given those
codes, solve for the rotation that best explains them; repeat. It starts from a random
rotation and converges quickly.

## Why It Still Matters

ITQ is the origin point for "learn the transform, don't just pick a random one." That idea
went quiet during the decade when product quantization dominated, and has returned in
[[ASH]], which is ITQ generalized past one bit per dimension — the same PCA-plus-learned-
rotation structure, but the coordinates are quantized to several bits instead of a sign.

The contrast with [[RaBitQ]] is the useful one: RaBitQ also rotates before binarizing, but
uses a **random** rotation, which needs no training and carries theoretical guarantees.
ITQ's rotation is fitted to the corpus, which costs a training step and makes the rotation
a versioned index artifact ([[PCA]] covers what that implies), in exchange for better
codes on real, non-uniform data.

## Related Concepts

- [[PCA]] — the reduction step ITQ builds on
- [[ASH]] — generalizes ITQ beyond one bit per dimension
- [[RaBitQ]] — same rotate-then-binarize shape, random rotation instead of learned
- [[Binary Quantization]] — the family of methods ITQ belongs to
- [[LSH]] — the data-agnostic hashing tradition ITQ departs from by learning from data
- [[Dimensionality Reduction]] · [[Vector Quantization]]

## Related Topics

- [[Dimensionality Reduction vs Quantization]] — ITQ is an early instance of doing both at once
