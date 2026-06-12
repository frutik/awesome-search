---
title: "Sparse Vector Retrieval"
aliases: ["sparse retrieval", "sparse embeddings", "sparse vectors"]
tags:
  - concept
  - search
  - retrieval
  - embeddings
---

# Sparse Vector Retrieval

## Definition

Sparse vector retrieval represents documents and queries as high-dimensional vectors where most values are zero — only a small fraction of dimensions are non-zero. The dimensions correspond to vocabulary terms (typically 30,000+ tokens), and non-zero values represent the learned importance of each term.

Unlike traditional bag-of-words methods (BM25, TF-IDF), modern sparse retrieval learns these weights via neural models rather than counting.

## How It Differs from Dense Retrieval

| Dimension | Sparse | Dense |
|-----------|--------|-------|
| Vector size | 30,000–100,000 dims | 384–4096 dims |
| Non-zero values | ~100–300 per doc | All dims non-zero |
| Interpretability | High (term weights visible) | Low (opaque) |
| Lexical matching | Native | Requires fine-tuning |
| Storage | Inverted index friendly | Requires ANN index |
| Speed | Very fast (hardware-optimized) | Slower (approx. search) |

## Key Models

### [[SPLADE]]
- BERT MLM head → vocabulary logits → Log(1 + ReLU(x)) → MaxPool over tokens
- Learns term expansion: "jaguar" in car context → high weight for "car", "vehicle", "speed"
- Created at NAVER LABS Europe by [[Stéphane Clinchant]] and [[Thibault Formal]]

### [[ELSER]]
- Elastic's production SPLADE-based model
- 17% NDCG@10 improvement over BM25
- Optimized for Elasticsearch inverted index

### uniCOIL
- Simpler: learns scalar weights for existing query terms only (no expansion)
- Fast, lower effectiveness than SPLADE

### DeepImpact
- Token-level importance prediction without expansion
- Trades some recall for speed

## Term Expansion

The key advantage of learned sparse models: they expand queries/documents beyond literal terms.

Example: Query "how to fix a flat tire" might expand to:
- "puncture", "wheel", "replace", "pressure", "pump", "sidewall"

This bridges the vocabulary mismatch gap without requiring dense embeddings.

## Storage and Retrieval

Sparse vectors map naturally to inverted indexes:
```
"car":     [doc1: 0.8, doc3: 0.4, doc7: 0.6]
"vehicle": [doc1: 0.6, doc2: 0.9, doc5: 0.3]
```
Retrieval uses standard posting list intersection + scoring — benefiting from decades of IR optimization.

## In Hybrid Search

[[Hybrid Search]] typically combines sparse + dense:
- **Sparse (SPLADE/BM25)**: lexical precision, term matching
- **Dense ([[Bi-Encoder]])**: semantic recall, paraphrase matching
- Combined via RRF (Reciprocal Rank Fusion) or weighted linear combination

## Related Concepts
- [[Embeddings]] — parent concept; dense vs sparse overview
- [[Sparse Embeddings]] — the representation type this retrieval method indexes

- [[Learned Sparse Retrieval]] — the training paradigm; SPLADE/ELSER are its implementations
- [[SPLADE]] — primary learned sparse model
- [[ELSER]] — Elastic's production sparse model
- [[Hybrid Search]] — sparse + dense combination
- [[Dense Vector Retrieval]] — complementary approach
- [[Bi-Encoder]] — dense counterpart
- [[RAG]] — retrieval pipeline that benefits from sparse

## People

- [[Stéphane Clinchant]] — SPLADE co-inventor, NAVER LABS
- [[Thibault Formal]] — SPLADE co-inventor, NAVER LABS
- [[James Briggs]] — SPLADE explainer articles, Pinecone
