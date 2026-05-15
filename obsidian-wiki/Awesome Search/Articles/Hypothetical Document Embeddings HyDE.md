---
title: "Hypothetical Document Embeddings (HyDE)"
source: "https://docs.haystack.deepset.ai/docs/hypothetical-document-embeddings-hyde"
author: ["deepset / Haystack"]
tags:
  - clippings
  - hyde
  - rag
  - embeddings
  - query-expansion
concepts:
  - Hypothetical Document Embeddings
  - RAG
  - Dense Vector Retrieval
  - Asymmetric Semantic Search
created: 2026-05-15
---

# Hypothetical Document Embeddings (HyDE)

**Source**: https://docs.haystack.deepset.ai/docs/hypothetical-document-embeddings-hyde  
**Publisher**: deepset / Haystack

## Summary

The Haystack documentation explains HyDE (Hypothetical Document Embeddings) — a technique that improves retrieval by having an LLM generate a hypothetical document that would answer the query, then using the embedding of that hypothetical document (rather than the raw query) for retrieval.

## Core Insight

**The problem**: A short question and a long answer are in different regions of the embedding space. The question "What is photosynthesis?" and a 500-word textbook passage about photosynthesis have different embeddings even though they're semantically matched.

**HyDE's solution**: Use an LLM to generate a *hypothetical* answer that looks like a real passage. The hypothetical answer is in the same region of embedding space as actual relevant passages.

```
Query: "What is photosynthesis?"
    ↓ LLM (generate hypothetical answer)
Hypothetical: "Photosynthesis is the process by which plants convert light energy..."
    ↓ Embedding model
hypothetical_embedding ─→ ANN search over real document embeddings
    ↓
Actual relevant passages (photosynthesis explanations)
```

## Why This Works

1. The hypothetical document uses the vocabulary and structure of an *answer* — matching actual relevant passages
2. The embedding model aligns semantically similar texts regardless of provenance
3. LLM-generated text naturally uses domain vocabulary and explanatory patterns

## Multiple Hypothetical Documents

For robustness, generate 5 hypothetical answers and average their embeddings:

```python
from haystack.components.generators import OpenAIGenerator
from haystack.components.embedders import OpenAITextEmbedder
import numpy as np

generator = OpenAIGenerator(model="gpt-3.5-turbo")
embedder = OpenAITextEmbedder()

def hyde_embed(query, n=5):
    # Generate multiple hypothetical answers
    hypotheticals = []
    for _ in range(n):
        response = generator.run(
            prompt=f"Write a passage that directly answers: {query}\nPassage:"
        )
        hypotheticals.append(response["replies"][0])
    
    # Embed each hypothetical
    embeddings = [embedder.run(text=h)["embedding"] for h in hypotheticals]
    
    # Average the embeddings
    return np.mean(embeddings, axis=0)
```

Averaging reduces noise from any single hypothetical that might miss the point.

## Implementation in Haystack Pipeline

```python
from haystack import Pipeline
from haystack.components.routers import MetadataRouter

hyde_pipeline = Pipeline()
hyde_pipeline.add_component("generator", OpenAIGenerator())
hyde_pipeline.add_component("embedder", OpenAITextEmbedder())  
hyde_pipeline.add_component("retriever", InMemoryEmbeddingRetriever(document_store))

hyde_pipeline.connect("generator.replies", "embedder.text")
hyde_pipeline.connect("embedder.embedding", "retriever.query_embedding")
```

## When HyDE Helps Most

HyDE is most effective when:
1. Queries are short but documents are long ([[Asymmetric Semantic Search]] scenario)
2. Domain-specific vocabulary where queries and docs use different phrasing
3. Open-domain QA where the question is very different from answer form

## When HyDE May Not Help

- When query and documents already use similar vocabulary
- When LLM hallucinations could lead to misleading hypotheticals
- When latency is critical (LLM call adds 100–500ms)
- Low-budget deployments (adds LLM API cost per query)

## Comparison with Other Query Improvements

| Technique | Cost | Benefit |
|-----------|------|---------|
| Raw query embedding | Free | Baseline |
| Query expansion (BM25) | Low | Better recall for synonyms |
| HyDE (1 hypothesis) | Medium (1 LLM call) | Better embedding alignment |
| HyDE (5 hypotheses) | High (5 LLM calls) | Best embedding alignment |
| [[Task-Aware Embeddings]] | Free (prompt prefix) | Better task alignment |

## Relation to Other Techniques

HyDE and [[Text Chunking]] are complementary:
- Chunking: shapes the document side to be more retrievable
- HyDE: shapes the query side to look more like documents

Together they address the asymmetric retrieval problem from both ends.

## Related Articles

- [[Chunking Strategies for LLM Applications]] — document-side complement
- [[Improve your RAG applications by moving to Task-aware Embeddings]] — alternative query-side improvement
- [[Symmetric vs. Asymmetric Semantic Search]] — the asymmetry problem HyDE solves

## Related Concepts

- [[Hypothetical Document Embeddings]] — primary concept
- [[RAG]] — primary use case
- [[Dense Vector Retrieval]] — infrastructure
- [[Asymmetric Semantic Search]] — the problem HyDE addresses
- [[Bi-Encoder]] — embedding model used
- [[Task-Aware Embeddings]] — alternative approach
