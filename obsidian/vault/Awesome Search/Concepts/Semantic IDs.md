---
title: "Semantic IDs"
aliases: ["Semantic ID", "Semantic Identifiers", "content-aware IDs"]
tags:
  - concept
  - generative-retrieval
  - embeddings
  - quantization
  - recommendation
---

# Semantic IDs

A **semantic ID** is a short sequence of discrete codes — derived from an item's or document's *content embedding* — that replaces the arbitrary atomic identifier (e.g. `User 5489`, `doc_001923`) traditionally used in retrieval and recommendation. Because the codes are learned from content, semantically similar items get *similar* ID prefixes, so the identifier itself carries meaning.

The codes are produced by quantizing a content embedding through [[RQ-VAE]] (residual-quantized vector quantization), giving a hierarchical, coarse-to-fine token sequence.

```
Inception     →  [12, 153, 87, 21]
Interstellar  →  [12, 153, 87, 99]   ← shared prefix = shared semantics (sci-fi / Nolan)
```

---

## Why Semantic IDs Matter

Atomic, randomly-assigned IDs are *opaque*: ID 5489 tells a model nothing about ID 5490. This causes well-known failures:

- **Cold start** — a brand-new item has a never-before-seen ID and no learned embedding; a semantic ID is computable from its content on day one.
- **Long-tail / sparsity** — rare items share code prefixes with popular neighbours, so signal transfers to the tail.
- **Vocabulary explosion** — a corpus of *N* items needs an *N*-way softmax over atomic IDs; a semantic ID factorizes this into a few small codebook predictions (e.g. 3 × 256 instead of 1 × 33k).
- **Generalization** — content-derived codes transfer across datasets and time in a way memorized atomic embeddings do not.

## How They Are Built

1. Encode item content (title, brand, category, text, image) into a dense embedding — e.g. a [[Dense Embeddings|T5 / sentence-transformer]] 768-d vector.
2. Quantize the embedding with [[RQ-VAE]]: each residual quantization level emits one codebook index.
3. Concatenate the per-level indices → the semantic ID (e.g. 3 levels × 256-entry codebooks → a 3-token ID).

The result is a tokenization of the corpus: every item becomes a short string over a small, learned vocabulary.

## Use in Retrieval — the Generative Angle

Semantic IDs are the identifier scheme that makes [[Generative Retrieval]] practical. Instead of dense-retrieve-then-rank, a sequence model **generates the target ID token-by-token**:

- **Recommendation**: a seq2seq Transformer reads a user's session (a sequence of item semantic IDs) and *generates* the next item's semantic ID. This is the [[TIGER]] formulation (Rajput et al., 2023, [arXiv:2305.05065](https://arxiv.org/pdf/2305.05065)).
- **Document retrieval**: the same idea predates recsys in [[Differentiable Search Index]] (DSI), where a model maps a query directly to a document's (semantically-structured) identifier.

Because IDs share prefixes, beam search over codebook tokens naturally explores a *neighbourhood* of related items — generalization is built into the decoding.

Semantic IDs have also been applied to the **ranking** stage at YouTube ([arXiv:2306.08121](https://arxiv.org/pdf/2306.08121)).

## Connection to Quantization

Semantic IDs reuse the machinery of [[Vector Quantization]] — but with a different *goal*. Classic VQ/PQ compress vectors to save memory for ANN search; semantic IDs use [[RQ-VAE]] to produce **generatable, hierarchical tokens** that a model can predict. Same tools (codebooks, residual quantization), different objective.

## Related Concepts
- [[RQ-VAE]] — the residual-quantization autoencoder that produces the codes
- [[Generative Retrieval]] — generating identifiers instead of scoring candidates
- [[Differentiable Search Index]] — the IR-native generative-retrieval precursor
- [[TIGER]] — generative recommendation over semantic IDs
- [[Vector Quantization]] — shared codebook/quantization machinery, compression-oriented
- [[Embeddings]] — the content representation that semantic IDs are derived from
- [[Dense Embeddings]] — the encoder output (e.g. T5) fed into RQ-VAE

## Articles
- [[Semantic IDs for Recommendation Systems]] — [[Janu Verma]]; hands-on explainer and Amazon Beauty experiment

## People
- [[Janu Verma]] — explainer and reference implementation
