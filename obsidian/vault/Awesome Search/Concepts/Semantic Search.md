---
title: Semantic Search
aliases:
  - neural search
  - meaning-based search
  - semantic retrieval
tags:
  - concept
  - search
  - retrieval
  - nlp
---

# Semantic Search

## Definition
## Definition

Semantic search retrieves documents based on the *meaning* of a query rather than exact keyword matching. It understands that "jaguar speed" and "how fast does a jaguar run?" are semantically equivalent, even though they share no keywords.

**Semantic search is a goal, not a technique.** The dominant modern implementation uses neural embeddings and vector similarity, but any approach that captures meaning — taxonomies, synonym graphs, LLM classifiers — qualifies. Conflating "semantic search" with "vector search" is a common mistake.

According to [[Doug Turnbull]], semantic search requires three things:
1. **Representation** — a shared space where queries and content can be compared
2. **Similarity function** — how near/far items are in that space
3. **Match criteria** — whether an item qualifies as a match at all (often forgotten)

Embeddings excel at 1 and 2 but struggle with 3 — there is no universal "good enough" threshold. Taxonomies handle all three explicitly.

## Contrast with Lexical Search

| Approach | Basis | Strengths | Weaknesses |
|----------|-------|-----------|------------|
| Keyword (BM25, TF-IDF) | Term overlap | Speed, exact match, interpretable | Vocabulary mismatch |
| Semantic (neural) | Meaning vectors | Paraphrases, intent, synonyms | Slower, opaque, costly |
| [[Hybrid Search]] | Both | Best of both | Complex |

## Core Architecture
## Approaches

### Embedding-Based (Dominant)

The most common modern approach uses a [[Bi-Encoder]]:
1. Encode query → dense vector (e.g., 768 dimensions)
2. Encode all documents → dense vectors (precomputed, stored in index)
3. Find nearest neighbors (ANN) at query time

The [[Dense Vector Retrieval]] infrastructure (FAISS, HNSW, Pinecone, Elasticsearch kNN) handles step 3 efficiently.

**Tradeoffs:** excellent at fuzzy/paraphrase matching; poor at exact constraints; no interpretable threshold for "match vs. no match."

### Taxonomy-Based (Non-Embedding)

A managed hierarchical vocabulary solves all three requirements explicitly:
- **Representation**: category tree (e.g., `Baby & Kids / Playroom / Rocking Horses`)
- **Similarity**: direct match > sibling > cousin > grandparent
- **Match criteria**: include/exclude specific tree levels by design

Can be implemented in a standard [[BM25]] index using a hierarchical tokenizer — ancestor paths become tokens, and BM25's IDF naturally scores leaf nodes (rare) higher than root nodes (common).

LLMs now make taxonomy maintenance tractable: they can classify products/queries into categories cheaply, and can "hallucinate" plausible category paths as a form of [[HyDE]]-style query expansion.

**Tradeoffs:** high explainability, precise match control, cold-start friendly; labor-intensive to maintain, vocabulary-dependent.

### Other Non-Embedding Approaches
- **Synonym graphs / thesauri** — explicit vocabulary expansion
- **Knowledge graphs** — entity relationships as the semantic layer
- **LLM reranking** — use language model judgment directly at retrieval time

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

## Articles

- [[Semantic Search Without Embeddings]] — taxonomy + BM25 as an alternative to embedding-based semantic search ([[Doug Turnbull]])