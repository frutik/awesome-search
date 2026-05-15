---
title: "Chunking Strategies for LLM Applications"
source: "https://www.pinecone.io/learn/chunking-strategies/"
author:
  - "[[Roie Schwaber-Cohen]]"
  - "[[Arjun Patel]]"
published: 2025-06-28
created: 2026-05-15
description: "A guide to chunking strategies for LLM applications — fixed-size, semantic, contextual, and document-structure-aware chunking."
tags:
  - clippings
---
# Chunking Strategies for LLM Applications

**Chunking** breaks large text into smaller segments to optimize content relevance for vector databases. Goal: chunks substantial enough to contain meaningful information, compact enough for low-latency retrieval.

## Methods

### Fixed-size chunking
Decide chunk token count and break accordingly. Usually matches the embedding model's context window. Start here and iterate only if insufficient.

### Content-aware chunking
- **Naive splitting**: by periods, newlines, whitespace
- **NLTK / spaCy**: trained sentence tokenization
- **Recursive character-level** (LangChain `RecursiveCharacterTextSplitter`): splits by `["\n\n", "\n", " ", ""]` — balances semantic and fixed-size splitting

### Document structure-based
Preserves structure: PDF headers/tables, HTML tags, Markdown headings, LaTeX commands.

### Semantic chunking
Groups sentences by topic using embedding similarity — identifies topic shifts as chunk boundaries (Greg Kamradt).

### Contextual chunking with LLMs
Anthropic's contextual retrieval (2024): Claude processes the whole document alongside each chunk, generating a contextualized description appended before embedding.

## Key considerations

1. **Data type** — lengthy articles vs. short content
2. **Embedding model** — adapt to training data
3. **Query type** — short/specific vs. long/complex
4. **Application** — semantic search, QA, RAG, agentic

## Chunk sizes

- 128–256 tokens: granular semantic info
- 512–1024 tokens: retains context

## Post-processing: chunk expansion
Retrieve neighboring chunks to provide surrounding context for each result.


## Related Concepts

- [[Text Chunking]]
- [[RAG]]
- [[Dense Embeddings]]
- [[Embeddings]]
- [[Agentic Search]]

## People

- [[Roie Schwaber-Cohen]]
- [[Arjun Patel]]
