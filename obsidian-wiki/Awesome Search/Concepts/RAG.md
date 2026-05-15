---
title: "RAG"
aliases: ["Retrieval-Augmented Generation", "Retrieval Augmented Generation"]
tags:
  - concept
  - search
  - llm
  - rag
---

# RAG (Retrieval-Augmented Generation)

## Definition

**RAG** combines a retrieval system with a generative language model. Instead of relying on the LLM's parametric memory alone, RAG retrieves relevant context from an external knowledge base and passes it to the LLM as context for generation.

```
User query → Retrieval → Top-k documents → LLM (query + docs) → Response
```

## Core Components

1. **Chunking** — Split documents into indexable units ([[Text Chunking]])
2. **Indexing** — Embed chunks and store in vector database
3. **Retrieval** — Find chunks most relevant to query ([[Dense Vector Retrieval]], [[Hybrid Search]])
4. **Generation** — LLM synthesizes answer from retrieved context

## Why RAG Matters for Search

- Grounds LLM responses in actual documents (reduces hallucination)
- Enables citing sources
- Knowledge can be updated without retraining the LLM
- Domain adaptation without fine-tuning

## RAG Quality Factors

**Retrieval quality** (most critical):
- Correct chunks must be retrieved; LLM can't fix bad retrieval
- [[Text Chunking]] strategy affects what's retrievable
- [[Embedding Fine-tuning]] improves domain-specific retrieval
- [[Hypothetical Document Embeddings]] boosts zero-shot recall

**Generation quality:**
- Context window management
- Prompt engineering
- Cross-encoder reranking before passing to LLM

## Agentic RAG

[[Agentic Search]] extends RAG by making retrieval iterative:
- Agent decides what to retrieve next based on current knowledge state
- Multi-step reasoning with multiple retrieval rounds
- Tools beyond text search (calculators, APIs, databases)

## Related Concepts
- [[Embeddings]] — the retrieval component of RAG uses embeddings to find relevant context
- [[Dense Embeddings]] — typically the retrieval representation in RAG pipelines

- [[Text Chunking]] — preprocessing for RAG
- [[Dense Vector Retrieval]] — typical retrieval method in RAG
- [[Hybrid Search]] — combining sparse + dense for better RAG retrieval
- [[Hypothetical Document Embeddings]] — query-side improvement
- [[Agentic Search]] — agentic extension of RAG
- [[Task-Aware Embeddings]] — improves RAG by task-conditioning queries

## Articles

- [[Chunking Strategies for LLM Applications]]
- [[Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex]]
- [[Improve your RAG applications by moving to Task-aware Embeddings]]
- [[Hypothetical Document Embeddings HyDE]]
- [[Agentic Search as an Agile Engineering Process]]
