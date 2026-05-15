---
title: "Chunking Strategies for LLM Applications"
source: "https://www.pinecone.io/learn/chunking-strategies/"
author: ["Pinecone"]
tags:
  - clippings
  - chunking
  - rag
  - embeddings
  - llm
concepts:
  - Text Chunking
  - RAG
  - Dense Vector Retrieval
created: 2026-05-15
---

# Chunking Strategies for LLM Applications

**Source**: https://www.pinecone.io/learn/chunking-strategies/  
**Publisher**: Pinecone

## Summary

A comprehensive guide to text chunking strategies for RAG and embedding-based retrieval, covering five approaches from fixed-size to semantic chunking.

## Why Chunking Matters

LLM context windows and embedding models have input length limits. Chunking splits documents into retrievable segments. The strategy significantly affects retrieval quality:
- **Too small**: chunks lack context, semantically incomplete
- **Too large**: irrelevant content dilutes the relevant signal; embedding model input limits hit
- **Just right**: ~1024 tokens for many tasks (empirically validated)

## Five Chunking Strategies

### 1. Fixed-Size Chunking
Split text at fixed token/character boundaries with optional overlap.
```python
from langchain.text_splitter import CharacterTextSplitter
splitter = CharacterTextSplitter(chunk_size=256, chunk_overlap=50)
chunks = splitter.split_text(text)
```
**Pros**: Simple, fast, predictable  
**Cons**: Breaks sentences mid-thought, no semantic awareness

### 2. Recursive Character Splitting
Try to split at paragraph → sentence → word boundaries in priority order.
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=256, chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""]
)
```
**Pros**: Preserves natural text boundaries better  
**Cons**: Still size-based, not semantically aware

### 3. Document Structure-Based
Exploit document-specific structure: markdown headers, HTML tags, code blocks, PDF sections.
- Markdown: split at `##` headers → each section is a chunk
- Code: function-level splitting

**Pros**: Semantically meaningful units  
**Cons**: Requires document-type-specific logic

### 4. Semantic Chunking
Compute sentence embeddings → split where embedding similarity drops below a threshold.
```python
# Split where adjacent sentence cosine similarity < threshold
sentences = sent_tokenize(text)
embeddings = embed(sentences)
breakpoints = find_breakpoints(embeddings, threshold=0.7)
```
**Pros**: True semantic boundaries  
**Cons**: Computationally expensive (requires embedding all sentences), variable chunk size

### 5. Contextual Chunking (LLM-based)
Use an LLM to generate context-enriching summaries that are prepended to each chunk before embedding.
**Pros**: Best quality  
**Cons**: Very expensive (LLM call per chunk), not practical for large corpora

## Optimal Chunk Size

Pinecone's guidance: start with 256–512 tokens, experiment for your use case. LlamaIndex study (see [[Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex]]) found 1024 tokens optimal for many benchmarks.

## Overlap

Overlap prevents losing context at chunk boundaries:
- Typical: 10–20% of chunk size
- Too much: redundant storage, similar chunks confuse retrieval
- Too little: boundary information lost

## Related Articles

- [[Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex]] — empirical chunk size study
- [[How to Chunk Text Data - A Comparative Analysis]] — comparative analysis
- [[SPLADE for Sparse Vector Search Explained]] — sparse retrieval handles chunking differently
- [[Nearest Neighbor Indexes for Similarity Search]] — indexing chunked vectors

## Related Concepts

- [[Text Chunking]] — primary topic
- [[RAG]] — primary use case
- [[Dense Vector Retrieval]] — what chunked vectors are indexed into
- [[Asymmetric Semantic Search]] — chunking enables short query → long doc retrieval
- [[Hypothetical Document Embeddings]] — alternative to chunking for query-side
