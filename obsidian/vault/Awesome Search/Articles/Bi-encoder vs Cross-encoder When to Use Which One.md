---
title: "Bi-encoder vs Cross-encoder: When to Use Which One?"
source: "https://medium.com/@sujathamudadla1213/bi-encoder-vs-cross-encoder-when-to-use-which-one-4a20edbe6d37"
author: ["Sujatha Mudadla"]
tags:
  - clippings
  - embeddings
  - search
  - neural-retrieval
concepts:
  - Bi-Encoder
  - Cross-Encoder
  - Retrieval Pipeline
created: 2026-05-15
---

# Bi-encoder vs Cross-encoder: When to Use Which One?

**Source**: https://medium.com/@sujathamudadla1213/bi-encoder-vs-cross-encoder-when-to-use-which-one-4a20edbe6d37

## Summary

A practical comparison of [[Bi-Encoder]] and [[Cross-Encoder]] architectures, explaining when each is appropriate and how they complement each other in a [[Retrieval Pipeline]].

## Bi-Encoder Architecture

**Mechanism**: Two separate encoders (often the same pre-trained model) encode query and document independently:
```
encoder(query) → q_embedding ──┐
                                ├→ cosine_similarity → score
encoder(document) → d_embedding ─┘
```

**Key property**: Documents can be pre-encoded and cached. At query time, only the query needs encoding — retrieval is a nearest-neighbor lookup.

**Characteristics**:
- Speed: very fast (milliseconds at scale with ANN)
- Scale: can search millions of documents
- Quality: good but not state-of-the-art
- Training: contrastive loss on (query, positive, negative) triples

**Best for**: First-stage retrieval, semantic similarity, duplicate detection, clustering

## Cross-Encoder Architecture

**Mechanism**: Query and document are concatenated and fed through a single encoder together:
```
encoder("[CLS] query [SEP] document [SEP]") → relevance_score
```

**Key property**: The model can attend to interactions between query terms and document terms at every layer — full cross-attention captures nuanced relevance signals.

**Characteristics**:
- Speed: slow (linear in corpus size, no pre-computation)
- Scale: can only score ~100–1000 candidates per query
- Quality: state-of-the-art for pairwise relevance
- Training: pointwise or pairwise loss on labeled (query, doc, relevance) data

**Best for**: Re-ranking a small candidate set, document pair classification

## The Two-Stage Combination

The standard production pattern:
```
[Bi-encoder] retrieve top-1000 candidates (fast)
    ↓
[Cross-encoder] rerank to top-10 (accurate)
```

This combines bi-encoder speed with cross-encoder accuracy.

## [[ColBERT]] as Middle Ground

[[ColBERT]]'s late interaction mechanism is explicitly positioned as a middle ground:
- Pre-computes document token embeddings (like bi-encoder)
- At query time: per-token MaxSim scoring (partial interaction)
- Faster than cross-encoder, more accurate than bi-encoder

## Decision Guide

| Scenario | Recommended |
|----------|-------------|
| Search over millions of docs | Bi-encoder (ANN) |
| Re-rank top-100 candidates | Cross-encoder |
| Balance speed and accuracy | ColBERT (late interaction) |
| Limited compute budget | Bi-encoder only |
| Highest accuracy required | Cross-encoder as final stage |

## Related Articles

- [[Announcing the Vespa ColBERT Embedder]] — ColBERT as hybrid solution
- [[What is ColBERT and Late Interaction and Why They Matter in Search]] — deep dive on late interaction
- [[Nearest Neighbor Indexes for Similarity Search]] — bi-encoder infrastructure

## Related Concepts

- [[Bi-Encoder]] — primary architecture
- [[Cross-Encoder]] — comparison architecture
- [[ColBERT]] — late interaction middle ground
- [[Late Interaction]] — ColBERT's mechanism
- [[Retrieval Pipeline]] — how they combine
- [[Dense Vector Retrieval]] — bi-encoder infrastructure
