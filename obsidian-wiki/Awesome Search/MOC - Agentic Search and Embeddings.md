---
title: "Map of Content: Agentic Search & Embeddings"
tags:
  - moc
  - search
  - embeddings
  - agentic-search
created: 2026-05-15
---

# Map of Content: Agentic Search & Embeddings

Entry point for the semantic knowledge graph covering the **Agentic Search** and **Embeddings** sections of the Awesome Search collection. Navigate by concept, person, or article.

---

## Core Paradigms

- [[Agentic Search]] — agents that plan, execute, verify, and refine retrieval
- [[RAG]] — retrieval-augmented generation pipeline
- [[Semantic Search]] — meaning-based retrieval
- [[Hybrid Search]] — sparse + dense combination

---

## Embedding Architectures

| Architecture | Key Property | Note |
|-------------|-------------|------|
| [[Bi-Encoder]] | Independent encoding, fast | Two-tower, dual encoder |
| [[Cross-Encoder]] | Joint encoding, accurate | Reranker |
| [[ColBERT]] | Per-token MaxSim | Late interaction |
| [[Late Interaction]] | Token-level alignment | ColBERT's mechanism |

---

## Vector Types

### Dense
- [[Embeddings]] — what embeddings are; dense vs sparse; training; economics
- [[Dense Embeddings]] — all-dimension active vectors; bi-encoder models; ANN indexing
- [[Dense Vector Retrieval]] — ANN indexes (HNSW, IVF, Flat)
- [[Matryoshka Embeddings]] — flexible-dimension, nested quality
- [[Task-Aware Embeddings]] — instruction-guided representations
- [[Multimodal Embeddings]] — cross-modal (image + text)



- [[Vector Similarity Metrics]] — cosine similarity, dot product, Euclidean (L2) distance

### Sparse
- [[Sparse Embeddings]] — vocabulary-space vectors; BM25 vs learned sparse (SPLADE/ELSER)
- [[Sparse Vector Retrieval]] — inverted index compatible
- [[SPLADE]] — BERT MLM → vocabulary-space sparse vectors
- [[ELSER]] — Elastic's production SPLADE

### Constructed Query Vectors
- [[Hypothetical Document Embeddings]] — LLM generates hypothetical answer → embed
- [[Wormhole Vectors]] — bridge sparse/dense/behavioral spaces
- [[Bag-of-Documents Model]] — query as distribution over documents

### Quantization
- [[Vector Quantization]] — compressing embeddings: scalar (SQ8), binary (BBQ), product (PQ), K-Quants/I-Quants
- [[BBQ]] — Elasticsearch's Better Binary Quantization + OSQ; 32× compression, 10–40× speed
- [[GGUF]] — quantized LLM weight format for local deployment (rerankers, query expansion)

---

## Retrieval Strategies

- [[Retrieval Pipeline]] — multi-stage: retrieve → rerank
- [[Asymmetric Semantic Search]] — short query → long document
- [[Vector Filtering]] — metadata predicates + ANN search
- [[Embedding Fine-tuning]] — domain adaptation

---

## Text Preparation
- [[Text Chunking]] — fixed, recursive, semantic, contextual methods

---

## Key People

| Person | Affiliation | Key Contributions |
|--------|-------------|------------------|
| [[Daniel Tunkelang]] | QueryUnderstanding.com | Agentic Search, Bag-of-Documents, Pipeline Distillation |
| [[Omar Khattab]] | Stanford | ColBERT creator |
| [[Matei Zaharia]] | Stanford/Databricks | ColBERT co-creator |
| [[Jo Kristian Bergum]] | Vespa | ColBERT 32x compression |
| [[Han Xiao]] | Jina AI | jina-colbert-v1-en (8192 tokens) |
| [[Trey Grainger]] | — | Wormhole Vectors, "AI-Powered Search" |
| [[Stéphane Clinchant]] | NAVER LABS | SPLADE co-inventor |
| [[Thibault Formal]] | NAVER LABS | SPLADE co-inventor |
| [[James Briggs]] | Pinecone | SPLADE explainer, Vector Filtering |
| [[Shaw Talebi]] | — | Fine-tuning text & multimodal embeddings |
| [[Asif Makhani]] | Infino AI | Co-authored Agentic Search with Tunkelang |
| [[Dima Kan]] | Aiven | Wormhole Vectors implementation |
| [[Lester Solbakken]] | hornet.dev | MAD framework, defensive retrieval |
| [[Thomas Veasey]] | Elastic | BBQ/OSQ quantization benchmarks |
| [[Piotr Mazurek]] | tensoreconomics.com | Embeddings economics, FLOPS/dollar analysis |
| [[Quynh Nguyen]] | Elastic | Multilingual embedding hybrid search |

