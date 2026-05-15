---
title: "Announcing the Vespa ColBERT Embedder"
source: "https://blog.vespa.ai/announcing-colbert-embedder-in-vespa/"
author: ["Jo Kristian Bergum"]
tags:
  - clippings
  - colbert
  - vespa
  - embeddings
  - search
concepts:
  - ColBERT
  - Late Interaction
  - Dense Vector Retrieval
created: 2026-05-15
---

# Announcing the Vespa ColBERT Embedder

**Source**: https://blog.vespa.ai/announcing-colbert-embedder-in-vespa/  
**Author**: [[Jo Kristian Bergum]]

## Summary

[[Jo Kristian Bergum]] announces native [[ColBERT]] support in Vespa, including a compression technique that reduces per-document storage from ~25MB to ~780KB (32x reduction) without significant quality loss.

## Key Contribution: 32x Storage Compression

The core technical innovation is **binary quantization of ColBERT token vectors**:

Standard ColBERT stores per-token embeddings as float32:
- 128 dimensions × 4 bytes × ~180 tokens/doc = ~90KB per document
- At 1M docs: ~90GB — prohibitively large

Vespa's approach: binarize token vectors using the sign of each dimension:
- 128 bits per token vector = 16 bytes
- ~180 tokens/doc = ~2.8KB per document  
- **32x reduction**, ~2.8GB at 1M docs

**Quality preservation**: Despite aggressive compression, Vespa reports minimal MRR/NDCG degradation because ColBERT's MaxSim operation is robust to binarization — it still identifies the correct top-token alignments.

## Native Vespa Integration

```yaml
# vespa.ai schema definition
field colbert_tokens type tensor<int8>(tokens{}, x[16]) {
  indexing: attribute | summary
}
```

The embedder handles:
- Document encoding at index time
- Query encoding at query time  
- MaxSim computation natively in Vespa's ranking framework
- No external ColBERT server required

## Performance Results

Bergum reports on BEIR benchmarks:
- Vespa ColBERT beats all tested single-vector bi-encoder models
- Competitive with full-precision ColBERT (original Stanford implementation)
- 32x storage reduction with <1% quality loss

## Why ColBERT in Vespa?

Vespa is uniquely suited for ColBERT because:
1. It supports arbitrary tensor operations in ranking
2. It can store multi-vector representations (one per token) per document
3. The MaxSim operation is expressible as a Vespa ranking function
4. It already had hybrid sparse+dense support

## Relation to Original ColBERT

- Original [[ColBERT]] (Omar Khattab, Matei Zaharia): float32 token embeddings, ~25MB/doc
- Vespa's implementation: binary quantization, ~780KB/doc
- Same query-time MaxSim semantics, drastically reduced storage footprint

## Related Articles

- [[What is ColBERT and Late Interaction and Why They Matter in Search]] — ColBERT theory
- [[Bi-encoder vs Cross-encoder When to Use Which One]] — architectural context
- [[Nearest Neighbor Indexes for Similarity Search]] — retrieval infrastructure

## Related Concepts

- [[ColBERT]] — primary technology
- [[Late Interaction]] — mechanism used
- [[Dense Vector Retrieval]] — infrastructure basis
- [[Bi-Encoder]] — what ColBERT improves on
- [[Hybrid Search]] — Vespa supports ColBERT + BM25 hybrid

## People

- [[Jo Kristian Bergum]] — author, Vespa Chief Scientist
- [[Omar Khattab]] — original ColBERT creator
- [[Matei Zaharia]] — ColBERT co-creator
