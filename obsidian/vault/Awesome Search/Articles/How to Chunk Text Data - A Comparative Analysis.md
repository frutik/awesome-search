---
title: "How to Chunk Text Data — A Comparative Analysis"
source: "https://towardsdatascience.com/how-to-chunk-text-data-a-comparative-analysis-3858c4a0997a"
author: []
tags:
  - clippings
  - chunking
  - rag
  - embeddings
concepts:
  - Text Chunking
  - RAG
  - Semantic Search
created: 2026-05-15
---

# How to Chunk Text Data — A Comparative Analysis

**Source**: https://towardsdatascience.com/how-to-chunk-text-data-a-comparative-analysis-3858c4a0997a  
**Publisher**: Towards Data Science

## Summary

A comparative analysis of text chunking methods for RAG and embedding-based retrieval, comparing fixed-size, recursive, semantic, and hybrid approaches with concrete code examples and quality comparisons.

## Chunking Methods Compared

### Fixed-Size Chunking
Simplest approach: split every N tokens, with overlap M.

```python
def fixed_chunk(text, chunk_size=512, overlap=50):
    tokens = tokenizer.encode(text)
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(tokenizer.decode(chunk))
    return chunks
```

**Verdict**: Fast and predictable. Acceptable baseline for many use cases.

### Recursive Splitting
LangChain's `RecursiveCharacterTextSplitter` — respects natural boundaries.

Splitting hierarchy: `\n\n` → `\n` → `. ` → ` ` → character

Better for narrative text, blog posts, books.

### Semantic Chunking
Group sentences with similar embeddings into the same chunk:

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def semantic_chunk(sentences, threshold=0.7):
    embeddings = model.encode(sentences)
    chunks, current_chunk = [], [sentences[0]]
    for i in range(1, len(sentences)):
        sim = cosine_similarity([embeddings[i-1]], [embeddings[i]])[0][0]
        if sim < threshold:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
        current_chunk.append(sentences[i])
    chunks.append(" ".join(current_chunk))
    return chunks
```

**Verdict**: Higher quality but 5–10x more compute (requires sentence-level embeddings).

### Proposition-Based Chunking
Split into atomic propositions (smallest standalone fact unit). Each proposition can be independently retrieved and understood.

Example: "The Eiffel Tower was built in 1889 and stands 330m tall" →
- "The Eiffel Tower was built in 1889"
- "The Eiffel Tower stands 330m tall"

**Verdict**: Highest precision for factual QA; very expensive (requires LLM).

## Comparative Results

| Method | Retrieval Precision | Cost | Chunk Consistency |
|--------|-------------------|------|-----------------|
| Fixed-size | Medium | Very low | High (predictable) |
| Recursive | Medium-High | Low | Medium |
| Semantic | High | Medium | Low (variable size) |
| Proposition | Very High | Very High | Low |

## Key Insight: Content Type Matters

- **Technical docs** (structured, sections): Document-structure splitting wins
- **Narrative text** (books, articles): Recursive or semantic splitting
- **Factual knowledge bases**: Proposition-based if budget allows
- **Code**: Function/class-level splitting

## Related Articles

- [[Chunking Strategies for LLM Applications]] — strategy overview
- [[Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex]] — empirical size study
- [[Hypothetical Document Embeddings HyDE]] — alternative: reframe query to match documents

## Related Concepts

- [[Text Chunking]] — primary topic
- [[RAG]] — use case
- [[Semantic Search]] — downstream retrieval
- [[Asymmetric Semantic Search]] — chunked docs retrieved by short queries
