---
title: "Announcing the Vespa ColBERT embedder"
source: "https://blog.vespa.ai/announcing-colbert-embedder-in-vespa/"
author:
  - "[[Jo Kristian Bergum]]"
published: 2024-02-14
created: 2026-05-15
description: "Vespa releases a native ColBERT embedder with token-level vector representations and 32x compression via asymmetric binarization."
tags:
  - clippings
---
# Announcing the Vespa ColBERT embedder

ColBERT maintains per-token vector representations. Each query token interacts with all document tokens via contextualized embeddings (MaxSim). Unlike single-vector models, it approaches cross-encoder performance in zero-shot settings with better training efficiency and explainability.

## Storage Optimization

A novel asymmetric binarization compression reduces storage by 32x. Query vectors keep full precision; document token vectors use binary representation. At `int8` precision, 128-dimensional floats compress to 16 bytes.

## Ranking Performance

MaxSim requires ~2×M×N×K floating-point ops. Re-ranking 100 documents takes ~23ms on a single CPU thread.

## BEIR Benchmark Results (compressed vs uncompressed)

| Dataset | Compressed nDCG@10 | Uncompressed nDCG@10 |
|---|---|---|
| trec-covid | 0.8003 | 0.7939 |
| nfcorpus | 0.3323 | 0.3434 |
| fiqa | 0.3885 | 0.3919 |

## Long Context

ColBERT handles extended documents via text chunking — supports array inputs mapped to multiple tensor dimensions for per-paragraph representations.

## Usage

Configured in `services.xml`, integrates with Vespa's ranking framework alongside BM25, cross-encoders, and other signals. Supports hybrid search and structured field embeddings.

## Related Concepts
- [[Embeddings]] — parent concept
- [[Dense Embeddings]] — ColBERT produces per-token dense embeddings
- [[ColBERT]] — the model being deployed in Vespa
- [[Late Interaction]] — the mechanism ColBERT implements
- [[Bi-Encoder]] — simpler alternative ColBERT improves upon
- [[Cross-Encoder]] — more accurate alternative ColBERT approximates
- [[Vector Quantization]] — asymmetric binarization gives 32× compression
- [[Dense Vector Retrieval]] — ANN index infrastructure
- [[Hybrid Search]] — Vespa supports ColBERT alongside BM25

## People
- [[Jo Kristian Bergum]] — Vespa; ColBERT embedder author