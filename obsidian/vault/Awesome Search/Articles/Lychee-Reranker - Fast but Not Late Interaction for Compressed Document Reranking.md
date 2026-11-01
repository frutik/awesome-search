---
type: article
created: 2026-10-30
title: "Lychee-Reranker: Fast but Not Late Interaction for Compressed Document Reranking"
source: "https://arxiv.org/abs/2606.22807"
author: ["Xinping Zhao"]
published: 2026-06
concepts: ["[[Fast but Not Late Interaction]]", "[[Late Interaction]]", "[[Cross-Encoder]]", "[[Reranking]]", "[[Matryoshka Embeddings]]", "[[Knowledge Distillation]]", "[[LoRA]]", "[[MUVERA]]", "[[Pooling]]"]
tools: ["[[Lychee-Reranker]]"]
tags: [paper, reranking, cross-encoder, efficiency, encoder-decoder]
---

# Lychee-Reranker: Fast but Not Late Interaction for Compressed Document Reranking

A 31-page technical report (arXiv 2606.22807, cs.CL) first-authored by Xinping Zhao, posted in June 2026 as *KaLM-Reranker-V1* and later renamed *Lychee-Reranker*; the arXiv listing shows a revision dated 16 October 2026. It introduces the [[Fast but Not Late Interaction]] (FBNL) design, implemented in the [[Lychee-Reranker]] model family.

---

## The Problem

Most [[Cross-Encoder|encoder-based and decoder-based rerankers]] process each query-passage pair jointly, so passage representations are recomputed for every query. The authors call this coupling of online computation the obstacle to efficient, flexible deployment. [[Late Interaction]] ([[ColBERT]]-style) encodes the two sides separately, but the paper argues its token-level similarity scoring limits expressiveness.

## The Design

An encoder-decoder model built on T5Gemma2:

- **Offline** — the encoder maps each passage to a reusable representation, compressed with Matryoshka embedding pooling (MEP): mean-pooling consecutive groups of at most *r* tokens. Ratios run from 1x to 128x; the default is r=4 and the paper recommends r=4 to r=16 for practical deployment. Cache size falls from O(N·n·d) to O(N·⌈n/r⌉·d).
- **Online** — the decoder reads a system prompt, a task instruction and the query, and models relevance through merged self-attention and cross-attention over the concatenated query context and the pre-encoded passage representations. The score is the softmax over the "yes" and "no" label tokens.

## Training

Three stages, on about 3.9M instances (one positive and at least 16 hard negatives each), versus 19M for [[Qwen3 Embedding Series|Qwen3-Reranker]]:

1. **SFT** with binary yes/no labels, loss summed over compression ratios {2, 8, 32, 128}.
2. **[[Knowledge Distillation]]** from Qwen3-Reranker-8B as teacher.
3. **Model soup** — averaging Stage 2 checkpoints trained with different [[LoRA]] configurations.

Models are initialised from T5Gemma-2 checkpoints (270M, 1B, 4B), trained on 32 RTX 5090 GPUs with a global batch size of 128.

## Results

All rerankers rescore the same top-100 candidates from KaLM-Embedding-V2.5, measured by nDCG@10, on [[BEIR]] (13 tasks; Touche2020 and TREC-COVID excluded for having only 49 and 50 queries), [[MIRACL]] (18 languages) and six LMEB dialogue-memory tasks.

| BEIR avg nDCG@10 | Score |
|---|---|
| Nano (0.27B) | 58.54 |
| Small (1B) | 61.07 (Qwen3-Reranker-0.6B: 59.36) |
| Large (4B) | 63.53 (Qwen3-Reranker-4B: 63.50; Qwen3-Reranker-8B: 65.11) |

On MIRACL, Large averages 74.92 versus 74.13 for Qwen3-Reranker-8B.

**Cost.** The efficiency claim rests on a time-complexity analysis (|q|=32, n=1024, r=4), not measured latency. Relative estimated online cost: Nano 1.0x, Small 4.6x, Large 29.1x, Qwen3-Reranker-0.6B 28.2x, Qwen3-Reranker-4B 157.8x, Qwen3-Reranker-8B 359.8x.

**Test-time compute.** Rerank 100 candidates at r=32 or r=64, then rescore the top 20 at r=2. For Small on BEIR, average nDCG@10 moved from 61.17 to 61.11 while estimated cost fell from 8.65x to 2.75x.

**Compression vs. size.**
- Smaller models are more sensitive: Nano drops from 58.75 to 55.11 on BEIR as r goes from 2 to 128, Large from 63.69 to 61.23.
- Returns diminish as compute rises; r=4 or r=8 often gives performance close to r=2 at much lower cost.
- Large at r=32 scores 62.18 on BEIR versus 61.17 for Small at r=2, but on MIRACL the order flips (73.26 vs 74.34), so model size and compression ratio should be chosen together.
- Without MEP, Stage 1 Nano on BEIR falls from 53.58 to 38.57 as r goes from 2 to 4; with MEP the decline is much slower.
- ROC-AUC stays relatively stable through r=32 and declines more at r=64 and r=128.

**Memory retrieval (LMEB).** Reranking gains over the first-stage retriever are larger here than on BEIR: 10.27, 12.85 and 14.91 points for Nano, Small and Large, versus 4.76, 7.29 and 9.75 on BEIR. Nano (61.07 average) outperforms embedding models such as bge-multilingual-gemma (59.30) and Nemotron-3-Embed-8B (59.86), so retrieve-then-rerank can beat simply scaling the embedder. On LongMemEval, Large scores 89.54 versus 78.93 for Qwen3-Reranker-8B.

A case study at r=8 shows decoder attention concentrating on passage chunks that match query-relevant spans, suggesting compact representations retain usable evidence.

## Limitations

- Efficiency figures are analytical estimates, not wall-clock measurements.
- Qwen3-Reranker-8B still holds the top BEIR average (65.11 vs 63.53 for Large).
- Quality drops as compression rises, faster for smaller models.
- Multilingual training is limited, and Stage 2 depends on a Qwen3-Reranker-8B teacher.

## Related Concepts
- [[Fast but Not Late Interaction]] · [[Late Interaction]] · [[Cross-Encoder]] · [[Reranking]]
- [[Matryoshka Embeddings]] · [[Pooling]] · [[Knowledge Distillation]] · [[LoRA]] · [[MUVERA]]

## Related Articles
- [[Qwen3 Embedding Series]] — source of the Qwen3-Reranker baselines
- [[MUVERA - Multi-Vector Retrieval via Fixed Dimensional Encodings]] — the other route to cheaper token-level document representations

## Tools
- [[Lychee-Reranker]]

## Datasets
- [[BEIR]] · [[MIRACL]]
