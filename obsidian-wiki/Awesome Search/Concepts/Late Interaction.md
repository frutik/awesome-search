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

## Related Concepts

- [[ColBERT]] — primary implementation of late interaction
- [[Bi-Encoder]] — no interaction model (the baseline)
- [[Cross-Encoder]] — early interaction (joint encoding)
- [[Dense Vector Retrieval]] — late interaction uses multi-vector dense representations

## Articles

- [[What is ColBERT and Late Interaction and Why They Matter in Search]]
- [[Announcing the Vespa ColBERT Embedder]]