---

## Articles by Topic

### Agentic Search
- [[Agentic Search as an Agile Engineering Process]]

- [[Superintelligent Retrieval Agent SIRA]] — LLM-enriched BM25; corpus enrichment + query expansion; beats agentic RAG on BEIR
- [[Mutually Assured Distraction]] — [[Lester Solbakken]]; MAD dynamic; abstention as retrieval control signal
- [[You Say Search I Say Recs - Spotify Agentic Query Understanding]] — LLM router; +115% similar artists, +91% new music releases
- [[Incremental AI Adoption for E-commerce Search]] — 4-level progression: traditional → conversational AI

### ColBERT / Late Interaction
- [[Announcing the Vespa ColBERT Embedder]]
- [[What is ColBERT and Late Interaction and Why They Matter in Search]]
- [[Bi-encoder vs Cross-encoder When to Use Which One]]

### Matryoshka Embeddings
- [[Matryoshka Embeddings - Faster OpenAI Vector Search]]
- [[Introduction to Matryoshka Embedding Models]]
- [[Matryoshka Representation Learning - A Guide to Faster Semantic Search]]

### Text Chunking
- [[Chunking Strategies for LLM Applications]]
- [[Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex]]
- [[How to Chunk Text Data - A Comparative Analysis]]

### Context-Aware / Task-Aware Embeddings
- [[Improve your RAG applications by moving to Task-aware Embeddings]]
- [[How Context-Aware Embeddings Are Transforming Enterprise Search]]

### SPLADE & Sparse Retrieval
- [[Hybrid Search SPLADE Sparse Encoder]]
- [[SPLADE for Sparse Vector Search Explained]]
- [[SPLADE - Sparse Bi-Encoder BERT Model for First-Stage Ranking]]
- [[Elastic Learned Sparse Encoder ELSER Retrieval Performance]]

### Constructed Query Vectors
- [[Hypothetical Document Embeddings HyDE]]
- [[Distilling Retrieval Pipelines to a Single Embedding Model]]
- [[Beyond Hybrid Search - Traversing Vector Spaces with Wormhole Vectors]]

- [[Wormhole Vectors Beyond Hybrid Search in OpenSearch]] — [[Dima Kan]]; production SKG traversal at Aiven

### Fine-tuning
- [[Fine-Tuning Text Embeddings For Domain-Specific Search]]
- [[Fine-tuning Multimodal Embedding Models]]

- [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]] — LoRA on 615M; LSPC dataset; 0.836 macro-F1
- [[Qwen3 Embedding Series]] — 0.6B/4B/8B; #1 MTEB multilingual; MRL support

### Vector Infrastructure
- [[Nearest Neighbor Indexes for Similarity Search]]
- [[The Missing WHERE Clause in Vector Search]]
- [[How to Choose the Best Model for Semantic Search]]
- [[Symmetric vs Asymmetric Semantic Search]]

- [[Why Are Embeddings So Cheap]] — [[Piotr Mazurek]]; compute-bound; ~$0.01/1M tokens at scale
- [[Multilingual Embedding Model Hybrid Search Reranking]] — [[Quynh Nguyen]]; E5 multilingual + RRF + Cohere reranker

### Quantization
- [[Elasticsearch BBQ Optimized Scalar Quantization vs TurboQuant]] — [[Thomas Veasey]]; OSQ vs TurboQuant; 10–40× CPU speedup via integer SIMD
- [[GGUF Quantization - A Technical Deep Dive]] — [[Michael Hannecke]]; K-Quants, I-Quants, imatrix, deployment guide

### Case Studies
- [[Migrating to Elasticsearch with Dense Vector for Carousell Spotlight]]
- [[Innovating Search Experience with Amazon OpenSearch and Amazon Bedrock]]

---

## Concept Relationship Map

```
Agentic Search
  └── uses → Retrieval Pipeline
               ├── Stage 1: Bi-Encoder / Sparse Vector Retrieval / Hybrid Search
               └── Stage 2: Cross-Encoder / ColBERT (Late Interaction)

RAG
  └── uses → Dense Vector Retrieval
               ├── input: Text Chunking → Bi-Encoder embeddings
               └── query: Asymmetric Semantic Search / HyDE / Task-Aware Embeddings

Hybrid Search
  ├── sparse leg: SPLADE / ELSER / BM25
  └── dense leg: Bi-Encoder
       └── advanced: Wormhole Vectors / Bag-of-Documents Model

Embedding Quality
  ├── Matryoshka Embeddings (flexible dimensions)
  ├── Embedding Fine-tuning (domain adaptation)
  ├── Multimodal Embeddings (image + text)
  └── Vector Filtering (metadata + ANN)
```
