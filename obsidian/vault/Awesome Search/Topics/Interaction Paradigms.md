---
type: topic
title: "Interaction Paradigms"
aliases: ["Interaction Timing Spectrum", "Query-Document Interaction", "Interaction Timeline", "No Late Early Interaction", "Interaction-based Retrieval Taxonomy"]
tags: [topic, neural-ir, search, retrieval, embeddings]
related_concepts: [Bi-Encoder, Late Interaction, ColBERT, Cross-Encoder, Dense Vector Retrieval, Reranking, Retrieval Pipeline, Learned Sparse Retrieval]
related_topics: [Reasoning Reranking, Frontier of Search 2025]
articles:
  - "[[What is ColBERT and Late Interaction and Why They Matter in Search]]"
  - "[[Cross-Encoders ColBERT and LLM-Based Re-Rankers]]"
  - "[[Bi-encoder vs Cross-encoder When to Use Which One]]"
created: 2026-06-25
---

# Interaction Paradigms

Neural retrieval models can be organized along a single axis: **when** the query and the document are allowed to interact. This timing decision is the master trade-off in neural IR — it determines whether documents can be encoded offline (and therefore whether the model can serve first-stage retrieval at scale) and how much fine-grained relevance signal the scorer can capture. Moving "later" in interaction buys quality; moving "earlier" (toward joint encoding) costs the ability to pre-compute.

This is the broader frame behind the comparison table that lives inside the [[Late Interaction]] concept. The three named points on the spectrum each have a dedicated concept note: [[Bi-Encoder]] (no interaction), [[Late Interaction]] / [[ColBERT]] (late, token-level), and [[Cross-Encoder]] (early, joint).

## The Spectrum

```
No Interaction        Late Interaction      Early Interaction
─────────────────────────────────────────────────────────────
  Bi-Encoder              ColBERT             Cross-Encoder
  (pre-compute)         (at query time,      (at query time,
                        token-level MaxSim)  full cross-attn)
     Fast ◄─────────────────────────────────────────► Accurate
```

```
Early interaction  (Cross-Encoder):  [Q + D] → Encoder → score
No interaction     (Bi-Encoder):     Q → enc → q; D → enc → d; score(q,d)
Late interaction   (ColBERT):        Q → enc → [q_tokens]; D → enc → [d_tokens]; MaxSim
```

## Comparison

| Paradigm | When Q·D interact | Doc pre-encode? | Signal granularity | Speed | Quality | Typical role |
|---|---|---|---|---|---|---|
| **No interaction** ([[Bi-Encoder]]) | Never — only final vectors compared | Yes (single vector) | Coarse (whole-doc) | Very fast | Good | First-stage retrieval |
| **Late interaction** ([[ColBERT]] / [[Late Interaction]]) | At query time, after independent encoding | Yes (per-token vectors) | Fine (token-level via [[ColBERT\|MaxSim]]) | Medium | Near cross-encoder | Retrieval or reranking |
| **Early interaction** ([[Cross-Encoder]]) | During encoding (joint cross-attention) | No — must encode each pair | Finest (full cross-attn) | Slow | Highest | Reranking top-k |

The order of the table *is* the order of the [[Retrieval Pipeline]]: cheap-and-coarse interaction filters the corpus, richer interaction reranks the survivors. Because rerankers only see ~100–1000 candidates, they can afford the expensive end of the spectrum — this is the same ladder explored in [[Reasoning Reranking]].

## Why Timing Is the Master Trade-off

- **Pre-computation gate.** If interaction is deferred until *after* the document is encoded (no / late), document representations can be built offline and indexed. Once interaction happens *during* encoding (early), every query–document pair must be encoded at query time — O(candidates) work that rules out first-stage use.
- **Granularity vs. storage.** Later interaction generally means keeping more per-document state: a single vector (bi-encoder) → many token vectors (late interaction, hence [[Token Pooling]] and compression concerns) → nothing stored but nothing reusable either (cross-encoder).
- **Quality climbs with interaction richness.** Full cross-attention (early) captures the subtlest relevance; whole-document dot products (none) capture the least; token-level MaxSim (late) lands in between.

## A Second Axis: Sparse vs. Dense

The interaction axis is orthogonal to *what the representation is*. The same "no / late / early" question can be asked of sparse models: [[Learned Sparse Retrieval]] ([[SPLADE]], [[ELSER]]) are effectively no-interaction models over learned sparse term weights, scored with an inverted index instead of dot products over dense vectors. [[Hybrid Search]] combines a sparse and a dense no-interaction retriever before any later-interaction reranking.

## Related Concepts
- [[Bi-Encoder]] — the no-interaction baseline (single-vector dual encoder)
- [[Late Interaction]] · [[ColBERT]] — token-level interaction at query time
- [[Cross-Encoder]] — early/joint interaction, the quality ceiling
- [[Dense Vector Retrieval]] — the representation most of this axis runs on
- [[Learned Sparse Retrieval]] — the same axis on sparse representations
- [[Reranking]] · [[Retrieval Pipeline]] — where each paradigm sits in a multi-stage system

## Related Topics
- [[Reasoning Reranking]] — extends the high-interaction end with LLM rerankers
- [[Frontier of Search 2025]] — late interaction as a 2025 frontier theme

## Related Articles
- [[What is ColBERT and Late Interaction and Why They Matter in Search]] — frames the interaction-timing spectrum directly
- [[Cross-Encoders ColBERT and LLM-Based Re-Rankers]] — compares the three paradigms as rerankers
- [[Bi-encoder vs Cross-encoder When to Use Which One]] — the two endpoints, when to pick each
