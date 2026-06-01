---
title: "Improving information retrieval in the Elastic Stack: Introducing Elastic Learned Sparse Encoder (ELSER)"
source: "https://www.elastic.co/search-labs/blog/elastic-learned-sparse-encoder-elser-retrieval-performance"
author:
  - "[[Thomas Veasey]]"
  - "[[Quentin Herreros]]"
published: 2023-06-21
created: 2026-05-15
description: "ELSER is Elastic's pre-trained sparse encoder for zero-shot retrieval, built on SPLADE architecture — 17% average NDCG@10 improvement over BM25 across BEIR benchmarks."
tags:
  - clippings
  - company-blog
---
# Elastic Learned Sparse Encoder (ELSER)

ELSER is a 100M-parameter pre-trained language model for zero-shot retrieval in Elasticsearch, built on the SPLADE architecture.

## Performance

- **vs. BM25**: 10 wins, 1 draw, 1 loss across 12 BEIR datasets; **average +17% NDCG@10**
- Outperforms SPLADEv2; integrates as a `text_expansion` query clause

## Why SPLADE architecture?

1. **Storage efficient**: Documents expand to ~100 tokens on average — approximate size parity with normal text indices
2. **Inverted index compatible**: Leverages mature Lucene with superior memory efficiency vs. ANN
3. **Controllable trade-offs**: FLOPS regularizer balances quality vs. latency
4. **Interpretable**: Highlights matching words naturally

SPLADE uses token logits from masked word prediction (not simple synonym expansion).

## Training

- **Distillation**: cross-encoder teacher → sparse student, using MSE loss on score margins
- **Teacher ensemble**: weighted combination of MiniLM and monot5-3b with score distribution smoothing
- **FLOPS regularization key findings**:
  - 99% of token pruning happens in first 50K training batches
  - Reducing regularization or substituting sparser alternatives hurt benchmark performance
  - Larger, diverse batches help more than clustered in-batch negatives
  - Functions analogously to stop-word removal

## Integration

Available via Elasticsearch Relevance Engine. Positioned as complementary to dense vector search, especially for cross-modal retrieval use cases.

## Related Concepts
- [[Embeddings]] — parent concept
- [[Sparse Embeddings]] — ELSER is a learned sparse embedding model
- [[ELSER]] — the model described in this article
- [[SPLADE]] — the architecture ELSER is based on
- [[BM25]] — classical baseline; ELSER achieves +17% NDCG@10 over BM25
- [[Hybrid Search]] — ELSER positioned as complement to dense vector search
- [[Sparse Vector Retrieval]] — inverted index compatibility
- [[NDCG]] — benchmark metric used throughout

## People
- [[Thomas Veasey]] — Elastic; ELSER co-author
- [[Quentin Herreros]] — Elastic; ELSER co-author