---
title: "ColPali"
aliases: ["ColPali model", "visual late interaction"]
tags:
  - concept
  - neural-ir
  - multimodal
  - late-interaction
---

# ColPali

## Definition

ColPali is a **visual document retrieval model** that applies [[Late Interaction]] (ColBERT-style MaxSim scoring) to document page images. Instead of extracting text and embedding it, ColPali encodes the entire page image into ~1000 token-level vectors using a vision-language model (PaliGemma backbone). At query time, the MaxSim operator scores each document by comparing all query vectors against all document vectors.

Paper: arxiv:2407.01449

## How It Works

```
Page image  → PaliGemma encoder → [v₁, v₂, ..., v₁₀₀₀]  (per-patch vectors)
Text query  → encoder          → [q₁, q₂, ..., qₙ]       (per-token vectors)

Score = Σᵢ max_j (qᵢ · vⱼ)    (MaxSim / maxSimDotProduct)
```

Unlike ColBERT (text-only), ColPali operates on visual patches — useful for PDFs, slides, and scanned documents where layout and visual content matter.

## Scaling Challenges

ColPali's ~1000 vectors per page create two bottlenecks at scale:
1. **Disk space** — storing thousands of float32 vectors per document is expensive
2. **Query computation** — maxSimDotProduct over 1000 vectors per doc is slow vs. bi-encoders

## Optimization Techniques

### Bit Vectors
Compress document vectors to 1-bit per dimension (sign quantization). Uses `maxSimInvHamming` (hamming distance inversion) for scoring. Enables fast bitwise SIMD operations at the cost of slight accuracy loss. Asymmetric variant: keep query vectors at full precision, quantize only document vectors — preserves score quality with full storage savings.

Elasticsearch field: `"element_type": "bit"` in `rank_vectors`.

### Average Vectors
Compress all page vectors into a single average vector (normalized). Index in HNSW (`dense_vector` field) for fast candidate retrieval. Combine with [[BBQ]] to reduce RAM usage. Accuracy drops compared to full MaxSim, recoverable via two-stage retrieval.

### Token Pooling
See [[Token Pooling]]. Groups semantically similar patch vectors via clustering, replacing each cluster with its mean. Pool factor 3 retains 97.8% of performance while reducing vector count by 66.7%.

## Two-Stage Retrieval Pattern

1. **Retrieve** — use average vector + HNSW kNN over millions of documents
2. **Rerank** — apply full maxSimDotProduct on top-k candidates

This makes ColPali viable for large-scale production workloads in Elasticsearch using the `rescorer` retriever (introduced in 8.18).

## ColPali vs. ColBERT

| | ColPali | [[ColBERT]] |
|---|---|---|
| Input modality | Images (document pages) | Text |
| Vectors per doc | ~1000 (visual patches) | ~100 (tokens) |
| Use case | Visual document search (PDFs, slides) | Text retrieval |
| Storage pressure | Higher | Lower |

## Related Concepts

- [[Late Interaction]] — architecture ColPali is built on
- [[ColBERT]] — text-domain sibling
- [[Token Pooling]] — compression for ColPali's multi-vectors
- [[BBQ]] — quantization to reduce RAM for HNSW index of average vectors
- [[HNSW]] — used for average-vector first-stage retrieval
- [[Multimodal Embeddings]] — broader context
- [[Reranking]] — ColPali used primarily as a reranker

## Articles

- [[ColPali & Elasticsearch - How to Search Complex Documents]]
- [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]]

## Related Topics

- [[Late Interaction in Elasticsearch]] — ColPali indexing/scaling in Elasticsearch
- [[Frontier of Search 2025]] — multimodal late interaction as a 2025 frontier theme
