---
title: "Late Interaction"
aliases: ["Token-level Interaction", "MaxSim"]
tags:
  - concept
  - search
  - neural-ir
---

# Late Interaction

## Definition

**Late interaction** is a retrieval architecture where query and document representations are computed **independently** (like [[Bi-Encoder]]) but interact at the **token level** during scoring (unlike single-vector bi-encoders). The best-known implementation is [[ColBERT]].

## How It Works

```
Query  → Encoder → [q₁, q₂, ..., qₘ]  (per-token vectors)
Doc    → Encoder → [d₁, d₂, ..., dₙ]  (per-token vectors)

Score = Σᵢ max_j (qᵢ · dⱼ)    (MaxSim)
```

The **MaxSim** operator finds, for each query token, the document token most similar to it, then sums these maximum similarities.

## Interaction Timeline Comparison

```
Early interaction  (Cross-Encoder):  [Q + D] → Encoder → score
No interaction     (Bi-Encoder):     Q → enc → q; D → enc → d; score(q,d)
Late interaction   (ColBERT):        Q → enc → [q_tokens]; D → enc → [d_tokens]; MaxSim
```

## Key Properties

- Documents can be **pre-encoded** (only token-level vectors stored per doc)
- Token-level scoring captures fine-grained relevance
- Requires more storage than single-vector bi-encoders (|tokens| × dim per document)
- Quality approaches [[Cross-Encoder]] while remaining scalable

## Compression

Since late interaction stores many vectors per document, storage is a concern:
- [[ColBERT]] uses 128-dim token vectors
- Vespa's implementation uses int8 compression (32x reduction)
- Residual compression in ColBERTv2 reduces storage 6-10x
- [[Token Pooling]] — clusters similar token vectors and replaces each cluster with its mean; pool factor 3 retains 97.8% performance while cutting vectors by 66.7%
- Bit vectors — sign quantization (>0 → 1); 32× storage reduction; pairs with hamming distance (`maxSimInvHamming`)
- Average vectors — single normalized mean vector per document; HNSW-indexable but loses per-token granularity

## Multimodal Extension: ColPali

[[ColPali]] applies late interaction to document page **images** (PDFs, slides) using a PaliGemma backbone. Generates ~1000 patch-level vectors per page instead of token-level vectors. Same MaxSim scoring, much higher storage pressure. Used primarily as a reranker over HNSW-retrieved candidates.

## Related Concepts

- [[ColBERT]] — primary text-domain implementation of late interaction
- [[ColPali]] — visual-domain late interaction (document page images)
- [[Token Pooling]] — compression for multi-vector late interaction embeddings
- [[Bi-Encoder]] — no interaction model (the baseline)
- [[Cross-Encoder]] — early interaction (joint encoding)
- [[Dense Vector Retrieval]] — late interaction uses multi-vector dense representations

## Articles

- [[What is ColBERT and Late Interaction and Why They Matter in Search]]
- [[Announcing the Vespa ColBERT Embedder]]
- [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]]
