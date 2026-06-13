---
created: 2026-05-15
title: "Qwen3 Embedding Series"
source: "https://qwen.ai/blog?id=qwen3-embedding"
author: "Qwen Team (Alibaba)"
published: 2025-06-05
tags: [embeddings, reranking, Qwen3, multilingual, MTEB, MRL, company-blog]
---

# Qwen3 Embedding Series

**Author:** Qwen Team (Alibaba)  
**License:** Apache 2.0

## Models

| Type | Models | Sizes | Context | Notes |
|---|---|---|---|---|
| Embedding | Qwen3-Embedding-{0.6B,4B,8B} | 0.6-8B | 32K | MRL support, instruction-aware |
| Reranking | Qwen3-Reranker-{0.6B,4B,8B} | 0.6-8B | 32K | Cross-encoder |

## Performance

**Qwen3-Embedding-8B**: #1 on MTEB Multilingual leaderboard as of June 2025 (score 70.58).

Key benchmarks (embedding):
- MTEB-R, CMTEB-R, MMTEB-R: all top-tier
- MTEB-Code: 75.41 (0.6B) to 81.22 (8B)

Reranker scores compared to competitors (MTEB-R):
- Qwen3-Reranker-8B: 69.02 vs BGE-reranker-v2-m3: 57.03

## Architecture

- **Embedding**: causal attention; final embedding = hidden state of `[EOS]` token (last layer)
- **Reranking**: cross-encoder; takes (query, document) pair → relevance score
- Both built on Qwen3 foundation, fine-tuned with LoRA

## Training Pipeline

Three stages:
1. **Contrastive pre-training** (large-scale weak supervision, synthetic pairs via Qwen3 LLM)
2. **Supervised fine-tuning** (high-quality labeled data: MS MARCO, NQ, MIRACL, etc.)
3. **Checkpoint merging** (slerp across intermediate checkpoints → robustness)

## Key Features

- **MRL (Matryoshka Representation Learning)**: flexible vector dimensions across all sizes
- **Instruction-aware**: supports custom instructions for task/language tuning
- **100+ languages** including programming languages
- Compatible with standard embedding + reranking pipelines

## Related Concepts

- [[Dense Vector Retrieval]]
- [[Embedding Fine-tuning]]
- [[Matryoshka Embeddings]]
- [[Semantic Search]]
