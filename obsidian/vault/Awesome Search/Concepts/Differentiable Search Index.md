---
title: "Differentiable Search Index"
aliases: ["DSI", "Differentiable Search Index"]
tags:
  - concept
  - generative-retrieval
  - retrieval
  - neural-ir
---

# Differentiable Search Index

**DSI** (Tay et al., Google, 2022 — *"Transformer Memory as a Differentiable Search Index"*) is the seminal formulation of [[Generative Retrieval]] for document search. A single Transformer is trained to map a query directly to the **identifier of a relevant document**, generating the `docid` autoregressively. The corpus is encoded into the model's parameters — the "index" is the network itself, hence *differentiable*.

---

## The Core Idea

Conventional retrieval separates indexing (build an inverted or ANN index) from retrieval (look up the query). DSI collapses both into one model with two training objectives:

- **Indexing**: learn `document text → docid` (memorize the corpus).
- **Retrieval**: learn `query → docid` (answer information needs).

At inference, the model performs constrained beam search over the docid vocabulary to return a ranked list.

## Document Identifiers

DSI's central insight is that **how you name documents matters**. It explores several schemes, finding that *semantically structured* identifiers — built by hierarchically clustering document embeddings so related documents share ID prefixes — generalize far better than arbitrary atomic numbers. This is the direct ancestor of modern [[Semantic IDs]] and the [[RQ-VAE]] code construction used in recommendation.

## Significance

DSI launched the generative-retrieval research line (NCI, GenRet, and the recsys offshoot [[TIGER]]). It reframed retrieval as a sequence-generation problem and showed that a model can serve as both store and search index — at the cost of corpus updates now meaning model updates, the paradigm's main open problem.

## Related Concepts
- [[Generative Retrieval]] — the paradigm DSI established
- [[Semantic IDs]] — descendant of DSI's semantically-structured docids
- [[RQ-VAE]] — the quantization recipe later used to build such IDs
- [[TIGER]] — the recommendation analogue of DSI
- [[Dense Vector Retrieval]] — the retrieve-then-rank approach DSI contrasts with

## Articles
- [[Semantic IDs for Recommendation Systems]] — [[Janu Verma]]; applies the DSI-style generative approach to items
