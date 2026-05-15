---
title: "Hypothetical Document Embeddings"
aliases: ["HyDE", "Hypothetical Document Embedding"]
tags:
  - concept
  - search
  - rag
  - query-understanding
---

# Hypothetical Document Embeddings (HyDE)

## Definition

**HyDE** (Hypothetical Document Embeddings) is a zero-shot dense retrieval technique that improves recall by using an LLM to generate **hypothetical documents** that answer the query, then averaging their embeddings to create a better query representation for nearest-neighbor search.

## The Problem It Solves

Dense retrievers are trained to match query embeddings against document embeddings. But for many real queries, especially in domain-specific settings, the query vector lies far from the relevant document vectors in embedding space — because questions and answers are linguistically very different.

HyDE addresses this by replacing the query vector with a **synthesized document vector** that looks more like the answer.

## How It Works

```
1. Query → LLM prompt → 5 hypothetical answer documents (n=5, temp=0.75)
2. Each hypothetical doc → embedding model → 5 vectors
3. Average 5 vectors → single "HyDE vector"
4. Use HyDE vector for nearest-neighbor search in corpus
```

**Intuition:** A hypothetical answer to "What is Python?" looks like a Wikipedia article about Python — and lies close to real Python articles in embedding space, even if the query "What is Python?" does not.

## Implementation (Haystack)

```python
generator = OpenAIGenerator(model="gpt-3.5-turbo", 
                             generation_kwargs={"n": 5, "temperature": 0.75})

# Custom component averages 5 hypothetical doc embeddings
class HypotheticalDocumentEmbedder:
    def run(self, documents):
        stacked = array([doc.embedding for doc in documents])
        return {"hypothetical_embedding": mean(stacked, axis=0).tolist()}
```

## When to Use

- Low recall in domain-specific retrieval
- Knowledge base with content very different from typical queries
- Zero-shot setting with no labeled query-document pairs

## Tradeoffs

| Pro | Con |
|---|---|
| Improves recall without any labeled data | Adds LLM latency to retrieval path |
| Works in zero-shot settings | Hypothetical docs may hallucinate irrelevant content |
| No changes to index or documents needed | Cost: N LLM calls per query |

## Related Concepts
- [[Embeddings]] — parent concept; HyDE manipulates the embedding space
- [[Dense Embeddings]] — HyDE operates in dense embedding space

- [[Dense Vector Retrieval]] — HyDE is used as a query-side enhancement
- [[RAG]] — HyDE improves the retrieval stage of RAG
- [[Asymmetric Semantic Search]] — HyDE effectively converts asymmetric to symmetric retrieval
- [[Text Chunking]] — alternative approach to improving retrieval quality
- [[Bag-of-Documents Model]] — complementary idea of training queries to predict document distributions

## Academic Reference

"Precise Zero-Shot Dense Retrieval without Relevance Labels" — ACL 2023

## Articles

- [[Hypothetical Document Embeddings HyDE]] — Haystack docs
