---
title: "Sparse Embeddings"
aliases: ["sparse vectors", "sparse representations", "learned sparse", "sparse retrieval vectors"]
tags:
  - concept
  - embeddings
  - vector-search
  - sparse
---

# Sparse Embeddings

A vector representation in vocabulary space where most dimensions are zero. Each non-zero dimension corresponds to a vocabulary token; its value represents how much that token contributes to the document or query's meaning.

Contrast with [[Dense Embeddings]], which have all dimensions active in a continuous latent space.

## The Vocabulary Space

A vocabulary of 30,000 tokens → a 30,000-dimensional vector. For any given document, only 10–200 tokens typically have non-zero weight. This sparsity is the defining property — and makes the vectors compatible with inverted indexes (the same infrastructure as BM25).

```
"running shoes for marathon training"
→ {running: 2.4, shoes: 3.1, marathon: 4.7, training: 2.1, jogging: 0.8, ...}
  (30k dimensions, ~5–20 non-zero)
```

## BM25: Classical Sparse Retrieval

[[BM25]] is the gold standard of classical sparse retrieval. Its "vectors" are implicit:
- Term weights based on TF-IDF with saturation (k1) and length normalization (b)
- No neural component; computed analytically from the corpus

BM25 vectors are never explicitly materialized — the inverted index stores term → posting list directly.

## Learned Sparse: SPLADE and ELSER

Neural models can produce explicit sparse vectors using the transformer's MLM (masked language modeling) head:
1. Pass document through BERT-like model
2. MLM head produces logits over full vocabulary
3. Apply ReLU + log → sparse non-negative vector
4. Non-zero dimensions = tokens that "matter" for this text

**Key difference from BM25**: the model can assign weight to tokens *not in the original text* (query/document expansion). A document about "running" might get weight on "jogging", "marathon", "cardio" even if those words don't appear.

### SPLADE
NAVER LABS. Trained with FLOPS regularization to enforce sparsity (otherwise the model learns dense representations). State-of-the-art learned sparse model on BEIR. See [[SPLADE]].

### ELSER
Elastic's production SPLADE variant, optimized for Elasticsearch deployment. Trained on MS MARCO + domain data. See [[ELSER]].

## Dense vs Sparse: Complementary Strengths

| Capability | Sparse (BM25/SPLADE) | Dense (E5/BGE) |
|---|---|---|
| Exact term match | ✅ Strong | ❌ Weak |
| Rare proper nouns, SKUs | ✅ Strong | ❌ Weak |
| Paraphrase / synonyms | ❌ Weak (BM25) / ✅ (SPLADE) | ✅ Strong |
| Cross-language retrieval | ❌ | ✅ (multilingual models) |
| Index type | Inverted index | ANN (HNSW/IVF) |
| Interpretability | ✅ Token weights visible | ❌ Latent dimensions |

This complementarity is why [[Hybrid Search]] (sparse + dense fusion) consistently outperforms either alone.

## Inverted Index Compatibility

Because sparse vectors are in vocabulary space, they can be stored in a standard inverted index:
- Each token → posting list of (doc_id, weight) pairs
- Query execution: retrieve posting lists for query tokens, score with dot product
- No ANN infrastructure required

Elasticsearch stores SPLADE/ELSER vectors in its `sparse_vector` field type, queried via `sparse_vector` query — same infrastructure as BM25, different weights.

## Hybrid Use

In [[Hybrid Search]], sparse and dense are run as parallel legs and fused with [[Reciprocal Rank Fusion]] or linear score combination. SPLADE as the sparse leg typically outperforms BM25 in hybrid because it expands vocabulary and improves recall.

## Related Concepts
- [[Embeddings]] — parent concept; dense vs. sparse overview
- [[Dense Embeddings]] — complementary representation
- [[SPLADE]] — learned sparse model (NAVER LABS)
- [[ELSER]] — Elastic's production SPLADE
- [[BM25]] — classical (non-neural) sparse retrieval
- [[Sparse Vector Retrieval]] — indexing and querying sparse vectors
- [[Hybrid Search]] — combining sparse + dense
- [[Reciprocal Rank Fusion]] — fusion strategy for hybrid search

## Articles
- [[SPLADE for Sparse Vector Search Explained]]
- [[Hybrid Search SPLADE Sparse Encoder]]
- [[Elastic Learned Sparse Encoder ELSER Retrieval Performance]]
