---
type: concept
title: "Fast but Not Late Interaction"
aliases: ["FBNL", "fast-but-not-late-interaction", "Compressed Document Reranking"]
tags:
  - concept
  - search
  - neural-ir
  - reranking
  - efficiency
created: 2026-10-30
---

# Fast but Not Late Interaction

**Fast but Not Late Interaction (FBNL)** is a reranker design from the [[Lychee-Reranker]] paper ([[Lychee-Reranker - Fast but Not Late Interaction for Compressed Document Reranking]]). An encoder-decoder model encodes passages **offline** into compressed, reusable representations; at query time a decoder reads the instruction and query together with those cached representations and answers relevant / not relevant.

---

## How It Works

```
Offline:  passage → Encoder → token states → mean-pool every r tokens → cache
Online:   [system prompt + instruction + query]  ──┐
                                                   ├→ Decoder (self + cross-attention) → P(yes)
          cached compressed passage states       ──┘
```

- **Compression** — Matryoshka embedding pooling (MEP) mean-pools consecutive groups of at most *r* tokens along the sequence dimension, 1x to 128x. Training sums the loss over several ratios so one model works at any of them ([[Matryoshka Embeddings]] applied to the token axis rather than the vector dimension). Cache size drops from O(N·n·d) to O(N·⌈n/r⌉·d). The default is r=4; r=4 to r=16 is recommended in practice.
- **Interaction** — the decoder models relevance through merged self-attention and cross-attention over the concatenated query context and pre-encoded passage representations. The score is the softmax over "yes" and "no" tokens.
- **Adjustable compute** — the ratio can be changed at inference. Reranking 100 candidates at r=32 or 64 and rescoring the top 20 at r=2 kept BEIR nDCG@10 for the Small model essentially flat (61.17 → 61.11) at about a third of the estimated cost.

## Where It Sits

The name defines the design by exclusion. The paper contrasts it with cross-encoders and with late interaction; the bi-encoder row below is added for orientation.

| | Passage side precomputed | Interaction | Used for |
|---|---|---|---|
| [[Bi-Encoder]] | one vector | dot product | retrieval |
| [[Late Interaction]] ([[ColBERT]]) | per-token vectors | token-level MaxSim, no parameters | retrieval or rerank |
| FBNL | compressed encoder states | learned decoder with cross-attention | rerank |
| [[Cross-Encoder]] | nothing | full joint transformer | rerank |

- Against **cross-encoders** — passages are not re-encoded for every query, which is where the online saving comes from.
- Against **late interaction** — the paper argues token-level similarity limits expressiveness; FBNL replaces it with a learned network. The cost is that every query-passage pair still needs a decoder pass, so FBNL reranks a candidate list and does not search an index.

So the design is a cross-encoder-style reranker with an amortised, compressed passage side, not a point between bi-encoder and late interaction.

## Versus MUVERA

Both shrink the token-level passage representation, in different places. [[MUVERA]] folds a late-interaction token set into one fixed-dimensional vector whose inner product approximates MaxSim, for first-stage ANN retrieval, with data-oblivious random construction. FBNL pools encoder states with a learned, compression-aware model and keeps them as a shorter sequence for a decoder to attend over, at the reranking stage. They address different pipeline stages.

## Caveats

The paper's cost numbers come from a time-complexity analysis, not measured latency. Quality falls as compression rises, faster for smaller models: Nano loses about 3.6 BEIR nDCG@10 points going from r=2 to r=128, Large about 2.5.

## Related Concepts
- [[Reranking]] · [[Cross-Encoder]] · [[Late Interaction]] · [[Bi-Encoder]] · [[ColBERT]]
- [[Matryoshka Embeddings]] · [[Pooling]] · [[MUVERA]] · [[Knowledge Distillation]]

## Related Tools
- [[Lychee-Reranker]]

## Related Articles
- [[Lychee-Reranker - Fast but Not Late Interaction for Compressed Document Reranking]]
