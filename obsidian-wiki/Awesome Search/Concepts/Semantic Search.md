---
title: "Semantic Search"
aliases: ["neural search", "meaning-based search", "semantic retrieval", "vector search"]
tags:
  - concept
  - search
  - retrieval
  - nlp
---

# Semantic Search

## Definition

Semantic search retrieves documents based on the *meaning* of a query rather than exact keyword matching. It understands that "jaguar speed" and "how fast does a jaguar run?" are semantically equivalent, even though they share no keywords.

This is the broad category encompassing [[Dense Vector Retrieval]], [[Bi-Encoder]] models, and related approaches that use neural representations to capture semantic meaning.

## Contrast with Lexical Search

| Approach | Basis | Strengths | Weaknesses |
|----------|-------|-----------|------------|
| Keyword (BM25, TF-IDF) | Term overlap | Speed, exact match, interpretable | Vocabulary mismatch |
| Semantic (neural) | Meaning vectors | Paraphrases, intent, synonyms | Slower, opaque, costly |
| [[Hybrid Search]] | Both | Best of both | Complex |

## Core Architecture

The dominant paradigm uses a [[Bi-Encoder]]:
1. Encode query → dense vector (e.g., 768 dimensions)
2. Encode all documents → dense vectors (precomputed, stored in index)
3. Find nearest neighbors (ANN) at query time

The [[Dense Vector Retrieval]] infrastructure (FAISS, HNSW, Pinecone, Elasticsearch kNN) handles step 3 efficiently.

## Dimensions of Semantic Search

### Symmetric vs. Asymmetric
- **[[Asymmetric Semantic Search]]**: short query → long document (QA, enterprise search)
- **Symmetric**: similar documents, duplicate detection, clustering

### Single vs. Multi-Modal
- **Text-only**: standard NLP embedding models
- **[[Multimodal Embeddings]]**: text + image, text + audio

### General vs. Domain-Specific
- **General**: `text-embedding-ada-002`, `all-MiniLM-L6-v2`
- **Domain-adapted**: [[Embedding Fine-tuning]]

### Static vs. Task-Aware
- **Static**: same embedding regardless of task
- **[[Task-Aware Embeddings]]**: different representation per task via instruction prefixes

## Quality Improvements over Pure Semantic

Pure semantic search can be enhanced with:
- **[[ColBERT]]**: per-token late interaction instead of single vector — more accurate, same asymptotic complexity
- **[[Hypothetical Document Embeddings]]**: generate hypothetical answer → embed → better query representation
- **[[Matryoshka Embeddings]]**: flexible dimension tradeoff (speed vs. quality)
- **[[Hybrid Search]]**: add sparse signal for lexical precision

## Infrastructure Requirements

Semantic search requires:
1. An embedding model (inference cost at index time + query time)
2. A vector index (FAISS, Annoy, HNSW, or managed: Pinecone, Weaviate, Qdrant)
3. Storage for dense vectors (~4 bytes × dimensions × num_docs)

See [[Dense Vector Retrieval]] for detailed infrastructure notes.

## Related Concepts
- [[Embeddings]] — the representation that enables semantic search
- [[Dense Embeddings]] — the specific vector type used in semantic search

- [[Dense Vector Retrieval]] — core infrastructure
- [[Bi-Encoder]] — primary architecture
- [[ColBERT]] — advanced late interaction
- [[Hybrid Search]] — semantic + lexical combination
- [[Asymmetric Semantic Search]] — most common use case
- [[Task-Aware Embeddings]] — instruction-guided representations
- [[Multimodal Embeddings]] — cross-modal extension
- [[Matryoshka Embeddings]] — flexible-dimension embeddings
- [[RAG]] — semantic search enables retrieval-augmented generation
- [[Agentic Search]] — semantic search as component of agent
