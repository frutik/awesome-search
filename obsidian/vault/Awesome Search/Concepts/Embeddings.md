---
title: "Embeddings"
aliases: ["embedding", "vector representation", "neural embeddings", "text embeddings"]
tags:
  - concept
  - embeddings
  - vector-search
  - foundations
---

# Embeddings

A numerical representation of an object (text, image, product, user) as a fixed-length vector of real numbers, where geometric proximity corresponds to semantic similarity. The core primitive of modern semantic search.

```
"running shoes"  →  [0.21, -0.84, 0.03, 0.67, ...]   (768 dimensions)
"jogging sneakers" →  [0.22, -0.81, 0.05, 0.65, ...]  ← close in space
"tax return"       →  [-0.45, 0.12, -0.78, 0.03, ...] ← far in space
```

## The Core Insight

Meaning can be encoded in direction and distance. Two vectors that point similarly encode similar meaning. This enables:
- **Similarity search** — find items closest in vector space to a query
- **Clustering** — group items by meaning
- **Algebra** — king − man + woman ≈ queen (Word2Vec era)
- **Transfer** — a model trained on general text produces useful representations for specialized domains

## Brief History

| Era | Model | Representation |
|---|---|---|
| 2013 | Word2Vec, GloVe | Word-level; static |
| 2015 | FastText | Subword-aware |
| 2018 | ELMo | Contextual word embeddings |
| 2018 | BERT | Contextual; CLS token as sentence rep |
| 2019+ | Sentence-BERT, E5, BGE | Sentence/passage bi-encoders |
| 2024+ | Qwen3, NV-Embed | Instruction-tuned; multi-task; MRL |

## Dense vs Sparse

The two main families differ in representation structure:

| Property | [[Dense Embeddings]] | [[Sparse Embeddings]] |
|---|---|---|
| Dimensionality | 256–3072 (all non-zero) | 30k–100k (mostly zero) |
| Space | Semantic latent space | Vocabulary space |
| Strengths | Semantic similarity, paraphrase | Exact match, rare terms |
| Index type | ANN (HNSW, IVF) | Inverted index |
| Examples | E5, BGE, OpenAI | BM25, SPLADE, ELSER |

Best results in practice: [[Hybrid Search]] combining both.

## How Embeddings Are Trained

**Contrastive learning** (most common for retrieval):
- Positive pairs: (query, relevant document)
- Negative pairs: (query, irrelevant document)
- Loss: pull positives together, push negatives apart (InfoNCE / NT-Xent)

**Masked language modeling** (BERT pretraining):
- Predict masked tokens — forces contextual understanding

**Knowledge distillation**:
- Train smaller model to mimic a larger teacher's embedding space
- See [[raw_articles/Distilling Retrieval Pipelines to a Single Embedding Model]]

**Fine-tuning**:
- Start from a general-purpose model; continue training on domain pairs
- See [[Embedding Fine-tuning]]

## Dimensionality

| Dims | Models | Notes |
|---|---|---|
| 256–384 | MiniLM, all-MiniLM | Fast; light memory |
| 768 | BERT-base, E5-base | Standard; good quality |
| 1024 | E5-large, BGE-large | Higher quality; slower |
| 1536 | OpenAI text-embedding-3-small | API-served |
| 3072 | OpenAI text-embedding-3-large | Highest quality API |

[[Matryoshka Embeddings]] (MRL) allow truncating to smaller dims at query time — the same model supports multiple dimensionalities.

## Embedding Quality vs Cost

At scale, the economics of embedding inference matter:
- Embedding generation is **compute-bound** (not memory-bound)
- RTX 4090 offers better FLOPS/$ than H100 for inference
- ~$0.01/1M tokens achievable with commodity hardware
- See [[Why Are Embeddings So Cheap]]

## Compression via Quantization

Full-precision (float32) embeddings are memory-hungry. [[Vector Quantization]] compresses them:
- **SQ8** (int8): 4× smaller, near-lossless
- **Binary / BBQ**: 32× smaller, fast Hamming distance
- **Product Quantization**: 32–64× smaller

See [[BBQ]] for Elasticsearch's implementation.

## Related Concepts
- [[Dense Embeddings]] — all dimensions active; semantic latent space
- [[Sparse Embeddings]] — vocabulary-space; mostly zero
- [[Dense Vector Retrieval]] — how dense embeddings are indexed and queried
- [[Sparse Vector Retrieval]] — inverted index approach
- [[Hybrid Search]] — combining dense + sparse
- [[Bi-Encoder]] — architecture that produces embeddings
- [[Embedding Fine-tuning]] — domain adaptation
- [[Matryoshka Embeddings]] — flexible-dimension embeddings
- [[Vector Quantization]] — compressing embeddings for scale
- [[Task-Aware Embeddings]] — instruction-guided representations
- [[Semantic IDs]] — embeddings quantized into discrete, content-derived identifiers
- [[Generative Retrieval]] — generating item/document IDs instead of scoring vectors

- [[Region-Based Representation]] — region (not point) embeddings: boxes, Gaussians, hyperbolic
- [[Box Embedding]] — words as axis-aligned boxes; containment & set operations
- [[Word2Box]] — unsupervised box embeddings, CBOW-style
- [[Set-Theoretic Embeddings]] — embeddings that support intersection/union/containment
- [[Word2Vec]] — the foundational point-embedding method

## Articles
- [[Why Are Embeddings So Cheap]] — [[Piotr Mazurek]]; economics of embedding inference
- [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]] — LoRA fine-tuning on domain data
- [[Qwen3 Embedding Series]] — state-of-the-art open-source embedding models
- [[raw_articles/Distilling Retrieval Pipelines to a Single Embedding Model]] — [[Daniel Tunkelang]]; bag-of-documents training approach

## People
- [[Daniel Tunkelang]] — bag-of-documents embedding model
- [[Piotr Mazurek]] — embedding economics
