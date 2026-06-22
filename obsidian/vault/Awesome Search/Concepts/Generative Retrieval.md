---
title: "Generative Retrieval"
aliases: ["Generative Retrieval", "Generative IR", "Generative Recommendation", "Model-Based Retrieval"]
tags:
  - concept
  - generative-retrieval
  - retrieval
  - neural-ir
---

# Generative Retrieval

A retrieval paradigm in which a single sequence model **generates the identifier of the target item or document** directly from the query, rather than embedding the query and scoring it against a separately-indexed corpus. The corpus is, in effect, memorized in the model's parameters; retrieval becomes autoregressive decoding.

Contrast with the dominant **retrieve-then-rank** stack ([[Dense Embeddings|dense bi-encoder]] + [[Approximate Nearest Neighbor Search|ANN]] + reranker): there the index is external and similarity is a dot product. In generative retrieval there is no external ANN index — the model *emits* a document/item ID token by token.

---

## How It Works

1. **Assign each item an identifier** the model can generate — ideally a [[Semantic IDs|semantic ID]] (a short sequence of content-derived codes) rather than an opaque atomic number.
2. **Train a seq2seq / decoder model** to map query (or user session) → identifier.
3. **Decode with beam search** over the identifier vocabulary to produce a ranked list of candidates.

Because well-constructed identifiers share prefixes among related items, beam search explores a *neighbourhood* of semantically-near results — generalization is baked into decoding.

## Lineage

- **[[Differentiable Search Index]]** (DSI, Tay et al., 2022) — the seminal document-retrieval formulation: encode the corpus into a Transformer and generate `docid`s from queries. Introduced semantically-structured document IDs.
- **NCI, GenRet, and successors** — refine ID construction and training for document retrieval.
- **[[TIGER]]** (Rajput et al., 2023) — carries the idea into recommendation: generate the next item's [[RQ-VAE]] semantic ID from a user session.

So the *same* mechanism spans IR and recsys; what differs is whether the generated identifier names a document or an item.

## Why It's Interesting for Search

- **No separate ANN index** to build, shard, and keep in sync with the model.
- **Cold start & long tail** handled through content-derived [[Semantic IDs]].
- **End-to-end** — relevance is learned directly into the generator rather than split across encoder + index + reranker.

**Open challenges:** scaling to web-size corpora, updating the "index" when documents change (the corpus lives in model weights), and decoding latency versus a tuned ANN lookup.

## Related Concepts
- [[Semantic IDs]] — the identifier scheme that makes generation tractable
- [[Differentiable Search Index]] — the IR-native origin of the paradigm
- [[RQ-VAE]] — produces the generatable hierarchical identifiers
- [[TIGER]] — generative recommendation instance
- [[Dense Vector Retrieval]] — the retrieve-then-score paradigm it contrasts with
- [[Bi-Encoder]] — the encoder-based retrieval it departs from

## Articles
- [[Semantic IDs for Recommendation Systems]] — [[Janu Verma]]; a worked generative-recommendation pipeline
