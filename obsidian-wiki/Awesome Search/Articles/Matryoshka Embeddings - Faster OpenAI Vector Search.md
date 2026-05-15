---
title: "Matryoshka Embeddings: Faster OpenAI Vector Search Using Adaptive Retrieval"
source: "https://supabase.com/blog/matryoshka-embeddings"
author: ["Supabase"]
tags:
  - clippings
  - embeddings
  - matryoshka
  - vector-search
  - performance
concepts:
  - Matryoshka Embeddings
  - Dense Vector Retrieval
  - Retrieval Pipeline
created: 2026-05-15
---

# Matryoshka Embeddings: Faster OpenAI Vector Search Using Adaptive Retrieval

**Source**: https://supabase.com/blog/matryoshka-embeddings  
**Publisher**: Supabase

## Summary

Supabase explores using [[Matryoshka Embeddings]] from OpenAI's `text-embedding-3-small` and `text-embedding-3-large` to implement **adaptive retrieval** — a two-pass search where a cheap first pass with truncated (small) embeddings narrows the candidate set, followed by re-ranking with full-dimension embeddings.

## OpenAI Matryoshka Models

OpenAI's `text-embedding-3-small` and `text-embedding-3-large` support native dimension truncation:
```python
import openai

# Full 1536 dims
embedding_full = openai.Embedding.create(
    input="search query", 
    model="text-embedding-3-large",
    dimensions=1536
)

# Truncated to 256 dims (still semantically valid!)
embedding_small = openai.Embedding.create(
    input="search query",
    model="text-embedding-3-large", 
    dimensions=256
)
```

The truncated version retains most of the semantic quality despite using only 16% of dimensions.

## Two-Pass Adaptive Retrieval

```
Query embedding (256-dim)
    ↓
[ANN search over 256-dim index]  →  top-1000 candidates (FAST)
    ↓
Re-embed candidates at full 1536-dim
    ↓
[Re-rank by full-dim cosine similarity]  →  top-10 results (ACCURATE)
```

**Why this works**: 256-dim embeddings are fast to compare (~6x speedup in SIMD operations) and retrieve a good candidate set. Full-dim embeddings then rerank accurately.

## Supabase Implementation with pgvector

```sql
-- Store both dimensions
ALTER TABLE documents ADD COLUMN embedding_256 vector(256);
ALTER TABLE documents ADD COLUMN embedding_1536 vector(1536);

-- First pass: fast 256-dim ANN
SELECT id FROM documents
ORDER BY embedding_256 <=> query_256
LIMIT 1000;

-- Second pass: rerank with 1536-dim cosine
SELECT id FROM documents  
WHERE id = ANY(first_pass_ids)
ORDER BY embedding_1536 <=> query_1536
LIMIT 10;
```

## Benchmark Results

Supabase benchmarks comparing full-dim vs. adaptive retrieval:
- **99% of the quality** at full dimension
- **8.3x faster** first-pass retrieval at 256 dims
- **580 QPS** at 99% accuracy benchmark
- Significant cost savings (fewer dimensions = smaller index = cheaper)

## When to Use Adaptive Retrieval

Optimal when:
- Large datasets where ANN speed matters
- Cost is a constraint (smaller index storage)
- Acceptable to run two-pass (latency budget covers re-ranking)

## Related Articles

- [[Introduction to Matryoshka Embedding Models]] — technical foundation
- [[Matryoshka Representation Learning - A Guide to Faster Semantic Search]] — theory
- [[Nearest Neighbor Indexes for Similarity Search]] — ANN infrastructure
- [[Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex]] — other RAG quality levers

## Related Concepts

- [[Matryoshka Embeddings]] — primary concept
- [[Dense Vector Retrieval]] — infrastructure for two-pass search
- [[Retrieval Pipeline]] — two-pass search is a pipeline
- [[Bi-Encoder]] — model architecture underlying matryoshka
