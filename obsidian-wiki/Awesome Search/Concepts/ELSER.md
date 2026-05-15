---
title: "ELSER"
aliases: ["Elastic Learned Sparse Encoder", "Elastic Learned Sparse EncodeR"]
tags:
  - concept
  - search
  - sparse-retrieval
  - elasticsearch
---

# ELSER

## Definition

**ELSER** (Elastic Learned Sparse EncodeR) is Elastic's pre-trained learned sparse retrieval model, built on the [[SPLADE]] architecture and integrated natively into Elasticsearch as a `text_expansion` query type. It achieves strong zero-shot retrieval performance without requiring task-specific fine-tuning.

Developed by Thomas Veasey and Quentin Herreros at Elastic.

## How It Differs from SPLADE

ELSER makes several training innovations beyond standard SPLADE:

**Improved teacher model:** Uses an ensemble of MiniLM and MonoT5-3B cross-encoders with monotonic score transformation to smooth distribution skew.

**Training insight:** Vocabulary tokens function as interdependent vector components, not independent lexical items — removing low-scoring tokens reduces quality.

**FLOPS regularizer behavior:** 99% of token pruning occurs in the first 50,000 batches (warmup phase), acting as implicit stop-word removal.

## Performance

BEIR benchmark vs. BM25: **10 wins, 1 draw, 1 loss** across 12 datasets — **17% average NDCG@10 improvement**.

Model size: only 100M parameters (much smaller than many generative models).

## Key Technical Properties

- **Storage efficient:** Documents expand to ~100 tokens on average (approximate size parity with text indices)
- **Inverted index compatible:** Leverages Lucene — no special ANN infrastructure needed
- **Interpretable:** Token highlighting shows which terms drove matches
- **Latency-quality tunable:** FLOPS regularizer controls this tradeoff

## Integration

Available in Elasticsearch as `text_expansion` query clause — one-click deployment without tuning.

## Related Concepts
- [[Embeddings]] — parent concept
- [[Sparse Embeddings]] — ELSER is Elastic's production learned sparse embedding model

- [[SPLADE]] — the architecture ELSER is based on
- [[Sparse Vector Retrieval]] — ELSER is a learned sparse model
- [[Hybrid Search]] — ELSER + BM25 (or dense) hybrid typically outperforms either alone
- [[Cross-Encoder]] — used as teacher in ELSER's distillation training

## Articles

- [[Elastic Learned Sparse Encoder ELSER Retrieval Performance]]
