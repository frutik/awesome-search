---
type: concept
title: "Text Chunking"
aliases: ["Chunking", "Document Chunking", "Text Splitting", "Chunking Strategies"]
tags:
  - concept
  - search
  - rag
  - embeddings
created: 2026-05-16
---

# Text Chunking

## Definition

**Text chunking** is the process of splitting large documents into smaller, semantically coherent segments before embedding and indexing. It's a foundational preprocessing step in [[RAG]] and [[Semantic Search]] systems.

## Why It Matters

1. **Context window limits** — Embedding models have token limits (typically 512-8192 tokens); text exceeding this is truncated
2. **Retrieval granularity** — Smaller chunks improve precision; larger chunks improve recall and context
3. **The "lost-in-the-middle" problem** — Even LLMs with large context windows struggle with content buried in the middle of long documents

## Chunking Methods

### Fixed-Size (Positional)
Split at fixed token count, optionally with overlap.
- **Pros:** Simple, consistent chunk sizes, fast
- **Cons:** No semantic awareness; may split mid-thought
- **Use when:** Starting point; most applications

### Sentence/Paragraph Splitting (Rule-based)
Split at sentence or paragraph boundaries using NLTK, spaCy, or LangChain.
- **Pros:** Linguistic coherence
- **Cons:** Variable chunk sizes; no semantic grouping

### Recursive Character Splitting (LangChain)
Splits using hierarchy: `["\n\n", "\n", " ", ""]` — tries paragraphs first, falls back to sentences, then words.
- Produces **uniform chunk distributions**
- LangChain's `RecursiveCharacterTextSplitter`

### Semantic Chunking
Uses embeddings to detect topic shifts; groups semantically similar sentences.
- Produces context-coherent chunks aligned with topic changes
- Higher computational cost
- Pioneer: Greg Kamradt

### Contextual Chunking (Anthropic)
LLM generates a context summary for each chunk and prepends it before embedding — preserves document-level context within each chunk.

### Boundary Classification (Decision-Model Chunking)
Instead of measuring embedding drift between neighbouring sentences, ask a classifier, for each gap, whether the next sentence starts a new topic. Cut where the probability passes a threshold, within minimum and maximum chunk sizes. [[Jevjitsu - How We Tried Generalized Classifiers on Everything]] does this with [[Jev]] over windows of numbered sentences.
- **Pros:** avoids splitting a paragraph that changes vocabulary mid-argument, and avoids merging adjacent passages that share vocabulary. Chunk size can be changed without new requests, because cuts are a pure function of the stored probabilities.
- **Cons:** text goes to an API (about $0.27 per million document tokens in that test), where other methods run locally for free.
- **Evidence:** on [[QASPER]], at matched mean chunk sizes, it beat fixed-size, recursive and embedding-based chunkers by 13.0% IoU, 11.2% precision and 9.1% recall (average relative), untuned.
## Choosing Chunk Size

Empirical from LlamaIndex study (Uber 10K SEC filing):
- **128 tokens** — fine-grained but loses context
- **512 tokens** — balanced
- **1024 tokens** — optimal (best faithfulness + relevancy in study)
- **2048 tokens** — diminishing returns

**Rule:** No universal answer — test on your specific data and queries.

## Method Comparison

| Method | Uniformity | Semantic Coherence | Seq. Preservation | Cost |
|---|---|---|---|---|
| Fixed-size | High | Low | Yes | Low |
| NLTK/spaCy | Low | High | Yes | Low |
| Recursive (LangChain) | High | Medium | Yes | Low |
| Semantic Clustering | Medium | High | Yes | Medium |
| KMeans Clustering | Variable | High | **No** | High |

## Related Concepts

- [[RAG]] — chunking is a core preprocessing step in RAG pipelines
- [[Dense Vector Retrieval]] — chunks become the units indexed as dense vectors
- [[Hypothetical Document Embeddings]] — an alternative to chunking for improving retrieval
- [[Embedding Fine-tuning]] — chunk quality affects downstream embedding quality

## Articles

- [[Chunking Strategies for LLM Applications]] — Pinecone
- [[Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex 1]] — LlamaIndex
- [[How to Chunk Text Data - A Comparative Analysis 1]] — Solano Todeschini

- [[Jevjitsu - How We Tried Generalized Classifiers on Everything]] — Qdrant; topic-boundary chunking with Jev, evaluated on [[QASPER]]
